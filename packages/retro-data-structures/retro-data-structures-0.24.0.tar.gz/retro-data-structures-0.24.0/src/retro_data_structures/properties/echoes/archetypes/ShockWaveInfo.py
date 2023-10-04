# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShockWaveInfo(BaseProperty):
    shock_wave_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    radius: float = dataclasses.field(default=0.0)
    height: float = dataclasses.field(default=1.0)
    unknown: float = dataclasses.field(default=0.5)
    radial_velocity: float = dataclasses.field(default=1.0)
    radial_velocity_acceleration: float = dataclasses.field(default=0.0)
    visor_electric_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    sound_visor_electric: int = dataclasses.field(default=0, metadata={'sound': True})

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'6\x9f}\t')  # 0x369f7d09
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shock_wave_effect))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\xc2\xbe\x03\r')  # 0xc2be030d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height))

        data.write(b'\xcfl\x1d\xe9')  # 0xcf6c1de9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'L\xd1E\x9b')  # 0x4cd1459b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radial_velocity))

        data.write(b'\nW\xb0\x9b')  # 0xa57b09b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radial_velocity_acceleration))

        data.write(b'\xbd2\x158')  # 0xbd321538
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.visor_electric_effect))

        data.write(b'X\xa4\x92\xef')  # 0x58a492ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_visor_electric))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            shock_wave_effect=data['shock_wave_effect'],
            damage=DamageInfo.from_json(data['damage']),
            radius=data['radius'],
            height=data['height'],
            unknown=data['unknown'],
            radial_velocity=data['radial_velocity'],
            radial_velocity_acceleration=data['radial_velocity_acceleration'],
            visor_electric_effect=data['visor_electric_effect'],
            sound_visor_electric=data['sound_visor_electric'],
        )

    def to_json(self) -> dict:
        return {
            'shock_wave_effect': self.shock_wave_effect,
            'damage': self.damage.to_json(),
            'radius': self.radius,
            'height': self.height,
            'unknown': self.unknown,
            'radial_velocity': self.radial_velocity,
            'radial_velocity_acceleration': self.radial_velocity_acceleration,
            'visor_electric_effect': self.visor_electric_effect,
            'sound_visor_electric': self.sound_visor_electric,
        }

    def _dependencies_for_shock_wave_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shock_wave_effect)

    def _dependencies_for_damage(self, asset_manager):
        yield from self.damage.dependencies_for(asset_manager)

    def _dependencies_for_visor_electric_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.visor_electric_effect)

    def _dependencies_for_sound_visor_electric(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_visor_electric)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_shock_wave_effect, "shock_wave_effect", "AssetId"),
            (self._dependencies_for_damage, "damage", "DamageInfo"),
            (self._dependencies_for_visor_electric_effect, "visor_electric_effect", "AssetId"),
            (self._dependencies_for_sound_visor_electric, "sound_visor_electric", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ShockWaveInfo.{field_name} ({field_type}): {e}"
                )


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ShockWaveInfo]:
    if property_count != 9:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x369f7d09
    shock_wave_effect = struct.unpack(">L", data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x337f9524
    damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x78c507eb
    radius = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc2be030d
    height = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xcf6c1de9
    unknown = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4cd1459b
    radial_velocity = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0a57b09b
    radial_velocity_acceleration = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbd321538
    visor_electric_effect = struct.unpack(">L", data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x58a492ef
    sound_visor_electric = struct.unpack('>l', data.read(4))[0]

    return ShockWaveInfo(shock_wave_effect, damage, radius, height, unknown, radial_velocity, radial_velocity_acceleration, visor_electric_effect, sound_visor_electric)


def _decode_shock_wave_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_decode_damage = DamageInfo.from_stream

def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radial_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radial_velocity_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor_electric_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_visor_electric(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x369f7d09: ('shock_wave_effect', _decode_shock_wave_effect),
    0x337f9524: ('damage', _decode_damage),
    0x78c507eb: ('radius', _decode_radius),
    0xc2be030d: ('height', _decode_height),
    0xcf6c1de9: ('unknown', _decode_unknown),
    0x4cd1459b: ('radial_velocity', _decode_radial_velocity),
    0xa57b09b: ('radial_velocity_acceleration', _decode_radial_velocity_acceleration),
    0xbd321538: ('visor_electric_effect', _decode_visor_electric_effect),
    0x58a492ef: ('sound_visor_electric', _decode_sound_visor_electric),
}
