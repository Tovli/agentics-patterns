from __future__ import annotations

import hashlib
import json
import math
from typing import Any


TRUSTED_CONFIDENCE_DECISIONS = (
    "present",
    "gather_more_evidence",
    "pivot_strategy",
    "signal_uncertainty",
)
TERMINAL_CONFIDENCE_DECISIONS = {"present", "signal_uncertainty"}
NONTERMINAL_CONFIDENCE_DECISIONS = {"gather_more_evidence", "pivot_strategy"}
TRUSTED_POLICY_GATE_BINDINGS = {
    "Responses below the presentation threshold must gather more evidence or explicitly signal uncertainty.": "confidence_gate",
    "Stagnation must trigger metaplanning and failed approaches must not be repeated.": "stagnation_recovery",
    "Outside the known knowledge boundary, the agent must degrade gracefully instead of guessing.": "knowledge_boundary",
    "Memory records only evaluated, distilled, non-sensitive lessons.": "memory_safety",
}
EXAMPLE_OUTPUT_KEYS = {
    "required_explicit_fields",
    "stagnation_recovery_required",
    "field_values",
    "policy_verdict",
}
POLICY_VERDICT_KEYS = {"allowed", "gates_checked", "blocked_actions", "notes"}
MEMORY_UPDATE_KEYS = {
    "responsible_agent",
    "terminal_evaluation_reference",
    "distilled_lesson",
    "applicability_conditions",
    "uncertainty",
    "excluded_sensitive_raw_data",
    "record_status",
    "rejection_reason",
}
MEMORY_RECORD_STATUSES = {"stored", "rejected"}


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


def non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def require_text(value: Any, label: str) -> str:
    if not non_empty_text(value):
        raise ValueError(f"{label} must be a non-empty string")
    return value


def require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if (
        not isinstance(value, list)
        or any(not non_empty_text(item) for item in value)
        or (not allow_empty and not value)
    ):
        raise ValueError(f"{label} must be a list of strings")
    return value


def require_probability(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} confidence must be a real finite number")
    if not 0 <= value <= 1:
        raise ValueError(f"{label} confidence must be between 0 and 1")
    return value


def require_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-bool integer greater than or equal to zero")
    return value


def require_positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{label} must be a positive non-bool integer")
    return value


def validate_example_fields(
    fields: dict[str, Any],
    input_payload: dict[str, Any],
    example_output: dict[str, Any],
) -> None:
    required_explicit_fields = example_output.get("required_explicit_fields", [])
    for field in required_explicit_fields:
        require_object(fields.get(field), field)

    prior_attempts = require_string_list(
        input_payload.get("prior_attempts"),
        "prior_attempts",
        allow_empty=True,
    )
    available_strategies = require_string_list(
        input_payload.get("available_strategies"),
        "available_strategies",
    )

    perception = require_object(fields.get("perception"), "perception")
    initial_confidence = require_probability(perception.get("initial_confidence"), "initial")

    attention = require_object(fields.get("attention_route"), "attention_route")
    destination = require_text(attention.get("destination"), "attention_route.destination")

    strategy = require_object(fields.get("selected_strategy"), "selected_strategy")
    strategy_name = require_text(strategy.get("strategy"), "selected_strategy.strategy")
    strategy_exclusions = require_string_list(
        strategy.get("excluded_failed_approaches"),
        "excluded_failed_approaches",
        allow_empty=not prior_attempts,
    )
    require_text(strategy.get("bounded_step"), "selected_strategy.bounded_step")

    execution = require_object(fields.get("execution_evidence"), "execution_evidence")
    tool_calls_used = require_nonnegative_int(
        execution.get("tool_calls_used"),
        "execution_evidence.tool_calls_used",
    )
    budget = require_object(input_payload.get("budget"), "budget")
    max_tool_calls = require_nonnegative_int(budget.get("max_tool_calls"), "budget.max_tool_calls")
    max_iterations = require_positive_int(
        budget.get("max_iterations"),
        "budget.max_iterations",
    )
    if tool_calls_used > max_tool_calls:
        raise ValueError("execution_evidence.tool_calls_used exceeds max_tool_calls")

    evaluation = require_object(fields.get("evaluation"), "evaluation")
    if not isinstance(evaluation.get("terminal"), bool):
        raise ValueError("evaluation.terminal must be boolean")
    iterations_used = require_positive_int(
        evaluation.get("iterations_used"),
        "evaluation.iterations_used",
    )
    if iterations_used > max_iterations:
        raise ValueError("evaluation.iterations_used exceeds max_iterations")
    evaluation_confidence = require_probability(
        evaluation.get("observed_confidence"),
        "evaluation observed",
    )
    confidence_trend = evaluation.get("confidence_trend")
    if not isinstance(confidence_trend, list) or not confidence_trend:
        raise ValueError("evaluation.confidence_trend must be a list of confidence values")
    for value in confidence_trend:
        require_probability(value, "evaluation trend")
    if confidence_trend[0] != initial_confidence:
        raise ValueError("confidence trend must start at initial confidence")
    if confidence_trend[-1] != evaluation_confidence:
        raise ValueError("confidence trend must end at evaluation observed confidence")

    decision = require_object(fields.get("confidence_gate_decision"), "confidence_gate_decision")
    if decision.get("decision_enum") != list(TRUSTED_CONFIDENCE_DECISIONS):
        raise ValueError("confidence gate must declare the trusted confidence decision enum")
    decision_name = decision.get("decision")
    if decision_name not in TRUSTED_CONFIDENCE_DECISIONS:
        raise ValueError("confidence gate decision must use the trusted confidence decision enum")
    observed = require_probability(decision.get("observed_confidence"), "observed")
    threshold = require_probability(decision.get("presentation_threshold"), "presentation threshold")
    if evaluation_confidence != observed:
        raise ValueError("evaluation confidence must equal confidence gate confidence")
    threshold_satisfied = observed >= threshold
    if not isinstance(decision.get("threshold_satisfied"), bool):
        raise ValueError("confidence_gate_decision.threshold_satisfied must be boolean")
    if decision["threshold_satisfied"] is not threshold_satisfied:
        raise ValueError("confidence gate threshold comparison is inconsistent")
    confidence_thresholds = require_object(
        input_payload.get("confidence_thresholds"),
        "confidence_thresholds",
    )
    for name, value in confidence_thresholds.items():
        require_probability(value, str(name))
    declared_threshold = require_probability(
        confidence_thresholds.get("present"),
        "declared presentation threshold",
    )
    if threshold != declared_threshold:
        raise ValueError("confidence gate must use the input presentation threshold")
    gather_more_threshold = confidence_thresholds.get("gather_more")
    if gather_more_threshold is None:
        raise ValueError("confidence_thresholds requires gather_more")
    if gather_more_threshold > declared_threshold:
        raise ValueError("gather_more threshold must be less than or equal to present threshold")
    if decision_name == "present":
        if not threshold_satisfied:
            raise ValueError("output cannot be presented below the presentation threshold")
    if decision_name in TERMINAL_CONFIDENCE_DECISIONS and evaluation["terminal"] is not True:
        raise ValueError("terminal decision requires a terminal evaluation")
    if decision_name in NONTERMINAL_CONFIDENCE_DECISIONS and evaluation["terminal"] is not False:
        raise ValueError("nonterminal decision requires a nonterminal evaluation")

    recovery_required = example_output.get("stagnation_recovery_required", False)
    if not isinstance(recovery_required, bool):
        raise ValueError("stagnation_recovery_required must be boolean")
    stagnation = require_object(fields.get("stagnation_response"), "stagnation_response")
    if recovery_required:
        if stagnation.get("detected") is not True:
            raise ValueError("stagnation recovery requires detected=true")
        if stagnation.get("route") != "metaplanning":
            raise ValueError("stagnation must route to metaplanning")
        if destination != "metaplanning":
            raise ValueError("attention route must target metaplanning during stagnation recovery")
        if strategy_name in prior_attempts:
            raise ValueError("selected strategy must not repeat a prior attempt")
        if strategy_name not in available_strategies:
            raise ValueError("selected strategy must be available")
        stagnation_exclusions = require_string_list(
            stagnation.get("excluded_failed_approaches"),
            "excluded_failed_approaches",
            allow_empty=not prior_attempts,
        )
        if any(attempt not in stagnation_exclusions for attempt in prior_attempts):
            raise ValueError("stagnation response must exclude every prior attempt")
        if any(attempt not in strategy_exclusions for attempt in prior_attempts):
            raise ValueError("selected strategy exclusions must cover every prior attempt")

    boundary = require_object(fields.get("knowledge_boundary"), "knowledge_boundary")
    for partition in ["supported_claims", "uncertain_claims", "out_of_bound_claims"]:
        require_string_list(boundary.get(partition), partition)
    if not non_empty_text(boundary.get("graceful_degradation")):
        raise ValueError("knowledge boundary requires non-empty graceful_degradation")

    memory = require_object(fields.get("memory_update"), "memory_update")
    unknown_memory_keys = set(memory) - MEMORY_UPDATE_KEYS
    if unknown_memory_keys:
        raise ValueError(f"unknown memory_update keys: {sorted(unknown_memory_keys)}")
    record_status = require_text(memory.get("record_status"), "memory_update.record_status")
    if record_status not in MEMORY_RECORD_STATUSES:
        raise ValueError("memory_update.record_status must be one of stored, rejected")
    if "rejection_reason" in memory:
        require_text(memory["rejection_reason"], "memory_update.rejection_reason")
    if decision_name in NONTERMINAL_CONFIDENCE_DECISIONS and record_status == "stored":
        raise ValueError("nonterminal decision cannot store memory")
    if decision_name in NONTERMINAL_CONFIDENCE_DECISIONS and record_status != "rejected":
        raise ValueError("nonterminal decision requires rejected memory")
    if record_status == "stored":
        if evaluation["terminal"] is not True:
            raise ValueError("stored memory requires a terminal evaluation")
        if decision_name not in TERMINAL_CONFIDENCE_DECISIONS:
            raise ValueError("stored memory requires a terminal decision")
        evaluation_id = require_text(evaluation.get("evaluation_id"), "evaluation.evaluation_id")
        memory_reference = require_text(
            memory.get("terminal_evaluation_reference"),
            "memory_update.terminal_evaluation_reference",
        )
        if memory_reference != evaluation_id:
            raise ValueError("memory update must reference the terminal evaluation")
        require_text(memory.get("distilled_lesson"), "memory_update.distilled_lesson")
        require_string_list(memory.get("applicability_conditions"), "applicability_conditions")
        require_string_list(memory.get("uncertainty"), "uncertainty")
        require_string_list(
            memory.get("excluded_sensitive_raw_data"),
            "excluded_sensitive_raw_data",
        )


def validate_policy_declaration(
    flow: dict[str, Any],
    example_output: dict[str, Any],
    explicit_fields: dict[str, Any],
) -> dict[str, Any] | None:
    verdict = example_output.get("policy_verdict")
    if verdict is None:
        return None
    verdict = require_object(verdict, "example_output.policy_verdict")
    unknown_verdict_keys = set(verdict) - POLICY_VERDICT_KEYS
    if unknown_verdict_keys:
        raise ValueError(f"unknown policy_verdict keys: {sorted(unknown_verdict_keys)}")
    if not isinstance(verdict.get("allowed"), bool):
        raise ValueError("explicit policy verdict allowed must be boolean")
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

    blocked_actions = verdict.get("blocked_actions")
    if not isinstance(blocked_actions, list) or not blocked_actions:
        raise ValueError("explicit policy verdict must record blocked unsafe actions")
    for item in blocked_actions:
        if (
            not isinstance(item, dict)
            or not non_empty_text(item.get("action"))
            or not non_empty_text(item.get("reason"))
        ):
            raise ValueError("each blocked action requires a non-empty action and reason")
    return {key: value for key, value in verdict.items() if key != "allow_evidence"}


def derive_policy_evidence(
    flow: dict[str, Any],
    fields: dict[str, Any],
) -> list[dict[str, str]]:
    evidence = []
    for gate in flow["policy_gates"]:
        kind = TRUSTED_POLICY_GATE_BINDINGS.get(gate)
        if kind is None:
            raise ValueError(f"unknown policy gate: {gate}")
        if kind == "confidence_gate":
            decision = fields["confidence_gate_decision"]
            detail = (
                f"decision={decision['decision']}; observed_confidence={decision['observed_confidence']}; "
                f"presentation_threshold={decision['presentation_threshold']}; "
                f"threshold_satisfied={decision['threshold_satisfied']}"
            )
        elif kind == "stagnation_recovery":
            stagnation = fields["stagnation_response"]
            detail = (
                f"detected={stagnation['detected']}; route={stagnation['route']}; "
                f"excluded_failed_approaches={len(stagnation['excluded_failed_approaches'])}"
            )
        elif kind == "knowledge_boundary":
            boundary = fields["knowledge_boundary"]
            detail = (
                f"supported={len(boundary['supported_claims'])}; uncertain={len(boundary['uncertain_claims'])}; "
                f"out_of_bound={len(boundary['out_of_bound_claims'])}; "
                f"graceful_degradation={boundary['graceful_degradation']}"
            )
        else:
            memory = fields["memory_update"]
            detail = (
                f"record_status={memory['record_status']}; "
                f"terminal_evaluation_reference={memory.get('terminal_evaluation_reference', 'none')}; "
                f"excluded_sensitive_raw_data={len(memory.get('excluded_sensitive_raw_data', []))}"
            )
        evidence.append({"gate": gate, "kind": kind, "evidence": detail})
    return evidence


def build_output(flow: dict[str, Any], input_payload: dict[str, Any]) -> dict[str, Any]:
    required_fields = flow["output_contract"]["required_fields"]
    has_example_output = "example_output" in flow
    example_output = flow.get("example_output", {})
    if has_example_output and not isinstance(example_output, dict):
        raise ValueError("example_output must be an object")
    unknown_example_output_keys = set(example_output) - EXAMPLE_OUTPUT_KEYS
    if unknown_example_output_keys:
        raise ValueError(f"unknown example_output keys: {sorted(unknown_example_output_keys)}")
    if has_example_output:
        required_explicit_fields = require_string_list(
            example_output.get("required_explicit_fields"),
            "required_explicit_fields",
        )
        if len(required_explicit_fields) != len(set(required_explicit_fields)):
            raise ValueError("required_explicit_fields must not contain duplicates")
        if not isinstance(example_output.get("stagnation_recovery_required"), bool):
            raise ValueError("stagnation_recovery_required must be boolean")
    explicit_fields = example_output.get("field_values", {})
    if not isinstance(explicit_fields, dict):
        raise ValueError("example_output.field_values must be an object")
    unexpected_fields = set(explicit_fields) - set(required_fields)
    if unexpected_fields:
        raise ValueError(f"Explicit values provided for non-contract fields: {sorted(unexpected_fields)}")
    policy_verdict = validate_policy_declaration(flow, example_output, explicit_fields)
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
    elif policy_verdict["allowed"]:
        policy_verdict["allow_evidence"] = derive_policy_evidence(
            flow,
            fields,
        )
    allowed = policy_verdict["allowed"]
    subject = scenario_subject(input_payload, flow)
    output = {
        "artifact_type": flow["output_contract"]["artifact_type"],
        "example_id": flow["id"],
        "status": "ready_for_review" if allowed else "blocked_by_policy",
        "summary": (
            f"{flow['name']} example completed for {subject}."
            if allowed
            else f"{flow['name']} example blocked by policy for {subject}."
        ),
        "fields": fields,
        "policy_verdict": policy_verdict,
    }
    output["receipt"] = {
        "required": bool(flow.get("receipt", {}).get("required", False)),
        "input_hash": digest(input_payload),
        "flow_hash": digest(flow),
        "output_hash": digest(output),
        "reviewer_verdict": "accepted_for_example" if allowed else "rejected_by_policy",
    }
    return output
