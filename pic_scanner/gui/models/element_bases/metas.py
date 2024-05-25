from abc import ABCMeta, abstractmethod


class AutoBuildMeta(ABCMeta):
    """
    Metaclass for classes that should build themselves upon instantiation when the `auto_build`
    attribute is True.

    This metaclass overrides the `__call__` method to build the instance if the `auto_build`
    attribute is True.
    """
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)

        if getattr(obj, 'auto_build', False) and not getattr(obj, 'is_built', False):
            obj.build()
        return obj


class AutoBuildRunMeta(ABCMeta):
    """
    Metaclass for classes that should build and run themselves upon instantiation when the `auto_build`
    and `auto_run` attributes are True.

    This metaclass overrides the `__call__` method to build and run the instance if the `auto_build`
    and `auto_run` attributes are True.
    """
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)

        if getattr(obj, 'auto_build', False) and not getattr(obj, 'is_built', False):
            obj.build()

        if getattr(obj, 'auto_run', False) and not getattr(obj, 'running', False):
            obj.run()

        return obj
