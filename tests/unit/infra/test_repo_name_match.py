"""Tolerant person-name resolution (partial names + ё/е)."""

from __future__ import annotations

from planner.infra.db.repo import match_person_name

_NAMES = ["Пётр Гарник", "Иван Буйнов", "Мария Таиров"]


def test_partial_first_name_resolves():
    assert match_person_name(_NAMES, "Пётр") == "Пётр Гарник"
    assert match_person_name(_NAMES, "Андр") == "Иван Буйнов"


def test_yo_ye_equivalence():
    assert match_person_name(_NAMES, "Пётр") == "Пётр Гарник"


def test_full_name_exact():
    assert match_person_name(_NAMES, "лёша гарник") == "Пётр Гарник"


def test_no_match_returns_none():
    assert match_person_name(_NAMES, "Неизвестный") is None
    assert match_person_name(_NAMES, "") is None
