# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class TouchAttackDirectionEnum(BaseProperty):
    attack_direction: enums.AttackDirection = dataclasses.field(default=enums.AttackDirection.Unknown1)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\x97!\xd0+')  # 0x9721d02b
        data.write(b'\x00\x04')  # size
        self.attack_direction.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_direction=enums.AttackDirection.from_json(data['attack_direction']),
        )

    def to_json(self) -> dict:
        return {
            'attack_direction': self.attack_direction.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x9721d02b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[TouchAttackDirectionEnum]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHL')

    dec = _FAST_FORMAT.unpack(data.read(10))
    assert (dec[0]) == _FAST_IDS
    return TouchAttackDirectionEnum(
        enums.AttackDirection(dec[2]),
    )


def _decode_attack_direction(data: typing.BinaryIO, property_size: int):
    return enums.AttackDirection.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9721d02b: ('attack_direction', _decode_attack_direction),
}
