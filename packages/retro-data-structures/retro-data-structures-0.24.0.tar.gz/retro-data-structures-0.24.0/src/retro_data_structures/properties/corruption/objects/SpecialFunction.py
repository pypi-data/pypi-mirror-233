# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SpecialFunction(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    function: enums.Function = dataclasses.field(default=enums.Function.What)
    string_parm: str = dataclasses.field(default='')
    value_parm: float = dataclasses.field(default=0.0)
    value_parm2: float = dataclasses.field(default=0.0)
    value_parm3: float = dataclasses.field(default=0.0)
    value_parm4: float = dataclasses.field(default=0.0)
    int_parm1: int = dataclasses.field(default=0)
    int_parm2: int = dataclasses.field(default=0)
    inventory_item_parm: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    sound1: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    sound2: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    sound3: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    extra_info: enums.ExtraInfo = dataclasses.field(default=enums.ExtraInfo.Unknown1)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPFN'

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8\xaf\xcf!')  # 0xb8afcf21
        data.write(b'\x00\x04')  # size
        self.function.to_stream(data)

        data.write(b'\x9dzWm')  # 0x9d7a576d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.string_parm.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\x02\x80\x99')  # 0x19028099
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm))

        data.write(b',\x93\xaa\xf5')  # 0x2c93aaf5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm2))

        data.write(b'\xe7\xcfyP')  # 0xe7cf7950
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm3))

        data.write(b'\xfa\xcaI\xe8')  # 0xfaca49e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.value_parm4))

        data.write(b'\xa74\xf8\xa5')  # 0xa734f8a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.int_parm1))

        data.write(b'\xb5\x81WK')  # 0xb581574b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.int_parm2))

        data.write(b'?\xa1d\xbc')  # 0x3fa164bc
        data.write(b'\x00\x04')  # size
        self.inventory_item_parm.to_stream(data)

        data.write(b'^\xcf\x8fg')  # 0x5ecf8f67
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound1))

        data.write(b'\xd8[\xfd\xc9')  # 0xd85bfdc9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound2))

        data.write(b'\x13\x07.l')  # 0x13072e6c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound3))

        data.write(b'\x82^\x1e\x14')  # 0x825e1e14
        data.write(b'\x00\x04')  # size
        self.extra_info.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            function=enums.Function.from_json(data['function']),
            string_parm=data['string_parm'],
            value_parm=data['value_parm'],
            value_parm2=data['value_parm2'],
            value_parm3=data['value_parm3'],
            value_parm4=data['value_parm4'],
            int_parm1=data['int_parm1'],
            int_parm2=data['int_parm2'],
            inventory_item_parm=enums.PlayerItem.from_json(data['inventory_item_parm']),
            sound1=data['sound1'],
            sound2=data['sound2'],
            sound3=data['sound3'],
            extra_info=enums.ExtraInfo.from_json(data['extra_info']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'function': self.function.to_json(),
            'string_parm': self.string_parm,
            'value_parm': self.value_parm,
            'value_parm2': self.value_parm2,
            'value_parm3': self.value_parm3,
            'value_parm4': self.value_parm4,
            'int_parm1': self.int_parm1,
            'int_parm2': self.int_parm2,
            'inventory_item_parm': self.inventory_item_parm.to_json(),
            'sound1': self.sound1,
            'sound2': self.sound2,
            'sound3': self.sound3,
            'extra_info': self.extra_info.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SpecialFunction]:
    if property_count != 14:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb8afcf21
    function = enums.Function.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9d7a576d
    string_parm = data.read(property_size)[:-1].decode("utf-8")

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x19028099
    value_parm = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2c93aaf5
    value_parm2 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe7cf7950
    value_parm3 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfaca49e8
    value_parm4 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa734f8a5
    int_parm1 = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb581574b
    int_parm2 = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3fa164bc
    inventory_item_parm = enums.PlayerItem.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5ecf8f67
    sound1 = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd85bfdc9
    sound2 = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x13072e6c
    sound3 = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x825e1e14
    extra_info = enums.ExtraInfo.from_stream(data)

    return SpecialFunction(editor_properties, function, string_parm, value_parm, value_parm2, value_parm3, value_parm4, int_parm1, int_parm2, inventory_item_parm, sound1, sound2, sound3, extra_info)


_decode_editor_properties = EditorProperties.from_stream

def _decode_function(data: typing.BinaryIO, property_size: int):
    return enums.Function.from_stream(data)


def _decode_string_parm(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_value_parm(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_value_parm2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_value_parm3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_value_parm4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_int_parm1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_int_parm2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_inventory_item_parm(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_sound1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_extra_info(data: typing.BinaryIO, property_size: int):
    return enums.ExtraInfo.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb8afcf21: ('function', _decode_function),
    0x9d7a576d: ('string_parm', _decode_string_parm),
    0x19028099: ('value_parm', _decode_value_parm),
    0x2c93aaf5: ('value_parm2', _decode_value_parm2),
    0xe7cf7950: ('value_parm3', _decode_value_parm3),
    0xfaca49e8: ('value_parm4', _decode_value_parm4),
    0xa734f8a5: ('int_parm1', _decode_int_parm1),
    0xb581574b: ('int_parm2', _decode_int_parm2),
    0x3fa164bc: ('inventory_item_parm', _decode_inventory_item_parm),
    0x5ecf8f67: ('sound1', _decode_sound1),
    0xd85bfdc9: ('sound2', _decode_sound2),
    0x13072e6c: ('sound3', _decode_sound3),
    0x825e1e14: ('extra_info', _decode_extra_info),
}
