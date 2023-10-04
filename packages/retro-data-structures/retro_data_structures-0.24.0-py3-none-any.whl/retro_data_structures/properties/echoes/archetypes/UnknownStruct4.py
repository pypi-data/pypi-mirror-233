# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct4(BaseProperty):
    behaviour_type: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\xc1\xe7G\xad')  # 0xc1e747ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.behaviour_type))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            behaviour_type=data['behaviour_type'],
        )

    def to_json(self) -> dict:
        return {
            'behaviour_type': self.behaviour_type,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xc1e747ad)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct4]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHl')

    dec = _FAST_FORMAT.unpack(data.read(10))
    assert (dec[0]) == _FAST_IDS
    return UnknownStruct4(
        dec[2],
    )


def _decode_behaviour_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc1e747ad: ('behaviour_type', _decode_behaviour_type),
}
