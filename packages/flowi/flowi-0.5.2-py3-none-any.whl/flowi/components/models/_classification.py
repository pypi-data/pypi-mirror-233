from typing import Any, List

import dask.dataframe as dd
from sklearn import svm

from flowi.components.component_base import ComponentBase
from flowi.components.model_selection import ModelSelection
from flowi.components.models._wrappers import OneHotModel, CategoryModel, BaseModel
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.utilities.logger import Logger
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import tensorflow as tf
from scikeras.wrappers import KerasClassifier
from hyperopt import hp

from flowi.utilities.tune import tune_param


class Classification(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        experiment_tracking = ExperimentTracking()
        model: BaseModel = result[0]
        parameters = result[1]
        model_type = result[2]

        model_uri = experiment_tracking.save_model(obj=model.model, file_path="model")
        experiment_tracking.log_tag(tag_name="model_type", value=model_type)
        experiment_tracking.log_model_param(key=model.model.__class__.__name__, value=parameters)
        return {
            "model": model,
            "parameters": parameters,
            "target_column": methods_kwargs["target_column"],
            "object": model,
            "model_uri": model_uri,
        }

    @staticmethod
    def _fit_sklearn(
        df: dd.DataFrame,
        model,
        parameters: dict,
        target_column: str,
        verbose: int = 0,
        has_model_selection_in_flow: bool = False,
    ):
        if not has_model_selection_in_flow:
            model_selection = ModelSelection()
            model, parameters = model_selection.tpe(
                df=df, model=model, parameters=parameters, target_column=target_column
            )

        return model, parameters

    @staticmethod
    def _to_list(x: Any):
        return x if isinstance(x, list) else [x]

    def s_v_c(
        self,
        df: dd.DataFrame,
        target_column: str,
        C: float or List[float] = 1.0,
        kernel: str or List[str] = "rbf",
        degree: int or List[int] = 3,
        gamma: str or List[str] = "scale",
        coef0: float or List[float] = 0.0,
        shrinking: bool or List[bool] = True,
        probability: bool or List[bool] = False,
        tol: float or List[float] = 1e-3,
        cache_size: float or List[float] = 200,
        class_weight: dict or str or List[str] or List[dict] = None,
        max_iter: int or List[int] = -1,
        decision_function_shape: str or List[str] = "ovr",
        break_ties: bool or List[bool] = False,
        random_state: int or List[int] = None,
        verbose: int = 0,
        has_model_selection_in_next_step: bool = False,
    ):

        kernels = self._to_list(kernel)
        # Todo: Fix precomputed kernel
        # if 'precomputed' in kernels and X_train.shape[0] != X_train.shape[1]:
        if "precomputed" in kernels:
            kernels.remove("precomputed")

        if isinstance(class_weight, str) and class_weight.lower() == "none":
            class_weight = None
        if isinstance(random_state, str) and random_state.lower() == "none":
            random_state = None

        parameters = {
            "C": tune_param(label="C", values=C),
            "kernel": tune_param(label="kernel", values=kernels),
            "degree": tune_param(label="degree", values=degree),
            "gamma": tune_param(label="gamma", values=gamma),
            "coef0": tune_param(label="coef0", values=coef0),
            "shrinking": tune_param(label="shrinking", values=shrinking),
            "probability": tune_param(label="probability", values=probability),
            "tol": tune_param(label="tol", values=tol),
            "cache_size": tune_param(label="cache_size", values=cache_size),
            "class_weight": tune_param(label="class_weight", values=class_weight),
            "decision_function_shape": tune_param(label="decision_function_shape", values=decision_function_shape),
            "break_ties": tune_param(label="break_ties", values=break_ties),
            "random_state": tune_param(label="random_state", values=random_state),
        }
        if max_iter != -1:
            parameters["max_iter"] = tune_param(label="max_iter", values=max_iter)

        model = svm.SVC()
        model_type = "category"
        model = CategoryModel(model=model)
        model, parameters = self._fit_sklearn(
            model=model,
            parameters=parameters,
            df=df,
            target_column=target_column,
            verbose=verbose,
            has_model_selection_in_flow=has_model_selection_in_next_step,
        )

        return model, parameters, model_type

    def tfcnn(
        self, df: dd.DataFrame, target_column: str, verbose: int = 0, has_model_selection_in_next_step: bool = False
    ):

        n_features = df.drop(target_column, axis=1).shape[1:]
        n_classes = df[target_column].unique().compute().shape[0]

        def build_model(lr=0.01, epsilon=0.9):
            model_ = Sequential([
                layers.Dense(512,
                             activation='relu',
                             input_shape=n_features,
                             kernel_regularizer=tf.keras.regularizers.l2(0.01)
                             ),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(n_classes, activation='softmax')
            ])

            opt = tf.keras.optimizers.Adam(
                learning_rate=lr,
                epsilon=epsilon,
            )

            model_.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])
            return model_

        niceties = dict(verbose=True, epochs=2)

        model = KerasClassifier(model=build_model, lr=0.1, epsilon=1e-7, **niceties)
        model_type = "one_hot"
        model = OneHotModel(model=model)

        parameters = {
            'lr': hp.loguniform('lr', 1e-3, 1e-1),
            'epsilon': hp.loguniform('epsilon', 1e-8, 1e-5)
        }

        model, parameters = self._fit_sklearn(
            model=model,
            parameters=parameters,
            df=df,
            target_column=target_column,
            verbose=verbose,
            has_model_selection_in_flow=has_model_selection_in_next_step,
        )

        return model, parameters, model_type
