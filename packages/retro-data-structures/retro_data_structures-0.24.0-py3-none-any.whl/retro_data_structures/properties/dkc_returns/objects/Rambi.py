# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.KongData import KongData
from retro_data_structures.properties.dkc_returns.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.dkc_returns.archetypes.ShadowData import ShadowData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct import UnknownStruct


@dataclasses.dataclass()
class Rambi(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    shadow_data: ShadowData = dataclasses.field(default_factory=ShadowData)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_struct: UnknownStruct = dataclasses.field(default_factory=UnknownStruct)
    patterned_info: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    kong_data: KongData = dataclasses.field(default_factory=KongData)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'RMBI'

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x81\xc8>')  # 0xbf81c83e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shadow_data.to_stream(data)
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

        data.write(b'\x00c\xf68')  # 0x63f638
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xbb\xb1\xdd')  # 0x43bbb1dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_info.to_stream(data, default_override={'step_up_height': 0.25})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ot8\xcf')  # 0x6f7438cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_data.to_stream(data)
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
            shadow_data=ShadowData.from_json(data['shadow_data']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            unknown_struct=UnknownStruct.from_json(data['unknown_struct']),
            patterned_info=PatternedAITypedef.from_json(data['patterned_info']),
            kong_data=KongData.from_json(data['kong_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'shadow_data': self.shadow_data.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_struct': self.unknown_struct.to_json(),
            'patterned_info': self.patterned_info.to_json(),
            'kong_data': self.kong_data.to_json(),
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Rambi]:
    if property_count != 6:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbf81c83e
    shadow_data = ShadowData.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x7e397fed
    actor_information = ActorParameters.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x0063f638
    unknown_struct = UnknownStruct.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x43bbb1dd
    patterned_info = PatternedAITypedef.from_stream(data, property_size, default_override={'step_up_height': 0.25})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x6f7438cf
    kong_data = KongData.from_stream(data, property_size)

    return Rambi(editor_properties, shadow_data, actor_information, unknown_struct, patterned_info, kong_data)


_decode_editor_properties = EditorProperties.from_stream

_decode_shadow_data = ShadowData.from_stream

_decode_actor_information = ActorParameters.from_stream

_decode_unknown_struct = UnknownStruct.from_stream

def _decode_patterned_info(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'step_up_height': 0.25})


_decode_kong_data = KongData.from_stream

_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbf81c83e: ('shadow_data', _decode_shadow_data),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x63f638: ('unknown_struct', _decode_unknown_struct),
    0x43bbb1dd: ('patterned_info', _decode_patterned_info),
    0x6f7438cf: ('kong_data', _decode_kong_data),
}
