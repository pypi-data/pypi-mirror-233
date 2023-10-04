# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class FalsePerspective(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    percentage_of_depth_range: float = dataclasses.field(default=0.0010000000474974513)
    near_clip_plane: float = dataclasses.field(default=20.0)
    far_clip_plane: float = dataclasses.field(default=8192.0)
    unknown: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FLPS'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7fpe\xd3')  # 0x7f7065d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.percentage_of_depth_range))

        data.write(b'\xf4\x81\x7f\x13')  # 0xf4817f13
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.near_clip_plane))

        data.write(b'\x84\xecJt')  # 0x84ec4a74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.far_clip_plane))

        data.write(b'\xa9\xd5\xffH')  # 0xa9d5ff48
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            percentage_of_depth_range=data['percentage_of_depth_range'],
            near_clip_plane=data['near_clip_plane'],
            far_clip_plane=data['far_clip_plane'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'percentage_of_depth_range': self.percentage_of_depth_range,
            'near_clip_plane': self.near_clip_plane,
            'far_clip_plane': self.far_clip_plane,
            'unknown': self.unknown,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FalsePerspective]:
    if property_count != 5:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7f7065d3
    percentage_of_depth_range = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf4817f13
    near_clip_plane = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x84ec4a74
    far_clip_plane = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa9d5ff48
    unknown = struct.unpack('>?', data.read(1))[0]

    return FalsePerspective(editor_properties, percentage_of_depth_range, near_clip_plane, far_clip_plane, unknown)


_decode_editor_properties = EditorProperties.from_stream

def _decode_percentage_of_depth_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_near_clip_plane(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_far_clip_plane(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7f7065d3: ('percentage_of_depth_range', _decode_percentage_of_depth_range),
    0xf4817f13: ('near_clip_plane', _decode_near_clip_plane),
    0x84ec4a74: ('far_clip_plane', _decode_far_clip_plane),
    0xa9d5ff48: ('unknown', _decode_unknown),
}
