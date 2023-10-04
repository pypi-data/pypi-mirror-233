# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class EmperorIngStage2TentacleData(BaseProperty):
    detection_time: float = dataclasses.field(default=0.0)
    forget_time: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xba\xa9%J')  # 0xbaa9254a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_time))

        data.write(b'\x1f\xe2\x8a6')  # 0x1fe28a36
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forget_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            detection_time=data['detection_time'],
            forget_time=data['forget_time'],
        )

    def to_json(self) -> dict:
        return {
            'detection_time': self.detection_time,
            'forget_time': self.forget_time,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xbaa9254a, 0x1fe28a36)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[EmperorIngStage2TentacleData]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHf')

    dec = _FAST_FORMAT.unpack(data.read(20))
    assert (dec[0], dec[3]) == _FAST_IDS
    return EmperorIngStage2TentacleData(
        dec[2],
        dec[5],
    )


def _decode_detection_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forget_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbaa9254a: ('detection_time', _decode_detection_time),
    0x1fe28a36: ('forget_time', _decode_forget_time),
}
