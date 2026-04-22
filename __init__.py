from typing import Any, Self, TypeVar, get_origin, get_args

class EvGen:
  __args__: dict[TypeVar, Any] = {}
  __cache__: dict[tuple[type[EvGen], tuple[Any, ...]], type[EvGen]] = {}

  @classmethod
  def __class_getitem__(cls: type[Self], args: Any) -> type[EvGen]:
    if not isinstance(args, tuple):
      args = (args,)
    if len(args) != len(cls.__parameters__):
      raise ValueError("Number of parameters does not match template")
    if (cls, args) in EvGen.__cache__:
      return EvGen.__cache__[cls, args]
    class SubEvGen(cls):
      __args__: dict[TypeVar, Any] = {**cls.__args__, **dict(zip(cls.__parameters__, args))}
    SubEvGen.    __name__ = cls.    __name__ + "[...]"
    SubEvGen.__qualname__ = cls.__qualname__ + "[...]"
    EvGen.__cache__[cls, args] = SubEvGen
    return SubEvGen

  @classmethod
  def _EvResolve(cls: type[Self], param: Any) -> Any:
    if (origin := get_origin(param)) is not None:                      # Если тип является GenericAlias, то
                                                                       # сохраняем его тип (совместимость с typing)
      return origin[tuple(cls._EvResolve(a) for a in get_args(param))] # Разрешаем параметры
    if param in cls.__args__:                                          # Проверяем, был ли параметр задан
      return cls._EvResolve(cls.__args__[param])                       # Рекуррентно разрешаем тип
    return param                                                       # Параметр не задан или отсутствует
