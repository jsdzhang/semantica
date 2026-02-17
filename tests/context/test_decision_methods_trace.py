"""Tests for decision trace capture convenience API."""

from datetime import datetime
from unittest.mock import Mock

from semantica.context.decision_methods import capture_decision_trace
from semantica.context.decision_models import Decision


def _sample_decision() -> Decision:
    return Decision(
        decision_id="decision_trace_test_001",
        category="credit_approval",
        scenario="Credit line increase for long-term customer",
        reasoning="Strong payment history and low utilization",
        outcome="approved",
        confidence=0.92,
        timestamp=datetime.now(),
        decision_maker="ai_agent",
    )


def test_capture_decision_trace_without_graph_store_is_backward_compatible():
    decision = _sample_decision()
    decision_id = capture_decision_trace(decision, cross_system_context={})
    assert decision_id == decision.decision_id


def test_capture_decision_trace_with_graph_store_records_trace_events():
    decision = _sample_decision()
    graph_store = Mock()
    graph_store.execute_query = Mock(return_value=[])

    decision_id = capture_decision_trace(
        decision=decision,
        cross_system_context={"crm": {"arr": 120000}},
        graph_store=graph_store,
        entities=["customer_123"],
        source_documents=["renewal_note_001"],
        policy_ids=["renewal_discount_policy_v3_2"],
        approvals=[
            {
                "approver": "vp_finance",
                "approval_method": "slack_dm",
                "approval_context": "Approved due to SEV-1 impact history",
            }
        ],
        precedents=[
            {
                "precedent_id": "decision_legacy_001",
                "relationship_type": "similar_scenario",
            }
        ],
        immutable_audit_log=True,
    )

    assert decision_id == decision.decision_id
    assert graph_store.execute_query.call_count > 0
