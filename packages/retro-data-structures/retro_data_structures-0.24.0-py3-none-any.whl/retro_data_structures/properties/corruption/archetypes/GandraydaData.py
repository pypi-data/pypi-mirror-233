# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct30 import UnknownStruct30
from retro_data_structures.properties.corruption.archetypes.UnknownStruct31 import UnknownStruct31
from retro_data_structures.properties.corruption.archetypes.UnknownStruct32 import UnknownStruct32
from retro_data_structures.properties.corruption.archetypes.UnknownStruct33 import UnknownStruct33
from retro_data_structures.properties.corruption.archetypes.UnknownStruct34 import UnknownStruct34
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class GandraydaData(BaseProperty):
    unknown_0x538d71cb: float = dataclasses.field(default=75.0)
    unknown_0xd42bba88: float = dataclasses.field(default=50.0)
    unknown_0xf4b9c6c3: float = dataclasses.field(default=30.0)
    unknown_0x4d4d934b: float = dataclasses.field(default=100.0)
    min_navigation_time: float = dataclasses.field(default=6.0)
    max_navigation_time: float = dataclasses.field(default=10.0)
    unknown_0x32dd1ed4: float = dataclasses.field(default=4.0)
    unknown_0x4ba741d5: float = dataclasses.field(default=8.0)
    unknown_0x1eebf378: float = dataclasses.field(default=13.0)
    melee_weapon: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    radial_melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x587fa387: float = dataclasses.field(default=7.0)
    unknown_0x3e9ac5f3: float = dataclasses.field(default=10.0)
    thrown_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    thrown_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    thrown_projectile_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    energy_wave_chance: float = dataclasses.field(default=100.0)
    unknown_0x61f74274: int = dataclasses.field(default=2)
    unknown_0x51a1ae4d: float = dataclasses.field(default=12.0)
    unknown_0xb2fc1097: float = dataclasses.field(default=18.0)
    unknown_0xd89e391a: float = dataclasses.field(default=4.0)
    unknown_0x8f906959: float = dataclasses.field(default=8.0)
    energy_wave_jump_apex: float = dataclasses.field(default=4.0)
    unknown_0x8b354dc6: float = dataclasses.field(default=15.0)
    energy_wave_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    energy_wave_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    grapple_attack_chance: float = dataclasses.field(default=100.0)
    unknown_0x24c6cdcf: float = dataclasses.field(default=10.0)
    unknown_0x1a730547: float = dataclasses.field(default=25.0)
    unknown_0x2684b001: float = dataclasses.field(default=3.0)
    grapple_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.4000000059604645, z=-1.600000023841858))
    grapple_turn_speed: float = dataclasses.field(default=180.0)
    unknown_0x776db913: float = dataclasses.field(default=4.0)
    unknown_0x49d8719b: float = dataclasses.field(default=7.0)
    grapple_mount_jump_apex: float = dataclasses.field(default=3.0)
    grapple_dismount_jump_apex: float = dataclasses.field(default=4.0)
    grapple_connected_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    elsc_0x323f59c3: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    elsc_0xe4f90605: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grapple_pull_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    grapple_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    grapple_shake_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xc2b3754e: float = dataclasses.field(default=0.75)
    unknown_0x21eecb94: float = dataclasses.field(default=1.0)
    unknown_0xb5fdc280: float = dataclasses.field(default=2.6666998863220215)
    unknown_0x41d8c39c: float = dataclasses.field(default=1.5)
    unknown_struct30: UnknownStruct30 = dataclasses.field(default_factory=UnknownStruct30)
    unknown_struct31: UnknownStruct31 = dataclasses.field(default_factory=UnknownStruct31)
    unknown_struct32: UnknownStruct32 = dataclasses.field(default_factory=UnknownStruct32)
    unknown_struct33: UnknownStruct33 = dataclasses.field(default_factory=UnknownStruct33)
    unknown_struct34: UnknownStruct34 = dataclasses.field(default_factory=UnknownStruct34)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x006')  # 54 properties

        data.write(b'S\x8dq\xcb')  # 0x538d71cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x538d71cb))

        data.write(b'\xd4+\xba\x88')  # 0xd42bba88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd42bba88))

        data.write(b'\xf4\xb9\xc6\xc3')  # 0xf4b9c6c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf4b9c6c3))

        data.write(b'MM\x93K')  # 0x4d4d934b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4d4d934b))

        data.write(b' e\x180')  # 0x20651830
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_navigation_time))

        data.write(b"ar'\xb6")  # 0x617227b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_navigation_time))

        data.write(b'2\xdd\x1e\xd4')  # 0x32dd1ed4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x32dd1ed4))

        data.write(b'K\xa7A\xd5')  # 0x4ba741d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4ba741d5))

        data.write(b'\x1e\xeb\xf3x')  # 0x1eebf378
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1eebf378))

        data.write(b'JBk\xb3')  # 0x4a426bb3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.melee_weapon))

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\x11\x89;')  # 0x5f11893b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radial_melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x7f\xa3\x87')  # 0x587fa387
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x587fa387))

        data.write(b'>\x9a\xc5\xf3')  # 0x3e9ac5f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3e9ac5f3))

        data.write(b'&\x97\xe47')  # 0x2697e437
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.thrown_projectile))

        data.write(b'\xac\x18\x7f\xa7')  # 0xac187fa7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.thrown_projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xaf\x08>')  # 0x76af083e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.thrown_projectile_visor_effect))

        data.write(b'r:\x93\x98')  # 0x723a9398
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'y\xbcu>')  # 0x79bc753e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.energy_wave_chance))

        data.write(b'a\xf7Bt')  # 0x61f74274
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x61f74274))

        data.write(b'Q\xa1\xaeM')  # 0x51a1ae4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x51a1ae4d))

        data.write(b'\xb2\xfc\x10\x97')  # 0xb2fc1097
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb2fc1097))

        data.write(b'\xd8\x9e9\x1a')  # 0xd89e391a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd89e391a))

        data.write(b'\x8f\x90iY')  # 0x8f906959
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f906959))

        data.write(b'\xb2\x81\xf4\x90')  # 0xb281f490
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.energy_wave_jump_apex))

        data.write(b'\x8b5M\xc6')  # 0x8b354dc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8b354dc6))

        data.write(b'v\xc6DY')  # 0x76c64459
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.energy_wave_projectile))

        data.write(b'7\xedn\xbb')  # 0x37ed6ebb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_wave_projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x0c\xec\xf7')  # 0xd20cecf7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_attack_chance))

        data.write(b'$\xc6\xcd\xcf')  # 0x24c6cdcf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x24c6cdcf))

        data.write(b'\x1as\x05G')  # 0x1a730547
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1a730547))

        data.write(b'&\x84\xb0\x01')  # 0x2684b001
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2684b001))

        data.write(b'\xb4\x9de}')  # 0xb49d657d
        data.write(b'\x00\x0c')  # size
        self.grapple_offset.to_stream(data)

        data.write(b'\xf4\xd1\xc7\x92')  # 0xf4d1c792
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_turn_speed))

        data.write(b'wm\xb9\x13')  # 0x776db913
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x776db913))

        data.write(b'I\xd8q\x9b')  # 0x49d8719b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x49d8719b))

        data.write(b'\xec\x97\xcd\xbb')  # 0xec97cdbb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_mount_jump_apex))

        data.write(b'mW\x96\xef')  # 0x6d5796ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_dismount_jump_apex))

        data.write(b'\x98\xe1\x91\x87')  # 0x98e19187
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.grapple_connected_visor_effect))

        data.write(b'2?Y\xc3')  # 0x323f59c3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc_0x323f59c3))

        data.write(b'\xe4\xf9\x06\x05')  # 0xe4f90605
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc_0xe4f90605))

        data.write(b'\x96\x80Z\xfd')  # 0x96805afd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'\x89\xe7I[')  # 0x89e7495b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_pull_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',\xe7R\x0f')  # 0x2ce7520f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x06lG')  # 0x58066c47
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.grapple_shake_sound))

        data.write(b'\xc2\xb3uN')  # 0xc2b3754e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc2b3754e))

        data.write(b'!\xee\xcb\x94')  # 0x21eecb94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x21eecb94))

        data.write(b'\xb5\xfd\xc2\x80')  # 0xb5fdc280
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb5fdc280))

        data.write(b'A\xd8\xc3\x9c')  # 0x41d8c39c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x41d8c39c))

        data.write(b'\xaf\x89\x84\xb2')  # 0xaf8984b2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct30.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdc\xb5\xb1\x12')  # 0xdcb5b112
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct31.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3\x0bb\xea')  # 0xc30b62ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct32.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7fN.}')  # 0x7f4e2e7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct33.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfcv\xc5\x1a')  # 0xfc76c51a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct34.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x538d71cb=data['unknown_0x538d71cb'],
            unknown_0xd42bba88=data['unknown_0xd42bba88'],
            unknown_0xf4b9c6c3=data['unknown_0xf4b9c6c3'],
            unknown_0x4d4d934b=data['unknown_0x4d4d934b'],
            min_navigation_time=data['min_navigation_time'],
            max_navigation_time=data['max_navigation_time'],
            unknown_0x32dd1ed4=data['unknown_0x32dd1ed4'],
            unknown_0x4ba741d5=data['unknown_0x4ba741d5'],
            unknown_0x1eebf378=data['unknown_0x1eebf378'],
            melee_weapon=data['melee_weapon'],
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            radial_melee_damage=DamageInfo.from_json(data['radial_melee_damage']),
            unknown_0x587fa387=data['unknown_0x587fa387'],
            unknown_0x3e9ac5f3=data['unknown_0x3e9ac5f3'],
            thrown_projectile=data['thrown_projectile'],
            thrown_projectile_damage=DamageInfo.from_json(data['thrown_projectile_damage']),
            thrown_projectile_visor_effect=data['thrown_projectile_visor_effect'],
            caud=data['caud'],
            energy_wave_chance=data['energy_wave_chance'],
            unknown_0x61f74274=data['unknown_0x61f74274'],
            unknown_0x51a1ae4d=data['unknown_0x51a1ae4d'],
            unknown_0xb2fc1097=data['unknown_0xb2fc1097'],
            unknown_0xd89e391a=data['unknown_0xd89e391a'],
            unknown_0x8f906959=data['unknown_0x8f906959'],
            energy_wave_jump_apex=data['energy_wave_jump_apex'],
            unknown_0x8b354dc6=data['unknown_0x8b354dc6'],
            energy_wave_projectile=data['energy_wave_projectile'],
            energy_wave_projectile_damage=DamageInfo.from_json(data['energy_wave_projectile_damage']),
            grapple_attack_chance=data['grapple_attack_chance'],
            unknown_0x24c6cdcf=data['unknown_0x24c6cdcf'],
            unknown_0x1a730547=data['unknown_0x1a730547'],
            unknown_0x2684b001=data['unknown_0x2684b001'],
            grapple_offset=Vector.from_json(data['grapple_offset']),
            grapple_turn_speed=data['grapple_turn_speed'],
            unknown_0x776db913=data['unknown_0x776db913'],
            unknown_0x49d8719b=data['unknown_0x49d8719b'],
            grapple_mount_jump_apex=data['grapple_mount_jump_apex'],
            grapple_dismount_jump_apex=data['grapple_dismount_jump_apex'],
            grapple_connected_visor_effect=data['grapple_connected_visor_effect'],
            elsc_0x323f59c3=data['elsc_0x323f59c3'],
            elsc_0xe4f90605=data['elsc_0xe4f90605'],
            part=data['part'],
            grapple_pull_damage=DamageInfo.from_json(data['grapple_pull_damage']),
            grapple_damage=DamageInfo.from_json(data['grapple_damage']),
            grapple_shake_sound=data['grapple_shake_sound'],
            unknown_0xc2b3754e=data['unknown_0xc2b3754e'],
            unknown_0x21eecb94=data['unknown_0x21eecb94'],
            unknown_0xb5fdc280=data['unknown_0xb5fdc280'],
            unknown_0x41d8c39c=data['unknown_0x41d8c39c'],
            unknown_struct30=UnknownStruct30.from_json(data['unknown_struct30']),
            unknown_struct31=UnknownStruct31.from_json(data['unknown_struct31']),
            unknown_struct32=UnknownStruct32.from_json(data['unknown_struct32']),
            unknown_struct33=UnknownStruct33.from_json(data['unknown_struct33']),
            unknown_struct34=UnknownStruct34.from_json(data['unknown_struct34']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x538d71cb': self.unknown_0x538d71cb,
            'unknown_0xd42bba88': self.unknown_0xd42bba88,
            'unknown_0xf4b9c6c3': self.unknown_0xf4b9c6c3,
            'unknown_0x4d4d934b': self.unknown_0x4d4d934b,
            'min_navigation_time': self.min_navigation_time,
            'max_navigation_time': self.max_navigation_time,
            'unknown_0x32dd1ed4': self.unknown_0x32dd1ed4,
            'unknown_0x4ba741d5': self.unknown_0x4ba741d5,
            'unknown_0x1eebf378': self.unknown_0x1eebf378,
            'melee_weapon': self.melee_weapon,
            'melee_damage': self.melee_damage.to_json(),
            'radial_melee_damage': self.radial_melee_damage.to_json(),
            'unknown_0x587fa387': self.unknown_0x587fa387,
            'unknown_0x3e9ac5f3': self.unknown_0x3e9ac5f3,
            'thrown_projectile': self.thrown_projectile,
            'thrown_projectile_damage': self.thrown_projectile_damage.to_json(),
            'thrown_projectile_visor_effect': self.thrown_projectile_visor_effect,
            'caud': self.caud,
            'energy_wave_chance': self.energy_wave_chance,
            'unknown_0x61f74274': self.unknown_0x61f74274,
            'unknown_0x51a1ae4d': self.unknown_0x51a1ae4d,
            'unknown_0xb2fc1097': self.unknown_0xb2fc1097,
            'unknown_0xd89e391a': self.unknown_0xd89e391a,
            'unknown_0x8f906959': self.unknown_0x8f906959,
            'energy_wave_jump_apex': self.energy_wave_jump_apex,
            'unknown_0x8b354dc6': self.unknown_0x8b354dc6,
            'energy_wave_projectile': self.energy_wave_projectile,
            'energy_wave_projectile_damage': self.energy_wave_projectile_damage.to_json(),
            'grapple_attack_chance': self.grapple_attack_chance,
            'unknown_0x24c6cdcf': self.unknown_0x24c6cdcf,
            'unknown_0x1a730547': self.unknown_0x1a730547,
            'unknown_0x2684b001': self.unknown_0x2684b001,
            'grapple_offset': self.grapple_offset.to_json(),
            'grapple_turn_speed': self.grapple_turn_speed,
            'unknown_0x776db913': self.unknown_0x776db913,
            'unknown_0x49d8719b': self.unknown_0x49d8719b,
            'grapple_mount_jump_apex': self.grapple_mount_jump_apex,
            'grapple_dismount_jump_apex': self.grapple_dismount_jump_apex,
            'grapple_connected_visor_effect': self.grapple_connected_visor_effect,
            'elsc_0x323f59c3': self.elsc_0x323f59c3,
            'elsc_0xe4f90605': self.elsc_0xe4f90605,
            'part': self.part,
            'grapple_pull_damage': self.grapple_pull_damage.to_json(),
            'grapple_damage': self.grapple_damage.to_json(),
            'grapple_shake_sound': self.grapple_shake_sound,
            'unknown_0xc2b3754e': self.unknown_0xc2b3754e,
            'unknown_0x21eecb94': self.unknown_0x21eecb94,
            'unknown_0xb5fdc280': self.unknown_0xb5fdc280,
            'unknown_0x41d8c39c': self.unknown_0x41d8c39c,
            'unknown_struct30': self.unknown_struct30.to_json(),
            'unknown_struct31': self.unknown_struct31.to_json(),
            'unknown_struct32': self.unknown_struct32.to_json(),
            'unknown_struct33': self.unknown_struct33.to_json(),
            'unknown_struct34': self.unknown_struct34.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[GandraydaData]:
    if property_count != 54:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x538d71cb
    unknown_0x538d71cb = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd42bba88
    unknown_0xd42bba88 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf4b9c6c3
    unknown_0xf4b9c6c3 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4d4d934b
    unknown_0x4d4d934b = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x20651830
    min_navigation_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x617227b6
    max_navigation_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x32dd1ed4
    unknown_0x32dd1ed4 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4ba741d5
    unknown_0x4ba741d5 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x1eebf378
    unknown_0x1eebf378 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4a426bb3
    melee_weapon = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc9416034
    melee_damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5f11893b
    radial_melee_damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x587fa387
    unknown_0x587fa387 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3e9ac5f3
    unknown_0x3e9ac5f3 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2697e437
    thrown_projectile = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xac187fa7
    thrown_projectile_damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x76af083e
    thrown_projectile_visor_effect = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x723a9398
    caud = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x79bc753e
    energy_wave_chance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x61f74274
    unknown_0x61f74274 = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x51a1ae4d
    unknown_0x51a1ae4d = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb2fc1097
    unknown_0xb2fc1097 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd89e391a
    unknown_0xd89e391a = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8f906959
    unknown_0x8f906959 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb281f490
    energy_wave_jump_apex = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8b354dc6
    unknown_0x8b354dc6 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x76c64459
    energy_wave_projectile = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x37ed6ebb
    energy_wave_projectile_damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd20cecf7
    grapple_attack_chance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x24c6cdcf
    unknown_0x24c6cdcf = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x1a730547
    unknown_0x1a730547 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2684b001
    unknown_0x2684b001 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb49d657d
    grapple_offset = Vector.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf4d1c792
    grapple_turn_speed = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x776db913
    unknown_0x776db913 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x49d8719b
    unknown_0x49d8719b = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xec97cdbb
    grapple_mount_jump_apex = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x6d5796ef
    grapple_dismount_jump_apex = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x98e19187
    grapple_connected_visor_effect = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x323f59c3
    elsc_0x323f59c3 = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe4f90605
    elsc_0xe4f90605 = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x96805afd
    part = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x89e7495b
    grapple_pull_damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2ce7520f
    grapple_damage = DamageInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x58066c47
    grapple_shake_sound = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc2b3754e
    unknown_0xc2b3754e = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x21eecb94
    unknown_0x21eecb94 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb5fdc280
    unknown_0xb5fdc280 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x41d8c39c
    unknown_0x41d8c39c = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xaf8984b2
    unknown_struct30 = UnknownStruct30.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xdcb5b112
    unknown_struct31 = UnknownStruct31.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc30b62ea
    unknown_struct32 = UnknownStruct32.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7f4e2e7d
    unknown_struct33 = UnknownStruct33.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfc76c51a
    unknown_struct34 = UnknownStruct34.from_stream(data, property_size)

    return GandraydaData(unknown_0x538d71cb, unknown_0xd42bba88, unknown_0xf4b9c6c3, unknown_0x4d4d934b, min_navigation_time, max_navigation_time, unknown_0x32dd1ed4, unknown_0x4ba741d5, unknown_0x1eebf378, melee_weapon, melee_damage, radial_melee_damage, unknown_0x587fa387, unknown_0x3e9ac5f3, thrown_projectile, thrown_projectile_damage, thrown_projectile_visor_effect, caud, energy_wave_chance, unknown_0x61f74274, unknown_0x51a1ae4d, unknown_0xb2fc1097, unknown_0xd89e391a, unknown_0x8f906959, energy_wave_jump_apex, unknown_0x8b354dc6, energy_wave_projectile, energy_wave_projectile_damage, grapple_attack_chance, unknown_0x24c6cdcf, unknown_0x1a730547, unknown_0x2684b001, grapple_offset, grapple_turn_speed, unknown_0x776db913, unknown_0x49d8719b, grapple_mount_jump_apex, grapple_dismount_jump_apex, grapple_connected_visor_effect, elsc_0x323f59c3, elsc_0xe4f90605, part, grapple_pull_damage, grapple_damage, grapple_shake_sound, unknown_0xc2b3754e, unknown_0x21eecb94, unknown_0xb5fdc280, unknown_0x41d8c39c, unknown_struct30, unknown_struct31, unknown_struct32, unknown_struct33, unknown_struct34)


def _decode_unknown_0x538d71cb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd42bba88(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf4b9c6c3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4d4d934b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_navigation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_navigation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x32dd1ed4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4ba741d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1eebf378(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_weapon(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_decode_melee_damage = DamageInfo.from_stream

_decode_radial_melee_damage = DamageInfo.from_stream

def _decode_unknown_0x587fa387(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3e9ac5f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_thrown_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_decode_thrown_projectile_damage = DamageInfo.from_stream

def _decode_thrown_projectile_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_energy_wave_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61f74274(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x51a1ae4d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb2fc1097(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd89e391a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f906959(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_wave_jump_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8b354dc6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_wave_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_decode_energy_wave_projectile_damage = DamageInfo.from_stream

def _decode_grapple_attack_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x24c6cdcf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1a730547(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2684b001(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_grapple_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x776db913(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x49d8719b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_mount_jump_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_dismount_jump_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_connected_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_elsc_0x323f59c3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_elsc_0xe4f90605(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_decode_grapple_pull_damage = DamageInfo.from_stream

_decode_grapple_damage = DamageInfo.from_stream

def _decode_grapple_shake_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xc2b3754e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x21eecb94(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb5fdc280(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x41d8c39c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_decode_unknown_struct30 = UnknownStruct30.from_stream

_decode_unknown_struct31 = UnknownStruct31.from_stream

_decode_unknown_struct32 = UnknownStruct32.from_stream

_decode_unknown_struct33 = UnknownStruct33.from_stream

_decode_unknown_struct34 = UnknownStruct34.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x538d71cb: ('unknown_0x538d71cb', _decode_unknown_0x538d71cb),
    0xd42bba88: ('unknown_0xd42bba88', _decode_unknown_0xd42bba88),
    0xf4b9c6c3: ('unknown_0xf4b9c6c3', _decode_unknown_0xf4b9c6c3),
    0x4d4d934b: ('unknown_0x4d4d934b', _decode_unknown_0x4d4d934b),
    0x20651830: ('min_navigation_time', _decode_min_navigation_time),
    0x617227b6: ('max_navigation_time', _decode_max_navigation_time),
    0x32dd1ed4: ('unknown_0x32dd1ed4', _decode_unknown_0x32dd1ed4),
    0x4ba741d5: ('unknown_0x4ba741d5', _decode_unknown_0x4ba741d5),
    0x1eebf378: ('unknown_0x1eebf378', _decode_unknown_0x1eebf378),
    0x4a426bb3: ('melee_weapon', _decode_melee_weapon),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x5f11893b: ('radial_melee_damage', _decode_radial_melee_damage),
    0x587fa387: ('unknown_0x587fa387', _decode_unknown_0x587fa387),
    0x3e9ac5f3: ('unknown_0x3e9ac5f3', _decode_unknown_0x3e9ac5f3),
    0x2697e437: ('thrown_projectile', _decode_thrown_projectile),
    0xac187fa7: ('thrown_projectile_damage', _decode_thrown_projectile_damage),
    0x76af083e: ('thrown_projectile_visor_effect', _decode_thrown_projectile_visor_effect),
    0x723a9398: ('caud', _decode_caud),
    0x79bc753e: ('energy_wave_chance', _decode_energy_wave_chance),
    0x61f74274: ('unknown_0x61f74274', _decode_unknown_0x61f74274),
    0x51a1ae4d: ('unknown_0x51a1ae4d', _decode_unknown_0x51a1ae4d),
    0xb2fc1097: ('unknown_0xb2fc1097', _decode_unknown_0xb2fc1097),
    0xd89e391a: ('unknown_0xd89e391a', _decode_unknown_0xd89e391a),
    0x8f906959: ('unknown_0x8f906959', _decode_unknown_0x8f906959),
    0xb281f490: ('energy_wave_jump_apex', _decode_energy_wave_jump_apex),
    0x8b354dc6: ('unknown_0x8b354dc6', _decode_unknown_0x8b354dc6),
    0x76c64459: ('energy_wave_projectile', _decode_energy_wave_projectile),
    0x37ed6ebb: ('energy_wave_projectile_damage', _decode_energy_wave_projectile_damage),
    0xd20cecf7: ('grapple_attack_chance', _decode_grapple_attack_chance),
    0x24c6cdcf: ('unknown_0x24c6cdcf', _decode_unknown_0x24c6cdcf),
    0x1a730547: ('unknown_0x1a730547', _decode_unknown_0x1a730547),
    0x2684b001: ('unknown_0x2684b001', _decode_unknown_0x2684b001),
    0xb49d657d: ('grapple_offset', _decode_grapple_offset),
    0xf4d1c792: ('grapple_turn_speed', _decode_grapple_turn_speed),
    0x776db913: ('unknown_0x776db913', _decode_unknown_0x776db913),
    0x49d8719b: ('unknown_0x49d8719b', _decode_unknown_0x49d8719b),
    0xec97cdbb: ('grapple_mount_jump_apex', _decode_grapple_mount_jump_apex),
    0x6d5796ef: ('grapple_dismount_jump_apex', _decode_grapple_dismount_jump_apex),
    0x98e19187: ('grapple_connected_visor_effect', _decode_grapple_connected_visor_effect),
    0x323f59c3: ('elsc_0x323f59c3', _decode_elsc_0x323f59c3),
    0xe4f90605: ('elsc_0xe4f90605', _decode_elsc_0xe4f90605),
    0x96805afd: ('part', _decode_part),
    0x89e7495b: ('grapple_pull_damage', _decode_grapple_pull_damage),
    0x2ce7520f: ('grapple_damage', _decode_grapple_damage),
    0x58066c47: ('grapple_shake_sound', _decode_grapple_shake_sound),
    0xc2b3754e: ('unknown_0xc2b3754e', _decode_unknown_0xc2b3754e),
    0x21eecb94: ('unknown_0x21eecb94', _decode_unknown_0x21eecb94),
    0xb5fdc280: ('unknown_0xb5fdc280', _decode_unknown_0xb5fdc280),
    0x41d8c39c: ('unknown_0x41d8c39c', _decode_unknown_0x41d8c39c),
    0xaf8984b2: ('unknown_struct30', _decode_unknown_struct30),
    0xdcb5b112: ('unknown_struct31', _decode_unknown_struct31),
    0xc30b62ea: ('unknown_struct32', _decode_unknown_struct32),
    0x7f4e2e7d: ('unknown_struct33', _decode_unknown_struct33),
    0xfc76c51a: ('unknown_struct34', _decode_unknown_struct34),
}
