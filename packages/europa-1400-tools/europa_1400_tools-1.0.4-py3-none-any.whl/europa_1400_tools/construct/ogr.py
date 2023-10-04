"""Construct for OGR files."""

from dataclasses import dataclass

import construct as cs
from construct_typed import DataclassMixin, DataclassStruct, csfield

from europa_1400_tools.construct.baf import Vector3
from europa_1400_tools.construct.base_construct import BaseConstruct
from europa_1400_tools.construct.common import ignoredcsfield


def is_01(obj, ctx):
    return obj == 1


def cancel_on_unacceptable(obj, ctx):
    if obj not in ctx.acceptable_values:
        raise cs.CancelParsing


@dataclass
class Skip0(DataclassMixin):
    """Structure of a skip0 block."""

    acceptable_values: list[int] = ignoredcsfield(cs.Computed(lambda ctx: [0]))
    skipped: list[int] = ignoredcsfield(
        cs.GreedyRange(cs.Byte * cancel_on_unacceptable)
    )


@dataclass
class Skip01(DataclassMixin):
    """Structure of a skip01 block."""

    acceptable_values: list[int] = ignoredcsfield(cs.Computed(lambda ctx: [0, 1]))
    skipped: list[int] = ignoredcsfield(
        cs.GreedyRange(cs.Byte * cancel_on_unacceptable)
    )


@dataclass
class Skip013(DataclassMixin):
    """Structure of a skip013 block."""

    acceptable_values: list[int] = ignoredcsfield(cs.Computed(lambda ctx: [0, 1, 3]))
    skipped: list[int] = ignoredcsfield(
        cs.GreedyRange(cs.Byte * cancel_on_unacceptable)
    )


@dataclass
class Skip12345678(DataclassMixin):
    """Structure of a skip0123456 block."""

    acceptable_values: list[int] = ignoredcsfield(
        cs.Computed(lambda ctx: [1, 2, 3, 4, 5, 6, 7, 8])
    )
    skipped: list[int] = ignoredcsfield(
        cs.GreedyRange(cs.Byte * cancel_on_unacceptable)
    )


@dataclass
class Skip012345678(DataclassMixin):
    """Structure of a skip0123456 block."""

    acceptable_values: list[int] = ignoredcsfield(
        cs.Computed(lambda ctx: [0, 1, 2, 3, 4, 5, 6, 7, 8])
    )
    skipped: list[int] = ignoredcsfield(
        cs.GreedyRange(cs.Byte * cancel_on_unacceptable)
    )


@dataclass
class LightDataBlock(DataclassMixin):
    """Structure of a light data block."""

    data: list[float] = csfield(cs.Array(9, cs.Float32l))
    zeros: bytes = ignoredcsfield(cs.Bytes(12))
    skipped: bytes | None = ignoredcsfield(
        cs.If(
            lambda ctx: ctx._.data_padding > 0, cs.Bytes(lambda ctx: ctx._.data_padding)
        )
    )


@dataclass
class ObjectData(DataclassMixin):
    """Structure of a object data block."""

    offset: Vector3 = csfield(DataclassStruct(Vector3))
    data: Vector3 = csfield(DataclassStruct(Vector3))


@dataclass
class DummyElement(DataclassMixin):
    """Structure of a dummy element."""

    skipped: bytes = ignoredcsfield(cs.Bytes(4))
    object_data: ObjectData = csfield(DataclassStruct(ObjectData))


@dataclass
class ObjectElement(DataclassMixin):
    """Structure of a object element."""

    skip0123456: Skip012345678 = ignoredcsfield(DataclassStruct(Skip012345678))
    name: str = csfield(cs.CString("ascii"))
    object_data: ObjectData = csfield(DataclassStruct(ObjectData))
    additional_flag: int | None = ignoredcsfield(
        cs.If(lambda ctx: cs.Peek(cs.Byte) == 1, cs.Byte)
    )
    object_data_additional: ObjectData | None = csfield(
        cs.If(lambda ctx: ctx.additional_flag == 1, DataclassStruct(ObjectData))
    )


@dataclass
class LightElement(DataclassMixin):
    """Structure of a footer element."""

    skipped: bytes = ignoredcsfield(cs.Bytes(6))
    data_padding: int = ignoredcsfield(
        cs.Computed(lambda ctx: len(ctx._.skip013.skipped))
    )
    data_count: int = csfield(
        cs.Computed(
            lambda ctx: 8
            if ctx.footer_padding == 8 and ctx._.type != 7 and ctx._.type != 8
            else 7
        )
    )
    light_data_blocks: list[LightDataBlock] = csfield(
        cs.Array(lambda ctx: ctx.data_count, DataclassStruct(LightDataBlock))
    )


@dataclass
class GroupElement(DataclassMixin):
    """Structure of a group element."""

    skip01: Skip01 = ignoredcsfield(DataclassStruct(Skip01))
    name: str = csfield(cs.CString("ascii"))
    skip013: Skip013 = ignoredcsfield(DataclassStruct(Skip013))
    type: int = csfield(cs.Byte)
    dummy_element: DummyElement | None = csfield(
        cs.If(lambda ctx: ctx.type == 2, DataclassStruct(DummyElement))
    )
    object_element: ObjectElement | None = csfield(
        cs.If(lambda ctx: ctx.type == 4, DataclassStruct(ObjectElement))
    )
    light_element: LightElement | None = csfield(
        cs.If(
            lambda ctx: ctx.type == 5
            or ctx.type == 6
            or ctx.type == 7
            or ctx.type == 8,
            DataclassStruct(LightElement),
        )
    )


@dataclass
class Ogr(BaseConstruct):
    """Structure of a OGR file."""

    magic1: int = csfield(cs.Byte)
    magic2: int = csfield(cs.Byte)
    magic3: int = csfield(cs.Int16ul)
    skipped1: bytes = ignoredcsfield(DataclassStruct(Skip12345678))
    skipped2: bytes = ignoredcsfield(DataclassStruct(Skip0))
    group_elements: list[GroupElement] = csfield(
        cs.GreedyRange(DataclassStruct(GroupElement) * is_01)
    )
