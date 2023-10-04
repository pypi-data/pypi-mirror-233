# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class ScanBeamInfo(BaseProperty):
    angle: float = dataclasses.field(default=20.0)
    cloud_color1: Color = dataclasses.field(default_factory=lambda: Color(r=0.24705900251865387, g=0.0, b=0.0, a=0.0))
    cloud_color2: Color = dataclasses.field(default_factory=lambda: Color(r=0.49803900718688965, g=1.0, b=0.09803900122642517, a=0.0))
    add_color1: Color = dataclasses.field(default_factory=lambda: Color(r=0.34902000427246094, g=0.0, b=0.0, a=0.0))
    add_color2: Color = dataclasses.field(default_factory=lambda: Color(r=0.1490200012922287, g=0.0, b=0.0, a=0.0))
    cloud_scale: float = dataclasses.field(default=10.0)
    fade_off_size: float = dataclasses.field(default=5.0)
    open_speed: float = dataclasses.field(default=4.0)
    scan_length: float = dataclasses.field(default=50.0)
    sound_scanning: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'8*\x19s')  # 0x382a1973
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angle))

        data.write(b'LA\xdc\xd4')  # 0x4c41dcd4
        data.write(b'\x00\x10')  # size
        self.cloud_color1.to_stream(data)

        data.write(b'\xca\xd5\xaez')  # 0xcad5ae7a
        data.write(b'\x00\x10')  # size
        self.cloud_color2.to_stream(data)

        data.write(b'\x1eR\x12N')  # 0x1e52124e
        data.write(b'\x00\x10')  # size
        self.add_color1.to_stream(data)

        data.write(b'\x98\xc6`\xe0')  # 0x98c660e0
        data.write(b'\x00\x10')  # size
        self.add_color2.to_stream(data)

        data.write(b'\x10\xc1\xde\xd2')  # 0x10c1ded2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloud_scale))

        data.write(b'\xaeq\xa2*')  # 0xae71a22a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_off_size))

        data.write(b'N)\xc8Z')  # 0x4e29c85a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.open_speed))

        data.write(b'\x03f\x03c')  # 0x3660363
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_length))

        data.write(b'\x1dS\xd1\xda')  # 0x1d53d1da
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_scanning))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            angle=data['angle'],
            cloud_color1=Color.from_json(data['cloud_color1']),
            cloud_color2=Color.from_json(data['cloud_color2']),
            add_color1=Color.from_json(data['add_color1']),
            add_color2=Color.from_json(data['add_color2']),
            cloud_scale=data['cloud_scale'],
            fade_off_size=data['fade_off_size'],
            open_speed=data['open_speed'],
            scan_length=data['scan_length'],
            sound_scanning=data['sound_scanning'],
        )

    def to_json(self) -> dict:
        return {
            'angle': self.angle,
            'cloud_color1': self.cloud_color1.to_json(),
            'cloud_color2': self.cloud_color2.to_json(),
            'add_color1': self.add_color1.to_json(),
            'add_color2': self.add_color2.to_json(),
            'cloud_scale': self.cloud_scale,
            'fade_off_size': self.fade_off_size,
            'open_speed': self.open_speed,
            'scan_length': self.scan_length,
            'sound_scanning': self.sound_scanning,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x382a1973, 0x4c41dcd4, 0xcad5ae7a, 0x1e52124e, 0x98c660e0, 0x10c1ded2, 0xae71a22a, 0x4e29c85a, 0x3660363, 0x1d53d1da)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ScanBeamInfo]:
    if property_count != 10:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHffffLHffffLHffffLHffffLHfLHfLHfLHfLHQ')

    dec = _FAST_FORMAT.unpack(data.read(152))
    assert (dec[0], dec[3], dec[9], dec[15], dec[21], dec[27], dec[30], dec[33], dec[36], dec[39]) == _FAST_IDS
    return ScanBeamInfo(
        dec[2],
        Color(*dec[5:9]),
        Color(*dec[11:15]),
        Color(*dec[17:21]),
        Color(*dec[23:27]),
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
    )


def _decode_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cloud_color1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_cloud_color2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_add_color1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_add_color2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_cloud_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_off_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_open_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_scanning(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x382a1973: ('angle', _decode_angle),
    0x4c41dcd4: ('cloud_color1', _decode_cloud_color1),
    0xcad5ae7a: ('cloud_color2', _decode_cloud_color2),
    0x1e52124e: ('add_color1', _decode_add_color1),
    0x98c660e0: ('add_color2', _decode_add_color2),
    0x10c1ded2: ('cloud_scale', _decode_cloud_scale),
    0xae71a22a: ('fade_off_size', _decode_fade_off_size),
    0x4e29c85a: ('open_speed', _decode_open_speed),
    0x3660363: ('scan_length', _decode_scan_length),
    0x1d53d1da: ('sound_scanning', _decode_sound_scanning),
}
