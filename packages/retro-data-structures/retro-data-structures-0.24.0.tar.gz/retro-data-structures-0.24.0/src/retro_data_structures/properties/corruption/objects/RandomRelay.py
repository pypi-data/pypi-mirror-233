# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class RandomRelay(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    count: int = dataclasses.field(default=1)
    random_adjust: int = dataclasses.field(default=0)
    percent_count: bool = dataclasses.field(default=False)
    is_random_chance: bool = dataclasses.field(default=False)
    choose_inactive: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'RRLY'

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\x91\xb8\xa2')  # 0x3291b8a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.count))

        data.write(b'\x7f\xcb3\xe8')  # 0x7fcb33e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.random_adjust))

        data.write(b'E\x80v\xe8')  # 0x458076e8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.percent_count))

        data.write(b'\xef{\x98&')  # 0xef7b9826
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_random_chance))

        data.write(b'C.\x9ds')  # 0x432e9d73
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.choose_inactive))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            count=data['count'],
            random_adjust=data['random_adjust'],
            percent_count=data['percent_count'],
            is_random_chance=data['is_random_chance'],
            choose_inactive=data['choose_inactive'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'count': self.count,
            'random_adjust': self.random_adjust,
            'percent_count': self.percent_count,
            'is_random_chance': self.is_random_chance,
            'choose_inactive': self.choose_inactive,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[RandomRelay]:
    if property_count != 6:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3291b8a2
    count = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7fcb33e8
    random_adjust = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x458076e8
    percent_count = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xef7b9826
    is_random_chance = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x432e9d73
    choose_inactive = struct.unpack('>?', data.read(1))[0]

    return RandomRelay(editor_properties, count, random_adjust, percent_count, is_random_chance, choose_inactive)


_decode_editor_properties = EditorProperties.from_stream

def _decode_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_random_adjust(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_percent_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_random_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_choose_inactive(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x3291b8a2: ('count', _decode_count),
    0x7fcb33e8: ('random_adjust', _decode_random_adjust),
    0x458076e8: ('percent_count', _decode_percent_count),
    0xef7b9826: ('is_random_chance', _decode_is_random_chance),
    0x432e9d73: ('choose_inactive', _decode_choose_inactive),
}
