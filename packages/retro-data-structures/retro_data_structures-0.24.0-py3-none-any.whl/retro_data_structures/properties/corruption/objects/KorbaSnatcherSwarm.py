# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.KorbaSnatcherData import KorbaSnatcherData
from retro_data_structures.properties.corruption.archetypes.SwarmBasicsData import SwarmBasicsData
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class KorbaSnatcherSwarm(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    korba_snatcher_properties: KorbaSnatcherData = dataclasses.field(default_factory=KorbaSnatcherData)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    active: bool = dataclasses.field(default=True)
    swarm_basics_data: SwarmBasicsData = dataclasses.field(default_factory=SwarmBasicsData)
    unknown_0x92827035: float = dataclasses.field(default=0.44999998807907104)
    unknown_0xdc30cb20: int = dataclasses.field(default=0)
    unknown_0x48387110: int = dataclasses.field(default=0)
    unknown_0x5d054897: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'KRBA'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_KorbaMaw.rso']

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U\x06\tK')  # 0x5506094b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.korba_snatcher_properties.to_stream(data)
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

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xbb/E')  # 0xc6bb2f45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.active))

        data.write(b'L\xfcF\xfe')  # 0x4cfc46fe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swarm_basics_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x92\x82p5')  # 0x92827035
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x92827035))

        data.write(b'\xdc0\xcb ')  # 0xdc30cb20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xdc30cb20))

        data.write(b'H8q\x10')  # 0x48387110
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x48387110))

        data.write(b']\x05H\x97')  # 0x5d054897
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x5d054897))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            korba_snatcher_properties=KorbaSnatcherData.from_json(data['korba_snatcher_properties']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            active=data['active'],
            swarm_basics_data=SwarmBasicsData.from_json(data['swarm_basics_data']),
            unknown_0x92827035=data['unknown_0x92827035'],
            unknown_0xdc30cb20=data['unknown_0xdc30cb20'],
            unknown_0x48387110=data['unknown_0x48387110'],
            unknown_0x5d054897=data['unknown_0x5d054897'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'korba_snatcher_properties': self.korba_snatcher_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'character_animation_information': self.character_animation_information.to_json(),
            'active': self.active,
            'swarm_basics_data': self.swarm_basics_data.to_json(),
            'unknown_0x92827035': self.unknown_0x92827035,
            'unknown_0xdc30cb20': self.unknown_0xdc30cb20,
            'unknown_0x48387110': self.unknown_0x48387110,
            'unknown_0x5d054897': self.unknown_0x5d054897,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[KorbaSnatcherSwarm]:
    if property_count != 10:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5506094b
    korba_snatcher_properties = KorbaSnatcherData.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7e397fed
    actor_information = ActorParameters.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa244c9d8
    character_animation_information = AnimationParameters.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc6bb2f45
    active = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4cfc46fe
    swarm_basics_data = SwarmBasicsData.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x92827035
    unknown_0x92827035 = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xdc30cb20
    unknown_0xdc30cb20 = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x48387110
    unknown_0x48387110 = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5d054897
    unknown_0x5d054897 = struct.unpack('>l', data.read(4))[0]

    return KorbaSnatcherSwarm(editor_properties, korba_snatcher_properties, actor_information, character_animation_information, active, swarm_basics_data, unknown_0x92827035, unknown_0xdc30cb20, unknown_0x48387110, unknown_0x5d054897)


_decode_editor_properties = EditorProperties.from_stream

_decode_korba_snatcher_properties = KorbaSnatcherData.from_stream

_decode_actor_information = ActorParameters.from_stream

_decode_character_animation_information = AnimationParameters.from_stream

def _decode_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_decode_swarm_basics_data = SwarmBasicsData.from_stream

def _decode_unknown_0x92827035(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdc30cb20(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x48387110(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x5d054897(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x5506094b: ('korba_snatcher_properties', _decode_korba_snatcher_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xc6bb2f45: ('active', _decode_active),
    0x4cfc46fe: ('swarm_basics_data', _decode_swarm_basics_data),
    0x92827035: ('unknown_0x92827035', _decode_unknown_0x92827035),
    0xdc30cb20: ('unknown_0xdc30cb20', _decode_unknown_0xdc30cb20),
    0x48387110: ('unknown_0x48387110', _decode_unknown_0x48387110),
    0x5d054897: ('unknown_0x5d054897', _decode_unknown_0x5d054897),
}
