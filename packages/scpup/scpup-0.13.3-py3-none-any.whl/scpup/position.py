from __future__ import annotations
from functools import partialmethod
import scpup


__all__ = [
  "EauLayout",
  "EauPosition",
  "EauGrid"
]


class EauLayout:
  __slots__ = (
    "type",
    "value",
    "offset"
  )

  @classmethod
  def _(cls, type: str, value: int = 0, *, offset: int = 0) -> EauLayout:
    """Initialize a layout object with the type of layout, a value (if applies)
    and some extra properties depending on the layout type

    Layout objects are not meant to be created directly calling the constructor,
    instead a partial method should be used because there is 1 for each layout
    type. If the value is calculated only with 1 value, you can either pass that
    value through the value param or the offset param, e.g.:

    ```python
    # The following 2 statements are equal:
    EauLayout.Top(5)
    EauLayout.Top(offset=5)

    # But if both are specified then only value will be used, in the example
    # below only 5 will be used
    EauLayout.Top(5, offset=10)
    ```

    Layout types:

    * Position:
        - value + offset
        - Anchor: centerx, centery
    * Top:
        - abs(value)
        - Anchor: centerx, top
    * Bottom:
        - size - abs(value)
        - Anchor: centerx, bottom
    * Left:
        - abs(value)
        - Anchor: left, centery
    * Right:
        - size - abs(value)
        - Anchor: right, centery
    * Center:
        - size // 2 + value
        - Anchor: centerx, centery

    Args:
      type:
        The type of layout. This is used to determine how will the value, offset
        and extra properties will be parsed.
      value:
        The value of the coordinate
      offset:
        A number to adjust the position of this layout
      total:
        Depending on the layout type this may be used differently.
        Defaults to 1.
    """
    instance = cls()
    instance.type = type
    instance.value = value
    instance.offset = offset
    return instance

  Position = partialmethod(_, 'Position')
  Top = partialmethod(_, 'Top')
  Bottom = partialmethod(_, 'Bottom')
  Center = partialmethod(_, 'Center')
  Left = partialmethod(_, 'Left')
  Right = partialmethod(_, 'Right')

  def parse(self, size: int) -> int:
    if self.type == "Position":
      return self.value + self.offset
    elif self.type == "Top" or self.type == "Left":
      return abs(self.offset)
    elif self.type == "Right" or self.type == "Bottom":
      return size - abs(self.offset)
    elif self.type == "Center":
      return size // 2 + self.offset
    raise ValueError(f"Unknown layout type: {self.type}")


class EauPosition:
  __slots__ = (
    "x",
    "y",
    "margin"
  )

  def __init__(
    self,
    x: int | EauLayout,
    y: int | EauLayout,
    *,
    margin: int | tuple[int, int] | tuple[int, int, int, int] = 0
  ):
    self.x = x if isinstance(x, EauLayout) else EauLayout.Position(x)
    self.y = y if isinstance(y, EauLayout) else EauLayout.Position(y)
    self.margin = margin

  def as_rectargs(self) -> dict[str, int]:
    displayService = scpup.EauService.get("EauDisplayService")
    width, height = displayService.size
    if isinstance(self.margin, int):
      ml = mr = mt = mb = self.margin
    elif len(self.margin) == 2:
      (ml, mt), (mr, mb) = self.margin, self.margin
    else:
      ml, mr, mt, mb = self.margin
    xarg = self.x.type.lower() if self.x.type in ["Left", "Right"] else "centerx"
    yarg = self.y.type.lower() if self.y.type in ["Top", "Bottom"] else "centery"
    if self.x.type == 'Right':
      ml = 0
      width -= mr
    if self.y.type == 'Bottom':
      mt = 0
      height -= mb
    return {
      xarg: ml + self.x.parse(width - (ml + mr)),
      yarg: mt + self.y.parse(height - (mt + mb))
    }


class EauGrid:
  __slots__ = (
    "rows",
    "cols",
    "margin"
  )

  def __init__(
    self, rows: int | None = None,
    cols: int | None = None,
    *,
    margin: int | tuple[int, int] | tuple[int, int, int, int] = 0
  ):
    self.rows = rows
    self.cols = cols
    if isinstance(margin, int):
      self.margin = (margin, margin, margin, margin)
    elif len(margin) == 2:
      self.margin = (margin[0], margin[0], margin[1], margin[1])
    else:
      self.margin = margin

  def __call__(self, x: int, y: int) -> EauPosition:
    return self.cell(x, y)

  def x(self, num: int) -> EauLayout:
    if not self.cols:
      raise ValueError("Columns were not specified for this grid.")
    elif num > self.cols or num < 1:
      raise ValueError(f"Column value must be between 1 and {self.cols}.")
    size = scpup.EauService.get("EauDisplayService").size
    w = (size[0] - (self.margin[0] + self.margin[1])) // (self.cols * 2)
    t = num * 2 - 1
    return EauLayout.Position(self.margin[0] + w * t)

  def y(self, num: int) -> EauLayout:
    if not self.rows:
      raise ValueError("Rows were not specified for this grid.")
    elif num > self.rows or num < 1:
      raise ValueError(f"Row value must be between 1 and {self.rows}.")
    size = scpup.EauService.get("EauDisplayService").size
    w = (size[1] - (self.margin[2] + self.margin[3])) // (self.rows * 2)
    t = num * 2 - 1
    return EauLayout.Position(self.margin[2] + w * t)

  def cell(self, x: int, y: int) -> EauPosition:
    if not self.rows or not self.cols:
      raise ValueError("Grid is not made for 2 axis.")
    elif x > self.cols or y > self.rows or x < 1 or y < 1:
      raise ValueError("Row and column values must be between 1 and the total of each axis.")
    return EauPosition(
      self.x(x),
      self.y(y)
    )
