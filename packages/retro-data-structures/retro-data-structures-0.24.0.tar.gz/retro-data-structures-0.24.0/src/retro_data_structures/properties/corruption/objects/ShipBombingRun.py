# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShipBombingRun(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    countdown_time: float = dataclasses.field(default=2.5)
    scan_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    executing_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    missile_empty: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SHBR'

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

        data.write(b'UGw\x00')  # 0x55477700
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.countdown_time))

        data.write(b'\xcejx\xc8')  # 0xce6a78c8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_sound))

        data.write(b'QT`\xac')  # 0x515460ac
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.executing_sound))

        data.write(b'\x10(\x98\x04')  # 0x10289804
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.missile_empty))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            countdown_time=data['countdown_time'],
            scan_sound=data['scan_sound'],
            executing_sound=data['executing_sound'],
            missile_empty=data['missile_empty'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'countdown_time': self.countdown_time,
            'scan_sound': self.scan_sound,
            'executing_sound': self.executing_sound,
            'missile_empty': self.missile_empty,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ShipBombingRun]:
    if property_count != 5:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x55477700
    countdown_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xce6a78c8
    scan_sound = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x515460ac
    executing_sound = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x10289804
    missile_empty = struct.unpack(">Q", data.read(8))[0]

    return ShipBombingRun(editor_properties, countdown_time, scan_sound, executing_sound, missile_empty)


_decode_editor_properties = EditorProperties.from_stream

def _decode_countdown_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_executing_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_missile_empty(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x55477700: ('countdown_time', _decode_countdown_time),
    0xce6a78c8: ('scan_sound', _decode_scan_sound),
    0x515460ac: ('executing_sound', _decode_executing_sound),
    0x10289804: ('missile_empty', _decode_missile_empty),
}
