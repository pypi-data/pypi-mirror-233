# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.RotationSplines import RotationSplines
from retro_data_structures.properties.corruption.archetypes.ScaleSplines import ScaleSplines
from retro_data_structures.properties.corruption.archetypes.TranslationSplines import TranslationSplines
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class ActorTransform(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_actor_transform: int = dataclasses.field(default=20)  # Flagset
    duration: float = dataclasses.field(default=10.0)
    rotation_controls: RotationSplines = dataclasses.field(default_factory=RotationSplines)
    scale_controls: ScaleSplines = dataclasses.field(default_factory=ScaleSplines)
    translation_control: TranslationSplines = dataclasses.field(default_factory=TranslationSplines)
    path_position: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ATRN'

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xcev\x89')  # 0xc6ce7689
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_actor_transform))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\xef\xe4\xeaW')  # 0xefe4ea57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotation_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/~\xc0\xa2')  # 0x2f7ec0a2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i"g\xea')  # 0x692267ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.translation_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\xb8\xaa\xca')  # 0x51b8aaca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path_position.to_stream(data)
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
            flags_actor_transform=data['flags_actor_transform'],
            duration=data['duration'],
            rotation_controls=RotationSplines.from_json(data['rotation_controls']),
            scale_controls=ScaleSplines.from_json(data['scale_controls']),
            translation_control=TranslationSplines.from_json(data['translation_control']),
            path_position=Spline.from_json(data['path_position']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_actor_transform': self.flags_actor_transform,
            'duration': self.duration,
            'rotation_controls': self.rotation_controls.to_json(),
            'scale_controls': self.scale_controls.to_json(),
            'translation_control': self.translation_control.to_json(),
            'path_position': self.path_position.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ActorTransform]:
    if property_count != 7:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc6ce7689
    flags_actor_transform = struct.unpack(">L", data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8b51e23f
    duration = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xefe4ea57
    rotation_controls = RotationSplines.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2f7ec0a2
    scale_controls = ScaleSplines.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x692267ea
    translation_control = TranslationSplines.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x51b8aaca
    path_position = Spline.from_stream(data, property_size)

    return ActorTransform(editor_properties, flags_actor_transform, duration, rotation_controls, scale_controls, translation_control, path_position)


_decode_editor_properties = EditorProperties.from_stream

def _decode_flags_actor_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_decode_rotation_controls = RotationSplines.from_stream

_decode_scale_controls = ScaleSplines.from_stream

_decode_translation_control = TranslationSplines.from_stream

_decode_path_position = Spline.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc6ce7689: ('flags_actor_transform', _decode_flags_actor_transform),
    0x8b51e23f: ('duration', _decode_duration),
    0xefe4ea57: ('rotation_controls', _decode_rotation_controls),
    0x2f7ec0a2: ('scale_controls', _decode_scale_controls),
    0x692267ea: ('translation_control', _decode_translation_control),
    0x51b8aaca: ('path_position', _decode_path_position),
}
