import pytest

from event_ticket_tier import (
    process_ticket_manifest,
    monitor_gate_flow,
)


def test_invalid_manifest_input():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_unconfirmed_manifest_is_skipped():
    result = process_ticket_manifest(
        [{"is_confirmed": False, "tier": "vip"}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_all_ticket_tiers():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "vip",
            "orders": [{"qty": 1, "promo": ""}],
        },
        {
            "is_confirmed": True,
            "tier": "premium",
            "orders": [{"qty": 1, "promo": ""}],
        },
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 1, "promo": ""}],
        },
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 285.0


def test_unknown_ticket_tier_is_rejected():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "gold", "orders": []}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_invalid_quantity_is_rejected():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 0}],
        }],
        0,
    )
    assert result["status"] == "ZERO_SALES"


def test_earlybird_discount():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 2, "promo": "EARLYBIRD"}],
        }],
        0,
    )
    assert result["total_revenue"] == 72.0


def test_bulk_order_discount():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 5, "promo": ""}],
        }],
        0,
    )
    assert result["total_revenue"] == 205.0


def test_fraudulent_vip_order_resets_manifest_total():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "vip",
            "orders": [
                {"qty": 2, "promo": ""},
                {"qty": 1, "promo": "FRAUD_RISK"},
            ],
        }],
        0,
    )
    assert result["status"] == "ZERO_SALES"


def test_fraudulent_non_vip_order_is_rejected():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "general",
            "orders": [
                {"qty": 2, "promo": "FRAUD_RISK"},
                {"qty": 1, "promo": ""},
            ],
        }],
        0,
    )
    assert result["total_revenue"] == 135.0


def test_exclusive_lounge_charge():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "general",
            "exclusive_lounge": True,
            "orders": [{"qty": 1, "promo": ""}],
        }],
        0,
    )
    assert result["total_revenue"] == 120.0


def test_service_tax_is_applied():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 2, "promo": ""}],
        }],
        0.1,
    )
    assert result["total_revenue"] == 99.0


def test_audit_rejected_after_more_than_four_rejections():
    result = process_ticket_manifest(
        [{
            "is_confirmed": True,
            "tier": "unknown",
        }] * 5,
        0.1,
    )
    assert result["status"] == "AUDIT_REJECTED"


def test_empty_manifest_returns_zero_sales():
    result = process_ticket_manifest([], 0.1)
    assert result == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES",
    }


def test_gate_flow_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_flow_normal():
    assert monitor_gate_flow([[20, 30, 40]]) == "FLOW_NORMAL"


def test_gate_flow_overflow():
    assert monitor_gate_flow([[60, 70]]) == "OVERFLOW"


def test_gate_flow_congestion_streak_resets():
    assert monitor_gate_flow([[60, 30, 60, 70]]) == "OVERFLOW"