"""Regression tests for malformed records and cancellation replay safety."""
import math

import pytest

from models import new_order, new_partner
from service import assign_order, estimate_eta, process_cancellation


@pytest.mark.parametrize("value", [True, False, -1, None, "3", math.nan, math.inf])
def test_eta_rejects_invalid_current_time_and_travel(value):
    order = new_order("O", "R", "D")
    partner = new_partner("P", "Z")
    result = estimate_eta(order, partner, {("Z", "R"): value, ("R", "D"): 1})
    assert result["eligible"] is False
    assert result["eta_minutes"] is None


def test_eta_rejects_invalid_workload():
    order = new_order("O", "R", "D")
    partner = new_partner("P", "Z")
    partner["workload_minutes"] = float("nan")
    result = estimate_eta(order, partner, {("Z", "R"): 1, ("R", "D"): 1})
    assert result["eligible"] is False


@pytest.mark.parametrize("capacity", [0, -1, True, 1.5, None])
def test_assignment_rejects_invalid_capacity(capacity):
    order = new_order("O", "R", "D")
    partner = new_partner("P", "Z")
    partner["capacity"] = capacity
    result = assign_order(order, [partner], {("Z", "R"): 1, ("R", "D"): 1})
    assert result["partner_id"] is None


def test_assignment_requires_active_to_be_boolean_true():
    order = new_order("O", "R", "D")
    partner = new_partner("P", "Z")
    partner["active"] = 1
    result = assign_order(order, [partner], {("Z", "R"): 1, ("R", "D"): 1})
    assert result["partner_id"] is None


def test_assignment_does_not_mutate_partner_records():
    order = new_order("O", "R", "D")
    partner = new_partner("P", "Z")
    before = dict(partner)
    assign_order(order, [partner], {("Z", "R"): 1, ("R", "D"): 1})
    assert partner == before


def test_replayed_event_id_with_different_order_payload_is_ignored():
    partner = new_partner("P", "Z")
    partner.update(
        active_order_ids=["O1", "O2"],
        workload_minutes=15,
        minutes_by_order={"O1": 5, "O2": 10},
        processed_cancellation_ids=["EVENT-1"],
    )
    result = process_cancellation(partner, "O2", "EVENT-1")
    assert result["active_order_ids"] == ["O1", "O2"]
    assert result["workload_minutes"] == 15
    assert result["processed_cancellation_ids"] == ["EVENT-1"]


def test_cancellation_does_not_mutate_input_partner():
    partner = new_partner("P", "Z")
    partner.update(active_order_ids=["O"], workload_minutes=4, minutes_by_order={"O": 4})
    original = {**partner, "active_order_ids": ["O"], "minutes_by_order": {"O": 4}}
    process_cancellation(partner, "O", "C")
    assert partner == original


def test_malformed_partner_and_order_are_safe():
    assert estimate_eta(None, {}, {})["eligible"] is False
    assert assign_order(None, [None, {}], {})["partner_id"] is None
