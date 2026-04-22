# EvPyGen

Данный модуль разработан для реализации обобщенного программирования,
аналогичного принятому в C++.

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

* Попытка использования шаблона с неверным количеством параметров:
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

## TODO
- [ ] Реализовать поддержку основных типов параметров шаблонов:
  - [x] Реализовать поддержку `TypeVar` (2026.04.21);
  - [ ] Реализовать поддержку `TypeVarTuple`;
  - [ ] Реализовать поддержку `ParamSpec`:
    - [ ] Реализовать поддержку `ParamSpecArgs`;
    - [ ] Реализовать поддержку `ParamSpecKwargs`.
- [x] Реализовать разрешение &laquo;составных типов&raquo; (объединений, опциональных, т.д.),
      определяемых `typing` (2026.04.22).
- [ ] Реализовать разрешение вложенных `EvGen`.