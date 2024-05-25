from inspyre_toolbox.syntactic_sweets.properties import RestrictedSetter


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
