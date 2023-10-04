# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums


@dataclasses.dataclass()
class PIDConvergence(BaseProperty):
    pid_type: enums.PIDType = dataclasses.field(default=enums.PIDType.Unknown2)
    k_p: float = dataclasses.field(default=0.0)
    k_i: float = dataclasses.field(default=0.0)
    k_d: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xd0\x81\x01#')  # 0xd0810123
        data.write(b'\x00\x04')  # size
        self.pid_type.to_stream(data)

        data.write(b'\xe8+\x99\xe1')  # 0xe82b99e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.k_p))

        data.write(b'\xcc\xf2\xca\xb2')  # 0xccf2cab2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.k_i))

        data.write(b'pl\xd9l')  # 0x706cd96c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.k_d))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            pid_type=enums.PIDType.from_json(data['pid_type']),
            k_p=data['k_p'],
            k_i=data['k_i'],
            k_d=data['k_d'],
        )

    def to_json(self) -> dict:
        return {
            'pid_type': self.pid_type.to_json(),
            'k_p': self.k_p,
            'k_i': self.k_i,
            'k_d': self.k_d,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xd0810123, 0xe82b99e1, 0xccf2cab2, 0x706cd96c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PIDConvergence]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHfLHfLHf')

    dec = _FAST_FORMAT.unpack(data.read(40))
    assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
    return PIDConvergence(
        enums.PIDType(dec[2]),
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_pid_type(data: typing.BinaryIO, property_size: int):
    return enums.PIDType.from_stream(data)


def _decode_k_p(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_k_i(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_k_d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd0810123: ('pid_type', _decode_pid_type),
    0xe82b99e1: ('k_p', _decode_k_p),
    0xccf2cab2: ('k_i', _decode_k_i),
    0x706cd96c: ('k_d', _decode_k_d),
}
