# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.GrappleData import GrappleData
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct17(BaseProperty):
    health: float = dataclasses.field(default=750.0)
    heart_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    body_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    mouth_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    stun_threshold: float = dataclasses.field(default=80.0)
    stun_decay: float = dataclasses.field(default=0.0)
    stun_delay_min: float = dataclasses.field(default=4.0)
    stun_delay_max: float = dataclasses.field(default=6.0)
    unknown_0xfefd7f33: float = dataclasses.field(default=8.0)
    unknown_0x189dd0d2: float = dataclasses.field(default=12.0)
    wander_distance: float = dataclasses.field(default=20.0)
    too_far_distance: float = dataclasses.field(default=60.0)
    dash_delay_maximum: float = dataclasses.field(default=40.0)
    dash_delay_minimum: float = dataclasses.field(default=40.0)
    dash_delay_variance: float = dataclasses.field(default=5.0)
    grapple_data: GrappleData = dataclasses.field(default_factory=GrappleData)
    unknown_0x0fea8352: float = dataclasses.field(default=0.5)
    unknown_0xe98a2cb3: float = dataclasses.field(default=2.0)
    unknown_0xed52ab86: float = dataclasses.field(default=5.0)
    unknown_0x0b320467: float = dataclasses.field(default=7.0)
    unknown_0x4bf067cb: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xad90c82a: float = dataclasses.field(default=0.5)
    unknown_0x63f5b908: float = dataclasses.field(default=400.0)
    unknown_0x5fae9a93: float = dataclasses.field(default=60.0)
    unknown_0x96ff34d5: float = dataclasses.field(default=4.0)
    unknown_0x709f9b34: float = dataclasses.field(default=6.0)
    unknown_0x61e664cc: float = dataclasses.field(default=25.0)
    charge_fireball: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    grapple_shimmer_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_0x55da2ea4: str = dataclasses.field(default='')
    unknown_0x20dc1c96: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'\xf0d\xb3\xbc')  # 0xf064b3bc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.heart_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\r\x920\xd1')  # 0xd9230d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.body_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed~\xdc\xa3')  # 0xed7edca3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mouth_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[\xdd\x1eL')  # 0x5bdd1e4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_threshold))

        data.write(b'`\x82C\x0f')  # 0x6082430f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_decay))

        data.write(b'2\xb6\x0f\xed')  # 0x32b60fed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_delay_min))

        data.write(b'\xd4\xd6\xa0\x0c')  # 0xd4d6a00c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_delay_max))

        data.write(b'\xfe\xfd\x7f3')  # 0xfefd7f33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfefd7f33))

        data.write(b'\x18\x9d\xd0\xd2')  # 0x189dd0d2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x189dd0d2))

        data.write(b"\xaf'\x0c\x93")  # 0xaf270c93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wander_distance))

        data.write(b'\x88\x19h\x8d')  # 0x8819688d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.too_far_distance))

        data.write(b'\x1b7\xed\xa7')  # 0x1b37eda7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dash_delay_maximum))

        data.write(b'\x8bD\xfdM')  # 0x8b44fd4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dash_delay_minimum))

        data.write(b'\xda\xc0^\xb5')  # 0xdac05eb5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dash_delay_variance))

        data.write(b'\xf6\t\xc67')  # 0xf609c637
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_data.to_stream(data, default_override={'grapple_type': 1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0f\xea\x83R')  # 0xfea8352
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0fea8352))

        data.write(b'\xe9\x8a,\xb3')  # 0xe98a2cb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe98a2cb3))

        data.write(b'\xedR\xab\x86')  # 0xed52ab86
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed52ab86))

        data.write(b'\x0b2\x04g')  # 0xb320467
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0b320467))

        data.write(b'K\xf0g\xcb')  # 0x4bf067cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4bf067cb))

        data.write(b'\xad\x90\xc8*')  # 0xad90c82a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xad90c82a))

        data.write(b'c\xf5\xb9\x08')  # 0x63f5b908
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x63f5b908))

        data.write(b'_\xae\x9a\x93')  # 0x5fae9a93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5fae9a93))

        data.write(b'\x96\xff4\xd5')  # 0x96ff34d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x96ff34d5))

        data.write(b'p\x9f\x9b4')  # 0x709f9b34
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x709f9b34))

        data.write(b'a\xe6d\xcc')  # 0x61e664cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61e664cc))

        data.write(b'\xb3H\xc4k')  # 0xb348c46b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_fireball.to_stream(data, default_override={'burn_damage': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'GmP\xf2')  # 0x476d50f2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.grapple_shimmer_model))

        data.write(b'U\xda.\xa4')  # 0x55da2ea4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x55da2ea4.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \xdc\x1c\x96')  # 0x20dc1c96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x20dc1c96))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=data['health'],
            heart_vulnerability=DamageVulnerability.from_json(data['heart_vulnerability']),
            body_vulnerability=DamageVulnerability.from_json(data['body_vulnerability']),
            mouth_vulnerability=DamageVulnerability.from_json(data['mouth_vulnerability']),
            stun_threshold=data['stun_threshold'],
            stun_decay=data['stun_decay'],
            stun_delay_min=data['stun_delay_min'],
            stun_delay_max=data['stun_delay_max'],
            unknown_0xfefd7f33=data['unknown_0xfefd7f33'],
            unknown_0x189dd0d2=data['unknown_0x189dd0d2'],
            wander_distance=data['wander_distance'],
            too_far_distance=data['too_far_distance'],
            dash_delay_maximum=data['dash_delay_maximum'],
            dash_delay_minimum=data['dash_delay_minimum'],
            dash_delay_variance=data['dash_delay_variance'],
            grapple_data=GrappleData.from_json(data['grapple_data']),
            unknown_0x0fea8352=data['unknown_0x0fea8352'],
            unknown_0xe98a2cb3=data['unknown_0xe98a2cb3'],
            unknown_0xed52ab86=data['unknown_0xed52ab86'],
            unknown_0x0b320467=data['unknown_0x0b320467'],
            unknown_0x4bf067cb=data['unknown_0x4bf067cb'],
            unknown_0xad90c82a=data['unknown_0xad90c82a'],
            unknown_0x63f5b908=data['unknown_0x63f5b908'],
            unknown_0x5fae9a93=data['unknown_0x5fae9a93'],
            unknown_0x96ff34d5=data['unknown_0x96ff34d5'],
            unknown_0x709f9b34=data['unknown_0x709f9b34'],
            unknown_0x61e664cc=data['unknown_0x61e664cc'],
            charge_fireball=LaunchProjectileData.from_json(data['charge_fireball']),
            grapple_shimmer_model=data['grapple_shimmer_model'],
            unknown_0x55da2ea4=data['unknown_0x55da2ea4'],
            unknown_0x20dc1c96=data['unknown_0x20dc1c96'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health,
            'heart_vulnerability': self.heart_vulnerability.to_json(),
            'body_vulnerability': self.body_vulnerability.to_json(),
            'mouth_vulnerability': self.mouth_vulnerability.to_json(),
            'stun_threshold': self.stun_threshold,
            'stun_decay': self.stun_decay,
            'stun_delay_min': self.stun_delay_min,
            'stun_delay_max': self.stun_delay_max,
            'unknown_0xfefd7f33': self.unknown_0xfefd7f33,
            'unknown_0x189dd0d2': self.unknown_0x189dd0d2,
            'wander_distance': self.wander_distance,
            'too_far_distance': self.too_far_distance,
            'dash_delay_maximum': self.dash_delay_maximum,
            'dash_delay_minimum': self.dash_delay_minimum,
            'dash_delay_variance': self.dash_delay_variance,
            'grapple_data': self.grapple_data.to_json(),
            'unknown_0x0fea8352': self.unknown_0x0fea8352,
            'unknown_0xe98a2cb3': self.unknown_0xe98a2cb3,
            'unknown_0xed52ab86': self.unknown_0xed52ab86,
            'unknown_0x0b320467': self.unknown_0x0b320467,
            'unknown_0x4bf067cb': self.unknown_0x4bf067cb,
            'unknown_0xad90c82a': self.unknown_0xad90c82a,
            'unknown_0x63f5b908': self.unknown_0x63f5b908,
            'unknown_0x5fae9a93': self.unknown_0x5fae9a93,
            'unknown_0x96ff34d5': self.unknown_0x96ff34d5,
            'unknown_0x709f9b34': self.unknown_0x709f9b34,
            'unknown_0x61e664cc': self.unknown_0x61e664cc,
            'charge_fireball': self.charge_fireball.to_json(),
            'grapple_shimmer_model': self.grapple_shimmer_model,
            'unknown_0x55da2ea4': self.unknown_0x55da2ea4,
            'unknown_0x20dc1c96': self.unknown_0x20dc1c96,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct17]:
    if property_count != 31:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf0668919
    health = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf064b3bc
    heart_vulnerability = DamageVulnerability.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0d9230d1
    body_vulnerability = DamageVulnerability.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xed7edca3
    mouth_vulnerability = DamageVulnerability.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5bdd1e4c
    stun_threshold = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x6082430f
    stun_decay = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x32b60fed
    stun_delay_min = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd4d6a00c
    stun_delay_max = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfefd7f33
    unknown_0xfefd7f33 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x189dd0d2
    unknown_0x189dd0d2 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xaf270c93
    wander_distance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8819688d
    too_far_distance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x1b37eda7
    dash_delay_maximum = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8b44fd4d
    dash_delay_minimum = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xdac05eb5
    dash_delay_variance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf609c637
    grapple_data = GrappleData.from_stream(data, property_size, default_override={'grapple_type': 1})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0fea8352
    unknown_0x0fea8352 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe98a2cb3
    unknown_0xe98a2cb3 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xed52ab86
    unknown_0xed52ab86 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0b320467
    unknown_0x0b320467 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4bf067cb
    unknown_0x4bf067cb = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xad90c82a
    unknown_0xad90c82a = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x63f5b908
    unknown_0x63f5b908 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5fae9a93
    unknown_0x5fae9a93 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x96ff34d5
    unknown_0x96ff34d5 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x709f9b34
    unknown_0x709f9b34 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x61e664cc
    unknown_0x61e664cc = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb348c46b
    charge_fireball = LaunchProjectileData.from_stream(data, property_size, default_override={'burn_damage': 2.0})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x476d50f2
    grapple_shimmer_model = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x55da2ea4
    unknown_0x55da2ea4 = data.read(property_size)[:-1].decode("utf-8")

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x20dc1c96
    unknown_0x20dc1c96 = struct.unpack('>f', data.read(4))[0]

    return UnknownStruct17(health, heart_vulnerability, body_vulnerability, mouth_vulnerability, stun_threshold, stun_decay, stun_delay_min, stun_delay_max, unknown_0xfefd7f33, unknown_0x189dd0d2, wander_distance, too_far_distance, dash_delay_maximum, dash_delay_minimum, dash_delay_variance, grapple_data, unknown_0x0fea8352, unknown_0xe98a2cb3, unknown_0xed52ab86, unknown_0x0b320467, unknown_0x4bf067cb, unknown_0xad90c82a, unknown_0x63f5b908, unknown_0x5fae9a93, unknown_0x96ff34d5, unknown_0x709f9b34, unknown_0x61e664cc, charge_fireball, grapple_shimmer_model, unknown_0x55da2ea4, unknown_0x20dc1c96)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_decode_heart_vulnerability = DamageVulnerability.from_stream

_decode_body_vulnerability = DamageVulnerability.from_stream

_decode_mouth_vulnerability = DamageVulnerability.from_stream

def _decode_stun_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_decay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_delay_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_delay_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfefd7f33(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x189dd0d2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wander_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_too_far_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dash_delay_maximum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dash_delay_minimum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dash_delay_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_data(data: typing.BinaryIO, property_size: int):
    return GrappleData.from_stream(data, property_size, default_override={'grapple_type': 1})


def _decode_unknown_0x0fea8352(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe98a2cb3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed52ab86(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0b320467(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4bf067cb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xad90c82a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x63f5b908(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5fae9a93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x96ff34d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x709f9b34(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61e664cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_fireball(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size, default_override={'burn_damage': 2.0})


def _decode_grapple_shimmer_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x55da2ea4(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown_0x20dc1c96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf0668919: ('health', _decode_health),
    0xf064b3bc: ('heart_vulnerability', _decode_heart_vulnerability),
    0xd9230d1: ('body_vulnerability', _decode_body_vulnerability),
    0xed7edca3: ('mouth_vulnerability', _decode_mouth_vulnerability),
    0x5bdd1e4c: ('stun_threshold', _decode_stun_threshold),
    0x6082430f: ('stun_decay', _decode_stun_decay),
    0x32b60fed: ('stun_delay_min', _decode_stun_delay_min),
    0xd4d6a00c: ('stun_delay_max', _decode_stun_delay_max),
    0xfefd7f33: ('unknown_0xfefd7f33', _decode_unknown_0xfefd7f33),
    0x189dd0d2: ('unknown_0x189dd0d2', _decode_unknown_0x189dd0d2),
    0xaf270c93: ('wander_distance', _decode_wander_distance),
    0x8819688d: ('too_far_distance', _decode_too_far_distance),
    0x1b37eda7: ('dash_delay_maximum', _decode_dash_delay_maximum),
    0x8b44fd4d: ('dash_delay_minimum', _decode_dash_delay_minimum),
    0xdac05eb5: ('dash_delay_variance', _decode_dash_delay_variance),
    0xf609c637: ('grapple_data', _decode_grapple_data),
    0xfea8352: ('unknown_0x0fea8352', _decode_unknown_0x0fea8352),
    0xe98a2cb3: ('unknown_0xe98a2cb3', _decode_unknown_0xe98a2cb3),
    0xed52ab86: ('unknown_0xed52ab86', _decode_unknown_0xed52ab86),
    0xb320467: ('unknown_0x0b320467', _decode_unknown_0x0b320467),
    0x4bf067cb: ('unknown_0x4bf067cb', _decode_unknown_0x4bf067cb),
    0xad90c82a: ('unknown_0xad90c82a', _decode_unknown_0xad90c82a),
    0x63f5b908: ('unknown_0x63f5b908', _decode_unknown_0x63f5b908),
    0x5fae9a93: ('unknown_0x5fae9a93', _decode_unknown_0x5fae9a93),
    0x96ff34d5: ('unknown_0x96ff34d5', _decode_unknown_0x96ff34d5),
    0x709f9b34: ('unknown_0x709f9b34', _decode_unknown_0x709f9b34),
    0x61e664cc: ('unknown_0x61e664cc', _decode_unknown_0x61e664cc),
    0xb348c46b: ('charge_fireball', _decode_charge_fireball),
    0x476d50f2: ('grapple_shimmer_model', _decode_grapple_shimmer_model),
    0x55da2ea4: ('unknown_0x55da2ea4', _decode_unknown_0x55da2ea4),
    0x20dc1c96: ('unknown_0x20dc1c96', _decode_unknown_0x20dc1c96),
}
