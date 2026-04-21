from typing import Any, Self

class EvGen:
  __args__: dict[Any, Any] = {}

  @classmethod
  def __class_getitem__(cls: type[Self], args: Any) -> type[EvGen]:
    if not isinstance(args, tuple):
      args = (args,)
    if len(args) != len(cls.__parameters__):
      raise ValueError("Number of parameters does not match template")
    class SubEvGen(cls):
      __args__ = {**cls.__args__, **dict(zip(cls.__parameters__, args))}
    return SubEvGen

  @classmethod
  def _EvResolve(cls: type[Self], param: Any) -> Any:
    if param in cls.__args__:
      return cls._EvResolve(cls.__args__[param])
    return param
