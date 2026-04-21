from types import GenericAlias
from typing import Any, Self, Generic, TypeVar, TypeVarTuple, ParamSpec
import warnings

def format_class_name(cls: type) -> str:
  if (module := getattr(cls, "__module__", None)) in (None, "__main__", "builtin"):
    return cls.__qualname__
  return module + "." + cls.__qualname__

class EvAlias(GenericAlias): # Для обратной совместимости с typing
  @classmethod
  def __new__(cls: type[Self], origin: type[EvGen], args: Any) -> Self:
    if not isinstance(args, tuple): # Сделано на всякий случай, чтобы параметры всегда были кортежем
      args = (args,)
    if not issubclass(origin, EvGen): # Проверяется, чтобы не затрагивать классы других библиотек/поектов
      raise TypeError(f"{format_class_name(EvAlias)} can be created only to {format_class_name(EvGen)}")
    return super().__new__(cls, origin, args) # Делегируем родному конструктору
  
  def __call__(self: Self, *args, **kwargs) -> EvGen:
    obj = self.__origin__.__new__(self.__origin__) # Необходимо, чтобы задать __orig_class__ до вызова конструктора
    obj.__orig_class__ = self                      # Для обратной совместимости с typing
    self.__origin__.__init__(obj, *args, **kwargs) # Теперь инициализация может использовать __orig_class__
    return obj
  
  def __getattr__(self, name: str) -> Any:
    # Вывоодим предупреждение, так как без объекта не понятно как задать __orig_class__
    warnings.warn(f"Getting attributes of {format_class_name(EvAlias)} not recommended", RuntimeWarning, 2)
    return self.__origin__.__getattr__(name) # Делигируем получение аттрибута классу

  def _EvParams(self: Self) -> tuple[Any, ...]:
    return self.__origin__._EvParams() # Запрашиваем список параметров у класса

  def _EvArgs(self: Self) -> tuple[Any, ...]:
    return self.__args__ # Возвращаем переданные параметры

  def _EvOrigin(self: Self) -> type[EvGen]:
    return self.__origin__._EvOrigin() # Запрашиваем исходный класс

class EvGen(Generic): # Для обратной совместимости с typing
  @classmethod
  def __class_getitem__(cls: type[EvGen], args: Any) -> EvAlias:
    return EvAlias(cls, args) # возвращаем вместо родного GenericAlias дочерний класс

  @classmethod
  def _EvParams(cls: type[Self]) -> tuple[Any, ...]: # Список параметров известен на этапе класса
    return getattr(cls, "__parameters__", ()) # Возвращаем список параметров

  def _EvArgs(self: Self) -> tuple[Any, ...] | None: # __orig_class__ может быть получен только от объекта
    origin: EvAlias | None = getattr(self, "__orig_class__", None)
    if origin is None:
      return None
    return origin._EvArgs() # Возвращаем переданные параметры

  @classmethod
  def _EvOrigin(cls: type[Self]) -> type[Self]: # Исходный класс известен на этапе класса
    return cls # Возвращаем сам класс