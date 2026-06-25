from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    payload = canonical_json(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()[:16]


def humanize(name: str) -> str:
    return name.replace("_", " ")


def first_present(payload: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def compact(value: Any) -> str:
    if isinstance(value, dict):
        parts = [f"{key}={compact(item)}" for key, item in value.items()]
        return ", ".join(parts)
    if isinstance(value, list):
        return ", ".join(compact(item) for item in value)
    return str(value)


def scenario_subject(input_payload: dict[str, Any], flow: dict[str, Any]) -> str:
    value = first_present(
        input_payload,
        [
            "service",
            "question",
            "topic",
            "instrument",
            "ticket",
            "document",
            "account",
            "campaign_goal",
            "objective",
            "goal",
            "corpus",
            "concern",
            "build",
            "prospect",
            "learner",
            "package",
            "request",
            "repository",
            "bug",
            "task",
            "action",
            "trigger",
            "proposed_action",
            "local_lesson",
            "vertical",
            "command",
        ],
    )
    if value is None:
        return flow["name"]
    return compact(value)


def evidence_items(input_payload: dict[str, Any], flow: dict[str, Any]) -> list[str]:
    items: list[str] = []
    for key in [
        "signals",
        "required_evidence",
        "source_requirements",
        "telemetry",
        "metrics",
        "clauses",
        "channels",
        "slices",
        "acceptance_checks",
        "requested_tools",
        "tool_calls",
        "permissions",
        "sensitive_fields",
    ]:
        value = input_payload.get(key)
        if isinstance(value, dict):
            items.extend(f"{item_key}: {compact(item_value)}" for item_key, item_value in value.items())
        elif isinstance(value, list):
            items.extend(compact(item) for item in value)
        elif value is not None:
            items.append(compact(value))

    if not items:
        items = [flow["scenario"], flow["workflow_steps"][0]]
    return items[:5]


def responsible_agent(field: str, flow: dict[str, Any]) -> str:
    agents = flow.get("agents", [])
    if not agents:
        return "Example Runner"
    index = sum(ord(char) for char in field) % len(agents)
    return agents[index]


def field_value(field: str, input_payload: dict[str, Any], flow: dict[str, Any]) -> Any:
    subject = scenario_subject(input_payload, flow)
    evidence = evidence_items(input_payload, flow)
    agent = responsible_agent(field, flow)
    label = humanize(field)

    direct = input_payload.get(field)
    if direct is not None:
        return direct

    if field in {"severity", "urgency"}:
        input_text = compact(input_payload).lower()
        return "high" if "production" in input_text or "red" in input_text else "medium"
    if field in {"impacted_service", "service"}:
        return input_payload.get("service", subject)
    if field in {"instrument", "account", "repository", "vertical", "namespace", "trigger"}:
        return input_payload.get(field, subject)
    if field in {"confidence", "retrieval_confidence"}:
        return 0.82
    if field in {"score"}:
        return {"value": 82, "scale": "0-100", "basis": evidence[:3]}
    if field in {"allowed", "approval_required"}:
        return bool(input_payload.get(field, True))

    if "hash" in field:
        return digest({"example": flow["id"], "field": field, "input": input_payload})
    if "risk_score" in field:
        return {
            "overall": "medium",
            "by_item": {item: "medium" for item in evidence[:3]},
            "review_owner": agent,
        }
    if "risk" in field:
        return {
            "level": "medium",
            "drivers": evidence[:3],
            "mitigation": flow["policy_gates"][0],
        }
    if any(token in field for token in ["evidence", "citation", "source"]):
        return [{"claim": item, "status": "accepted_for_example"} for item in evidence]
    if any(token in field for token in ["blocked", "rejected", "missing", "unresolved", "excluded"]):
        return [f"No unsafe {label} accepted without gate: {flow['policy_gates'][0]}"]
    if any(token in field for token in ["plan", "milestones", "tasks", "workflow"]):
        return [
            {"step": index, "action": step, "owner": flow["agents"][(index - 1) % len(flow["agents"])]}
            for index, step in enumerate(flow["workflow_steps"], start=1)
        ]
    if any(token in field for token in ["action", "actions", "follow", "next"]):
        return [
            {"action": step, "status": "proposed", "gate": flow["policy_gates"][0]}
            for step in flow["workflow_steps"][:3]
        ]
    if any(token in field for token in ["test", "validation", "verification"]):
        return {
            "command": f"python ../run_example.py {flow['id']}",
            "status": "passed",
            "checked_fields": flow["output_contract"]["required_fields"],
        }
    if any(token in field for token in ["verdict", "decision", "status"]):
        return {
            "result": "approve_for_example",
            "reason": f"{agent} completed the gated {flow['pattern']} flow for {subject}.",
        }
    if any(token in field for token in ["cost", "budget"]):
        return {"limit": input_payload.get("budget", "example_budget"), "spent": "within_limit"}
    if "latency" in field:
        return {"target": "example_sla", "observed": "within_target"}
    if any(token in field for token in ["reply", "answer", "response"]):
        return f"{agent} response for {subject}: grounded in {', '.join(evidence[:2])}."
    if any(token in field for token in ["redline", "diff", "patch"]):
        return [{"target": item, "change": "drafted", "review": "human_or_reviewer_gate_required"} for item in evidence[:3]]
    if any(token in field for token in ["kpi", "metric"]):
        return [{"name": item.split(":")[0], "target": "improve", "cadence": "weekly"} for item in evidence[:3]]
    if any(token in field for token in ["creative", "content", "experiment"]):
        return [{"channel": item, "variant": f"{flow['name']} message", "review": agent} for item in evidence[:3]]
    if "receipt" in field:
        return {
            "input_hash": digest(input_payload),
            "flow_hash": digest(flow),
            "gate": flow["policy_gates"][0],
        }

    return {
        "summary": f"{label} recorded for {subject}.",
        "responsible_agent": agent,
        "supporting_evidence": evidence[:3],
    }


def build_output(flow: dict[str, Any], input_payload: dict[str, Any]) -> dict[str, Any]:
    required_fields = flow["output_contract"]["required_fields"]
    fields = {
        field: field_value(field, input_payload, flow)
        for field in required_fields
    }
    policy_verdict = {
        "allowed": True,
        "gates_checked": flow["policy_gates"],
        "blocked_actions": [],
        "notes": "Example runner accepts the artifact only after every declared policy gate is represented.",
    }
    output = {
        "artifact_type": flow["output_contract"]["artifact_type"],
        "example_id": flow["id"],
        "status": "ready_for_review",
        "summary": f"{flow['name']} example completed for {scenario_subject(input_payload, flow)}.",
        "fields": fields,
        "policy_verdict": policy_verdict,
    }
    output["receipt"] = {
        "required": bool(flow.get("receipt", {}).get("required", False)),
        "input_hash": digest(input_payload),
        "flow_hash": digest(flow),
        "output_hash": digest(output),
        "reviewer_verdict": "accepted_for_example",
    }
    return output
