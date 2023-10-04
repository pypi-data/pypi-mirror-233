# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class DynamicLightIntensity(BaseProperty):
    intensity: Spline = dataclasses.field(default_factory=Spline)
    intensity_duration: float = dataclasses.field(default=0.0)
    intensity_loops: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'#\x9d\r+')  # 0x239d0d2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.intensity.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9\r\x88\x99')  # 0xc90d8899
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.intensity_duration))

        data.write(b'\xaeg\xe0P')  # 0xae67e050
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.intensity_loops))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            intensity=Spline.from_json(data['intensity']),
            intensity_duration=data['intensity_duration'],
            intensity_loops=data['intensity_loops'],
        )

    def to_json(self) -> dict:
        return {
            'intensity': self.intensity.to_json(),
            'intensity_duration': self.intensity_duration,
            'intensity_loops': self.intensity_loops,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DynamicLightIntensity]:
    if property_count != 3:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x239d0d2b
    intensity = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc90d8899
    intensity_duration = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xae67e050
    intensity_loops = struct.unpack('>?', data.read(1))[0]

    return DynamicLightIntensity(intensity, intensity_duration, intensity_loops)


_decode_intensity = Spline.from_stream

def _decode_intensity_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_intensity_loops(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x239d0d2b: ('intensity', _decode_intensity),
    0xc90d8899: ('intensity_duration', _decode_intensity_duration),
    0xae67e050: ('intensity_loops', _decode_intensity_loops),
}
