# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.OffsetPosition import OffsetPosition
from retro_data_structures.properties.dkc_returns.archetypes.PathPosition import PathPosition
from retro_data_structures.properties.dkc_returns.archetypes.SpindlePosition import SpindlePosition
from retro_data_structures.properties.dkc_returns.archetypes.SurfacePosition import SurfacePosition
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct73 import UnknownStruct73


@dataclasses.dataclass()
class CameraPosition(BaseProperty):
    position_type: enums.PositionType = dataclasses.field(default=enums.PositionType.Unknown2)
    flags_camera_position: int = dataclasses.field(default=2)  # Flagset
    path: PathPosition = dataclasses.field(default_factory=PathPosition)
    spindle: SpindlePosition = dataclasses.field(default_factory=SpindlePosition)
    surface: SurfacePosition = dataclasses.field(default_factory=SurfacePosition)
    offset: OffsetPosition = dataclasses.field(default_factory=OffsetPosition)
    unknown_struct73: UnknownStruct73 = dataclasses.field(default_factory=UnknownStruct73)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xb7\xcdG\x10')  # 0xb7cd4710
        data.write(b'\x00\x04')  # size
        self.position_type.to_stream(data)

        data.write(b'\xb1\xb6\xcf3')  # 0xb1b6cf33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_camera_position))

        data.write(b'\xe8\xab\x9b\xc8')  # 0xe8ab9bc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xc1\xdf\x0c')  # 0x9ec1df0c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xb2\xd1\xe6')  # 0xbbb2d1e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surface.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07\xd1\x94\xaf')  # 0x7d194af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xbf\x81\xd7')  # 0xebbf81d7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct73.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            position_type=enums.PositionType.from_json(data['position_type']),
            flags_camera_position=data['flags_camera_position'],
            path=PathPosition.from_json(data['path']),
            spindle=SpindlePosition.from_json(data['spindle']),
            surface=SurfacePosition.from_json(data['surface']),
            offset=OffsetPosition.from_json(data['offset']),
            unknown_struct73=UnknownStruct73.from_json(data['unknown_struct73']),
        )

    def to_json(self) -> dict:
        return {
            'position_type': self.position_type.to_json(),
            'flags_camera_position': self.flags_camera_position,
            'path': self.path.to_json(),
            'spindle': self.spindle.to_json(),
            'surface': self.surface.to_json(),
            'offset': self.offset.to_json(),
            'unknown_struct73': self.unknown_struct73.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[CameraPosition]:
    if property_count != 7:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb7cd4710
    position_type = enums.PositionType.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb1b6cf33
    flags_camera_position = struct.unpack(">L", data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe8ab9bc8
    path = PathPosition.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9ec1df0c
    spindle = SpindlePosition.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbbb2d1e6
    surface = SurfacePosition.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x07d194af
    offset = OffsetPosition.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xebbf81d7
    unknown_struct73 = UnknownStruct73.from_stream(data, property_size)

    return CameraPosition(position_type, flags_camera_position, path, spindle, surface, offset, unknown_struct73)


def _decode_position_type(data: typing.BinaryIO, property_size: int):
    return enums.PositionType.from_stream(data)


def _decode_flags_camera_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_decode_path = PathPosition.from_stream

_decode_spindle = SpindlePosition.from_stream

_decode_surface = SurfacePosition.from_stream

_decode_offset = OffsetPosition.from_stream

_decode_unknown_struct73 = UnknownStruct73.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb7cd4710: ('position_type', _decode_position_type),
    0xb1b6cf33: ('flags_camera_position', _decode_flags_camera_position),
    0xe8ab9bc8: ('path', _decode_path),
    0x9ec1df0c: ('spindle', _decode_spindle),
    0xbbb2d1e6: ('surface', _decode_surface),
    0x7d194af: ('offset', _decode_offset),
    0xebbf81d7: ('unknown_struct73', _decode_unknown_struct73),
}
