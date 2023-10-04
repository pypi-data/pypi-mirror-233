# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.PIDConvergence import PIDConvergence
from retro_data_structures.properties.dkc_returns.archetypes.ProportionalConvergence import ProportionalConvergence
from retro_data_structures.properties.dkc_returns.archetypes.SpringConvergence import SpringConvergence
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct66 import UnknownStruct66
from retro_data_structures.properties.dkc_returns.archetypes.VelocityConvergence import VelocityConvergence


@dataclasses.dataclass()
class Convergence(BaseProperty):
    convergence_type: enums.ConvergenceType = dataclasses.field(default=enums.ConvergenceType.Unknown4)
    velocity: VelocityConvergence = dataclasses.field(default_factory=VelocityConvergence)
    unknown_struct66: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    spring: SpringConvergence = dataclasses.field(default_factory=SpringConvergence)
    pid: PIDConvergence = dataclasses.field(default_factory=PIDConvergence)
    proportional: ProportionalConvergence = dataclasses.field(default_factory=ProportionalConvergence)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'.\xf2$\x01')  # 0x2ef22401
        data.write(b'\x00\x04')  # size
        self.convergence_type.to_stream(data)

        data.write(b'o\x9d\x9b3')  # 0x6f9d9b33
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.velocity.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\xf4}\xdf')  # 0x1ff47ddf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct66.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c\xf38\x16')  # 0xcf33816
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spring.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xe4\x02\xef')  # 0xf9e402ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pid.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08VH\xbc')  # 0x85648bc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.proportional.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            convergence_type=enums.ConvergenceType.from_json(data['convergence_type']),
            velocity=VelocityConvergence.from_json(data['velocity']),
            unknown_struct66=UnknownStruct66.from_json(data['unknown_struct66']),
            spring=SpringConvergence.from_json(data['spring']),
            pid=PIDConvergence.from_json(data['pid']),
            proportional=ProportionalConvergence.from_json(data['proportional']),
        )

    def to_json(self) -> dict:
        return {
            'convergence_type': self.convergence_type.to_json(),
            'velocity': self.velocity.to_json(),
            'unknown_struct66': self.unknown_struct66.to_json(),
            'spring': self.spring.to_json(),
            'pid': self.pid.to_json(),
            'proportional': self.proportional.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Convergence]:
    if property_count != 6:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2ef22401
    convergence_type = enums.ConvergenceType.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x6f9d9b33
    velocity = VelocityConvergence.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x1ff47ddf
    unknown_struct66 = UnknownStruct66.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0cf33816
    spring = SpringConvergence.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf9e402ef
    pid = PIDConvergence.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x085648bc
    proportional = ProportionalConvergence.from_stream(data, property_size)

    return Convergence(convergence_type, velocity, unknown_struct66, spring, pid, proportional)


def _decode_convergence_type(data: typing.BinaryIO, property_size: int):
    return enums.ConvergenceType.from_stream(data)


_decode_velocity = VelocityConvergence.from_stream

_decode_unknown_struct66 = UnknownStruct66.from_stream

_decode_spring = SpringConvergence.from_stream

_decode_pid = PIDConvergence.from_stream

_decode_proportional = ProportionalConvergence.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2ef22401: ('convergence_type', _decode_convergence_type),
    0x6f9d9b33: ('velocity', _decode_velocity),
    0x1ff47ddf: ('unknown_struct66', _decode_unknown_struct66),
    0xcf33816: ('spring', _decode_spring),
    0xf9e402ef: ('pid', _decode_pid),
    0x85648bc: ('proportional', _decode_proportional),
}
