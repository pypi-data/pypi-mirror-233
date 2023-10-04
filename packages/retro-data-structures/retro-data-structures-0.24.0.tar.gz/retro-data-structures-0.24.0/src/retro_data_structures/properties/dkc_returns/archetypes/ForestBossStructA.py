# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class ForestBossStructA(BaseProperty):
    sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown: Spline = dataclasses.field(default_factory=Spline)
    pitch: Spline = dataclasses.field(default_factory=Spline)
    volume: Spline = dataclasses.field(default_factory=Spline)
    maximum_input_value: float = dataclasses.field(default=15.0)
    minimum_input_value: float = dataclasses.field(default=0.0)

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

        data.write(b'\xa5]\xac\xf6')  # 0xa55dacf6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound))

        data.write(b'\x8a\x93\x93y')  # 0x8a939379
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0er\x7f\xc4')  # 0xe727fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xfb\xe4\x84')  # 0xf3fbe484
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\x974\x05')  # 0xe2973405
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_input_value))

        data.write(b'\xa3\x80\x0b\x83')  # 0xa3800b83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_input_value))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            sound=data['sound'],
            unknown=Spline.from_json(data['unknown']),
            pitch=Spline.from_json(data['pitch']),
            volume=Spline.from_json(data['volume']),
            maximum_input_value=data['maximum_input_value'],
            minimum_input_value=data['minimum_input_value'],
        )

    def to_json(self) -> dict:
        return {
            'sound': self.sound,
            'unknown': self.unknown.to_json(),
            'pitch': self.pitch.to_json(),
            'volume': self.volume.to_json(),
            'maximum_input_value': self.maximum_input_value,
            'minimum_input_value': self.minimum_input_value,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ForestBossStructA]:
    if property_count != 6:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa55dacf6
    sound = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8a939379
    unknown = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0e727fc4
    pitch = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf3fbe484
    volume = Spline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe2973405
    maximum_input_value = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa3800b83
    minimum_input_value = struct.unpack('>f', data.read(4))[0]

    return ForestBossStructA(sound, unknown, pitch, volume, maximum_input_value, minimum_input_value)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_decode_unknown = Spline.from_stream

_decode_pitch = Spline.from_stream

_decode_volume = Spline.from_stream

def _decode_maximum_input_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_input_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa55dacf6: ('sound', _decode_sound),
    0x8a939379: ('unknown', _decode_unknown),
    0xe727fc4: ('pitch', _decode_pitch),
    0xf3fbe484: ('volume', _decode_volume),
    0xe2973405: ('maximum_input_value', _decode_maximum_input_value),
    0xa3800b83: ('minimum_input_value', _decode_minimum_input_value),
}
