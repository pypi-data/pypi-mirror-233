from __future__ import annotations

import collections
import dataclasses
import keyword
import logging
import re
import struct
import typing
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import inflection

# ruff: noqa: E501
# ruff: noqa: C901
# ruff: noqa: PLR0912  lots of branches
# ruff: noqa: PLR0915  lots of statements
# ruff: noqa: PLW0603  we use globals here

rds_root = Path(__file__).parent.joinpath("src", "retro_data_structures")
FAST_DECODE_ASSERT = True  # fast import will assert the ids are in the correct order instead of failing if not

_game_id_to_file = {
    "Prime": "prime",
    "Echoes": "echoes",
    "Corruption": "corruption",
    "DKCReturns": "dkc_returns",
    "PrimeRemastered": "prime_remastered",
}
_game_id_to_enum = {
    "Prime": "PRIME",
    "Echoes": "ECHOES",
    "Corruption": "CORRUPTION",
    "DKCReturns": "DKC_RETURNS",
    "PrimeRemastered": "PRIME_REMASTER",
}

_CODE_PARSE_UINT16 = {
    ">": 'struct.unpack(">H", data.read(2))[0]',
    "<": 'struct.unpack("<H", data.read(2))[0]',
}
_CODE_PARSE_UINT32 = {
    ">": 'struct.unpack(">L", data.read(4))[0]',
    "<": 'struct.unpack("<L", data.read(4))[0]',
}


def get_endianness(game_id):
    return ">" if game_id != "PrimeRemastered" else "<"


@dataclasses.dataclass(frozen=True)
class EnumDefinition:
    name: str
    values: dict[str, typing.Any]
    enum_base: str = "Enum"


_enums_by_game: dict[str, list[EnumDefinition]] = {}


def _scrub_enum(string: str):
    s = re.sub(r"\W", "", string)  # remove non-word characters
    s = re.sub(r"^(?=\d)", "_", s)  # add leading underscore to strings starting with a number
    s = re.sub(r"^None$", "_None", s)  # add leading underscore to None
    s = s or "_EMPTY"  # add name for empty string keys
    return s


def create_enums_file(game_id: str, enums: list[EnumDefinition]):
    code = '"""\nGenerated file.\n"""\nimport enum\nimport typing\nimport struct\n'
    endianness = get_endianness(game_id)

    for e in enums:
        code += f"\n\nclass {_scrub_enum(e.name)}(enum.{e.enum_base}):\n"
        for name, value in e.values.items():
            code += f"    {_scrub_enum(name)} = {value}\n"

        code += "\n    @classmethod\n"
        code += "    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):\n"
        code += f"        return cls({_CODE_PARSE_UINT32[endianness]})\n"

        code += "\n    def to_stream(self, data: typing.BinaryIO):\n"
        code += '        data.write(struct.pack("' + endianness + 'L", self.value))\n'

        code += "\n    @classmethod\n"
        code += "    def from_json(cls, data):\n"
        code += "        return cls(data)\n"

        code += "\n    def to_json(self):\n"
        code += "        return self.value\n"

    return code


def _prop_default_value(element: Element, game_id: str, path: Path) -> dict:
    default_value_types = {
        "Int": lambda el: struct.unpack("l", struct.pack("L", (int(el.text, 10) & 0xFFFFFFFF)))[0],
        "Float": lambda el: float(el.text),
        "Bool": lambda el: el.text == "true",
        "Short": lambda el: int(el.text, 10) & 0xFFFF,
        "Color": lambda el: {e.tag: float(e.text) for e in el},
        "Vector": lambda el: {e.tag: float(e.text) for e in el},
        "Flags": lambda el: int(el.text, 10) & 0xFFFFFFFF,
        "Choice": lambda el: int(el.text, 10) & 0xFFFFFFFF,
        "Enum": lambda el: int(el.text, 16) & 0xFFFFFFFF,
        "Sound": lambda el: int(el.text, 10) & 0xFFFFFFFF,
    }

    default_value = None
    has_default = False
    if (default_value_element := element.find("DefaultValue")) is not None:
        default_value = default_value_types.get(element.attrib["Type"], lambda el: el.text)(default_value_element)
        has_default = True
    return {"has_default": has_default, "default_value": default_value}


def _prop_struct(element: Element, game_id: str, path: Path) -> dict:
    return {
        "archetype": element.attrib.get("Archetype"),
        "properties": _parse_properties(element, game_id, path)["properties"],
    }


def _prop_asset(element: Element, game_id: str, path: Path) -> dict:
    type_filter = []
    if element.find("TypeFilter"):
        type_filter = [t.text for t in element.find("TypeFilter")]
    return {"type_filter": type_filter}


def _prop_array(element: Element, game_id: str, path: Path) -> dict:
    # print(ElementTree.tostring(element, encoding='utf8', method='xml'))
    item_archetype = None
    if (item_archetype_element := element.find("ItemArchetype")) is not None:
        item_archetype = _parse_single_property(item_archetype_element, game_id, path, include_id=False)
    # print(item_archetype)
    return {"item_archetype": item_archetype}


def _prop_choice(element: Element, game_id: str, path: Path) -> dict:
    _parse_choice(element, game_id, path)
    extras = {"archetype": element.attrib.get("Archetype")}
    extras.update(_prop_default_value(element, game_id, path))
    return extras


def _prop_flags(element: Element, game_id: str, path: Path) -> dict:
    extras = _prop_default_value(element, game_id, path)
    if (flags_element := element.find("Flags")) is not None:
        extras["flags"] = {
            element.attrib["Name"]: int(element.attrib["Mask"], 16) for element in flags_element.findall("Element")
        }

        name = None
        if element.find("Name") is not None:
            name = element.find("Name").text
        elif element.attrib.get("ID"):
            name = property_names.get(int(element.attrib.get("ID"), 16))

        if name == "Unknown" and element.attrib.get("ID"):
            name += f'_{element.attrib.get("ID")}'

        _enums_by_game[game_id].append(EnumDefinition(name, extras["flags"], enum_base="IntFlag"))
        extras["flagset_name"] = name

    return extras


def _parse_single_property(element: Element, game_id: str, path: Path, include_id: bool = True) -> dict:
    parsed = {}
    if include_id:
        parsed.update({"id": int(element.attrib["ID"], 16)})

    if (name := element.attrib.get("Name", "")) == "":
        name_element = element.find("Name")
        name = name_element.text if name_element is not None and name_element.text is not None else ""

    cook = element.find("CookPreference")

    parsed.update(
        {
            "type": element.attrib["Type"],
            "name": name,
            "cook_preference": cook.text if cook is not None and cook.text is not None else "Always",
        }
    )

    ignore_dependencies_mlvl = element.attrib.get("IgnoreDependenciesMlvl", "False")
    ignore_dependencies_mlvl = ignore_dependencies_mlvl.lower() != "false"
    if ignore_dependencies_mlvl:
        parsed["ignore_dependencies_mlvl"] = True

    property_type_extras = {
        "Struct": _prop_struct,
        "Asset": _prop_asset,
        "Array": _prop_array,
        "Enum": _prop_choice,
        "Choice": _prop_choice,
        "Flags": _prop_flags,
    }

    parsed.update(property_type_extras.get(element.attrib["Type"], _prop_default_value)(element, game_id, path))

    return parsed


def _parse_properties(properties: Element, game_id: str, path: Path) -> dict:
    elements = []
    if (sub_properties := properties.find("SubProperties")) is not None:
        for element in sub_properties:
            element = typing.cast(Element, element)

            elements.append(_parse_single_property(element, game_id, path))

    return {
        "type": "Struct",
        "name": properties.find("Name").text if properties.find("Name") is not None else "",
        "atomic": properties.find("Atomic") is not None,
        "incomplete": properties.attrib.get("Incomplete") == "true",
        "properties": elements,
    }


def _parse_choice(properties: Element, game_id: str, path: Path) -> dict:
    _type = properties.attrib.get("Type", "Choice")
    choices = {}

    if (values := properties.find("Values")) is not None:
        for element in values:
            element = typing.cast(Element, element)
            choices[element.attrib["Name"]] = int(element.attrib["ID"], 16)

        name = ""
        if properties.find("Name") is not None:
            name = properties.find("Name").text
        elif properties.attrib.get("ID"):
            name = property_names.get(int(properties.attrib.get("ID"), 16), path.stem + properties.attrib.get("ID"))
        else:
            return {
                "type": _type,
                "choices": choices,
            }

        _enums_by_game[game_id].append(EnumDefinition(name, choices, enum_base="IntEnum"))

    return {
        "type": _type,
    }


_parse_choice.unknowns = {}


def parse_script_object_file(path: Path, game_id: str) -> dict:
    t = ElementTree.parse(path)
    root = t.getroot()
    result = _parse_properties(root.find("Properties"), game_id, path)

    if modules := root.find("Modules"):
        result["modules"] = [item.text for item in modules.findall("Element")]

    return result


def parse_property_archetypes(path: Path, game_id: str) -> dict:
    t = ElementTree.parse(path)
    root = t.getroot()
    archetype = root.find("PropertyArchetype")
    _type = archetype.attrib["Type"]
    if _type == "Struct":
        return _parse_properties(archetype, game_id, path)
    elif _type in {"Choice", "Enum"}:
        return _parse_choice(archetype, game_id, path)
    else:
        raise ValueError(f"Unknown Archetype format: {_type}")


property_names: dict[int, str] = {}


def read_property_names(map_path: Path):
    global property_names

    t = ElementTree.parse(map_path)
    root = t.getroot()
    m = root.find("PropertyMap")

    property_names = {
        int(item.find("Key").attrib["ID"], 16): item.find("Value").attrib["Name"]
        for item in typing.cast(typing.Iterable[Element], m)
    }

    return property_names


def get_paths(elements: typing.Iterable[Element]) -> dict[str, str]:
    return {item.find("Key").text: item.find("Value").attrib["Path"] for item in elements}


def get_key_map(elements: typing.Iterable[Element]) -> dict[str, str]:
    return {item.find("Key").text: item.find("Value").text for item in elements}


_to_snake_case_re = re.compile(r"(?<!^)(?=[A-Z])")
_invalid_chars_table = str.maketrans("", "", "()?'")
_to_underscore_table = str.maketrans("/ ", "__")


def _filter_property_name(n: str) -> str:
    result = (
        inflection.underscore(n.translate(_to_underscore_table).replace("#", "Number"))
        .translate(_invalid_chars_table)
        .lower()
    )
    if keyword.iskeyword(result):
        result += "_"
    return result


def _ensure_is_generated_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    path.joinpath(".gitignore").write_text("*")
    init = path.joinpath("__init__.py")
    if not init.is_file():
        init.write_text("")


def _fix_module_name(output_path: Path, class_path: str):
    # We created a nested module, but there was already a class with that name.
    rename_root = output_path
    for part in class_path.split("/")[:-1]:
        nested_dir = rename_root.joinpath(part)
        maybe_file = rename_root.joinpath(part + ".py")

        _ensure_is_generated_dir(nested_dir)
        if maybe_file.is_file():
            maybe_file.replace(rename_root.joinpath(part, "__init__.py"))
        rename_root = nested_dir


@dataclasses.dataclass
class PropDetails:
    raw: dict
    prop_type: str
    need_enums: bool
    comment: str | None
    parse_code: str
    build_code: list[str]
    from_json_code: str
    to_json_code: str
    custom_cook_pref: bool
    known_size: int | None
    meta: dict
    needed_imports: dict[str, str]
    format_specifier: str | None
    dependency_code: str | None

    @property
    def id(self):
        return self.raw["id"]


def _get_default(meta: dict) -> str:
    if "default" in meta:
        default_value = meta["default"]
    else:
        default_value: str = meta["default_factory"]
        if default_value.startswith("lambda: "):
            default_value = default_value[len("lambda: ") :]
        else:
            default_value += "()"
    return default_value


@dataclasses.dataclass
class ClassDefinition:
    game_id: str
    raw_name: str
    raw_def: dict
    class_name: str
    class_path: str
    is_struct: bool
    is_incomplete: bool

    class_code: str = ""
    after_class_code: str = ""
    properties_builder: str = ""
    property_count: int = 0
    modules: list[str] = dataclasses.field(default_factory=list)

    all_props: dict[str, PropDetails] = dataclasses.field(default_factory=dict)
    needed_imports: dict = dataclasses.field(default_factory=dict)
    need_enums: bool = False
    has_custom_cook_pref: bool = False

    @property
    def atomic(self) -> bool:
        return self.raw_def["atomic"]

    def add_prop(self, prop: PropDetails, prop_name: str):
        self.all_props[prop_name] = prop
        self.need_enums = self.need_enums or prop.need_enums
        self.has_custom_cook_pref = self.has_custom_cook_pref or prop.custom_cook_pref
        endianness = get_endianness(self.game_id)

        self.needed_imports.update(prop.needed_imports)

        if prop.prop_type is None:
            raise ValueError(f"Unable to parse property {prop_name} of {self.raw_name}")

        self.class_code += f"    {prop_name}: {prop.prop_type}"
        if prop.meta:
            self.class_code += " = dataclasses.field({})".format(
                ", ".join(f"{key}={value}" for key, value in prop.meta.items())
            )

        if prop.comment is not None:
            self.class_code += f"  # {prop.comment}"
        self.class_code += "\n"

        if self.atomic or self.game_id == "Prime":
            pass
            # self.properties_builder is handled in write_to_stream
        else:
            # build
            prop_id_bytes = struct.pack(endianness + "L", prop.id)
            self.properties_builder += "\n"
            build_prop = [f"data.write({repr(prop_id_bytes)})  # {hex(prop.id)}"]

            if prop.known_size is not None:
                placeholder = repr(struct.pack(endianness + "H", prop.known_size))
                build_prop.append(f"data.write({placeholder})  # size")
            else:
                placeholder = repr(b"\x00\x00")
                build_prop.append("before = data.tell()")
                build_prop.append(f"data.write({placeholder})  # size placeholder")

            for build in prop.build_code:
                build_prop.append(build.replace("{obj}", f"self.{prop_name}"))

            if prop.known_size is None:
                build_prop.append("after = data.tell()")
                build_prop.append("data.seek(before)")
                build_prop.append(f'data.write(struct.pack("{endianness}H", after - before - 2))')
                build_prop.append("data.seek(after)")

            if not prop.custom_cook_pref:
                build_prop = [f"        {text}" for text in build_prop]
                self.property_count += 1

            elif prop.raw["cook_preference"] == "Never":
                build_prop = []

            else:
                default_value = _get_default(prop.meta)

                if prop.raw["cook_preference"] == "Default":
                    self.properties_builder += f"        self.{prop_name} = default_override.get({repr(prop_name)}, {default_value})  # Cooks with Default\n"
                    build_prop = [f"        {text}" for text in build_prop]
                    self.property_count += 1

                elif prop.raw["cook_preference"] == "OnlyIfModified":
                    self.properties_builder += (
                        f"        if self.{prop_name} != default_override.get({repr(prop_name)}, {default_value}):\n"
                    )
                    self.properties_builder += "            num_properties_written += 1\n"
                    build_prop = [f"            {text}" for text in build_prop]

                else:
                    raise ValueError(f"Unknown cook preference: {prop.raw['cook_preference']}")

            self.properties_builder += "\n".join(build_prop)
            self.properties_builder += "\n"

    def finalize_props(self):
        if self.keep_unknown_properties():
            self.class_code += "    unknown_properties: dict[int, bytes] = dataclasses.field(default_factory=dict)\n"

    def keep_unknown_properties(self):
        return self.is_incomplete

    def _can_fast_decode(self) -> bool:
        return all(prop.format_specifier is not None for prop in self.all_props.values())

    def _create_fast_decode_body(self):
        num_props = len(self.all_props)
        ids = [hex(prop.id) for prop in self.all_props.values()]
        big_format = get_endianness(self.game_id) + "".join(
            f"LH{prop.format_specifier}" for prop in self.all_props.values()
        )
        yield "_FAST_FORMAT = None"
        yield f"_FAST_IDS = ({', '.join(ids)})"
        yield ""
        yield ""

        yield f"def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[{self.class_name}]:"
        yield f"    if property_count != {num_props}:"
        yield "        return None"
        yield ""
        yield "    global _FAST_FORMAT"
        yield "    if _FAST_FORMAT is None:"
        yield f"        _FAST_FORMAT = struct.Struct({repr(big_format)})"
        yield ""

        if not FAST_DECODE_ASSERT:
            yield "    before = data.tell()"
        yield f"    dec = _FAST_FORMAT.unpack(data.read({struct.calcsize(big_format)}))"

        fast_check = []
        ret_state = [f"    return {self.class_name}("]

        offset = 0
        for prop in self.all_props.values():
            fast_check.append(f"dec[{offset}]")

            offset += 2  # prop id + size
            if len(prop.format_specifier) == 1:
                value = f"dec[{offset}]"
                if prop.prop_type.startswith("enums."):
                    st = f"        {prop.prop_type}({value}),"
                else:
                    st = f"        {value},"
            else:
                st = f"        {prop.prop_type}(*dec[{offset}:{offset + len(prop.format_specifier)}]),"

            ret_state.append(st)
            offset += len(prop.format_specifier)

        if FAST_DECODE_ASSERT:
            yield f"    assert ({', '.join(fast_check)}) == _FAST_IDS"
        else:
            yield f"    if ({', '.join(fast_check)}) != _FAST_IDS:"
            yield "        data.seek(before)"
            yield "        return None"
            yield ""

        yield from ret_state
        yield "    )"

    def _create_simple_decode_body(self):
        num_props = len(self.all_props)
        endianness = get_endianness(self.game_id)
        [hex(prop.id) for prop in self.all_props.values()]

        yield f"def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[{self.class_name}]:"
        yield f"    if property_count != {num_props}:"
        yield "        return None"
        yield ""

        for prop_name, prop in self.all_props.items():
            # yield "    data.read(6)"  # TODO: assert correct
            yield f'    property_id, property_size = struct.unpack("{endianness}LH", data.read(6))'
            yield f"    assert property_id == 0x{prop.id:08x}"
            yield f"    {prop_name} = {prop.parse_code}"
            yield ""

        all_fields = ", ".join(self.all_props.keys())
        yield f"    return {self.class_name}({all_fields})"

    def write_from_stream(self):
        game_id = self.game_id
        endianness = get_endianness(game_id)

        self.class_code += """
    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
"""
        if self.atomic or game_id == "Prime":
            self.class_code += "        property_size = None  # Atomic\n"
            if game_id == "Prime" and self.is_struct:
                self.class_code += f"        property_count = {_CODE_PARSE_UINT32[endianness]}\n"

            for prop_name, prop in self.all_props.items():
                self.class_code += f"        {prop_name} = {prop.parse_code}\n"

            self.class_code += f"        return cls({', '.join(prop_name for prop_name in self.all_props)})\n"
            return

        if self.is_struct:
            self.class_code += (
                '        struct_id, size, property_count = struct.unpack("' + endianness + 'LHH", data.read(8))\n'
            )
            self.class_code += "        assert struct_id == 0xFFFFFFFF\n"
            self.class_code += "        root_size_start = data.tell() - 2\n\n"
        else:
            self.class_code += f"        property_count = {_CODE_PARSE_UINT16[endianness]}\n"

        self.class_code += "        if (result := _fast_decode(data, property_count)) is not None:\n"
        self.class_code += "            return result\n\n"

        if self._can_fast_decode():
            for fast_decode in self._create_fast_decode_body():
                self.after_class_code += f"{fast_decode}\n"
        else:
            for fast_decode in self._create_simple_decode_body():
                self.after_class_code += f"{fast_decode}\n"
        self.after_class_code += "\n\n"

        if self.keep_unknown_properties():
            read_unknown = 'present_fields["unknown_properties"][property_id] = data.read(property_size)'
            unknown_fields_declare = '\n        present_fields["unknown_properties"] = {}\n'
        else:
            read_unknown = 'raise RuntimeError(f"Unknown property: 0x{property_id:08x}")'
            unknown_fields_declare = ""

        self.class_code += f"""        present_fields = default_override or {{}}{unknown_fields_declare}
        for _ in range(property_count):
            property_id, property_size = struct.unpack("{endianness}LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                {read_unknown}
            assert data.tell() - start == property_size\n
"""
        if self.is_struct:
            self.class_code += "        assert data.tell() - root_size_start == size\n"

        self.class_code += "        return cls(**present_fields)\n"

        signature = "data: typing.BinaryIO, property_size: int"
        for prop_name, prop in self.all_props.items():
            if prop.parse_code.endswith(".from_stream(data, property_size)"):
                suffix_size = len("(data, property_size)")
                self.after_class_code += f"_decode_{prop_name} = {prop.parse_code[:-suffix_size]}\n\n"
            else:
                self.after_class_code += f"def _decode_{prop_name}({signature}):\n"
                self.after_class_code += f"    return {prop.parse_code}\n\n\n"

        decoder_type = "typing.Callable[[typing.BinaryIO, int], typing.Any]"
        self.after_class_code += f"_property_decoder: typing.Dict[int, typing.Tuple[str, {decoder_type}]] = {{\n"
        for prop_name, prop in self.all_props.items():
            self.after_class_code += f"    {hex(prop.id)}: ({repr(prop_name)}, _decode_{prop_name}),\n"
        self.after_class_code += "}\n"

    def write_to_stream(self):
        self.class_code += """
    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
"""
        endianness = get_endianness(self.game_id)

        if self.has_custom_cook_pref:
            assert self.game_id != "Prime"

        if self.atomic or self.game_id == "Prime":
            assert not self.has_custom_cook_pref

            if self.game_id == "Prime" and self.is_struct:
                num_props = len(self.all_props)
                prop_count_repr = repr(struct.pack(endianness + "L", num_props))
                self.class_code += f"        data.write({prop_count_repr})  # {num_props} properties\n"

            for prop_name, prop in self.all_props.items():
                for build in prop.build_code:
                    self.class_code += f"        {build.format(obj=f'self.{prop_name}')}\n"
            return

        # After here we don't need to worry about Prime (or atomic)
        has_root_size_offset = False

        if self.is_struct:
            null_bytes = repr(b"\xFF\xFF\xFF\xFF")
            self.class_code += f"        data.write({null_bytes})  # struct object id\n"
            placeholder = repr(b"\x00\x00")
            self.class_code += "        root_size_offset = data.tell()\n"
            self.class_code += f"        data.write({placeholder})  # placeholder for root struct size\n"
            has_root_size_offset = True

        elif self.has_custom_cook_pref:
            self.class_code += "        num_properties_offset = data.tell()\n"

        if self.keep_unknown_properties():
            self.class_code += f'        data.write(struct.pack("{endianness}H", {self.property_count} + len(self.unknown_properties)))\n'
        else:
            prop_count_repr = repr(struct.pack(endianness + "H", self.property_count))
            self.class_code += f"        data.write({prop_count_repr})  # {self.property_count} properties\n"

        if self.has_custom_cook_pref:
            self.class_code += f"        num_properties_written = {self.property_count}\n"

        self.class_code += self.properties_builder
        if self.keep_unknown_properties():
            self.class_code += "\n        for property_id, property_data in self.unknown_properties.items():\n"
            self.class_code += (
                f'            data.write(struct.pack("{endianness}LH", property_id, len(property_data)))\n'
            )
            self.class_code += "            data.write(property_data)\n"
            num_props_variable = "num_properties_written + len(self.unknown_properties)"
        else:
            num_props_variable = "num_properties_written"

        if has_root_size_offset:
            self.class_code += "\n        struct_end_offset = data.tell()\n"
            self.class_code += "        data.seek(root_size_offset)\n"
            self.class_code += (
                '        data.write(struct.pack("' + endianness + 'H", struct_end_offset - root_size_offset - 2))\n'
            )
            if self.has_custom_cook_pref:
                self.class_code += f'        data.write(struct.pack("{endianness}H", {num_props_variable}))\n'
            self.class_code += "        data.seek(struct_end_offset)\n"

        elif self.has_custom_cook_pref:
            self.class_code += "\n"
            self.class_code += f"        if num_properties_written != {self.property_count}:\n"
            self.class_code += "            struct_end_offset = data.tell()\n"
            self.class_code += "            data.seek(num_properties_offset)\n"
            self.class_code += f'            data.write(struct.pack("{endianness}H", {num_props_variable}))\n'
            self.class_code += "            data.seek(struct_end_offset)\n"

    def write_from_json(self):
        self.class_code += """
    @classmethod
    def from_json(cls, data: dict):
        return cls(
"""
        space = "            "
        for prop_name, prop in self.all_props.items():
            self.class_code += f"{space}{prop_name}={prop.from_json_code.format(obj=f'data[{repr(prop_name)}]')},\n"

        if self.keep_unknown_properties():
            self.needed_imports["base64"] = True
            self.class_code += """
            unknown_properties={
                int(property_id, 16): base64.b64decode(property_data)
                for property_id, property_data in data["unknown_properties"].items()
            },
"""

        self.class_code += "        )\n"

    def write_to_json(self):
        self.class_code += """
    def to_json(self) -> dict:
        return {
"""
        space = "            "
        for prop_name, prop in self.all_props.items():
            self.class_code += f"{space}{repr(prop_name)}: {prop.to_json_code.format(obj=f'self.{prop_name}')},\n"

        if self.keep_unknown_properties():
            self.needed_imports["base64"] = True
            self.class_code += """
            'unknown_properties': {
                hex(property_id): base64.b64encode(property_data)
                for property_id, property_data in self.unknown_properties.items()
            }
"""

        self.class_code += "        }\n"

    def write_dependencies(self):
        if self.keep_unknown_properties() or self.game_id not in {"Prime", "Echoes"}:
            return

        has_dep = False

        for prop_name, prop in self.all_props.items():
            if prop.dependency_code is None:
                continue

            has_dep = True
            prop_code = prop.dependency_code.format(obj=f"self.{prop_name}")
            if prop.raw.get("ignore_dependencies_mlvl"):
                self.needed_imports["retro_data_structures.base_resource"] = "Dependency"
                prop_code = f"for it in {prop_code}:\n            yield Dependency(it.type, it.id, True)"
            else:
                prop_code = f"yield from {prop_code}"

            self.class_code += f"""
    def _dependencies_for_{prop_name}(self, asset_manager):
        {prop_code}
"""

        if has_dep:
            method_list = "\n".join(
                f'            (self._dependencies_for_{prop_name}, "{prop_name}", "{prop.prop_type}"),'
                for prop_name, prop in self.all_props.items()
                if prop.dependency_code is not None
            )
            self.class_code += f"""
    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
{method_list}
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for {self.class_name}.{{field_name}} ({{field_type}}): {{e}}"
                )
"""
        else:
            self.class_code += """
    def dependencies_for(self, asset_manager):
        yield from []
"""


def _add_default_types(core_path: Path, game_id: str):
    game_code = f"""
    @classmethod
    def game(cls) -> Game:
        return Game.{_game_id_to_enum[game_id]}
"""

    endianness = get_endianness(game_id)

    core_path.joinpath("Color.py").write_text(
        f"""# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Color(BaseProperty):
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 0.0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(*struct.unpack('{endianness}ffff', data.read(16)))

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack('{endianness}ffff', self.r, self.g, self.b, self.a))

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["r"], data["g"], data["b"], data["a"])

    def to_json(self) -> dict:
        return {{
            "r": self.r,
            "g": self.g,
            "b": self.b,
            "a": self.a,
        }}
"""
        + game_code
    )
    core_path.joinpath("Vector.py").write_text(
        f"""# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Vector(BaseProperty):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(*struct.unpack('{endianness}fff', data.read(12)))

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack('{endianness}fff', self.x, self.y, self.z))

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["x"], data["y"], data["z"])

    def to_json(self) -> dict:
        return {{
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }}

    def dependencies_for(self, asset_manager):
        yield from []
"""
        + game_code
    )
    if game_id == "PrimeRemastered":
        asset_code = "import uuid\n\nAssetId = uuid.UUID\ndefault_asset_id = uuid.UUID(int=0)\n"
    else:
        if game_id in ["Prime", "Echoes"]:
            invalid_id = "0xFFFFFFFF"
        else:
            invalid_id = "0xFFFFFFFFFFFFFFFF"
        asset_code = f"AssetId = int\ndefault_asset_id = {invalid_id}\n"
    core_path.joinpath("AssetId.py").write_text(asset_code)

    if game_id == "PrimeRemastered":
        core_path.joinpath("PooledString.py").write_text(
            f"""# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from .AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PooledString(BaseProperty):
    index: int = -1
    size_or_str: typing.Union[int, bytes] = b""

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        a, b = struct.unpack('{endianness}lL', data.read(8))
        if a == -1:
            b = data.read(b)
        return cls(a, b)

    def to_stream(self, data: typing.BinaryIO):
        a, b = self.index, self.size_or_str
        if a == -1:
            b = len(b)
        data.write(struct.pack('{endianness}lL', a, b))
        if a == -1:
            data.write(self.size_or_str)

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["index"], data["size_or_str"])

    def to_json(self) -> dict:
        return {{
            "index": self.index,
            "size_or_str": self.size_or_str,
        }}
"""
            + game_code
        )
        return

    if game_id in ["Prime", "Echoes"]:
        format_specifier = "L"
        known_size = 12
    else:
        format_specifier = "Q"
        known_size = 16

    core_path.joinpath("AnimationParameters.py").write_text(
        f"""# Generated file
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from .AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class AnimationParameters(BaseProperty):
    ancs: AssetId = default_asset_id
    character_index: int = 0
    initial_anim: int = 0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(*struct.unpack('{endianness}{format_specifier}LL', data.read({known_size})))

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack('{endianness}{format_specifier}LL', self.ancs, self.character_index, self.initial_anim))

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["ancs"], data["character_index"], data["initial_anim"])

    def to_json(self) -> dict:
        return {{
            "ancs": self.ancs,
            "character_index": self.character_index,
            "initial_anim": self.initial_anim,
        }}

    def dependencies_for(self, asset_manager):
        yield from asset_manager.get_dependencies_for_ancs(self.ancs, self.character_index)
"""
        + game_code
    )
    core_path.joinpath("Spline.py").write_text(
        """# Generated file
import dataclasses
import typing
import base64

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Spline(BaseProperty):
    data: bytes = b""

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        assert size is not None
        result = cls()
        result.data = data.read(size)
        return result

    def to_stream(self, data: typing.BinaryIO):
        data.write(self.data)

    @classmethod
    def from_json(cls, data):
        return cls(base64.b64decode(data))

    def to_json(self) -> str:
        return base64.b64encode(self.data).decode("ascii")
"""
        + game_code
    )


def parse_game(templates_path: Path, game_xml: Path, game_id: str) -> dict:
    logging.info("Parsing templates for game %s: %s", game_id, game_xml)

    base_path = templates_path / game_xml.parent

    t = ElementTree.parse(templates_path / game_xml)
    root = t.getroot()

    states = get_key_map(root.find("States"))
    messages = get_key_map(root.find("Messages"))

    game_enums = []
    _enums_by_game[game_id] = game_enums

    if game_id == "Prime":
        enum_value_repr = str
        enum_base = "IntEnum"
    else:
        enum_value_repr = repr
        enum_base = "Enum"

    if states:
        game_enums.append(
            EnumDefinition(
                "State",
                {value: enum_value_repr(key) for key, value in states.items()},
                enum_base=enum_base,
            )
        )

    if messages:
        game_enums.append(
            EnumDefinition(
                "Message",
                {value: enum_value_repr(key) for key, value in messages.items()},
                enum_base=enum_base,
            )
        )

    script_objects_paths = dict(get_paths(root.find("ScriptObjects")).items())
    script_objects = {
        four_cc: parse_script_object_file(base_path / path, game_id) for four_cc, path in script_objects_paths.items()
    }
    property_archetypes = {
        name: parse_property_archetypes(base_path / path, game_id)
        for name, path in get_paths(root.find("PropertyArchetypes")).items()
    }

    code_path = rds_root.joinpath("properties", _game_id_to_file[game_id])
    _ensure_is_generated_dir(code_path)
    import_base = f"retro_data_structures.properties.{_game_id_to_file[game_id]}"
    endianness = get_endianness(game_id)

    class LiteralPropType(typing.NamedTuple):
        python_type: str
        struct_format: str
        default: typing.Any

        @property
        def byte_count(self):
            return struct.calcsize(endianness + self.struct_format)

    _literal_prop_types = {
        "Int": LiteralPropType("int", "l", 0),
        "Float": LiteralPropType("float", "f", 0.0),
        "Bool": LiteralPropType("bool", "?", False),
        "Short": LiteralPropType("int", "h", 0),
    }

    core_path = code_path.joinpath("core")
    _ensure_is_generated_dir(core_path)
    _add_default_types(core_path, game_id)

    known_enums: dict[str, EnumDefinition] = {_scrub_enum(e.name): e for e in _enums_by_game[game_id]}

    def get_prop_details(prop) -> PropDetails:
        raw_type = prop["type"]
        prop_type = None
        need_enums = False
        comment = None
        parse_code = "None"
        build_code = []
        from_json_code = "None"
        to_json_code = "None"
        known_size = None
        meta = {}
        needed_imports = {}
        format_specifier = None
        dependency_code = None

        if raw_type == "Sound":
            raw_type = "Int"
            meta["default"] = 65535
            meta["metadata"] = {"sound": True}
            dependency_code = "asset_manager.get_audio_group_dependency({obj})"

        if raw_type == "Struct":
            archetype_path: str = prop["archetype"].replace("_", ".")
            prop_type = archetype_path.split(".")[-1]
            needed_imports[f"{import_base}.archetypes.{archetype_path}"] = prop_type
            meta["default_factory"] = prop_type
            from_json_code = f"{prop_type}.from_json({{obj}})"
            to_json_code = "{obj}.to_json()"
            dependency_code = "{obj}.dependencies_for(asset_manager)"

            default_override = {}
            for inner_prop in prop["properties"]:
                if not inner_prop.get("has_default"):
                    continue

                inner_name = _filter_property_name(inner_prop["name"] or property_names.get(inner_prop["id"]))
                assert inner_name is not None
                if inner_name == "unknown":
                    print(f"Ignoring default override for field {inner_prop['id']:08x}: no known name")
                    continue

                inner_details = get_prop_details(inner_prop)
                default_override[inner_name] = _get_default(inner_details.meta)
                needed_imports.update(inner_details.needed_imports)
                need_enums = need_enums or inner_details.need_enums

            if default_override:
                override = ", ".join(f"{repr(key)}: {value}" for key, value in default_override.items())
                parse_code = f"{prop_type}.from_stream(data, property_size, default_override={{{override}}})"
                build_code.append(f"{{obj}}.to_stream(data, default_override={{{override}}})")
            else:
                parse_code = f"{prop_type}.from_stream(data, property_size)"
                build_code.append("{obj}.to_stream(data)")

        elif prop["type"] in ["Choice", "Enum"]:
            default_value = prop["default_value"] if prop["has_default"] else 0
            enum_name = _scrub_enum(prop["archetype"] or prop["name"] or property_names.get(prop["id"]) or "")
            format_specifier = "L"

            uses_known_enum = enum_name in known_enums and (
                default_value in list(known_enums[enum_name].values.values())
            )
            if uses_known_enum:
                prop_type = f"enums.{enum_name}"
                need_enums = True
                parse_code = f"enums.{enum_name}.from_stream(data)"
                build_code.append("{obj}.to_stream(data)")
                from_json_code = f"{prop_type}.from_json({{obj}})"
                to_json_code = "{obj}.to_json()"

                for key, value in known_enums[enum_name].values.items():
                    if value == default_value:
                        meta["default"] = f"enums.{enum_name}.{_scrub_enum(key)}"
                assert "default" in meta
            else:
                comment = "Choice"
                prop_type = "int"
                meta["default"] = repr(default_value)
                parse_code = _CODE_PARSE_UINT32[endianness]
                build_code.append('data.write(struct.pack("' + endianness + 'L", {obj}))')
                from_json_code = "{obj}"
                to_json_code = "{obj}"

        elif raw_type == "Flags":
            default_value = repr(prop["default_value"] if prop["has_default"] else 0)
            format_specifier = "L"

            if "flagset_name" in prop:
                prop_type = "enums." + _scrub_enum(prop["flagset_name"])
                need_enums = True
                meta["default"] = f"{prop_type}({default_value})"
                parse_code = f"{prop_type}.from_stream(data)"
                build_code.append("{obj}.to_stream(data)")
                from_json_code = f"{prop_type}.from_json({{obj}})"
                to_json_code = "{obj}.to_json()"
            else:
                prop_type = "int"
                comment = "Flagset"
                meta["default"] = default_value
                parse_code = _CODE_PARSE_UINT32[endianness]
                build_code.append('data.write(struct.pack("' + endianness + 'L", {obj}))')
                from_json_code = "{obj}"
                to_json_code = "{obj}"

        elif raw_type == "Asset":
            prop_type = "AssetId"
            needed_imports[f"{import_base}.core.AssetId"] = "AssetId, default_asset_id"
            field_meta = {"asset_types": prop["type_filter"]}
            if not any(asset_type in prop["type_filter"] for asset_type in ("MLVL", "MREA")):
                dependency_code = "asset_manager.get_dependencies_for_asset({obj})"

            if "ignore_dependencies_mlvl" in prop:
                field_meta["ignore_dependencies_mlvl"] = True

            meta["metadata"] = repr(field_meta)
            default_value = "default_asset_id"

            meta["default"] = default_value

            if game_id in ["PrimeRemastered"]:
                needed_imports["uuid"] = True
                known_size = 16
                parse_code = "uuid.UUID(bytes_le=data.read(16))"
                build_code.append("data.write({obj}.bytes_le)")
                from_json_code = "uuid.UUID({obj})"
                to_json_code = "str({obj})"

            else:
                if game_id in ["Prime", "Echoes"]:
                    format_specifier = "L"
                    known_size = 4
                else:
                    format_specifier = "Q"
                    known_size = 8

                format_with_prefix = f'"{endianness}{format_specifier}"'
                parse_code = f"struct.unpack({format_with_prefix}, data.read({known_size}))[0]"
                build_code.append(f"data.write(struct.pack({format_with_prefix}, {{obj}}))")
                from_json_code = "{obj}"
                to_json_code = "{obj}"

        elif raw_type in ["AnimationSet", "Spline", "PooledString"]:
            if raw_type == "AnimationSet":
                prop_type = "AnimationParameters"
                dependency_code = "{obj}.dependencies_for(asset_manager)"
            else:
                prop_type = raw_type
            needed_imports[f"{import_base}.core.{prop_type}"] = prop_type
            parse_code = f"{prop_type}.from_stream(data, property_size)"
            build_code.append("{obj}.to_stream(data)")
            from_json_code = f"{prop_type}.from_json({{obj}})"
            to_json_code = "{obj}.to_json()"
            meta["default_factory"] = prop_type

        elif raw_type == "Array":
            inner_prop = get_prop_details(prop["item_archetype"])

            prop_type = f"list[{inner_prop.prop_type}]"
            need_enums = inner_prop.need_enums
            comment = inner_prop.comment
            meta["default_factory"] = "list"
            if len(inner_prop.format_specifier or "") == 1:
                specifier = f"{repr(endianness)} + {repr(inner_prop.format_specifier)} * (count := {_CODE_PARSE_UINT32[endianness]})"
                parse_code = f"list(struct.unpack({specifier}, data.read(count * {inner_prop.known_size})))"
            else:
                parse_code = f"[{inner_prop.parse_code} for _ in range({_CODE_PARSE_UINT32[endianness]})]"
            build_code.extend(
                [
                    "array = {obj}",
                    'data.write(struct.pack("' + endianness + 'L", len(array)))',
                    "for item in array:",
                    *["    " + inner.format(obj="item") for inner in inner_prop.build_code],
                ]
            )
            from_json_code = "[{inner} for item in {{obj}}]".format(inner=inner_prop.from_json_code.format(obj="item"))
            to_json_code = "[{inner} for item in {{obj}}]".format(inner=inner_prop.to_json_code.format(obj="item"))
            needed_imports.update(inner_prop.needed_imports)

        elif raw_type == "String":
            prop_type = "str"
            meta["default"] = repr(prop["default_value"] if prop["has_default"] else "")
            null_byte = repr(b"\x00")
            if game_id == "Prime":
                # No property size for Prime 1
                parse_code = f'b"".join(iter(lambda: data.read(1), {null_byte})).decode("utf-8")'
            else:
                parse_code = 'data.read(property_size)[:-1].decode("utf-8")'
            build_code.extend(
                [
                    'data.write({obj}.encode("utf-8"))',
                    f"data.write({null_byte})",
                ]
            )
            from_json_code = "{obj}"
            to_json_code = "{obj}"

        elif raw_type in ["Color", "Vector"]:
            prop_type = raw_type
            needed_imports[f"{import_base}.core.{raw_type}"] = prop_type
            parse_code = f"{prop_type}.from_stream(data)"
            build_code.append("{obj}.to_stream(data)")
            from_json_code = f"{prop_type}.from_json({{obj}})"
            to_json_code = "{obj}.to_json()"

            if raw_type == "Color":
                format_specifier = "f" * 4
            else:
                format_specifier = "f" * 3

            s = struct.Struct(f"{endianness}f")

            if prop["has_default"]:
                default_value = {k: s.unpack(s.pack(v))[0] for k, v in prop["default_value"].items()}
                if raw_type == "Color":
                    value = {"A": 0.0, **default_value}
                    meta["default_factory"] = "lambda: Color(r={R}, g={G}, b={B}, a={A})".format(**value)
                else:
                    meta["default_factory"] = "lambda: Vector(x={X}, y={Y}, z={Z})".format(**default_value)
            else:
                meta["default_factory"] = prop_type

        elif raw_type in _literal_prop_types:
            literal_prop = _literal_prop_types[raw_type]
            prop_type = literal_prop.python_type
            struct_format = endianness + literal_prop.struct_format
            format_specifier = literal_prop.struct_format

            parse_code = f"struct.unpack({repr(struct_format)}, data.read({literal_prop.byte_count}))[0]"
            build_code.append(f"data.write(struct.pack({repr(struct_format)}, {{obj}}))")
            from_json_code = "{obj}"
            to_json_code = "{obj}"

            default_value = prop["default_value"] if prop["has_default"] else literal_prop.default
            try:
                s = struct.Struct(struct_format)
                default_value = s.unpack(s.pack(default_value))[0]
            except struct.error as e:
                print(f"{hex(prop['id'])} ({prop['type']}) has invalid default value  {default_value}: {e}")
                default_value = literal_prop.default
            meta["default"] = repr(default_value)

        if "default" not in meta and "default_factory" not in meta:
            raise ValueError(f"Unable to find default value for prop {prop}.")

        if prop_type is None:
            print("what?")
            print(prop)

        if known_size is None and format_specifier is not None:
            known_size = struct.calcsize(endianness + format_specifier)

        return PropDetails(
            prop,
            prop_type,
            need_enums,
            comment,
            parse_code,
            build_code,
            from_json_code,
            to_json_code,
            custom_cook_pref=prop["cook_preference"] != "Always",
            known_size=known_size,
            meta=meta,
            needed_imports=needed_imports,
            format_specifier=format_specifier,
            dependency_code=dependency_code,
        )

    def parse_struct(name: str, this, output_path: Path, struct_fourcc: str | None = None):
        is_struct = struct_fourcc is not None and game_id != "PrimeRemastered"
        if this["type"] != "Struct":
            print("Ignoring {}. Is a {}".format(name, this["type"]))
            return

        all_names = [
            _filter_property_name(prop["name"] or property_names.get(prop["id"]) or "unnamed")
            for prop in this["properties"]
        ]

        cls = ClassDefinition(
            game_id=game_id,
            raw_name=name,
            raw_def=this,
            class_name=name.split("_")[-1] if game_id != "PrimeRemastered" else name,
            class_path=name.replace("_", "/") if game_id != "PrimeRemastered" else name,
            is_struct=is_struct,
            is_incomplete=this["incomplete"],
        )
        base_class = "BaseObjectType" if is_struct else "BaseProperty"
        cls.class_code = f"@dataclasses.dataclass()\nclass {cls.class_name}({base_class}):\n"
        _fix_module_name(output_path, cls.class_path)

        if "modules" in this:
            cls.modules.extend(this["modules"])

        for prop, prop_name in zip(this["properties"], all_names):
            final_prop_name = prop_name
            if all_names.count(prop_name) > 1:
                final_prop_name += "_0x{:08x}".format(prop["id"])

            cls.add_prop(get_prop_details(prop), final_prop_name)
        cls.finalize_props()

        cls.class_code += "\n    @classmethod\n"
        cls.class_code += "    def game(cls) -> Game:\n"
        cls.class_code += f"        return Game.{_game_id_to_enum[game_id]}\n"

        if is_struct:
            cls.class_code += "\n    def get_name(self) -> typing.Optional[str]:\n"
            if game_id == "Prime":
                if "name" in cls.all_props:
                    name_field = "self.name"
                else:
                    name_field = "None"
            elif "editor_properties" in cls.all_props:
                name_field = "self.editor_properties.name"
            else:
                name_field = "None"

            cls.class_code += f"        return {name_field}\n"

            cls.class_code += "\n    def set_name(self, name: str) -> None:\n"
            if name_field == "None":
                cls.class_code += '        raise RuntimeError(f"{self.__class__.__name__} does not have name")\n'
            else:
                cls.class_code += f"        {name_field} = name\n"

            cls.class_code += "\n    @classmethod\n"
            if game_id in ["Prime", "PrimeRemastered"]:
                cls.class_code += "    def object_type(cls) -> int:\n"
                cls.class_code += f"        return {struct_fourcc}\n"
            else:
                cls.class_code += "    def object_type(cls) -> str:\n"
                cls.class_code += f"        return {repr(struct_fourcc)}\n"

        if cls.modules:
            cls.class_code += "\n    @classmethod\n"
            cls.class_code += "    def modules(cls) -> typing.List[str]:\n"
            cls.class_code += f"        return {repr(cls.modules)}\n"

        # from stream
        cls.write_from_stream()

        # to stream
        cls.write_to_stream()

        # json stuff
        cls.write_from_json()
        cls.write_to_json()

        cls.write_dependencies()

        code_code = "# Generated File\n"
        code_code += "import dataclasses\nimport struct\nimport typing\n"

        code_code += "\nfrom retro_data_structures.game_check import Game\n"
        code_code += f"from retro_data_structures.properties.base_property import {base_class}\n"

        if cls.need_enums:
            code_code += f"import retro_data_structures.enums.{_game_id_to_file[game_id]} as enums\n"

        for import_path, code_import in sorted(cls.needed_imports.items()):
            if code_import is True:
                code_code += f"import {import_path}\n"
            else:
                code_code += f"from {import_path} import {code_import}\n"

        code_code += "\n\n"
        code_code += cls.class_code
        if cls.after_class_code:
            code_code += "\n\n"
            code_code += cls.after_class_code
        final_path = output_path.joinpath(cls.class_path).with_suffix(".py")
        final_path.parent.mkdir(parents=True, exist_ok=True)

        # There's already a module with same name as this class. Place it as the __init__.py inside
        if final_path.with_suffix("").is_dir():
            final_path = final_path.with_suffix("").joinpath("__init__.py")

        _ensure_is_generated_dir(final_path.parent)
        final_path.write_text(code_code)

    path = code_path.joinpath("objects")
    _ensure_is_generated_dir(path)

    if game_id in ["Prime", "PrimeRemastered"]:

        def four_cc_wrap(it):
            return it

        four_cc_type = "int"
    else:
        four_cc_wrap = repr
        four_cc_type = "str"

    getter_func = "# Generated File\n"
    getter_func += "import functools\nimport typing\n\n"
    getter_func += "from retro_data_structures.properties.base_property import BaseObjectType\n"

    base_import_path = f"retro_data_structures.properties.{_game_id_to_file[game_id]}.objects."
    fourcc_mapping = "\n_FOUR_CC_MAPPING = {\n"
    for object_fourcc, script_object in script_objects.items():
        stem = Path(script_objects_paths[object_fourcc]).stem
        parse_struct(stem, script_object, path, struct_fourcc=object_fourcc)

        getter_func += f"from {base_import_path}{stem} import {stem}\n"
        fourcc_mapping += f"    {four_cc_wrap(object_fourcc)}: {stem},\n"

    getter_func += fourcc_mapping
    getter_func += "}\n\n\n"

    getter_func += "@functools.lru_cache(maxsize=None)\n"
    getter_func += f"def get_object(four_cc: {four_cc_type}) -> typing.Type[BaseObjectType]:\n"
    getter_func += "    return _FOUR_CC_MAPPING[four_cc]\n"
    path.joinpath("__init__.py").write_text(getter_func)

    print("> Creating archetypes")
    path = code_path.joinpath("archetypes")
    _ensure_is_generated_dir(path)
    for archetype_name, archetype in property_archetypes.items():
        parse_struct(archetype_name, archetype, path, struct_fourcc=None)
    print("> Done.")

    return {
        "script_objects": script_objects,
        "property_archetypes": property_archetypes,
        "enums": game_enums,
    }


def parse_game_list(templates_path: Path) -> dict:
    t = ElementTree.parse(templates_path / "GameList.xml")
    root = t.getroot()
    return {game.attrib["ID"]: Path(game.find("GameTemplate").text) for game in root}


def write_shared_type_with_common_import(
    output_file: Path, kind: str, import_path: str, all_objects: dict[str, list[str]]
):
    declarations = []
    base = f"import retro_data_structures.{import_path}."

    used_games = set()

    for object_name, games in sorted(all_objects.items()):
        if len(games) < 2:
            continue

        type_name = object_name.split("_")[-1]

        used_games.update(games)
        declarations.append(
            "{} = typing.Union[\n{}\n]".format(
                object_name, ",\n".join(f"    _{_game_id_to_file[game]}_{kind}.{type_name}" for game in games)
            )
        )

    if kind == "enums":
        left_kind = ""
    else:
        left_kind = f".{kind}"

    output_file.write_text(
        "# Generated File\nimport typing\n\n{imports}\n\n{declarations}\n".format(
            imports="\n".join(
                f"{base}{_game_id_to_file[game]}{left_kind} as _{_game_id_to_file[game]}_{kind}"
                for game in sorted(used_games)
            ),
            declarations="\n".join(declarations),
        )
    )


def write_shared_type(output_file: Path, kind: str, all_objects: dict[str, list[str]]):
    imports = []
    declarations = []
    base = "import retro_data_structures.properties."

    for object_name, games in sorted(all_objects.items()):
        if len(games) < 2:
            continue

        import_name = object_name.replace("_", ".")
        type_name = object_name.split("_")[-1]

        for game in games:
            imports.append(f"{base}{_game_id_to_file[game]}.{kind}.{import_name} as _{object_name}_{game}")
        declarations.append(
            "{} = typing.Union[\n{}\n]".format(
                object_name, ",\n".join(f"    _{object_name}_{game}.{type_name}" for game in games)
            )
        )

    output_file.write_text(
        "# Generated File\nimport typing\n\n{imports}\n\n{declarations}\n".format(
            imports="\n".join(imports),
            declarations="\n".join(declarations),
        )
    )


def write_shared_types_helpers(all_games: dict):
    all_archetypes = collections.defaultdict(list)
    all_objects = collections.defaultdict(list)
    all_enums = collections.defaultdict(list)

    for game_id, game_data in all_games.items():
        for script_object in game_data["script_objects"].values():
            if game_id in all_objects[script_object["name"]]:
                continue
            all_objects[script_object["name"]].append(game_id)

        for archetype in game_data["property_archetypes"].values():
            if "name" not in archetype:
                continue
            if "UnknownStruct" in archetype["name"]:
                continue
            if game_id in all_archetypes[archetype["name"]]:
                continue
            all_archetypes[archetype["name"]].append(game_id)

        for enum_def in game_data["enums"]:
            assert isinstance(enum_def, EnumDefinition)
            if "Unknown" not in enum_def.name:
                all_enums[_scrub_enum(enum_def.name)].append(game_id)

    write_shared_type_with_common_import(
        rds_root.joinpath("enums", "shared_enums.py"),
        "enums",
        "enums",
        all_enums,
    )
    path_to_props = rds_root.joinpath("properties")
    write_shared_type_with_common_import(
        path_to_props.joinpath("shared_objects.py"),
        "objects",
        "properties",
        all_objects,
    )
    write_shared_type(
        path_to_props.joinpath("shared_archetypes.py"),
        "archetypes",
        all_archetypes,
    )
    write_shared_type(
        path_to_props.joinpath("shared_core.py"),
        "core",
        {
            name: ["Prime", "Echoes", "Corruption", "DKCReturns"]
            for name in ["AnimationParameters", "AssetId", "Color", "Spline", "Vector"]
        },
    )


def parse(game_ids: typing.Iterable[str] | None = None) -> dict:
    base_dir = Path(__file__).parent
    templates_path = base_dir.joinpath("retro-script-object-templates")
    read_property_names(templates_path / "PropertyMap.xml")

    game_list = parse_game_list(templates_path)
    _parse_choice.unknowns = {game: 0 for game in game_list.keys()}

    all_games = {
        _id: parse_game(templates_path, game_path, _id)
        for _id, game_path in game_list.items()
        if game_ids is None or _id in game_ids
    }
    write_shared_types_helpers(all_games)
    return all_games


def persist_data(parse_result):
    logging.info("Persisting the parsed properties")

    # First write the enums
    for game_id in parse_result.keys():
        if game_id in _game_id_to_file:
            rds_root.joinpath("enums", f"{_game_id_to_file[game_id]}.py").write_text(
                create_enums_file(game_id, _enums_by_game[game_id])
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # persist_data(parse(["PrimeRemastered"]))
    persist_data(parse(_game_id_to_file.keys()))
