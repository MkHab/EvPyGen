Данный модуль разработан для реализации обобщенного программирования,
аналогичного принятому в C++.

```python
from typing import Self
from EvPyGen import EvGen

class TemplateClassA[TP1, TP2](EvGen):
  @classmethod
  def printResolved(cls: type[Self]) -> None:
    print(f"{__class__}.TP1 = {cls._EvResolve(TP1)}")
    print(f"{__class__}.TP2 = {cls._EvResolve(TP2)}")

class TemplateClassB[TP1, TP2, TP3](TemplateClassA[TP1 | TP2, str]):
  @classmethod
  def printResolved(cls: type[Self]) -> None:
    print(f"{__class__}.TP1 = {cls._EvResolve(TP1)}")
    print(f"{__class__}.TP2 = {cls._EvResolve(TP2)}")
    print(f"{__class__}.TP3 = {cls._EvResolve(TP3)}")
    super().printResolved()

TemplateClassA[int] # ValueError: Number of parameters does not match template
TemplateClassA[int, float].printResolved()
# <class '__main__.TemplateClassA'>.TP1 = <class 'int'>
# <class '__main__.TemplateClassA'>.TP2 = <class 'float'>
TemplateClassB[int, float, str].printResolved()
# <class '__main__.TemplateClassB'>.TP1 = <class 'int'>
# <class '__main__.TemplateClassB'>.TP2 = <class 'float'>
# <class '__main__.TemplateClassB'>.TP3 = <class 'str'>
# <class '__main__.TemplateClassA'>.TP1 = int | float
# <class '__main__.TemplateClassA'>.TP2 = <class 'str'>
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