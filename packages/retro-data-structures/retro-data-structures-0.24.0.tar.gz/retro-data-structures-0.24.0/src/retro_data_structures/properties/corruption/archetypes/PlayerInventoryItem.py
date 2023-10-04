# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerInventoryItem(BaseProperty):
    amount: int = dataclasses.field(default=0)
    capacity: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x94\xaf\x14E')  # 0x94af1445
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.amount))

        data.write(b'm\xc5\x9f\x13')  # 0x6dc59f13
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.capacity))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            amount=data['amount'],
            capacity=data['capacity'],
        )

    def to_json(self) -> dict:
        return {
            'amount': self.amount,
            'capacity': self.capacity,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x94af1445, 0x6dc59f13)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerInventoryItem]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHl')

    dec = _FAST_FORMAT.unpack(data.read(20))
    assert (dec[0], dec[3]) == _FAST_IDS
    return PlayerInventoryItem(
        dec[2],
        dec[5],
    )


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_capacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x94af1445: ('amount', _decode_amount),
    0x6dc59f13: ('capacity', _decode_capacity),
}
