# EvPyGen

Данный модуль разработан для реализации обобщенного программирования,
аналогичного принятому в C++.

Данный проект призван решить следующие проблемы:
1. Потерю сведений о шаблоне при создании экземпляра, проявляющуюся в:
  * **Потере `typing.get_origin`.** Так, например, код
    ```Python
    from typing import get_origin

    get_origin(list[int])
    ```
    ожидаемо возвращает `list`, тогда как при создании экземпляра
    ```Python
    from typing import get_origin

    get_origin(list[int](i for i in range(5)))
    ```
    возвращаемое значение меняется на `None`.
  * **Потере `typing.get_args`.** Так, например, код
    ```Python
    from typing import get_args

    get_args(list[int])
    ```
    ожидаемо возвращает `(int,)`, тогда как при создании экземпляра
    ```Python
    from typing import get_args

    get_args(list[int](i for i in range(5)))
    ```
    возвращаемое значение меняется на пустой кортеж.
2. Отсутствие стандартной возможности запросить переданные шаблону
   параметры из экземпляра. Стандартная реализация `typing` задает
   аттрибут `__orig_class__`, он не регламентирован и не доступен
   в некоторых ситуациях (например, в конструкторе).
3. Неразличимость экземпляров различных шаблонов, в частности
  `type(list[str]()) == type(list[int]())` возвращает `True`.

## Предлагаемые решения

Основным предлагаемым решением является динамическое создание дочерних классов,
обладающих аттрибутом `__args__`, хранящим словарь, отображающий `TypeVar` в
переданные шаблону параметры.

## Пример использования

Для начала определим два класса, на примере которых будут продемонстрированы
основные возможности такого подхода:
```python
from typing import Self
from EvPyGen import EvGen

class TemplateClassA[TP1, TP2](EvGen):
    @classmethod
    def printResolved(cls: type[Self]) -> None:
        print(f"{__class__.__qualname__}.TP1 = {cls._EvResolve(TP1)}")
        print(f"{__class__.__qualname__}.TP2 = {cls._EvResolve(TP2)}")

class TemplateClassB[TP1, TP2, TP3](TemplateClassA[TP1 | TP2, str]):
    @classmethod
    def printResolved(cls: type[Self]) -> None:
        print(f"{__class__.__qualname__}.TP1 = {cls._EvResolve(TP1)}")
        print(f"{__class__.__qualname__}.TP2 = {cls._EvResolve(TP2)}")
        print(f"{__class__.__qualname__}.TP3 = {cls._EvResolve(TP3)}")
        super().printResolved()
```

* Попытка использования шаблона с неверным количеством параметров
  ```python
  TemplateClassA[int]
  ```
  приводит к соответствующей ошибке:
  ```text
  ValueError: Number of parameters does not match template
  ```
* При передаче шаблону корректного набора параметров ошибка не
  возникает и становится возможным запросить переданные параметры,
  например, через описанный выше метод `printResolved`:
  ```python
  TemplateClassA[int, float].printResolved()
  ```
  Что приводит к выводу программы:
  ```text
  TemplateClassA.TP1 = <class 'int'>
  TemplateClassA.TP2 = <class 'float'>
  ```
* Данные шаблоны можно использовать в качестве родительских классов,
  причем разрешение параметров происходит на всех уровнях наследования.
  Так, использование описанного выше шаблона `TemplateClassB`
  ```python
  TemplateClassB[int, float, str].printResolved()
  ```
  приводит к выводу:
  ```text
  TemplateClassB.TP1 = <class 'int'>
  TemplateClassB.TP2 = <class 'float'>
  TemplateClassB.TP3 = <class 'str'>
  TemplateClassA.TP1 = int | float
  TemplateClassA.TP2 = <class 'str'>
  ```
* Задание одинаковых значений приводит не к созданию новой сущности, а к
  возврату уже созданной, то есть
  `TemplateClassA[int, float] == TemplateClassB[int, float]` возвращает
  `True`, а
  `TemplateClassA[int, float] == TemplateClassB[int, str]` вернет
  `False`.

## TODO
- [ ] Реализовать поддержку основных типов параметров шаблонов:
  - [x] реализовать поддержку `TypeVar` (2026.04.21);
  - [ ] реализовать поддержку `TypeVarTuple`;
  - [ ] реализовать поддержку `ParamSpec`:
    - [ ] реализовать поддержку `ParamSpecArgs`;
    - [ ] реализовать поддержку `ParamSpecKwargs`.
- [x] Реализовать разрешение &laquo;составных типов&raquo; (объединений, опциональных, т.д.),
      определяемых `typing` (2026.04.22).
- [ ] Реализовать разрешение вложенных `EvGen`.
- [x] Реализовать кеширование шаблонов таким образом, чтобы одинаковые параметры приводили
      к использованию одного и того же экземпляра (2026.04.22).