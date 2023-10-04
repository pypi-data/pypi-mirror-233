# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct283(BaseProperty):
    unknown_0x968337ab: int = dataclasses.field(default=1)
    unknown_0x8308e359: int = dataclasses.field(default=3)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if (result := _fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x96\x837\xab')  # 0x968337ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x968337ab))

        data.write(b'\x83\x08\xe3Y')  # 0x8308e359
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8308e359))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x968337ab=data['unknown_0x968337ab'],
            unknown_0x8308e359=data['unknown_0x8308e359'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x968337ab': self.unknown_0x968337ab,
            'unknown_0x8308e359': self.unknown_0x8308e359,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x968337ab, 0x8308e359)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct283]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHl')

    dec = _FAST_FORMAT.unpack(data.read(20))
    assert (dec[0], dec[3]) == _FAST_IDS
    return UnknownStruct283(
        dec[2],
        dec[5],
    )


def _decode_unknown_0x968337ab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8308e359(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x968337ab: ('unknown_0x968337ab', _decode_unknown_0x968337ab),
    0x8308e359: ('unknown_0x8308e359', _decode_unknown_0x8308e359),
}
