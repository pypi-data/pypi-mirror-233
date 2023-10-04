# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.DynamicLightFalloff import DynamicLightFalloff
from retro_data_structures.properties.corruption.archetypes.DynamicLightIntensity import DynamicLightIntensity
from retro_data_structures.properties.corruption.archetypes.DynamicLightMotionSpline import DynamicLightMotionSpline
from retro_data_structures.properties.corruption.archetypes.DynamicLightParent import DynamicLightParent
from retro_data_structures.properties.corruption.archetypes.DynamicLightSpotlight import DynamicLightSpotlight
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class DynamicLight(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    light_type: int = dataclasses.field(default=2)
    unknown_0xe42bab04: bool = dataclasses.field(default=True)
    unknown_0x364a7b36: bool = dataclasses.field(default=True)
    unknown_0x4ea02861: bool = dataclasses.field(default=True)
    unknown_0xa502605d: bool = dataclasses.field(default=True)
    unknown_0xa19817f0: bool = dataclasses.field(default=True)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    intensity: DynamicLightIntensity = dataclasses.field(default_factory=DynamicLightIntensity)
    falloff: DynamicLightFalloff = dataclasses.field(default_factory=DynamicLightFalloff)
    spotlight: DynamicLightSpotlight = dataclasses.field(default_factory=DynamicLightSpotlight)
    motion_spline: DynamicLightMotionSpline = dataclasses.field(default_factory=DynamicLightMotionSpline)
    parent: DynamicLightParent = dataclasses.field(default_factory=DynamicLightParent)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DLHT'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xc4\xe36')  # 0x7fc4e336
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_type))

        data.write(b'\xe4+\xab\x04')  # 0xe42bab04
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe42bab04))

        data.write(b'6J{6')  # 0x364a7b36
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x364a7b36))

        data.write(b'N\xa0(a')  # 0x4ea02861
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4ea02861))

        data.write(b'\xa5\x02`]')  # 0xa502605d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa502605d))

        data.write(b'\xa1\x98\x17\xf0')  # 0xa19817f0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa19817f0))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'rS\x1e\xde')  # 0x72531ede
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.intensity.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\x9bR\xda')  # 0x219b52da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.falloff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95F\xf4I')  # 0x9546f449
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spotlight.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x142!8')  # 0x14322138
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf74\xdf\x8c')  # 0xf734df8c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.parent.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            light_type=data['light_type'],
            unknown_0xe42bab04=data['unknown_0xe42bab04'],
            unknown_0x364a7b36=data['unknown_0x364a7b36'],
            unknown_0x4ea02861=data['unknown_0x4ea02861'],
            unknown_0xa502605d=data['unknown_0xa502605d'],
            unknown_0xa19817f0=data['unknown_0xa19817f0'],
            color=Color.from_json(data['color']),
            intensity=DynamicLightIntensity.from_json(data['intensity']),
            falloff=DynamicLightFalloff.from_json(data['falloff']),
            spotlight=DynamicLightSpotlight.from_json(data['spotlight']),
            motion_spline=DynamicLightMotionSpline.from_json(data['motion_spline']),
            parent=DynamicLightParent.from_json(data['parent']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'light_type': self.light_type,
            'unknown_0xe42bab04': self.unknown_0xe42bab04,
            'unknown_0x364a7b36': self.unknown_0x364a7b36,
            'unknown_0x4ea02861': self.unknown_0x4ea02861,
            'unknown_0xa502605d': self.unknown_0xa502605d,
            'unknown_0xa19817f0': self.unknown_0xa19817f0,
            'color': self.color.to_json(),
            'intensity': self.intensity.to_json(),
            'falloff': self.falloff.to_json(),
            'spotlight': self.spotlight.to_json(),
            'motion_spline': self.motion_spline.to_json(),
            'parent': self.parent.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DynamicLight]:
    if property_count != 13:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7fc4e336
    light_type = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe42bab04
    unknown_0xe42bab04 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x364a7b36
    unknown_0x364a7b36 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4ea02861
    unknown_0x4ea02861 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa502605d
    unknown_0xa502605d = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa19817f0
    unknown_0xa19817f0 = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x37c7d09d
    color = Color.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x72531ede
    intensity = DynamicLightIntensity.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x219b52da
    falloff = DynamicLightFalloff.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9546f449
    spotlight = DynamicLightSpotlight.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x14322138
    motion_spline = DynamicLightMotionSpline.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xf734df8c
    parent = DynamicLightParent.from_stream(data, property_size)

    return DynamicLight(editor_properties, light_type, unknown_0xe42bab04, unknown_0x364a7b36, unknown_0x4ea02861, unknown_0xa502605d, unknown_0xa19817f0, color, intensity, falloff, spotlight, motion_spline, parent)


_decode_editor_properties = EditorProperties.from_stream

def _decode_light_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xe42bab04(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x364a7b36(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4ea02861(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa502605d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa19817f0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_decode_intensity = DynamicLightIntensity.from_stream

_decode_falloff = DynamicLightFalloff.from_stream

_decode_spotlight = DynamicLightSpotlight.from_stream

_decode_motion_spline = DynamicLightMotionSpline.from_stream

_decode_parent = DynamicLightParent.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7fc4e336: ('light_type', _decode_light_type),
    0xe42bab04: ('unknown_0xe42bab04', _decode_unknown_0xe42bab04),
    0x364a7b36: ('unknown_0x364a7b36', _decode_unknown_0x364a7b36),
    0x4ea02861: ('unknown_0x4ea02861', _decode_unknown_0x4ea02861),
    0xa502605d: ('unknown_0xa502605d', _decode_unknown_0xa502605d),
    0xa19817f0: ('unknown_0xa19817f0', _decode_unknown_0xa19817f0),
    0x37c7d09d: ('color', _decode_color),
    0x72531ede: ('intensity', _decode_intensity),
    0x219b52da: ('falloff', _decode_falloff),
    0x9546f449: ('spotlight', _decode_spotlight),
    0x14322138: ('motion_spline', _decode_motion_spline),
    0xf734df8c: ('parent', _decode_parent),
}
