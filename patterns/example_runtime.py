from __future__ import annotations

import hashlib
import json
from typing import Any


TRUSTED_CONFIDENCE_DECISIONS = (
    "present",
    "gather_more_evidence",
    "pivot_strategy",
    "signal_uncertainty",
)


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
            "kernel",
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


def validate_example_fields(
    fields: dict[str, Any],
    input_payload: dict[str, Any],
    example_output: dict[str, Any],
) -> None:
    decision = fields.get("confidence_gate_decision")
    if decision is not None:
        if decision.get("decision_enum") != list(TRUSTED_CONFIDENCE_DECISIONS):
            raise ValueError("confidence gate must declare the trusted confidence decision enum")
        if decision.get("decision") not in TRUSTED_CONFIDENCE_DECISIONS:
            raise ValueError("confidence gate decision must use the trusted confidence decision enum")
        observed = decision.get("observed_confidence")
        threshold = decision.get("presentation_threshold")
        if not isinstance(observed, (int, float)) or not isinstance(threshold, (int, float)):
            raise ValueError("confidence gate decision requires numeric observed confidence and threshold")
        threshold_satisfied = observed >= threshold
        if decision.get("threshold_satisfied") is not threshold_satisfied:
            raise ValueError("confidence gate threshold comparison is inconsistent")
        declared_threshold = input_payload.get("confidence_thresholds", {}).get("present")
        if declared_threshold is not None and threshold != declared_threshold:
            raise ValueError("confidence gate must use the input presentation threshold")
        if decision["decision"] == "present" and not threshold_satisfied:
            raise ValueError("output cannot be presented below the presentation threshold")

    recovery_required = example_output.get("stagnation_recovery_required", False)
    if not isinstance(recovery_required, bool):
        raise ValueError("stagnation_recovery_required must be boolean")
    stagnation = fields.get("stagnation_response")
    if recovery_required:
        if not isinstance(stagnation, dict) or stagnation.get("detected") is not True:
            raise ValueError("stagnation recovery requires detected=true")
    if isinstance(stagnation, dict) and (recovery_required or stagnation.get("detected") is True):
        if stagnation.get("route") != "metaplanning":
            raise ValueError("stagnation must route to metaplanning")
        excluded = stagnation.get("excluded_failed_approaches", [])
        missing_exclusions = [
            attempt for attempt in input_payload.get("prior_attempts", [])
            if attempt not in excluded
        ]
        if missing_exclusions:
            raise ValueError("stagnation response must exclude every failed approach")

    boundary = fields.get("knowledge_boundary")
    if boundary is not None:
        for partition in ["supported_claims", "uncertain_claims", "out_of_bound_claims"]:
            if not boundary.get(partition):
                raise ValueError(f"knowledge boundary requires a non-empty {partition} partition")

    memory = fields.get("memory_update")
    if memory is not None:
        required_memory_values = [
            "terminal_evaluation_reference",
            "distilled_lesson",
            "applicability_conditions",
            "uncertainty",
            "excluded_sensitive_raw_data",
        ]
        for key in required_memory_values:
            if not memory.get(key):
                raise ValueError(f"memory update requires {key}")
        evaluation = fields.get("evaluation", {})
        if not evaluation.get("terminal"):
            raise ValueError("memory update requires a terminal evaluation")
        if memory["terminal_evaluation_reference"] != evaluation.get("evaluation_id"):
            raise ValueError("memory update must reference the terminal evaluation")


def non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def explicit_policy_verdict(
    flow: dict[str, Any],
    example_output: dict[str, Any],
    explicit_fields: dict[str, Any],
) -> dict[str, Any] | None:
    verdict = example_output.get("policy_verdict")
    if verdict is None:
        return None
    if verdict.get("gates_checked") != flow["policy_gates"]:
        raise ValueError("explicit policy verdict must check every declared gate in order")
    if verdict.get("allowed"):
        required_explicit_fields = example_output.get("required_explicit_fields")
        if not isinstance(required_explicit_fields, list) or not required_explicit_fields:
            raise ValueError("allowed policy verdict requires a non-empty required_explicit_fields contract")
        non_contract_fields = set(required_explicit_fields) - set(
            flow["output_contract"]["required_fields"]
        )
        if non_contract_fields:
            raise ValueError(f"required_explicit_fields contains non-contract fields: {sorted(non_contract_fields)}")
        missing_explicit_fields = set(required_explicit_fields) - set(explicit_fields)
        if missing_explicit_fields:
            raise ValueError(
                f"allowed policy verdict is missing required explicit fields: {sorted(missing_explicit_fields)}"
            )

        evidence = verdict.get("allow_evidence", [])
        if not isinstance(evidence, list) or len(evidence) != len(flow["policy_gates"]):
            raise ValueError(
                "allowed policy verdict requires exactly one evidence record per declared gate"
            )
        for gate in flow["policy_gates"]:
            gate_evidence = [
                item
                for item in evidence
                if isinstance(item, dict) and item.get("gate") == gate
            ]
            if len(gate_evidence) != 1:
                raise ValueError(
                    "allowed policy verdict requires exactly one evidence record per declared gate"
                )
            if not non_empty_text(gate_evidence[0].get("evidence")):
                raise ValueError("each policy gate requires non-empty evidence")

        blocked_actions = verdict.get("blocked_actions")
        if not isinstance(blocked_actions, list) or not blocked_actions:
            raise ValueError("allowed policy verdict must record blocked unsafe actions")
        for item in blocked_actions:
            if (
                not isinstance(item, dict)
                or not non_empty_text(item.get("action"))
                or not non_empty_text(item.get("reason"))
            ):
                raise ValueError("each blocked action requires a non-empty action and reason")
    return verdict


def build_output(flow: dict[str, Any], input_payload: dict[str, Any]) -> dict[str, Any]:
    required_fields = flow["output_contract"]["required_fields"]
    has_example_output = "example_output" in flow
    example_output = flow.get("example_output", {})
    if has_example_output and not isinstance(example_output, dict):
        raise ValueError("example_output must be an object")
    explicit_fields = example_output.get("field_values", {})
    if not isinstance(explicit_fields, dict):
        raise ValueError("example_output.field_values must be an object")
    unexpected_fields = set(explicit_fields) - set(required_fields)
    if unexpected_fields:
        raise ValueError(f"Explicit values provided for non-contract fields: {sorted(unexpected_fields)}")
    policy_verdict = explicit_policy_verdict(flow, example_output, explicit_fields)
    fields = {
        field: explicit_fields[field] if field in explicit_fields else field_value(field, input_payload, flow)
        for field in required_fields
    }
    if has_example_output:
        validate_example_fields(fields, input_payload, example_output)
    if policy_verdict is None:
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
