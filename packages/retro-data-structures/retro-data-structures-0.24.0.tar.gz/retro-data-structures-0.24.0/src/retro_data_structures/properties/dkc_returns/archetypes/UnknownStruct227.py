# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct227(BaseProperty):
    box_min_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    box_max_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))

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

        data.write(b'\x1c\xa9\x85\xde')  # 0x1ca985de
        data.write(b'\x00\x0c')  # size
        self.box_min_offset.to_stream(data)

        data.write(b';\x12\xe2\xef')  # 0x3b12e2ef
        data.write(b'\x00\x0c')  # size
        self.box_max_offset.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            box_min_offset=Vector.from_json(data['box_min_offset']),
            box_max_offset=Vector.from_json(data['box_max_offset']),
        )

    def to_json(self) -> dict:
        return {
            'box_min_offset': self.box_min_offset.to_json(),
            'box_max_offset': self.box_max_offset.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x1ca985de, 0x3b12e2ef)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct227]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfffLHfff')

    dec = _FAST_FORMAT.unpack(data.read(36))
    assert (dec[0], dec[5]) == _FAST_IDS
    return UnknownStruct227(
        Vector(*dec[2:5]),
        Vector(*dec[7:10]),
    )


def _decode_box_min_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_box_max_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1ca985de: ('box_min_offset', _decode_box_min_offset),
    0x3b12e2ef: ('box_max_offset', _decode_box_max_offset),
}
