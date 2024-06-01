from inspyre_toolbox.syntactic_sweets.properties import RestrictedSetter
from typing import Union
from functools import wraps


def validate_float_between(min_value: float = 0.0, max_value: float = 1.0):
    """
    Decorator to ensure that a property setter only accepts floats between a given range.

    Parameters:
        min_value (Union[float, int], optional):
            The minimum value that the property can be.

        max_value (Union[float, int], optional):
            The maximum value that the property can be.

    Returns:
        function:
            The decorated function.

    Raises:
        ValueError:
            If the value is not between the specified range.

    Examples:
        >>> class Test:
        ...     @validate_float_between(0.0, 1.0)
        ...     def test(self, value):
        ...         return value
        ...
        >>> t = Test()
        >>> t.test(0.5)
        0.5
        >>> t.test(1.5)
        Traceback (most recent call last):
        ...
        AttributeError: Value must be between 0.0 and 1.0
    """
    def decorator(func):
        @wraps(func)
        def wrapper(instance, value):
            if isinstance(value, (int, float)) and min_value < value <= max_value:
                return func(instance, float(value))
            else:
                raise ValueError(f"Value must be between {min_value} and {max_value}")

        return wrapper
    return decorator


class ReactiveProperty:
    def __init__(self, default_value=None, callback=None, *args, **kwargs):
        self._default_value = default_value
        self._callbacks = []
        if callback:
            self.add_callback(callback, *args, **kwargs)

    def __set_name__(self, owner, name):
        self._name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self._name):
            setattr(instance, self._name, self._default_value)
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        setattr(instance, self._name, value)
        for callback, args, kwargs in self._callbacks:
            callback(value, *args, **kwargs)

    def add_callback(self, callback, *args, **kwargs):
        self._callbacks.append((callback, args, kwargs))

class FrozenProperty(RestrictedSetter):
    def __init__(self, *args, **kwargs):
        """
        Initialize the FrozenProperty object.

        Args:
            initial (any): Initial value of the property.
            allowed_types (type or tuple of types, optional): Allowed types for the property value.

        Raises:
            AttributeError: If the initial value is not of the correct type.
        """
        super().__init__(*args, **kwargs)
        if "initial" in kwargs:
            self.initial = kwargs['initial']

        if 'allowed_types' in kwargs and (
                self.initial is not None and
                not isinstance(
                        self.initial,
                        kwargs['allowed_types']
                        )
        ):
            raise AttributeError(
                    f"Initial value must be of type {kwargs['allowed_types']}, not {type(self.initial)}"
                    )

    def __get__(self, instance, owner):
        return self if instance is None else instance.__dict__.get(self.attr_name)

    def __set__(self, instance, value):
        if not instance.__dict__.get(f"_{self.attr_name}_frozen", False):
            if self.allowed_types and not isinstance(value, self.allowed_types):
                raise AttributeError(
                    f"Value must be of type {self.allowed_types}, not {type(value)}"
                )
            instance.__dict__[self.attr_name] = value
            instance.__dict__[f"_{self.attr_name}_frozen"] = True
        else:
            raise AttributeError("Cannot modify a frozen property")

    def __set_name__(self, owner, name):
        self.attr_name = name


def freeze_property(cls):
    class FrozenPropertyClass(cls):
        def __setattr__(self, name, value):
            try:
                prop = getattr(self.__class__, name)
                if isinstance(prop, FrozenProperty) and self.__dict__.get(f"_{name}_frozen", False):
                    raise AttributeError(f"Cannot modify a frozen property: {name}")
            except AttributeError:
                pass
            super().__setattr__(name, value)

    return FrozenPropertyClass
