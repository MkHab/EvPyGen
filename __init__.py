from typing import Any, Self, get_origin, get_args

class EvGen:
  __args__: dict[Any, Any] = {}

  @classmethod
  def __class_getitem__(cls: type[Self], args: Any) -> type[EvGen]:
    if not isinstance(args, tuple):
      args = (args,)
    if len(args) != len(cls.__parameters__):
      raise ValueError("Number of parameters does not match template")
    class SubEvGen(cls):
      __args__: dict[Any, Any] = {**cls.__args__, **dict(zip(cls.__parameters__, args))}
    return SubEvGen

  @classmethod
  def _EvResolve(cls: type[Self], param: Any) -> Any:
    if (origin := get_origin(param)) is not None:                      # Если тип является GenericAlias, то
                                                                       # сохраняем его тип (совместимость с typing)
      return origin[tuple(cls._EvResolve(a) for a in get_args(param))] # Разрешаем параметры
    if param in cls.__args__:                                          # Проверяем, был ли параметр задан
      return cls._EvResolve(cls.__args__[param])                       # Рекуррентно разрешаем тип
    return param                                                       # Параметр не задан или отсутствует
