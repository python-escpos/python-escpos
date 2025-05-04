"""Example for Kanji features."""

from escpos.printer import Usb

checkerboard_kanji = (
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
)

p = Usb(0x04B8, 0x0E1F, {}, profile="TM-T20II")

p.set_kanji_encoding("iso2022_jp")

p.set(align="center")

p.set_kanji_decoration(double_height=True)
p.set_kanji_underline(2)
p.kanji_text("漢字モード\n")
p.set_kanji_decoration()
p.ln()

p.kanji_text("こんにちは世界！\n")
p.ln()

p.define_user_defined_kanji(b"\x77\x7e", checkerboard_kanji)
p.write_user_defined_kanji(b"\x77\x7e")
p.kanji_text("←外字\n")
p.delete_user_defined_kanji(b"\x77\x7e")
p.cut()
