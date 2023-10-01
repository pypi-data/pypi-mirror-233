"""Utility functions for Z-Wave JS locks."""
from __future__ import annotations

from typing import TypedDict, cast

from ..const import CommandClass
from ..const.command_class.lock import (
    ATTR_CODE_SLOT,
    ATTR_IN_USE,
    ATTR_NAME,
    ATTR_USERCODE,
    LOCK_USERCODE_PROPERTY,
    LOCK_USERCODE_STATUS_PROPERTY,
    CodeSlotStatus,
)
from ..exceptions import NotFoundError
from ..model.node import Node
from ..model.value import SetValueResult, Value, get_value_id_str


def get_code_slot_value(node: Node, code_slot: int, property_name: str) -> Value:
    """Get a code slot value."""
    value = node.values.get(
        get_value_id_str(
            node,
            CommandClass.USER_CODE,
            property_name,
            endpoint=0,
            property_key=code_slot,
        )
    )

    if not value:
        raise NotFoundError(f"{property_name} for code slot {code_slot} not found")

    return value


class CodeSlot(TypedDict, total=False):
    """Represent a code slot."""

    code_slot: int  # required
    name: str  # required
    in_use: bool | None  # required
    usercode: str | None


def _get_code_slots(node: Node, include_usercode: bool = False) -> list[CodeSlot]:
    """Get all code slots on the lock and optionally include usercode."""
    code_slot = 1
    slots: list[CodeSlot] = []

    # Loop until we can't find a code slot
    while True:
        try:
            value = get_code_slot_value(node, code_slot, LOCK_USERCODE_PROPERTY)
            status_value = get_code_slot_value(
                node, code_slot, LOCK_USERCODE_STATUS_PROPERTY
            )
        except NotFoundError:
            return slots

        code_slot = int(value.property_key)  # type: ignore
        in_use = (
            None
            if status_value.value is None
            else status_value.value == CodeSlotStatus.ENABLED
        )

        # we know that code slots will always have a property key
        # that is an int, so we can ignore mypy
        slot = {
            ATTR_CODE_SLOT: code_slot,
            ATTR_NAME: value.metadata.label,
            ATTR_IN_USE: in_use,
        }
        if include_usercode:
            slot[ATTR_USERCODE] = value.value

        slots.append(cast(CodeSlot, slot))
        code_slot += 1


def get_code_slots(node: Node) -> list[CodeSlot]:
    """Get all code slots on the lock and whether or not they are used."""
    return _get_code_slots(node, False)


def get_usercodes(node: Node) -> list[CodeSlot]:
    """Get all code slots and usercodes on the lock."""
    return _get_code_slots(node, True)


def get_usercode(node: Node, code_slot: int) -> CodeSlot:
    """Get usercode from slot X on the lock."""
    value = get_code_slot_value(node, code_slot, LOCK_USERCODE_PROPERTY)
    status_value = get_code_slot_value(node, code_slot, LOCK_USERCODE_STATUS_PROPERTY)

    code_slot = int(value.property_key)  # type: ignore
    in_use = (
        None
        if status_value.value is None
        else status_value.value == CodeSlotStatus.ENABLED
    )

    return cast(
        CodeSlot,
        {
            ATTR_CODE_SLOT: code_slot,
            ATTR_NAME: value.metadata.label,
            ATTR_IN_USE: in_use,
            ATTR_USERCODE: value.value,
        },
    )


async def get_usercode_from_node(node: Node, code_slot: int) -> CodeSlot:
    """
    Fetch a usercode directly from a node.

    Should be used when Z-Wave JS's ValueDB hasn't been populated for this code slot.
    This call will populate the ValueDB and trigger value update events from the
    driver.
    """
    await node.async_invoke_cc_api(
        CommandClass.USER_CODE, "get", code_slot, wait_for_result=True
    )
    return get_usercode(node, code_slot)


async def set_usercode(
    node: Node, code_slot: int, usercode: str
) -> SetValueResult | None:
    """Set the usercode to index X on the lock."""
    value = get_code_slot_value(node, code_slot, LOCK_USERCODE_PROPERTY)

    if len(str(usercode)) < 4:
        raise ValueError("User code must be at least 4 digits")

    return await node.async_set_value(value, usercode)


async def clear_usercode(node: Node, code_slot: int) -> SetValueResult | None:
    """Clear a code slot on the lock."""
    value = get_code_slot_value(node, code_slot, LOCK_USERCODE_STATUS_PROPERTY)
    return await node.async_set_value(value, CodeSlotStatus.AVAILABLE.value)
