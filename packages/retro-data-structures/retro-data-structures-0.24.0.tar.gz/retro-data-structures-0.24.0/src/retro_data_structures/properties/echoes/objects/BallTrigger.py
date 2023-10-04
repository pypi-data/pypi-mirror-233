# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.TriggerInfo import TriggerInfo
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class BallTrigger(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    trigger: TriggerInfo = dataclasses.field(default_factory=TriggerInfo)
    attraction_force: float = dataclasses.field(default=20.0)
    attraction_angle: float = dataclasses.field(default=60.0)
    attraction_distance: float = dataclasses.field(default=20.0)
    attraction_direction: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=0.0, z=0.0))
    no_ball_movement: bool = dataclasses.field(default=False)
    bounds_size_multiplier: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'BALT'

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
        num_properties_written = 7

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\xa2t\x11')  # 0x77a27411
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.trigger.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\x1b\x11I')  # 0xb61b1149
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attraction_force))

        data.write(b'\x81\xafQ\xd5')  # 0x81af51d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attraction_angle))

        data.write(b'\xbb8\xd0w')  # 0xbb38d077
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attraction_distance))

        data.write(b'\xeaQ\x1d\x83')  # 0xea511d83
        data.write(b'\x00\x0c')  # size
        self.attraction_direction.to_stream(data)

        data.write(b'\xb6\x13\xf4\xe4')  # 0xb613f4e4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.no_ball_movement))

        if self.bounds_size_multiplier != default_override.get('bounds_size_multiplier', 1.0):
            num_properties_written += 1
            data.write(b"'fcj")  # 0x2766636a
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.bounds_size_multiplier))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.write(struct.pack(">H", num_properties_written))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            trigger=TriggerInfo.from_json(data['trigger']),
            attraction_force=data['attraction_force'],
            attraction_angle=data['attraction_angle'],
            attraction_distance=data['attraction_distance'],
            attraction_direction=Vector.from_json(data['attraction_direction']),
            no_ball_movement=data['no_ball_movement'],
            bounds_size_multiplier=data['bounds_size_multiplier'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'trigger': self.trigger.to_json(),
            'attraction_force': self.attraction_force,
            'attraction_angle': self.attraction_angle,
            'attraction_distance': self.attraction_distance,
            'attraction_direction': self.attraction_direction.to_json(),
            'no_ball_movement': self.no_ball_movement,
            'bounds_size_multiplier': self.bounds_size_multiplier,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_trigger(self, asset_manager):
        yield from self.trigger.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_trigger, "trigger", "TriggerInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for BallTrigger.{field_name} ({field_type}): {e}"
                )


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[BallTrigger]:
    if property_count != 8:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x77a27411
    trigger = TriggerInfo.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb61b1149
    attraction_force = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x81af51d5
    attraction_angle = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbb38d077
    attraction_distance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xea511d83
    attraction_direction = Vector.from_stream(data)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb613f4e4
    no_ball_movement = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2766636a
    bounds_size_multiplier = struct.unpack('>f', data.read(4))[0]

    return BallTrigger(editor_properties, trigger, attraction_force, attraction_angle, attraction_distance, attraction_direction, no_ball_movement, bounds_size_multiplier)


_decode_editor_properties = EditorProperties.from_stream

_decode_trigger = TriggerInfo.from_stream

def _decode_attraction_force(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attraction_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attraction_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attraction_direction(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_no_ball_movement(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bounds_size_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x77a27411: ('trigger', _decode_trigger),
    0xb61b1149: ('attraction_force', _decode_attraction_force),
    0x81af51d5: ('attraction_angle', _decode_attraction_angle),
    0xbb38d077: ('attraction_distance', _decode_attraction_distance),
    0xea511d83: ('attraction_direction', _decode_attraction_direction),
    0xb613f4e4: ('no_ball_movement', _decode_no_ball_movement),
    0x2766636a: ('bounds_size_multiplier', _decode_bounds_size_multiplier),
}
