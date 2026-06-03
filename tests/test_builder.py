"""Tests for fleet_deepagents_export.builder helpers.

Focuses on interrupt-config normalization — Fleet exports interrupt keys as
``"<url>::<tool>::<source>"`` but HumanInTheLoopMiddleware matches bare tool
names, so without normalization the human-in-the-loop gate never fires.
"""

from __future__ import annotations

from fleet_deepagents_export import builder as b


def test_normalizes_composite_key_to_tool_name():
    cfg = {"https://tools.langchain.com::gmail_send_email::Fleet": True}
    assert b._normalize_interrupt_config(cfg) == {"gmail_send_email": True}


def test_idempotent_on_bare_name():
    # Already-bare keys pass through unchanged (no "::" to split).
    assert b._normalize_interrupt_config({"gmail_send_email": True}) == {
        "gmail_send_email": True
    }


def test_empty_or_none_returns_empty_dict():
    assert b._normalize_interrupt_config(None) == {}
    assert b._normalize_interrupt_config({}) == {}


def test_preserves_dict_value():
    cfg = {"https://x::send::Fleet": {"allow_accept": True, "allow_respond": False}}
    assert b._normalize_interrupt_config(cfg) == {
        "send": {"allow_accept": True, "allow_respond": False}
    }


def test_tool_name_containing_double_colon_survives():
    # Name is everything between the URL and source segments.
    cfg = {"https://x::weird::name::Fleet": True}
    assert b._normalize_interrupt_config(cfg) == {"weird::name": True}


def test_allowlist_keeps_known_tool():
    cfg = {"https://tools.langchain.com::gmail_send_email::Fleet": True}
    out = b._normalize_interrupt_config(cfg, valid_tool_names={"gmail_send_email"})
    assert out == {"gmail_send_email": True}


def test_allowlist_drops_unknown_tool():
    cfg = {"https://x::ghost_tool::Fleet": True}
    out = b._normalize_interrupt_config(cfg, valid_tool_names={"gmail_send_email"})
    assert out == {}
