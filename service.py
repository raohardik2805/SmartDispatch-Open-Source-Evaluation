"""Dispatch ETA, partner selection, and cancellation helpers."""
from copy import deepcopy
import math


def _valid_minutes(value):
    """Return whether value is a finite, non-negative number (excluding bool)."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value) and value >= 0
    except (OverflowError, TypeError, ValueError):
        return False


def _valid_identifier(value):
    return isinstance(value, str) and bool(value.strip())


def _ineligible(partner):
    partner_id = partner.get("partner_id") if isinstance(partner, dict) else None
    return {"partner_id": partner_id, "pickup_minutes": None,
            "eta_minutes": None, "eligible": False}


def estimate_eta(order, partner, travel, now=0):
    """Estimate pickup and delivery time; missing/invalid inputs are ineligible."""
    if not isinstance(order, dict) or not isinstance(partner, dict) or not isinstance(travel, dict):
        return _ineligible(partner)
    required_order_fields = ("order_id", "restaurant_id", "destination_zone")
    if not all(_valid_identifier(order.get(field)) for field in required_order_fields):
        return _ineligible(partner)
    if not _valid_identifier(partner.get("partner_id")) or not _valid_identifier(partner.get("zone")):
        return _ineligible(partner)

    prep = order.get("prep_minutes")
    workload = partner.get("workload_minutes", 0)
    if not all(_valid_minutes(value) for value in (now, prep, workload)):
        return _ineligible(partner)

    leg1 = travel.get((partner["zone"], order["restaurant_id"]))
    leg2 = travel.get((order["restaurant_id"], order["destination_zone"]))
    if not _valid_minutes(leg1) or not _valid_minutes(leg2):
        return _ineligible(partner)

    pickup = now + leg1 + workload
    eta = pickup + prep + leg2
    if not _valid_minutes(pickup) or not _valid_minutes(eta):
        return _ineligible(partner)
    return {"partner_id": partner["partner_id"], "pickup_minutes": pickup,
            "eta_minutes": eta, "eligible": True}


def assign_order(order, partners, travel, now=0):
    """Choose the lowest-ETA active partner with spare capacity."""
    order_id = order.get("order_id") if isinstance(order, dict) else None
    if not isinstance(partners, (list, tuple)):
        partners = ()
    options = []
    for partner in partners:
        if not isinstance(partner, dict) or partner.get("active") is not True:
            continue
        capacity = partner.get("capacity")
        active_orders = partner.get("active_order_ids", [])
        if (not isinstance(capacity, int) or isinstance(capacity, bool)
                or capacity < 1 or not isinstance(active_orders, list)
                or len(active_orders) >= capacity):
            continue
        estimate = estimate_eta(order, partner, travel, now)
        if estimate["eligible"]:
            options.append(estimate)

    if not options:
        return {"order_id": order_id, "partner_id": None, "pickup_minutes": None,
                "eta_minutes": None, "reason": "no eligible partner or missing time data"}
    chosen = min(options, key=lambda item: (item["eta_minutes"], item["partner_id"]))
    return {"order_id": order_id, "partner_id": chosen["partner_id"],
            "pickup_minutes": chosen["pickup_minutes"], "eta_minutes": chosen["eta_minutes"],
            "reason": "assigned"}


def process_cancellation(partner, order_id, event_id):
    """Apply a cancellation once per event ID and never release workload twice."""
    if not isinstance(partner, dict):
        return partner
    out = deepcopy(partner)
    active_orders = out.setdefault("active_order_ids", [])
    processed = out.setdefault("processed_cancellation_ids", [])
    if not isinstance(active_orders, list):
        active_orders = []
        out["active_order_ids"] = active_orders
    if not isinstance(processed, list):
        processed = []
        out["processed_cancellation_ids"] = processed

    # A repeated event ID is a replay, even if its payload differs.
    if event_id is not None and event_id in processed:
        return out

    if order_id in active_orders:
        active_orders.remove(order_id)
        minutes_by_order = out.get("minutes_by_order", {})
        minutes = minutes_by_order.get(order_id, 0) if isinstance(minutes_by_order, dict) else 0
        workload = out.get("workload_minutes", 0)
        if not _valid_minutes(workload):
            workload = 0
        if not _valid_minutes(minutes):
            minutes = 0
        out["workload_minutes"] = max(0, workload - minutes)

    if event_id is not None:
        processed.append(event_id)
    return out
