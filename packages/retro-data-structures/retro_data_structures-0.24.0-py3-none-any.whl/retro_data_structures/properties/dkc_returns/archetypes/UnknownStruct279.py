# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct279(BaseProperty):
    unknown_0x8a58a7f8: int = dataclasses.field(default=1)
    unknown_0x6f51c96b: float = dataclasses.field(default=2.0)
    unknown_0x72d0dc87: float = dataclasses.field(default=30.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'oQ\xc9k')  # 0x6f51c96b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6f51c96b))

        data.write(b'r\xd0\xdc\x87')  # 0x72d0dc87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72d0dc87))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x8a58a7f8=data['unknown_0x8a58a7f8'],
            unknown_0x6f51c96b=data['unknown_0x6f51c96b'],
            unknown_0x72d0dc87=data['unknown_0x72d0dc87'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'unknown_0x6f51c96b': self.unknown_0x6f51c96b,
            'unknown_0x72d0dc87': self.unknown_0x72d0dc87,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8a58a7f8, 0x6f51c96b, 0x72d0dc87)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct279]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHf')

    dec = _FAST_FORMAT.unpack(data.read(30))
    assert (dec[0], dec[3], dec[6]) == _FAST_IDS
    return UnknownStruct279(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6f51c96b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x72d0dc87(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x6f51c96b: ('unknown_0x6f51c96b', _decode_unknown_0x6f51c96b),
    0x72d0dc87: ('unknown_0x72d0dc87', _decode_unknown_0x72d0dc87),
}
