# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.GrappleBeam import GrappleBeam


@dataclasses.dataclass()
class Grapple(BaseProperty):
    grapple_distance: float = dataclasses.field(default=25.0)
    grapple_beam_length: float = dataclasses.field(default=10.0)
    grapple_swing_time: float = dataclasses.field(default=3.299999952316284)
    grapple_max_velocity: float = dataclasses.field(default=23.0)
    grapple_camera_speed: float = dataclasses.field(default=90.0)
    grapple_pull_close_distance: float = dataclasses.field(default=0.5)
    grapple_pull_dampen_distance: float = dataclasses.field(default=2.0)
    grapple_pull_velocity: float = dataclasses.field(default=30.0)
    grapple_pull_camera_speed: float = dataclasses.field(default=90.0)
    grapple_turn_rate: float = dataclasses.field(default=35.0)
    grapple_jump_force: float = dataclasses.field(default=13.0)
    grapple_release_time: float = dataclasses.field(default=1.0)
    grapple_control_scheme: int = dataclasses.field(default=2)
    grapple_hold_orbit_button: bool = dataclasses.field(default=True)
    grapple_turn_controls_reversed: bool = dataclasses.field(default=True)
    beam: GrappleBeam = dataclasses.field(default_factory=GrappleBeam)

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'\xa7&1k')  # 0xa726316b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_distance))

        data.write(b'3\xe7\x9bQ')  # 0x33e79b51
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_beam_length))

        data.write(b'\x9d\xd3\xe8\x8b')  # 0x9dd3e88b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_swing_time))

        data.write(b'\xfb`[\xa4')  # 0xfb605ba4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_max_velocity))

        data.write(b'\xfe\x98\xb8\xe9')  # 0xfe98b8e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_camera_speed))

        data.write(b'\x92\x10\xa2^')  # 0x9210a25e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_close_distance))

        data.write(b'\xbe\x0c\x8b^')  # 0xbe0c8b5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_dampen_distance))

        data.write(b'&\x03\xa0\xbe')  # 0x2603a0be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_velocity))

        data.write(b'[\x98\xa3\xbd')  # 0x5b98a3bd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_camera_speed))

        data.write(b'\x87\xd4\xb5\xd6')  # 0x87d4b5d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_turn_rate))

        data.write(b'\xb7\xf8*\x9f')  # 0xb7f82a9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_jump_force))

        data.write(b'9Tx\xa8')  # 0x395478a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_release_time))

        data.write(b'\x93\xc0\x13\xc9')  # 0x93c013c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grapple_control_scheme))

        data.write(b'\x8e\xee\xd66')  # 0x8eeed636
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_hold_orbit_button))

        data.write(b'\xe1\xeb\x12\xe2')  # 0xe1eb12e2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_turn_controls_reversed))

        data.write(b'\xae\x1f\xc4|')  # 0xae1fc47c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            grapple_distance=data['grapple_distance'],
            grapple_beam_length=data['grapple_beam_length'],
            grapple_swing_time=data['grapple_swing_time'],
            grapple_max_velocity=data['grapple_max_velocity'],
            grapple_camera_speed=data['grapple_camera_speed'],
            grapple_pull_close_distance=data['grapple_pull_close_distance'],
            grapple_pull_dampen_distance=data['grapple_pull_dampen_distance'],
            grapple_pull_velocity=data['grapple_pull_velocity'],
            grapple_pull_camera_speed=data['grapple_pull_camera_speed'],
            grapple_turn_rate=data['grapple_turn_rate'],
            grapple_jump_force=data['grapple_jump_force'],
            grapple_release_time=data['grapple_release_time'],
            grapple_control_scheme=data['grapple_control_scheme'],
            grapple_hold_orbit_button=data['grapple_hold_orbit_button'],
            grapple_turn_controls_reversed=data['grapple_turn_controls_reversed'],
            beam=GrappleBeam.from_json(data['beam']),
        )

    def to_json(self) -> dict:
        return {
            'grapple_distance': self.grapple_distance,
            'grapple_beam_length': self.grapple_beam_length,
            'grapple_swing_time': self.grapple_swing_time,
            'grapple_max_velocity': self.grapple_max_velocity,
            'grapple_camera_speed': self.grapple_camera_speed,
            'grapple_pull_close_distance': self.grapple_pull_close_distance,
            'grapple_pull_dampen_distance': self.grapple_pull_dampen_distance,
            'grapple_pull_velocity': self.grapple_pull_velocity,
            'grapple_pull_camera_speed': self.grapple_pull_camera_speed,
            'grapple_turn_rate': self.grapple_turn_rate,
            'grapple_jump_force': self.grapple_jump_force,
            'grapple_release_time': self.grapple_release_time,
            'grapple_control_scheme': self.grapple_control_scheme,
            'grapple_hold_orbit_button': self.grapple_hold_orbit_button,
            'grapple_turn_controls_reversed': self.grapple_turn_controls_reversed,
            'beam': self.beam.to_json(),
        }

    def _dependencies_for_beam(self, asset_manager):
        yield from self.beam.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_beam, "beam", "GrappleBeam"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Grapple.{field_name} ({field_type}): {e}"
                )


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Grapple]:
    if property_count != 16:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa726316b
    grapple_distance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x33e79b51
    grapple_beam_length = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9dd3e88b
    grapple_swing_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfb605ba4
    grapple_max_velocity = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfe98b8e9
    grapple_camera_speed = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9210a25e
    grapple_pull_close_distance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbe0c8b5e
    grapple_pull_dampen_distance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2603a0be
    grapple_pull_velocity = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5b98a3bd
    grapple_pull_camera_speed = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x87d4b5d6
    grapple_turn_rate = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb7f82a9f
    grapple_jump_force = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x395478a8
    grapple_release_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x93c013c9
    grapple_control_scheme = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8eeed636
    grapple_hold_orbit_button = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe1eb12e2
    grapple_turn_controls_reversed = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xae1fc47c
    beam = GrappleBeam.from_stream(data, property_size)

    return Grapple(grapple_distance, grapple_beam_length, grapple_swing_time, grapple_max_velocity, grapple_camera_speed, grapple_pull_close_distance, grapple_pull_dampen_distance, grapple_pull_velocity, grapple_pull_camera_speed, grapple_turn_rate, grapple_jump_force, grapple_release_time, grapple_control_scheme, grapple_hold_orbit_button, grapple_turn_controls_reversed, beam)


def _decode_grapple_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_beam_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_swing_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_max_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_camera_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_close_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_dampen_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_camera_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_jump_force(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_release_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_control_scheme(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grapple_hold_orbit_button(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_turn_controls_reversed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_decode_beam = GrappleBeam.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa726316b: ('grapple_distance', _decode_grapple_distance),
    0x33e79b51: ('grapple_beam_length', _decode_grapple_beam_length),
    0x9dd3e88b: ('grapple_swing_time', _decode_grapple_swing_time),
    0xfb605ba4: ('grapple_max_velocity', _decode_grapple_max_velocity),
    0xfe98b8e9: ('grapple_camera_speed', _decode_grapple_camera_speed),
    0x9210a25e: ('grapple_pull_close_distance', _decode_grapple_pull_close_distance),
    0xbe0c8b5e: ('grapple_pull_dampen_distance', _decode_grapple_pull_dampen_distance),
    0x2603a0be: ('grapple_pull_velocity', _decode_grapple_pull_velocity),
    0x5b98a3bd: ('grapple_pull_camera_speed', _decode_grapple_pull_camera_speed),
    0x87d4b5d6: ('grapple_turn_rate', _decode_grapple_turn_rate),
    0xb7f82a9f: ('grapple_jump_force', _decode_grapple_jump_force),
    0x395478a8: ('grapple_release_time', _decode_grapple_release_time),
    0x93c013c9: ('grapple_control_scheme', _decode_grapple_control_scheme),
    0x8eeed636: ('grapple_hold_orbit_button', _decode_grapple_hold_orbit_button),
    0xe1eb12e2: ('grapple_turn_controls_reversed', _decode_grapple_turn_controls_reversed),
    0xae1fc47c: ('beam', _decode_beam),
}
