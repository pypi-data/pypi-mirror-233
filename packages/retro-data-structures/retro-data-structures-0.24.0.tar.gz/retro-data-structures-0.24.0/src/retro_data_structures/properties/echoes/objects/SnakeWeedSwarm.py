# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class SnakeWeedSwarm(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    density: float = dataclasses.field(default=1.0)
    max_depth: float = dataclasses.field(default=1.0)
    location_variance: float = dataclasses.field(default=0.5)
    detection_radius: float = dataclasses.field(default=4.0)
    grab_radius: float = dataclasses.field(default=1.0)
    unknown_0x723737bc: float = dataclasses.field(default=2.0)
    unknown_0x57452dd9: float = dataclasses.field(default=0.20000000298023224)
    retreat_depth: float = dataclasses.field(default=2.5)
    move_speed: float = dataclasses.field(default=1.5)
    unknown_0x11f854e2: float = dataclasses.field(default=3.0)
    max_slope: float = dataclasses.field(default=5.0)
    min_size: float = dataclasses.field(default=1.0)
    max_size: float = dataclasses.field(default=1.0)
    height_offset: float = dataclasses.field(default=0.0)
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_wait_time: float = dataclasses.field(default=0.0)
    sound_looped: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_into_ground: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_outof_ground: int = dataclasses.field(default=0, metadata={'sound': True})

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SNAK'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['SnakeWeedSwarm.rel']

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
        data.write(b'\x00\x16')  # 22 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2_\xb0\x8c')  # 0xe25fb08c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd\xe5\xfe\x9f')  # 0x64e5fe9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.density))

        data.write(b'#\xce\xf9_')  # 0x23cef95f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_depth))

        data.write(b'\xbe\x02\xe4V')  # 0xbe02e456
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.location_variance))

        data.write(b'!\xcd\xcf!')  # 0x21cdcf21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_radius))

        data.write(b'\x89fG#')  # 0x89664723
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_radius))

        data.write(b'r77\xbc')  # 0x723737bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x723737bc))

        data.write(b'WE-\xd9')  # 0x57452dd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x57452dd9))

        data.write(b'\\ \xb0\xc7')  # 0x5c20b0c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.retreat_depth))

        data.write(b'd\x97\xc7P')  # 0x6497c750
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_speed))

        data.write(b'\x11\xf8T\xe2')  # 0x11f854e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x11f854e2))

        data.write(b'\xa7U\xc1\xdf')  # 0xa755c1df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_slope))

        data.write(b'U\x8cm\xd7')  # 0x558c6dd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_size))

        data.write(b'\xc5\xff}=')  # 0xc5ff7d3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_size))

        data.write(b'\xb2\xeb\xc2:')  # 0xb2ebc23a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height_offset))

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data, default_override={'di_weapon_type': 9})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0\xcd\xc7\xe3')  # 0xe0cdc7e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_wait_time))

        data.write(b'\xcd}\x99n')  # 0xcd7d996e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_looped))

        data.write(b'\x10&\xdb\x89')  # 0x1026db89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_into_ground))

        data.write(b'\xcd\xe1sF')  # 0xcde17346
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_outof_ground))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            animation_information=AnimationParameters.from_json(data['animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            density=data['density'],
            max_depth=data['max_depth'],
            location_variance=data['location_variance'],
            detection_radius=data['detection_radius'],
            grab_radius=data['grab_radius'],
            unknown_0x723737bc=data['unknown_0x723737bc'],
            unknown_0x57452dd9=data['unknown_0x57452dd9'],
            retreat_depth=data['retreat_depth'],
            move_speed=data['move_speed'],
            unknown_0x11f854e2=data['unknown_0x11f854e2'],
            max_slope=data['max_slope'],
            min_size=data['min_size'],
            max_size=data['max_size'],
            height_offset=data['height_offset'],
            contact_damage=DamageInfo.from_json(data['contact_damage']),
            damage_wait_time=data['damage_wait_time'],
            sound_looped=data['sound_looped'],
            sound_into_ground=data['sound_into_ground'],
            sound_outof_ground=data['sound_outof_ground'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'animation_information': self.animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'density': self.density,
            'max_depth': self.max_depth,
            'location_variance': self.location_variance,
            'detection_radius': self.detection_radius,
            'grab_radius': self.grab_radius,
            'unknown_0x723737bc': self.unknown_0x723737bc,
            'unknown_0x57452dd9': self.unknown_0x57452dd9,
            'retreat_depth': self.retreat_depth,
            'move_speed': self.move_speed,
            'unknown_0x11f854e2': self.unknown_0x11f854e2,
            'max_slope': self.max_slope,
            'min_size': self.min_size,
            'max_size': self.max_size,
            'height_offset': self.height_offset,
            'contact_damage': self.contact_damage.to_json(),
            'damage_wait_time': self.damage_wait_time,
            'sound_looped': self.sound_looped,
            'sound_into_ground': self.sound_into_ground,
            'sound_outof_ground': self.sound_outof_ground,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_animation_information(self, asset_manager):
        yield from self.animation_information.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_contact_damage(self, asset_manager):
        yield from self.contact_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_looped(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_looped)

    def _dependencies_for_sound_into_ground(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_into_ground)

    def _dependencies_for_sound_outof_ground(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_outof_ground)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_animation_information, "animation_information", "AnimationParameters"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_contact_damage, "contact_damage", "DamageInfo"),
            (self._dependencies_for_sound_looped, "sound_looped", "int"),
            (self._dependencies_for_sound_into_ground, "sound_into_ground", "int"),
            (self._dependencies_for_sound_outof_ground, "sound_outof_ground", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SnakeWeedSwarm.{field_name} ({field_type}): {e}"
                )


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SnakeWeedSwarm]:
    if property_count != 22:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe25fb08c
    animation_information = AnimationParameters.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7e397fed
    actor_information = ActorParameters.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x64e5fe9f
    density = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x23cef95f
    max_depth = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbe02e456
    location_variance = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x21cdcf21
    detection_radius = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x89664723
    grab_radius = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x723737bc
    unknown_0x723737bc = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x57452dd9
    unknown_0x57452dd9 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5c20b0c7
    retreat_depth = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x6497c750
    move_speed = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x11f854e2
    unknown_0x11f854e2 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa755c1df
    max_slope = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x558c6dd7
    min_size = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc5ff7d3d
    max_size = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb2ebc23a
    height_offset = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd756416e
    contact_damage = DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 9})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe0cdc7e3
    damage_wait_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xcd7d996e
    sound_looped = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x1026db89
    sound_into_ground = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xcde17346
    sound_outof_ground = struct.unpack('>l', data.read(4))[0]

    return SnakeWeedSwarm(editor_properties, animation_information, actor_information, density, max_depth, location_variance, detection_radius, grab_radius, unknown_0x723737bc, unknown_0x57452dd9, retreat_depth, move_speed, unknown_0x11f854e2, max_slope, min_size, max_size, height_offset, contact_damage, damage_wait_time, sound_looped, sound_into_ground, sound_outof_ground)


_decode_editor_properties = EditorProperties.from_stream

_decode_animation_information = AnimationParameters.from_stream

_decode_actor_information = ActorParameters.from_stream

def _decode_density(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_depth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_location_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x723737bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x57452dd9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_retreat_depth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x11f854e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_slope(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 9})


def _decode_damage_wait_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_looped(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_into_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_outof_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe25fb08c: ('animation_information', _decode_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x64e5fe9f: ('density', _decode_density),
    0x23cef95f: ('max_depth', _decode_max_depth),
    0xbe02e456: ('location_variance', _decode_location_variance),
    0x21cdcf21: ('detection_radius', _decode_detection_radius),
    0x89664723: ('grab_radius', _decode_grab_radius),
    0x723737bc: ('unknown_0x723737bc', _decode_unknown_0x723737bc),
    0x57452dd9: ('unknown_0x57452dd9', _decode_unknown_0x57452dd9),
    0x5c20b0c7: ('retreat_depth', _decode_retreat_depth),
    0x6497c750: ('move_speed', _decode_move_speed),
    0x11f854e2: ('unknown_0x11f854e2', _decode_unknown_0x11f854e2),
    0xa755c1df: ('max_slope', _decode_max_slope),
    0x558c6dd7: ('min_size', _decode_min_size),
    0xc5ff7d3d: ('max_size', _decode_max_size),
    0xb2ebc23a: ('height_offset', _decode_height_offset),
    0xd756416e: ('contact_damage', _decode_contact_damage),
    0xe0cdc7e3: ('damage_wait_time', _decode_damage_wait_time),
    0xcd7d996e: ('sound_looped', _decode_sound_looped),
    0x1026db89: ('sound_into_ground', _decode_sound_into_ground),
    0xcde17346: ('sound_outof_ground', _decode_sound_outof_ground),
}
