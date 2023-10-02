from typing import Union

from hyperopt import hp


def tune_param(label: str, values: Union[list, str, int, float, bool, dict, None], method: str = ""):
    if method:
        if isinstance(values, list):
            return getattr(hp, method)(label, values)
        else:
            return getattr(hp, method)(label, [values])

    if isinstance(values, str) or isinstance(values, bool) or isinstance(values, dict) or values is None:
        return hp.choice(label, [values])
    elif isinstance(values, int):
        return hp.randint(label, int(values / 2), int(values * 2))
    elif isinstance(values, float):
        print("inside values", values / 2, values * 2)
        return hp.uniform(label, values / 2, values * 2)
    elif isinstance(values, list):
        if isinstance(values[0], str) or isinstance(values[0], bool) or isinstance(values, dict) or values[0] is None:
            return hp.choice(label, values)
        elif isinstance(values[0], int):
            if len(values) == 2:
                return hp.randint(label, values[0], values[-1])
            else:
                return hp.choice(label, values)
        else:
            if len(values) == 2:
                return hp.uniform(label, values[0], values[-1])
            else:
                return hp.choice(label, values)
    else:
        raise ValueError("Tune param error. Not sure which method to use."
                         f"Label: {label}, values: {values}")
