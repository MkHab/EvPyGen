from typing import Any, Self, TypeVar, get_origin, get_args

class EvTemplate:
  __args__: dict[TypeVar, Any] = {}
  __cache__: dict[tuple[type[EvTemplate], tuple[Any, ...]], type[EvTemplate]] = {}

  @classmethod
  def __class_getitem__(cls: type[Self], args: Any) -> type[EvTemplate]:
    if not isinstance(args, tuple): # Если параметр 1, то сделать его кортежем
      args = (args,)
    if len(args) != len(cls.__parameters__): # проверка количества параметров
      raise ValueError("Number of parameters does not match template")
    if (cls, args) in EvTemplate.__cache__:  # класс уже был создан
      return EvTemplate.__cache__[cls, args] # возвращаем уже созданный класс, а не создаем новый
    class EvTemplateSpecification(cls):
      __args__: dict[TypeVar, Any] = {        # Задаем __args__, чтобы они были доступны из конструктора
        **cls.__args__,                       # Наследуем параметры родителей
        **dict(zip(cls.__parameters__, args)) # Добавляем текущие параметры
      }
    EvTemplateSpecification.    __name__ = cls.    __name__ + "[...]" # Явное задание имени спецификации
    EvTemplateSpecification.__qualname__ = cls.__qualname__ + "[...]" # Явное задание полного имени спецификации
    EvTemplate.__cache__[cls, args] = EvTemplateSpecification         # кэшируем класс
    return EvTemplateSpecification

  @classmethod
  def _EvResolve(cls: type[Self], param: Any) -> Any:
    if (origin := get_origin(param)) is not None:                      # Если тип является GenericAlias, то
                                                                       # сохраняем его тип (совместимость с typing)
      return origin[tuple(cls._EvResolve(a) for a in get_args(param))] # Разрешаем параметры
    if param in cls.__args__:                                          # Проверяем, был ли параметр задан
      return cls._EvResolve(cls.__args__[param])                       # Рекуррентно разрешаем тип
    return param                                                       # Параметр не задан или отсутствует
