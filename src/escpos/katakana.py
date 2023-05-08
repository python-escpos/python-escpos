#  -*- coding: utf-8 -*-
"""Helpers to encode Japanese characters.

I doubt that this currently works correctly.
"""


try:
    import jaconv
except ImportError:
    jaconv = None


def encode_katakana(text):
    """I don't think this quite works yet."""
    encoded = []
    for char in text:
        if jaconv:
            # try to convert japanese text to half-katakanas
            char = jaconv.z2h(jaconv.hira2kata(char))
            # TODO: "the conversion may result in multiple characters"
            # If that really can happen (I am not really shure), than the string would have to be split and every single
            #  character has to passed through the following lines.

        if char in TXT_ENC_KATAKANA_MAP:
            encoded.append(TXT_ENC_KATAKANA_MAP[char])
        else:
            # TODO doesn't this discard all that is not in the map? Can we be sure that the input does contain only
            # encodable characters? We could at least throw an exception if encoding is not possible.
            pass
    return b"".join(encoded)


TXT_ENC_KATAKANA_MAP = {
    # Maps UTF-8 Katakana symbols to KATAKANA Page Codes
    # TODO: has this really to be hardcoded?
    # Half-Width Katakanas
    "｡": b"\xa1",
    "｢": b"\xa2",
    "｣": b"\xa3",
    "､": b"\xa4",
    "･": b"\xa5",
    "ｦ": b"\xa6",
    "ｧ": b"\xa7",
    "ｨ": b"\xa8",
    "ｩ": b"\xa9",
    "ｪ": b"\xaa",
    "ｫ": b"\xab",
    "ｬ": b"\xac",
    "ｭ": b"\xad",
    "ｮ": b"\xae",
    "ｯ": b"\xaf",
    "ｰ": b"\xb0",
    "ｱ": b"\xb1",
    "ｲ": b"\xb2",
    "ｳ": b"\xb3",
    "ｴ": b"\xb4",
    "ｵ": b"\xb5",
    "ｶ": b"\xb6",
    "ｷ": b"\xb7",
    "ｸ": b"\xb8",
    "ｹ": b"\xb9",
    "ｺ": b"\xba",
    "ｻ": b"\xbb",
    "ｼ": b"\xbc",
    "ｽ": b"\xbd",
    "ｾ": b"\xbe",
    "ｿ": b"\xbf",
    "ﾀ": b"\xc0",
    "ﾁ": b"\xc1",
    "ﾂ": b"\xc2",
    "ﾃ": b"\xc3",
    "ﾄ": b"\xc4",
    "ﾅ": b"\xc5",
    "ﾆ": b"\xc6",
    "ﾇ": b"\xc7",
    "ﾈ": b"\xc8",
    "ﾉ": b"\xc9",
    "ﾊ": b"\xca",
    "ﾋ": b"\xcb",
    "ﾌ": b"\xcc",
    "ﾍ": b"\xcd",
    "ﾎ": b"\xce",
    "ﾏ": b"\xcf",
    "ﾐ": b"\xd0",
    "ﾑ": b"\xd1",
    "ﾒ": b"\xd2",
    "ﾓ": b"\xd3",
    "ﾔ": b"\xd4",
    "ﾕ": b"\xd5",
    "ﾖ": b"\xd6",
    "ﾗ": b"\xd7",
    "ﾘ": b"\xd8",
    "ﾙ": b"\xd9",
    "ﾚ": b"\xda",
    "ﾛ": b"\xdb",
    "ﾜ": b"\xdc",
    "ﾝ": b"\xdd",
    "ﾞ": b"\xde",
    "ﾟ": b"\xdf",
}
