# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.CameraConstraints import CameraConstraints
from retro_data_structures.properties.corruption.archetypes.CameraFieldOfView import CameraFieldOfView
from retro_data_structures.properties.corruption.archetypes.CameraInterpolation import CameraInterpolation
from retro_data_structures.properties.corruption.archetypes.CameraMotion import CameraMotion
from retro_data_structures.properties.corruption.archetypes.CameraNavigation import CameraNavigation
from retro_data_structures.properties.corruption.archetypes.CameraOrientation import CameraOrientation
from retro_data_structures.properties.corruption.archetypes.CameraPosition import CameraPosition
from retro_data_structures.properties.corruption.archetypes.CameraRotation import CameraRotation
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.InterpolationMethod import InterpolationMethod


@dataclasses.dataclass()
class CameraHint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    priority: int = dataclasses.field(default=50)
    timer: float = dataclasses.field(default=0.0)
    flags_camera_hint: int = dataclasses.field(default=30853)  # Flagset
    constraints: CameraConstraints = dataclasses.field(default_factory=CameraConstraints)
    position_behavior: CameraPosition = dataclasses.field(default_factory=CameraPosition)
    navigation_behavior: CameraNavigation = dataclasses.field(default_factory=CameraNavigation)
    motion_behavior: CameraMotion = dataclasses.field(default_factory=CameraMotion)
    orientation_behavior: CameraOrientation = dataclasses.field(default_factory=CameraOrientation)
    rotation_behavior: CameraRotation = dataclasses.field(default_factory=CameraRotation)
    field_of_view_behavior: CameraFieldOfView = dataclasses.field(default_factory=CameraFieldOfView)
    interpolation_behavior: CameraInterpolation = dataclasses.field(default_factory=CameraInterpolation)
    control_frame_interpolation: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CAMH'

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

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

        data.write(b'\x87GU.')  # 0x8747552e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.timer))

        data.write(b'!\xd7 \xa9')  # 0x21d720a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_camera_hint))

        data.write(b'\x97\xa9?\x8f')  # 0x97a93f8f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.constraints.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1\xbd\\@')  # 0xd1bd5c40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.position_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'K\xe3IK')  # 0x4be3494b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.navigation_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xc3\xe7u')  # 0xebc3e775
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'e\xfc\x11\xff')  # 0x65fc11ff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xa7\xc3\x8d')  # 0xa7c38d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotation_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\x12j\xd1')  # 0xfc126ad1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.field_of_view_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"vH'\xd4")  # 0x764827d4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.interpolation_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xd0\xd47')  # 0x95d0d437
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_frame_interpolation.to_stream(data)
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
            priority=data['priority'],
            timer=data['timer'],
            flags_camera_hint=data['flags_camera_hint'],
            constraints=CameraConstraints.from_json(data['constraints']),
            position_behavior=CameraPosition.from_json(data['position_behavior']),
            navigation_behavior=CameraNavigation.from_json(data['navigation_behavior']),
            motion_behavior=CameraMotion.from_json(data['motion_behavior']),
            orientation_behavior=CameraOrientation.from_json(data['orientation_behavior']),
            rotation_behavior=CameraRotation.from_json(data['rotation_behavior']),
            field_of_view_behavior=CameraFieldOfView.from_json(data['field_of_view_behavior']),
            interpolation_behavior=CameraInterpolation.from_json(data['interpolation_behavior']),
            control_frame_interpolation=InterpolationMethod.from_json(data['control_frame_interpolation']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'priority': self.priority,
            'timer': self.timer,
            'flags_camera_hint': self.flags_camera_hint,
            'constraints': self.constraints.to_json(),
            'position_behavior': self.position_behavior.to_json(),
            'navigation_behavior': self.navigation_behavior.to_json(),
            'motion_behavior': self.motion_behavior.to_json(),
            'orientation_behavior': self.orientation_behavior.to_json(),
            'rotation_behavior': self.rotation_behavior.to_json(),
            'field_of_view_behavior': self.field_of_view_behavior.to_json(),
            'interpolation_behavior': self.interpolation_behavior.to_json(),
            'control_frame_interpolation': self.control_frame_interpolation.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[CameraHint]:
    if property_count != 13:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x42087650
    priority = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x8747552e
    timer = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x21d720a9
    flags_camera_hint = struct.unpack(">L", data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x97a93f8f
    constraints = CameraConstraints.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd1bd5c40
    position_behavior = CameraPosition.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4be3494b
    navigation_behavior = CameraNavigation.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xebc3e775
    motion_behavior = CameraMotion.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x65fc11ff
    orientation_behavior = CameraOrientation.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x00a7c38d
    rotation_behavior = CameraRotation.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xfc126ad1
    field_of_view_behavior = CameraFieldOfView.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x764827d4
    interpolation_behavior = CameraInterpolation.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x95d0d437
    control_frame_interpolation = InterpolationMethod.from_stream(data, property_size)

    return CameraHint(editor_properties, priority, timer, flags_camera_hint, constraints, position_behavior, navigation_behavior, motion_behavior, orientation_behavior, rotation_behavior, field_of_view_behavior, interpolation_behavior, control_frame_interpolation)


_decode_editor_properties = EditorProperties.from_stream

def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flags_camera_hint(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_decode_constraints = CameraConstraints.from_stream

_decode_position_behavior = CameraPosition.from_stream

_decode_navigation_behavior = CameraNavigation.from_stream

_decode_motion_behavior = CameraMotion.from_stream

_decode_orientation_behavior = CameraOrientation.from_stream

_decode_rotation_behavior = CameraRotation.from_stream

_decode_field_of_view_behavior = CameraFieldOfView.from_stream

_decode_interpolation_behavior = CameraInterpolation.from_stream

_decode_control_frame_interpolation = InterpolationMethod.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x42087650: ('priority', _decode_priority),
    0x8747552e: ('timer', _decode_timer),
    0x21d720a9: ('flags_camera_hint', _decode_flags_camera_hint),
    0x97a93f8f: ('constraints', _decode_constraints),
    0xd1bd5c40: ('position_behavior', _decode_position_behavior),
    0x4be3494b: ('navigation_behavior', _decode_navigation_behavior),
    0xebc3e775: ('motion_behavior', _decode_motion_behavior),
    0x65fc11ff: ('orientation_behavior', _decode_orientation_behavior),
    0xa7c38d: ('rotation_behavior', _decode_rotation_behavior),
    0xfc126ad1: ('field_of_view_behavior', _decode_field_of_view_behavior),
    0x764827d4: ('interpolation_behavior', _decode_interpolation_behavior),
    0x95d0d437: ('control_frame_interpolation', _decode_control_frame_interpolation),
}
