""" Data Validation Functions """

# %%
import types
from warnings import warn
import numpy as np
import pandas as pd
import inspect
from functools import wraps


# %% Static Methods

def _validate_no_nans(inputs: dict, name: str):
    """ Raise ValueError if any Input is NaN """

    # iterate over inputs dictionary & test if value is a NaN
    for k, v in inputs.items():

        # error message
        msg = f"{name} error: input {k} is {v}; nans not allowed"

        if pd.api.types.is_number(v):
            if np.isnan(v).any():
                raise ValueError(msg)


def _test_class(var, hint, value, name):
    """ Test value vs. hint which hint was <class 'int'> etc... """
    if not type(value) == hint:
        msg = f"{name} error: var {var} of type {type(value)} passed; " \
              f"doesn't match function type hint == {hint}"
        raise ValueError(msg)


def _test_union_hint(var, hint, value, name):
    """ Test value vs. hint when the hint is a types.UnionType """

    # one can't just convert UnionType back to a tuple of types - need a hack!
    # we convert to string, remove whitespaces then split on the union (|)
    deunion = f"{hint}".replace(" ", "").split("|")

    # now iterate over union
    for i, v in enumerate(deunion):
        match v:
            case 'None':
                deunion[i] = types.NoneType
            case 'int':
                deunion[i] = int
            case 'float':
                deunion[i] = float
            case 'str':
                deunion[i] = str
            case 'dict':
                deunion[i] = dict
            case 'list':
                deunion[i] = list
            case 'tuple':
                deunion[i] = tuple
            case 'numpy.ndarray':
                deunion[i] = np.ndarray
            case 'pandas.core.frame.DataFrame':
                deunion[i] = pd.DataFrame
            case 'pandas.core.series.Series':
                deunion[i] = pd.Series
            case 'pandas._libs.tslibs.timestamps.Timestamp':
                deunion[i] = pd.Timestamp
            case _:
                # if un-coded type, throw a warning
                deunion[i] = types.NoneType
                msg = f"data validation warning: un-coded type {v} in union "
                warn(msg)

    # we zip tuples of (value, type) i.e. (7.5, float)
    # iterate over with isinstance to get a list of booleans
    # if any bool is True means we had a type match
    z = any([isinstance(*z) for z in zip([value] * len(deunion), deunion)])
    if not z:
        msg = f"{name} error: var {var} of type {type(value)} passed; " \
              f"doesn't match function type hint == {hint}"
        raise ValueError(msg)


# %% Data Validation Class

class TypeHintValidation:
    """ TopGun Type Hint Based Data Validation Class

    Idea is to use as decorator to functions where we want to validate inputs.
    By default, this will validate that inputs don't breach function type hints.
    There is also an option to apply additional validation 'methods' by adding
    these as list.

    We can also apply additional methods:
        - nan: will raise error if a number type has had a NaN value is passed
        - others haven't been written

    Important:
        - Decorator ONLY receives explicitly input variables!
        - means a func default value has a type error it will not be checked.

    Example Syntax:
    @TypeHintValidation(methods=['nan'])
    def f(x: int, y: pd.Series | pd.DataFrame):

    References:
        https://medium.com/@ankurpan96/a-handy-validator-using-decorators-in-python-a8722da02fba
        https://levelup.gitconnected.com/validations-in-python-using-metaprogramming-and-decorators-advanced-python-ee4d4278a6b3
        https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator
    """

    def __init__(self, methods=None):

        if methods is None:
            self.methods = []
        elif isinstance(methods, str):
            self.methods = [methods]
        elif isinstance(methods, list):
            self.methods = methods
        else:
            self.methods = []
            msg = f"data validation warning: methods = {methods} provided, " \
                  f"which is unknown; additional methods set to None."
            warn(msg)

    def __call__(self, func):

        # add func to self, so we can access it in the inner function
        self.func = func
        self.hints = func.__annotations__   # dict calling func type hints

        @wraps(func)
        def data_validation_function(*args, **kwargs):
            """ Inner Function in TypeHintValidation Decorator """

            # create dictionary or inputs where var name is the key
            inputs = dict(zip(self.func.__code__.co_varnames, args)) | kwargs

            # iterate over inputs
            # remember only user inputs passed; func defaults not given to decorator
            for k, v in inputs.items():

                # frequently None is given as an input not match by Type Hine
                # generally where a func grabs something from self in a class
                # we provide option to skip tests if None is provided
                if 'none' in self.methods and isinstance(v, types.NoneType):
                    continue

                # check if k-th var name has type hint
                if k in self.hints:

                    hint = self.hints[k]    # type hint object for k-th input

                    # hints can come in multiple formats
                    # most commonly hint will be class of type i.e <class 'int'>
                    # these are trivial to unpack using inspect.isclass()
                    if inspect.isclass(hint):
                        _test_class(k, hint, v, self.func.__name__)
                    elif isinstance(hint, types.NoneType):
                        # for None, we need to pass types.NoneType as hint
                        _test_class(k, types.NoneType, v, self.func.__name__)
                    elif isinstance(hint, types.UnionType):
                        _test_union_hint(k, hint, v, self.func.__name__)
                    else:
                        warn(f"data validation: unknown method in {hint}")

            # additional methods:
            if 'nan' in self.methods:
                _validate_no_nans(inputs, self.func.__name__)

            return self.func(*args, **kwargs)

        return data_validation_function
