from typing import Any, Callable

import dask.dataframe as dd
import numpy as np
from dask_ml.metrics import accuracy_score
from scikeras.wrappers import KerasClassifier

from flowi.components.component_base import ComponentBase
from flowi.components.data_preparation import DataPreparationSKLearn
from flowi.components.models._wrappers import OneHotModel
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.utilities.logger import Logger
import hyperopt
from hyperopt import fmin, tpe, Trials


class ModelSelection(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        experiment_tracking = ExperimentTracking()
        model = result[0]
        parameters = result[1]

        experiment_tracking.save_model(obj=model, file_path="model")
        experiment_tracking.log_model_param(key=model.__class__.__name__, value=parameters)
        return {
            "model": model,
            "parameters": parameters,
            "target_column": methods_kwargs["target_column"],
            "object": model,
        }

    def tpe(
        self,
        df: dd.DataFrame,
        target_column: str,
        model,
        parameters: dict,
        early_stopping: bool or str = None,
        n_trials: int = 10,
        cv: int = 5,
    ):
        if isinstance(model, OneHotModel):
            flowi_model = model
            model = flowi_model.model

            sklean_data_prep = DataPreparationSKLearn()
            X, y = sklean_data_prep.prepare_train(df=df, target_column=target_column)
            y = flowi_model.encode(y)
        else:
            flowi_model = model
            model = flowi_model.model

            sklean_data_prep = DataPreparationSKLearn()
            X, y = sklean_data_prep.prepare_train(df=df, target_column=target_column)
            y = flowi_model.encode(y)

        X = X.compute()
        y = y.compute()

        best_model = None
        best_score = np.Inf
        best_params = dict()

        def objective(params):
            nonlocal best_params, best_score, best_model

            initial_params = model.get_params()
            new_params = initial_params | params
            klass = model.__class__
            new_object = klass(**new_params)
            new_object.fit(X, y)

            y_pred = new_object.predict(X)
            score = accuracy_score(y_true=y, y_pred=y_pred)

            if score < best_score:
                best_score = score
                best_model = new_object
                best_params = new_params

            return {
                'loss': score,
                'status': hyperopt.STATUS_OK,
                'model': new_object
            }

        trials = Trials()
        fmin(fn=objective,
             space=parameters,
             algo=tpe.suggest,
             max_evals=n_trials,
             trials=trials,
        )

        model = best_model
        self._logger.debug(f"Model: {model.__class__.__name__}")
        self._logger.debug(f"Best Parameters: {best_params}")

        if isinstance(model, KerasClassifier):
            flowi_model.model = model
            model = flowi_model
        else:
            flowi_model.model = model
            model = flowi_model

        return model, best_params
