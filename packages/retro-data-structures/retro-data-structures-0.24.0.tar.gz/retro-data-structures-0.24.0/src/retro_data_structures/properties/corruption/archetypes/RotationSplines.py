# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class RotationSplines(BaseProperty):
    x_rotation: Spline = dataclasses.field(default_factory=Spline)
    y_rotation: Spline = dataclasses.field(default_factory=Spline)
    z_rotation: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'i\xd8D}')  # 0x69d8447d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_rotation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd0#\x9f\x95')  # 0xd0239f95
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_rotation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1^\xf5\xec')  # 0xc15ef5ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_rotation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x_rotation=Spline.from_json(data['x_rotation']),
            y_rotation=Spline.from_json(data['y_rotation']),
            z_rotation=Spline.from_json(data['z_rotation']),
        )

    def to_json(self) -> dict:
        return {
            'x_rotation': self.x_rotation.to_json(),
            'y_rotation': self.y_rotation.to_json(),
            'z_rotation': self.z_rotation.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[RotationSplines]:
    if property_count != 3:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x69d8447d
    x_rotation = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd0239f95
    y_rotation = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc15ef5ec
    z_rotation = Spline.from_stream(data, property_size)

    return RotationSplines(x_rotation, y_rotation, z_rotation)


_decode_x_rotation = Spline.from_stream

_decode_y_rotation = Spline.from_stream

_decode_z_rotation = Spline.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x69d8447d: ('x_rotation', _decode_x_rotation),
    0xd0239f95: ('y_rotation', _decode_y_rotation),
    0xc15ef5ec: ('z_rotation', _decode_z_rotation),
}
