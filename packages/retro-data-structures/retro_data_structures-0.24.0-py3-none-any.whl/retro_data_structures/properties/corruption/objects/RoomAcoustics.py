# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.UnknownStruct54 import UnknownStruct54


@dataclasses.dataclass()
class RoomAcoustics(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    priority: enums.Priority = dataclasses.field(default=enums.Priority.Unknown2)
    unknown_struct54: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'RMAC'

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b\xe7\xca\x9e')  # 0xbe7ca9e
        data.write(b'\x00\x04')  # size
        self.priority.to_stream(data)

        data.write(b'U[\x05^')  # 0x555b055e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            priority=enums.Priority.from_json(data['priority']),
            unknown_struct54=UnknownStruct54.from_json(data['unknown_struct54']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'priority': self.priority.to_json(),
            'unknown_struct54': self.unknown_struct54.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[RoomAcoustics]:
    if property_count != 3:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0be7ca9e
    priority = enums.Priority.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x555b055e
    unknown_struct54 = UnknownStruct54.from_stream(data, property_size)

    return RoomAcoustics(editor_properties, priority, unknown_struct54)


_decode_editor_properties = EditorProperties.from_stream

def _decode_priority(data: typing.BinaryIO, property_size: int):
    return enums.Priority.from_stream(data)


_decode_unknown_struct54 = UnknownStruct54.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbe7ca9e: ('priority', _decode_priority),
    0x555b055e: ('unknown_struct54', _decode_unknown_struct54),
}
