# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class SpindleCameraStruct(BaseProperty):
    interpolant_type: int = dataclasses.field(default=0)
    interpolant_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'>\x9c\xf1@')  # 0x3e9cf140
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.interpolant_type))

        data.write(b'\x9aY\x8f\xa5')  # 0x9a598fa5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.interpolant_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            interpolant_type=data['interpolant_type'],
            interpolant_spline=Spline.from_json(data['interpolant_spline']),
        )

    def to_json(self) -> dict:
        return {
            'interpolant_type': self.interpolant_type,
            'interpolant_spline': self.interpolant_spline.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SpindleCameraStruct]:
    if property_count != 2:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3e9cf140
    interpolant_type = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9a598fa5
    interpolant_spline = Spline.from_stream(data, property_size)

    return SpindleCameraStruct(interpolant_type, interpolant_spline)


def _decode_interpolant_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_decode_interpolant_spline = Spline.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3e9cf140: ('interpolant_type', _decode_interpolant_type),
    0x9a598fa5: ('interpolant_spline', _decode_interpolant_spline),
}
