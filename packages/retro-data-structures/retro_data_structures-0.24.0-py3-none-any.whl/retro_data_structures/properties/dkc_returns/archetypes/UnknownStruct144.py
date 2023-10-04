# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct144(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    title: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    how_to: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    movement: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    grab: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    jump: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    pause: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    crouch: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    ground_pound: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    blow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    roll: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    mount: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    dismount: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    blow_input: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    crouch_input: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    roll_input: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    mount_input: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    dismount_input: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    text_background: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x16')  # 22 properties

        data.write(b'0[22')  # 0x305b3232
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'^\xe2\xdbK')  # 0x5ee2db4b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.how_to))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\xcb%\xf1W')  # 0xcb25f157
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.movement))

        data.write(b'\xe1\x00W3')  # 0xe1005733
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.grab))

        data.write(b'\x934p\x99')  # 0x93347099
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jump))

        data.write(b'K\xfd\xe2\xcc')  # 0x4bfde2cc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pause))

        data.write(b'\xd4p\xc3\xd7')  # 0xd470c3d7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.crouch))

        data.write(b'`\xfa\xff\x80')  # 0x60faff80
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ground_pound))

        data.write(b'\xc1\x82\xd9\x10')  # 0xc182d910
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.blow))

        data.write(b'\xbb4tG')  # 0xbb347447
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.roll))

        data.write(b'\x9f\xec\x1f6')  # 0x9fec1f36
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.mount))

        data.write(b'\x93@\xabD')  # 0x9340ab44
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dismount))

        data.write(b"'5\x98\x1e")  # 0x2735981e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.blow_input))

        data.write(b'\x9e\x94\xfb\xac')  # 0x9e94fbac
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xc2QZ\x84')  # 0xc2515a84
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.crouch_input))

        data.write(b'\x06\x04Y\xc3')  # 0x60459c3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.roll_input))

        data.write(b'\\\xe3e\x90')  # 0x5ce36590
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.mount_input))

        data.write(b'16\xe4\xfa')  # 0x3136e4fa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dismount_input))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            title=data['title'],
            how_to=data['how_to'],
            back=data['back'],
            back_core=data['back_core'],
            movement=data['movement'],
            grab=data['grab'],
            jump=data['jump'],
            pause=data['pause'],
            crouch=data['crouch'],
            ground_pound=data['ground_pound'],
            blow=data['blow'],
            roll=data['roll'],
            mount=data['mount'],
            dismount=data['dismount'],
            blow_input=data['blow_input'],
            strg=data['strg'],
            crouch_input=data['crouch_input'],
            roll_input=data['roll_input'],
            mount_input=data['mount_input'],
            dismount_input=data['dismount_input'],
            text_background=data['text_background'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title': self.title,
            'how_to': self.how_to,
            'back': self.back,
            'back_core': self.back_core,
            'movement': self.movement,
            'grab': self.grab,
            'jump': self.jump,
            'pause': self.pause,
            'crouch': self.crouch,
            'ground_pound': self.ground_pound,
            'blow': self.blow,
            'roll': self.roll,
            'mount': self.mount,
            'dismount': self.dismount,
            'blow_input': self.blow_input,
            'strg': self.strg,
            'crouch_input': self.crouch_input,
            'roll_input': self.roll_input,
            'mount_input': self.mount_input,
            'dismount_input': self.dismount_input,
            'text_background': self.text_background,
        }


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct144]:
    if property_count != 22:
        return None

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x305b3232
    unknown_struct29 = UnknownStruct29.from_stream(data, property_size)

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xa4f20c17
    title = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5ee2db4b
    how_to = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe9336455
    back = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x770bcd3b
    back_core = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xcb25f157
    movement = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe1005733
    grab = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x93347099
    jump = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x4bfde2cc
    pause = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xd470c3d7
    crouch = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x60faff80
    ground_pound = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc182d910
    blow = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xbb347447
    roll = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9fec1f36
    mount = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9340ab44
    dismount = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x2735981e
    blow_input = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x9e94fbac
    strg = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xc2515a84
    crouch_input = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x060459c3
    roll_input = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x5ce36590
    mount_input = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0x3136e4fa
    dismount_input = struct.unpack(">Q", data.read(8))[0]

    property_id, property_size = struct.unpack(">LH", data.read(6))
    assert property_id == 0xe119319b
    text_background = struct.unpack(">Q", data.read(8))[0]

    return UnknownStruct144(unknown_struct29, title, how_to, back, back_core, movement, grab, jump, pause, crouch, ground_pound, blow, roll, mount, dismount, blow_input, strg, crouch_input, roll_input, mount_input, dismount_input, text_background)


_decode_unknown_struct29 = UnknownStruct29.from_stream

def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_how_to(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_movement(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_grab(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_pause(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_crouch(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_blow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_roll(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_mount(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dismount(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_blow_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_crouch_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_roll_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_mount_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dismount_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', _decode_unknown_struct29),
    0xa4f20c17: ('title', _decode_title),
    0x5ee2db4b: ('how_to', _decode_how_to),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0xcb25f157: ('movement', _decode_movement),
    0xe1005733: ('grab', _decode_grab),
    0x93347099: ('jump', _decode_jump),
    0x4bfde2cc: ('pause', _decode_pause),
    0xd470c3d7: ('crouch', _decode_crouch),
    0x60faff80: ('ground_pound', _decode_ground_pound),
    0xc182d910: ('blow', _decode_blow),
    0xbb347447: ('roll', _decode_roll),
    0x9fec1f36: ('mount', _decode_mount),
    0x9340ab44: ('dismount', _decode_dismount),
    0x2735981e: ('blow_input', _decode_blow_input),
    0x9e94fbac: ('strg', _decode_strg),
    0xc2515a84: ('crouch_input', _decode_crouch_input),
    0x60459c3: ('roll_input', _decode_roll_input),
    0x5ce36590: ('mount_input', _decode_mount_input),
    0x3136e4fa: ('dismount_input', _decode_dismount_input),
    0xe119319b: ('text_background', _decode_text_background),
}
