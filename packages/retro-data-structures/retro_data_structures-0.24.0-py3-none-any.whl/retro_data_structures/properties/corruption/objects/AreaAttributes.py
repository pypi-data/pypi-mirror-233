# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.RainProperties import RainProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class AreaAttributes(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    need_sky: bool = dataclasses.field(default=False)
    environment_effects: enums.EnvironmentEffects = dataclasses.field(default=enums.EnvironmentEffects.Unknown1)
    rain_properties: RainProperties = dataclasses.field(default_factory=RainProperties)
    environment_group_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    density: float = dataclasses.field(default=1.0)
    normal_lighting: float = dataclasses.field(default=1.0)
    unknown_0x6dade808: float = dataclasses.field(default=42.0)
    override_sky: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    use_override_sky: bool = dataclasses.field(default=True)
    unknown_0xe3426206: bool = dataclasses.field(default=False)
    phazon_damage: enums.PhazonDamage = dataclasses.field(default=enums.PhazonDamage.Unknown1)
    unknown_0x07b26bf9: bool = dataclasses.field(default=True)
    unknown_0x46cc1b48: bool = dataclasses.field(default=False)
    damage_spline: Spline = dataclasses.field(default_factory=Spline)
    environment_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'REAA'

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xd4\xbe\xe7')  # 0x95d4bee7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.need_sky))

        data.write(b"\xea'\x00\xe9")  # 0xea2700e9
        data.write(b'\x00\x04')  # size
        self.environment_effects.to_stream(data)

        data.write(b'\xce\x03(\xfa')  # 0xce0328fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rain_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V&>5')  # 0x56263e35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.environment_group_sound))

        data.write(b'd\xe5\xfe\x9f')  # 0x64e5fe9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.density))

        data.write(b'\xba_\x80\x1e')  # 0xba5f801e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_lighting))

        data.write(b'm\xad\xe8\x08')  # 0x6dade808
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6dade808))

        data.write(b'\xd2\x08\xc9\xfa')  # 0xd208c9fa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.override_sky))

        data.write(b')DS\x02')  # 0x29445302
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_override_sky))

        data.write(b'\xe3Bb\x06')  # 0xe3426206
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe3426206))

        data.write(b'N\x08\xb9\x84')  # 0x4e08b984
        data.write(b'\x00\x04')  # size
        self.phazon_damage.to_stream(data)

        data.write(b'\x07\xb2k\xf9')  # 0x7b26bf9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x07b26bf9))

        data.write(b'F\xcc\x1bH')  # 0x46cc1b48
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x46cc1b48))

        data.write(b'\xfa\x87:g')  # 0xfa873a67
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xa0\xe6\x9b')  # 0xe7a0e69b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.environment_damage_info.to_stream(data)
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
            need_sky=data['need_sky'],
            environment_effects=enums.EnvironmentEffects.from_json(data['environment_effects']),
            rain_properties=RainProperties.from_json(data['rain_properties']),
            environment_group_sound=data['environment_group_sound'],
            density=data['density'],
            normal_lighting=data['normal_lighting'],
            unknown_0x6dade808=data['unknown_0x6dade808'],
            override_sky=data['override_sky'],
            use_override_sky=data['use_override_sky'],
            unknown_0xe3426206=data['unknown_0xe3426206'],
            phazon_damage=enums.PhazonDamage.from_json(data['phazon_damage']),
            unknown_0x07b26bf9=data['unknown_0x07b26bf9'],
            unknown_0x46cc1b48=data['unknown_0x46cc1b48'],
            damage_spline=Spline.from_json(data['damage_spline']),
            environment_damage_info=DamageInfo.from_json(data['environment_damage_info']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'need_sky': self.need_sky,
            'environment_effects': self.environment_effects.to_json(),
            'rain_properties': self.rain_properties.to_json(),
            'environment_group_sound': self.environment_group_sound,
            'density': self.density,
            'normal_lighting': self.normal_lighting,
            'unknown_0x6dade808': self.unknown_0x6dade808,
            'override_sky': self.override_sky,
            'use_override_sky': self.use_override_sky,
            'unknown_0xe3426206': self.unknown_0xe3426206,
            'phazon_damage': self.phazon_damage.to_json(),
            'unknown_0x07b26bf9': self.unknown_0x07b26bf9,
            'unknown_0x46cc1b48': self.unknown_0x46cc1b48,
            'damage_spline': self.damage_spline.to_json(),
            'environment_damage_info': self.environment_damage_info.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[AreaAttributes]:
    if property_count != 16:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x95d4bee7
    need_sky = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xea2700e9
    environment_effects = enums.EnvironmentEffects.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xce0328fa
    rain_properties = RainProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x56263e35
    environment_group_sound = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x64e5fe9f
    density = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xba5f801e
    normal_lighting = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x6dade808
    unknown_0x6dade808 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd208c9fa
    override_sky = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x29445302
    use_override_sky = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe3426206
    unknown_0xe3426206 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4e08b984
    phazon_damage = enums.PhazonDamage.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x07b26bf9
    unknown_0x07b26bf9 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x46cc1b48
    unknown_0x46cc1b48 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfa873a67
    damage_spline = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe7a0e69b
    environment_damage_info = DamageInfo.from_stream(data, property_size)

    return AreaAttributes(editor_properties, need_sky, environment_effects, rain_properties, environment_group_sound, density, normal_lighting, unknown_0x6dade808, override_sky, use_override_sky, unknown_0xe3426206, phazon_damage, unknown_0x07b26bf9, unknown_0x46cc1b48, damage_spline, environment_damage_info)


_decode_editor_properties = EditorProperties.from_stream

def _decode_need_sky(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_environment_effects(data: typing.BinaryIO, property_size: int):
    return enums.EnvironmentEffects.from_stream(data)


_decode_rain_properties = RainProperties.from_stream

def _decode_environment_group_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_density(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_lighting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6dade808(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_override_sky(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_use_override_sky(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe3426206(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_phazon_damage(data: typing.BinaryIO, property_size: int):
    return enums.PhazonDamage.from_stream(data)


def _decode_unknown_0x07b26bf9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x46cc1b48(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_decode_damage_spline = Spline.from_stream

_decode_environment_damage_info = DamageInfo.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x95d4bee7: ('need_sky', _decode_need_sky),
    0xea2700e9: ('environment_effects', _decode_environment_effects),
    0xce0328fa: ('rain_properties', _decode_rain_properties),
    0x56263e35: ('environment_group_sound', _decode_environment_group_sound),
    0x64e5fe9f: ('density', _decode_density),
    0xba5f801e: ('normal_lighting', _decode_normal_lighting),
    0x6dade808: ('unknown_0x6dade808', _decode_unknown_0x6dade808),
    0xd208c9fa: ('override_sky', _decode_override_sky),
    0x29445302: ('use_override_sky', _decode_use_override_sky),
    0xe3426206: ('unknown_0xe3426206', _decode_unknown_0xe3426206),
    0x4e08b984: ('phazon_damage', _decode_phazon_damage),
    0x7b26bf9: ('unknown_0x07b26bf9', _decode_unknown_0x07b26bf9),
    0x46cc1b48: ('unknown_0x46cc1b48', _decode_unknown_0x46cc1b48),
    0xfa873a67: ('damage_spline', _decode_damage_spline),
    0xe7a0e69b: ('environment_damage_info', _decode_environment_damage_info),
}
