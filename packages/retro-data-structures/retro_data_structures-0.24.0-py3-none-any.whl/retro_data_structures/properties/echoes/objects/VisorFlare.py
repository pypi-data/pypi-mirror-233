# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.FlareDef import FlareDef


@dataclasses.dataclass()
class VisorFlare(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    blend_mode: int = dataclasses.field(default=0)
    constant_scale: bool = dataclasses.field(default=True)
    fade_time: float = dataclasses.field(default=0.10000000149011612)
    fade_factor: float = dataclasses.field(default=1.0)
    rotate_factor: float = dataclasses.field(default=2.0)
    combat_visor_mode: int = dataclasses.field(default=0)
    unknown: bool = dataclasses.field(default=True)
    no_occlusion_test: bool = dataclasses.field(default=False)
    flare1: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare2: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare3: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare4: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare5: FlareDef = dataclasses.field(default_factory=FlareDef)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FLAR'

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb\x13\xefF')  # 0xcb13ef46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.blend_mode))

        data.write(b'\xe0\xc5\xfc\x06')  # 0xe0c5fc06
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.constant_scale))

        data.write(b'\xd4\x12LL')  # 0xd4124c4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_time))

        data.write(b'\xd6\xfb1\xbf')  # 0xd6fb31bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_factor))

        data.write(b'1a\xf3\x8c')  # 0x3161f38c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotate_factor))

        data.write(b'C\xb5\x03\xa6')  # 0x43b503a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.combat_visor_mode))

        data.write(b'\xa5\x1f$>')  # 0xa51f243e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\x05\x08\x81\xa9')  # 0x50881a9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.no_occlusion_test))

        data.write(b'<%r#')  # 0x3c257223
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flare1.to_stream(data, default_override={'scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05\xa8N\xe6')  # 0x5a84ee6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flare2.to_stream(data, default_override={'position': 0.25, 'scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\xd3Z\xa5')  # 0x12d35aa5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flare3.to_stream(data, default_override={'position': 0.5, 'scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xb27l')  # 0x76b2376c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flare4.to_stream(data, default_override={'position': 0.75, 'scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\xc9#/')  # 0x61c9232f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flare5.to_stream(data, default_override={'position': 1.0, 'scale': 1.0})
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
            blend_mode=data['blend_mode'],
            constant_scale=data['constant_scale'],
            fade_time=data['fade_time'],
            fade_factor=data['fade_factor'],
            rotate_factor=data['rotate_factor'],
            combat_visor_mode=data['combat_visor_mode'],
            unknown=data['unknown'],
            no_occlusion_test=data['no_occlusion_test'],
            flare1=FlareDef.from_json(data['flare1']),
            flare2=FlareDef.from_json(data['flare2']),
            flare3=FlareDef.from_json(data['flare3']),
            flare4=FlareDef.from_json(data['flare4']),
            flare5=FlareDef.from_json(data['flare5']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'blend_mode': self.blend_mode,
            'constant_scale': self.constant_scale,
            'fade_time': self.fade_time,
            'fade_factor': self.fade_factor,
            'rotate_factor': self.rotate_factor,
            'combat_visor_mode': self.combat_visor_mode,
            'unknown': self.unknown,
            'no_occlusion_test': self.no_occlusion_test,
            'flare1': self.flare1.to_json(),
            'flare2': self.flare2.to_json(),
            'flare3': self.flare3.to_json(),
            'flare4': self.flare4.to_json(),
            'flare5': self.flare5.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_flare1(self, asset_manager):
        yield from self.flare1.dependencies_for(asset_manager)

    def _dependencies_for_flare2(self, asset_manager):
        yield from self.flare2.dependencies_for(asset_manager)

    def _dependencies_for_flare3(self, asset_manager):
        yield from self.flare3.dependencies_for(asset_manager)

    def _dependencies_for_flare4(self, asset_manager):
        yield from self.flare4.dependencies_for(asset_manager)

    def _dependencies_for_flare5(self, asset_manager):
        yield from self.flare5.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_flare1, "flare1", "FlareDef"),
            (self._dependencies_for_flare2, "flare2", "FlareDef"),
            (self._dependencies_for_flare3, "flare3", "FlareDef"),
            (self._dependencies_for_flare4, "flare4", "FlareDef"),
            (self._dependencies_for_flare5, "flare5", "FlareDef"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for VisorFlare.{field_name} ({field_type}): {e}"
                )


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[VisorFlare]:
    if property_count != 14:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x255a4580
    editor_properties = EditorProperties.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xcb13ef46
    blend_mode = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe0c5fc06
    constant_scale = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd4124c4c
    fade_time = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd6fb31bf
    fade_factor = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3161f38c
    rotate_factor = struct.unpack('>f', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x43b503a6
    combat_visor_mode = struct.unpack('>l', data.read(4))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa51f243e
    unknown = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x050881a9
    no_occlusion_test = struct.unpack('>?', data.read(1))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3c257223
    flare1 = FlareDef.from_stream(data, property_size, default_override={'scale': 1.0})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x05a84ee6
    flare2 = FlareDef.from_stream(data, property_size, default_override={'position': 0.25, 'scale': 1.0})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x12d35aa5
    flare3 = FlareDef.from_stream(data, property_size, default_override={'position': 0.5, 'scale': 1.0})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x76b2376c
    flare4 = FlareDef.from_stream(data, property_size, default_override={'position': 0.75, 'scale': 1.0})

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x61c9232f
    flare5 = FlareDef.from_stream(data, property_size, default_override={'position': 1.0, 'scale': 1.0})

    return VisorFlare(editor_properties, blend_mode, constant_scale, fade_time, fade_factor, rotate_factor, combat_visor_mode, unknown, no_occlusion_test, flare1, flare2, flare3, flare4, flare5)


_decode_editor_properties = EditorProperties.from_stream

def _decode_blend_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_constant_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotate_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_combat_visor_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_no_occlusion_test(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_flare1(data: typing.BinaryIO, property_size: int):
    return FlareDef.from_stream(data, property_size, default_override={'scale': 1.0})


def _decode_flare2(data: typing.BinaryIO, property_size: int):
    return FlareDef.from_stream(data, property_size, default_override={'position': 0.25, 'scale': 1.0})


def _decode_flare3(data: typing.BinaryIO, property_size: int):
    return FlareDef.from_stream(data, property_size, default_override={'position': 0.5, 'scale': 1.0})


def _decode_flare4(data: typing.BinaryIO, property_size: int):
    return FlareDef.from_stream(data, property_size, default_override={'position': 0.75, 'scale': 1.0})


def _decode_flare5(data: typing.BinaryIO, property_size: int):
    return FlareDef.from_stream(data, property_size, default_override={'position': 1.0, 'scale': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xcb13ef46: ('blend_mode', _decode_blend_mode),
    0xe0c5fc06: ('constant_scale', _decode_constant_scale),
    0xd4124c4c: ('fade_time', _decode_fade_time),
    0xd6fb31bf: ('fade_factor', _decode_fade_factor),
    0x3161f38c: ('rotate_factor', _decode_rotate_factor),
    0x43b503a6: ('combat_visor_mode', _decode_combat_visor_mode),
    0xa51f243e: ('unknown', _decode_unknown),
    0x50881a9: ('no_occlusion_test', _decode_no_occlusion_test),
    0x3c257223: ('flare1', _decode_flare1),
    0x5a84ee6: ('flare2', _decode_flare2),
    0x12d35aa5: ('flare3', _decode_flare3),
    0x76b2376c: ('flare4', _decode_flare4),
    0x61c9232f: ('flare5', _decode_flare5),
}
