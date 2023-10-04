# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.echoes as enums
from retro_data_structures.properties.echoes.archetypes.ConditionalTest import ConditionalTest
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class ConditionalRelay(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    trigger_on_first_think: bool = dataclasses.field(default=False)
    multiplayer_mask_and_negate: int = dataclasses.field(default=7680)
    conditional1: ConditionalTest = dataclasses.field(default_factory=ConditionalTest)
    conditional2: ConditionalTest = dataclasses.field(default_factory=ConditionalTest)
    conditional3: ConditionalTest = dataclasses.field(default_factory=ConditionalTest)
    conditional4: ConditionalTest = dataclasses.field(default_factory=ConditionalTest)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CRLY'

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

        data.write(b'D\xdb\x8a\xf2')  # 0x44db8af2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.trigger_on_first_think))

        data.write(b',\xc5Nw')  # 0x2cc54e77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.multiplayer_mask_and_negate))

        data.write(b'\xce\xc1i2')  # 0xcec16932
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.conditional1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\t\xdd\xc0')  # 0xe709ddc0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.conditional2.to_stream(data, default_override={'boolean': enums.Boolean.Unknown})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'IaLQ')  # 0x49614c51
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.conditional3.to_stream(data, default_override={'boolean': enums.Boolean.Unknown})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4\x98\xb4$')  # 0xb498b424
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.conditional4.to_stream(data, default_override={'boolean': enums.Boolean.Unknown})
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
            trigger_on_first_think=data['trigger_on_first_think'],
            multiplayer_mask_and_negate=data['multiplayer_mask_and_negate'],
            conditional1=ConditionalTest.from_json(data['conditional1']),
            conditional2=ConditionalTest.from_json(data['conditional2']),
            conditional3=ConditionalTest.from_json(data['conditional3']),
            conditional4=ConditionalTest.from_json(data['conditional4']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'trigger_on_first_think': self.trigger_on_first_think,
            'multiplayer_mask_and_negate': self.multiplayer_mask_and_negate,
            'conditional1': self.conditional1.to_json(),
            'conditional2': self.conditional2.to_json(),
            'conditional3': self.conditional3.to_json(),
            'conditional4': self.conditional4.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_conditional1(self, asset_manager):
        yield from self.conditional1.dependencies_for(asset_manager)

    def _dependencies_for_conditional2(self, asset_manager):
        yield from self.conditional2.dependencies_for(asset_manager)

    def _dependencies_for_conditional3(self, asset_manager):
        yield from self.conditional3.dependencies_for(asset_manager)

    def _dependencies_for_conditional4(self, asset_manager):
        yield from self.conditional4.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_conditional1, "conditional1", "ConditionalTest"),
            (self._dependencies_for_conditional2, "conditional2", "ConditionalTest"),
            (self._dependencies_for_conditional3, "conditional3", "ConditionalTest"),
            (self._dependencies_for_conditional4, "conditional4", "ConditionalTest"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ConditionalRelay.{field_name} ({field_type}): {e}"
                )


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ConditionalRelay]:
    if property_count != 7:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x44db8af2
    trigger_on_first_think = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2cc54e77
    multiplayer_mask_and_negate = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xcec16932
    conditional1 = ConditionalTest.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe709ddc0
    conditional2 = ConditionalTest.from_stream(data, property_size, default_override={'boolean': enums.Boolean.Unknown})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x49614c51
    conditional3 = ConditionalTest.from_stream(data, property_size, default_override={'boolean': enums.Boolean.Unknown})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xb498b424
    conditional4 = ConditionalTest.from_stream(data, property_size, default_override={'boolean': enums.Boolean.Unknown})

    return ConditionalRelay(editor_properties, trigger_on_first_think, multiplayer_mask_and_negate, conditional1, conditional2, conditional3, conditional4)


_decode_editor_properties = EditorProperties.from_stream

def _decode_trigger_on_first_think(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_multiplayer_mask_and_negate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_decode_conditional1 = ConditionalTest.from_stream

def _decode_conditional2(data: typing.BinaryIO, property_size: int):
    return ConditionalTest.from_stream(data, property_size, default_override={'boolean': enums.Boolean.Unknown})


def _decode_conditional3(data: typing.BinaryIO, property_size: int):
    return ConditionalTest.from_stream(data, property_size, default_override={'boolean': enums.Boolean.Unknown})


def _decode_conditional4(data: typing.BinaryIO, property_size: int):
    return ConditionalTest.from_stream(data, property_size, default_override={'boolean': enums.Boolean.Unknown})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x44db8af2: ('trigger_on_first_think', _decode_trigger_on_first_think),
    0x2cc54e77: ('multiplayer_mask_and_negate', _decode_multiplayer_mask_and_negate),
    0xcec16932: ('conditional1', _decode_conditional1),
    0xe709ddc0: ('conditional2', _decode_conditional2),
    0x49614c51: ('conditional3', _decode_conditional3),
    0xb498b424: ('conditional4', _decode_conditional4),
}
