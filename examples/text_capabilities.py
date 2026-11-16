# /// script
# requires-python = ">=3.11"
# dependencies = ["python-escpos"]
# [tool.uv.sources]
# python-escpos = { path = "../", editable = true }
# ///
"""Show the text formatting capabilities of the library.

Every section prints a short title followed by a sample line,
so the result on paper tells which setting produced which look.
Not every printer supports every setting (for example ``smooth`` or ``flip``),
unsupported settings are usually ignored by the printer.
"""

from escpos import printer

# p = printer.Usb(0x04B8, 0x0E20, profile="TM-P80")
p = printer.Dummy(profile="TM-P80")


def sample(title: str, **kwargs: bool | int | str) -> None:
    """Print a title and a sample line with the given text settings.

    The settings are reset to the defaults before the title is printed,
    so only the sample line is formatted.
    """
    p.set_with_default()
    p.textln(title)
    p.set_with_default(**kwargs)  # type: ignore[arg-type]
    p.textln("The quick brown fox")
    p.ln()


p.set_with_default(align="center", bold=True)
p.textln("Text capabilities")
p.ln()

# Emphasis
sample("Default")
sample("Bold", bold=True)
sample("Underline (1 dot)", underline=1)
sample("Underline (2 dots)", underline=2)
sample("Bold and underline", bold=True, underline=1)
sample("Inverted (white on black)", invert=True)

# Alignment
sample("Align left", align="left")
sample("Align center", align="center")
sample("Align right", align="right")

# Fonts
sample("Font A", font="a")
sample("Font B", font="b")

# Size
sample("Double width", double_width=True)
sample("Double height", double_height=True)
sample("Double width and height", double_width=True, double_height=True)
sample("Custom size (width 3, height 2)", custom_size=True, width=3, height=2)

# Other printer settings
sample("Smooth", smooth=True)
sample("Upside down (flip)", flip=True)

# Horizontal tabs: set the tab stops first, then use "\t" in the text.
p.set_with_default()
p.textln("Horizontal tabs (every 8 characters)")
p.control("HT", count=4, tab_size=8)
p.textln("A\tB\tC\tD")
p.ln()

p.cut(mode="PART", feed=True)
