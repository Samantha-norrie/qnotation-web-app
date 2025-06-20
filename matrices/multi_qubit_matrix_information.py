from abc import ABC, abstractmethod
import numpy as np

class MultiQubitMatrixInformation(ABC):

    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        names = getattr(cls, "names", [])
        for name in names:
            MultiQubitMatrixInformation.registry[name.lower()] = cls

    @classmethod
    def get_little_endian(cls, params={}):
        pass

    @classmethod
    def get_big_endian(cls, params={}):
        pass

    @classmethod
    def get_gate_class(cls, name):
        try:
            return cls.registry[name.lower()]
        except KeyError:
            raise ValueError(f"No gate class found for name '{name}'")