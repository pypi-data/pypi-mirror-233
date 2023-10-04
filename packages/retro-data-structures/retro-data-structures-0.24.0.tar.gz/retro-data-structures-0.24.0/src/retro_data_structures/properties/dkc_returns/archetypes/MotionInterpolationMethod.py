# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.InterpolationMethod import InterpolationMethod
from retro_data_structures.properties.dkc_returns.archetypes.NonSlowdown import NonSlowdown


@dataclasses.dataclass()
class MotionInterpolationMethod(BaseProperty):
    motion_type: int = dataclasses.field(default=1102650983)  # Choice
    non_slowdown: NonSlowdown = dataclasses.field(default_factory=NonSlowdown)
    motion_control: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod)

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

        data.write(b'\x94\x8a\xf5q')  # 0x948af571
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.motion_type))

        data.write(b'y\xdeK\xa5')  # 0x79de4ba5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.non_slowdown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x7f\x9fE')  # 0x287f9f45
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_type=data['motion_type'],
            non_slowdown=NonSlowdown.from_json(data['non_slowdown']),
            motion_control=InterpolationMethod.from_json(data['motion_control']),
        )

    def to_json(self) -> dict:
        return {
            'motion_type': self.motion_type,
            'non_slowdown': self.non_slowdown.to_json(),
            'motion_control': self.motion_control.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[MotionInterpolationMethod]:
    if property_count != 3:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x948af571
    motion_type = struct.unpack(">L", data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x79de4ba5
    non_slowdown = NonSlowdown.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x287f9f45
    motion_control = InterpolationMethod.from_stream(data, property_size)

    return MotionInterpolationMethod(motion_type, non_slowdown, motion_control)


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_decode_non_slowdown = NonSlowdown.from_stream

_decode_motion_control = InterpolationMethod.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x948af571: ('motion_type', _decode_motion_type),
    0x79de4ba5: ('non_slowdown', _decode_non_slowdown),
    0x287f9f45: ('motion_control', _decode_motion_control),
}
