from __future__ import annotations
from functools import partialmethod
import scpup


__all__ = [
  "EauLayout",
  "EauPosition"
]


class EauLayout:
  __slots__ = (
    "type",
    "value",
    "offset",
    "total"
  )

  def __init__(self, type: str, value: int = 0, *, offset: int = 0, total: int = 1) -> None:
    self.type = type
    self.value = value
    self.offset = offset
    self.total = total

  @classmethod
  def _create(cls, type: str, value: int = 0, *, offset: int = 0, total: int = 1) -> "EauLayout":
    return cls(type, value, offset=offset, total=total)

  Position = partialmethod(_create, 'Position')
  Top = partialmethod(_create, 'Top')
  Bottom = partialmethod(_create, 'Bottom')
  Center = partialmethod(_create, 'Center')
  Left = partialmethod(_create, 'Left')
  Right = partialmethod(_create, 'Right')
  Grid = partialmethod(_create, 'Grid')

  def parse(self, size: int) -> int:
    if self.type == "Position":
      return self.value + self.offset
    elif self.type == "Top" or self.type == "Left":
      return abs(self.offset)
    elif self.type == "Right" or self.type == "Bottom":
      return size - abs(self.offset)
    elif self.type == "Center":
      return size // 2 + self.offset
    elif self.type == "Grid":
      if self.value > self.total:
        raise ValueError(f"Value cannot be greater than total. Value: {self.value}. Total: {self.total}")
      w = size // (self.total * 2)
      t = self.value * 2 - 1
      return w * t + self.offset
    raise ValueError(f"Unknown layout type: {self.type}")


class EauPosition:
  __slots__ = (
    "x",
    "y",
    "margin"
  )

  def __init__(self,
               x: int | EauLayout,
               y: int | EauLayout,
               *,
               margin: int | tuple[int, int] | tuple[int, int, int, int] | None = None):
    self.x = x if isinstance(x, EauLayout) else EauLayout.Position(x)
    self.y = y if isinstance(y, EauLayout) else EauLayout.Position(y)
    self.margin = margin

  def as_rectargs(self) -> dict[str, int]:
    displayService = scpup.EauService.get("EauDisplayService")
    size = displayService.size
    xarg = self.x.type.lower() if self.x.type in ["Left", "Right"] else "centerx"
    yarg = self.y.type.lower() if self.y.type in ["Top", "Bottom"] else "centery"
    if isinstance(self.margin, int):
      ml = mr = mt = mb = self.margin
    elif self.margin is None:
      ml = mr = mt = mb = 0
    elif len(self.margin) == 2:
      (ml, mt), (mr, mb) = self.margin, self.margin
    else:
      ml, mr, mt, mb = self.margin
    return {
      xarg: ml + self.x.parse(size[0] - (ml + mr)),
      yarg: mt + self.y.parse(size[1] - (mt + mb))
    }
