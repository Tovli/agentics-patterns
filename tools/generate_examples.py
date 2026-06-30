from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "patterns"
STATUS = ROOT / "EXAMPLE_STATUS.md"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from patterns.example_runtime import build_output


def example(
    id: str,
    section: str,
    number: int,
    name: str,
    pattern: str,
    scenario: str,
    agents: list[str],
    workflow_steps: list[str],
    policy_gates: list[str],
    input_payload: dict,
    artifact_type: str,
    output_fields: list[str],
    reference: dict | None = None,
) -> dict:
    spec = {
        "id": id,
        "section": section,
        "number": number,
        "name": name,
        "pattern": pattern,
        "scenario": scenario,
        "agents": agents,
        "workflow_steps": workflow_steps,
        "policy_gates": policy_gates,
        "input": input_payload,
        "output_contract": {
            "artifact_type": artifact_type,
            "required_fields": output_fields,
        },
    }
    if reference is not None:
        spec["reference"] = reference
    return spec


SPECS = [
    example(
        "minimal-base-harness",
        "catalog",
        0,
        "Minimal base harness",
        "Kernel smoke-test scaffold",
        "A new package scaffold needs a single doctor command before any domain agents are added.",
        ["Harness Doctor"],
        [
            "Initialize the harness workspace.",
            "Load the kernel and host adapter.",
            "Check MCP wiring, memory backend, and host adapter health.",
            "Return one PASS/FAIL report with remediation hints.",
        ],
        ["No domain action is allowed from the minimal scaffold."],
        {
            "command": "doctor",
            "workspace": "new-harness",
            "checks": ["kernel", "mcp", "memory", "host_adapter"],
        },
        "doctor_report",
        ["overall_status", "checks", "failed_checks", "remediation"],
    ),
    example(
        "devops-incident-response",
        "catalog",
        1,
        "DevOps incident response",
        "Alert -> runbook -> gated action -> escalation -> postmortem",
        "Checkout latency crosses the paging threshold while database saturation is suspected.",
        ["Responder", "Runbook Runner", "Policy Gate", "Escalator", "Postmortem Writer"],
        [
            "Classify alert severity and impacted service.",
            "Find the closest runbook and propose bounded diagnostics.",
            "Gate shell, network, and kubectl actions before execution.",
            "Escalate when severity or uncertainty crosses policy.",
            "Draft timeline, root cause, contributing factors, and follow-ups.",
        ],
        [
            "Production mutations require explicit human approval.",
            "Escalation is mandatory for high severity or unclear blast radius.",
        ],
        {
            "alert": "p95 checkout latency above 2500ms for 10 minutes",
            "service": "checkout-api",
            "environment": "production",
            "signals": ["db_cpu_92_percent", "error_rate_1_4_percent"],
        },
        "incident_packet",
        ["severity", "impacted_service", "evidence", "actions_taken", "actions_blocked", "escalation_target", "postmortem_draft"],
    ),
    example(
        "coding-senior-engineering-pod",
        "catalog",
        2,
        "Senior engineering pod",
        "Architect -> implementer -> reviewer -> test-writer",
        "A repository issue asks for deterministic retry behavior around a flaky API client.",
        ["Architect", "Implementer", "Reviewer", "Test Writer"],
        [
            "Convert the issue into a minimal file-level implementation plan.",
            "Write or update the focused failing test.",
            "Implement the smallest local-style patch.",
            "Review the diff for correctness, security, reuse, and overengineering.",
            "Run validation gates and summarize residual risk.",
        ],
        [
            "No implementation starts before a concrete plan exists.",
            "No merge recommendation is allowed before tests and review.",
        ],
        {
            "issue": "Retry transient 503 responses up to three times with jitter.",
            "repository": "payments-sdk",
            "constraints": ["preserve_public_api", "avoid_new_dependencies"],
        },
        "patch_packet",
        ["plan", "changed_files", "tests", "review_findings", "validation_result", "residual_risk"],
    ),
    example(
        "research-evidence-dossier",
        "catalog",
        3,
        "Evidence dossier",
        "Decompose -> search -> grade -> synthesize -> fact-check -> cite",
        "A product team asks whether passkeys reduce account takeover risk for consumer apps.",
        ["Scout", "Web Searcher", "Source Grader", "Synthesizer", "Fact Checker", "Citer"],
        [
            "Break the research question into independent sub-questions.",
            "Collect primary and secondary sources for each sub-question.",
            "Grade sources for authority, recency, bias, and relevance.",
            "Synthesize only claims backed by accepted evidence.",
            "Attack each claim and normalize citations.",
        ],
        ["Unsupported claims must be removed or marked as assumptions."],
        {
            "question": "Do passkeys reduce account takeover risk for consumer apps?",
            "required_evidence": ["standards", "incident_data", "deployment_reports"],
            "deadline": "same-day brief",
        },
        "evidence_dossier",
        ["answer", "evidence_table", "confidence", "disputed_claims", "missing_evidence", "citations"],
    ),
    example(
        "trading-paper-decision",
        "catalog",
        4,
        "Paper trading decision",
        "Watch -> signal -> risk gate -> paper execution -> attribution",
        "A momentum signal appears in a liquid ETF, but portfolio drawdown is near the weekly limit.",
        ["Market Watcher", "Signal Generator", "Risk Checker", "Paper Executor", "Postmortem Analyst"],
        [
            "Summarize market state and relevant conditions.",
            "Propose signal, confidence, horizon, and invalidation criteria.",
            "Check exposure, drawdown, liquidity, concentration, and circuit breakers.",
            "Route only approved orders to paper execution.",
            "Attribute outcome to thesis, timing, risk, or noise.",
        ],
        [
            "Risk Checker is non-bypassable.",
            "Executor runs paper-by-default unless live trading is explicitly approved.",
        ],
        {
            "instrument": "SPY",
            "signal": "intraday breakout above prior high",
            "portfolio_state": {"weekly_drawdown_percent": 2.8, "limit_percent": 3.0},
        },
        "trade_ticket",
        ["hypothesis", "signal", "invalidation_criteria", "risk_checks", "order_intent", "paper_live_status", "post_trade_analysis"],
    ),
    example(
        "support-resolution",
        "catalog",
        5,
        "Customer support resolution",
        "Triage -> KB retrieval -> grounded response -> escalation",
        "A frustrated enterprise customer reports that SSO stopped working after a certificate rotation.",
        ["Triager", "KB Searcher", "Responder", "Escalator", "Memory Updater"],
        [
            "Classify intent, urgency, customer tier, and sentiment.",
            "Retrieve cited policy and product answers from the KB.",
            "Draft a grounded customer-facing response.",
            "Escalate when confidence, policy coverage, tone, or authority requires it.",
            "Store distilled account and ticket learning.",
        ],
        ["The responder abstains instead of inventing product or policy details."],
        {
            "ticket": "SSO login fails after IdP certificate rotation.",
            "customer_tier": "enterprise",
            "sentiment": "frustrated",
        },
        "support_reply_packet",
        ["classification", "cited_kb_articles", "customer_reply", "confidence", "escalation_reason", "next_action"],
    ),
    example(
        "legal-draft-contract-review",
        "catalog",
        6,
        "Draft-only contract review",
        "Redline -> citation check -> risk rating -> human lawyer",
        "A vendor MSA includes broad indemnity and unilateral renewal language that conflicts with the playbook.",
        ["Redliner", "Citation Checker", "Risk Rater", "Human Lawyer Gate"],
        [
            "Compare clauses against the contract playbook.",
            "Propose clause-level draft redlines.",
            "Verify every cited authority or policy reference.",
            "Score residual legal and commercial risk per clause.",
            "Route draft redline and memo for licensed human review.",
        ],
        [
            "Output is draft-only and is never presented as legal advice.",
            "Licensed human review is required before external use.",
        ],
        {
            "document": "vendor_msa",
            "clauses": ["indemnity", "renewal", "limitation_of_liability"],
            "playbook": "standard_vendor_contract_playbook_v3",
        },
        "draft_redline_packet",
        ["redlines", "issue_list", "negotiation_notes", "citation_status", "risk_score_per_clause", "draft_only_disclaimer"],
    ),
    example(
        "business-kpi-strategy",
        "catalog",
        7,
        "KPI-grounded strategy",
        "Analyze -> choose bet -> operationalize",
        "A business unit must choose one quarterly growth bet after pipeline conversion slowed.",
        ["Analyst", "Strategist", "Ops Coordinator", "Feasibility Reviewer"],
        [
            "Turn current metrics into findings.",
            "Choose one strategic bet and state trade-offs.",
            "Translate the bet into owners, actions, milestones, and KPIs.",
            "Review feasibility and metric alignment.",
        ],
        ["Strategic recommendations must tie directly to metrics."],
        {
            "quarter": "Q3",
            "metrics": {"pipeline_conversion": "down_12_percent", "activation": "flat", "retention": "up_3_percent"},
            "decision": "select_one_growth_bet",
        },
        "quarterly_plan",
        ["findings", "strategic_choice", "rejected_alternatives", "action_owners", "kpis", "milestones", "review_cadence"],
    ),
    example(
        "crm-lifecycle-management",
        "catalog",
        8,
        "CRM lifecycle management",
        "Qualify -> manage account -> watch churn",
        "A mid-market account expands usage but has three unresolved support tickets before renewal.",
        ["Lead Qualifier", "Account Manager", "Churn Watcher", "Memory Updater"],
        [
            "Score fit, urgency, potential value, and routing.",
            "Choose the next relationship play.",
            "Monitor churn signals and explain early risk.",
            "Update lifecycle memory with distilled state.",
        ],
        ["CRM mutation is suggestion-only unless explicitly permitted."],
        {
            "account": "Northstar Health",
            "event": "renewal_60_days_out",
            "signals": ["usage_up_22_percent", "three_open_support_tickets", "champion_changed_roles"],
        },
        "account_brief",
        ["stage", "score", "next_best_action", "relationship_context", "churn_risk", "missing_facts"],
    ),
    example(
        "marketing-campaign-strategy",
        "catalog",
        9,
        "Campaign strategy",
        "Audience -> message -> content -> SEO/analytics loop",
        "A B2B SaaS team wants a launch campaign for a new compliance dashboard.",
        ["Strategist", "Content Creator", "SEO Analyst", "Analytics Reviewer", "Memory Updater"],
        [
            "Define audience, positioning, channel, and target metric.",
            "Draft channel-specific assets.",
            "Ground content in search demand and analytics.",
            "Revise campaign brief before human review and publishing.",
            "Feed measured results back into memory.",
        ],
        ["Traffic, SEO, and competitor claims require analytics or cited evidence."],
        {
            "campaign_goal": "launch compliance dashboard",
            "icp": "security operations leaders at mid-market SaaS companies",
            "channels": ["blog", "linkedin", "webinar"],
        },
        "campaign_brief",
        ["icp", "message", "content_plan", "channels", "seo_targets", "analytics_baseline", "kpi", "experiments"],
    ),
    example(
        "advertising-media-optimization",
        "catalog",
        10,
        "Media optimization",
        "Media plan -> creative -> performance readout -> budget reallocation",
        "A paid acquisition team has a fixed budget and must rebalance underperforming channels weekly.",
        ["Media Planner", "Copywriter", "Performance Analyst", "Budget Reallocator"],
        [
            "Allocate spend across channels based on objective and audience.",
            "Create format-specific creative variants.",
            "Read performance metrics against KPIs and stop-loss thresholds.",
            "Recommend budget reallocation and flag weak creative or channel fit.",
        ],
        ["Creative ideation cannot control spend reallocation without performance evidence."],
        {
            "objective": "trial_signups",
            "budget_usd": 25000,
            "channels": ["search", "linkedin", "retargeting"],
        },
        "media_plan",
        ["audience", "channel_split", "budget", "creative_variants", "kpis", "test_plan", "stop_loss_thresholds", "optimization_recommendation"],
    ),
    example(
        "ai-ml-lifecycle",
        "catalog",
        11,
        "ML lifecycle",
        "Data -> train -> evaluate -> deploy behind guardrails",
        "An ML team wants to ship a classifier for support-ticket routing only if it beats the baseline across slices.",
        ["Data Curator", "Trainer", "Evaluator", "Deployer", "Drift Monitor"],
        [
            "Build a dataset card with provenance and limits.",
            "Run reproducible training or fine-tuning.",
            "Compare against baseline, subgroup slices, and failure cases.",
            "Deploy only if evaluation gates pass.",
            "Monitor post-deploy drift and regressions.",
        ],
        ["Evaluator is independent; training metrics alone cannot drive deployment."],
        {
            "objective": "route support tickets by product area",
            "baseline_accuracy": 0.72,
            "slices": ["enterprise", "free_tier", "billing", "security"],
        },
        "eval_report",
        ["dataset_summary", "baseline_delta", "metrics", "subgroup_performance", "risks", "ship_no_ship_decision", "deployment_guardrails"],
    ),
    example(
        "agentics-controlled-swarm",
        "catalog",
        12,
        "Controlled swarm",
        "Orchestrator -> planner -> workers -> critic",
        "A harness must evaluate three independent integration options without exceeding a fixed budget.",
        ["Orchestrator", "Planner", "Worker Pool", "Critic", "Memory Curator"],
        [
            "Set objective, budget, max depth, and stopping condition.",
            "Decompose work into dependency-aware tasks.",
            "Run bounded worker tasks.",
            "Review outputs through a critic before landing them.",
            "Decide whether to continue, retry, or stop and store distilled lessons.",
        ],
        ["No run starts without budget, max depth, stopping condition, and critic gate."],
        {
            "goal": "compare auth provider integrations",
            "budget": {"max_worker_tasks": 6, "max_depth": 2},
            "stopping_condition": "one recommended provider with unresolved risks listed",
        },
        "run_report",
        ["goal", "plan", "task_graph", "worker_outputs", "critic_findings", "final_result", "cost", "unresolved_issues"],
    ),
    example(
        "retrieval-review",
        "catalog",
        13,
        "Retrieval review",
        "Index -> retrieve -> answer -> source review",
        "A documentation assistant answers a policy question from a newly indexed handbook corpus.",
        ["Indexer", "Retriever", "Answer Drafter", "Source Reviewer"],
        [
            "Chunk, embed, and store source documents.",
            "Retrieve candidate passages with citations.",
            "Draft an answer only from retrieved evidence.",
            "Grade answer fidelity against sources.",
            "Reject or retry weak and unsupported answers.",
        ],
        ["Retrieval confidence and answer faithfulness are assessed separately."],
        {
            "corpus": "employee_handbook",
            "question": "What is the parental leave policy for contractors?",
            "retrieval_top_k": 5,
        },
        "reviewed_answer",
        ["cited_response", "source_list", "retrieval_confidence", "unsupported_claims", "reviewer_verdict"],
    ),
    example(
        "health-safe-wellness-coordination",
        "catalog",
        14,
        "Safe wellness coordination",
        "Intake -> red-flag triage -> resource coordination",
        "A user describes stress, poor sleep, and a concerning symptom while asking for next steps.",
        ["Intake Agent", "Red-Flag Triage", "Care Coordinator", "Clinician Escalation Gate"],
        [
            "Collect structured wellness information without diagnosing.",
            "Detect red flags and route to appropriate resource type.",
            "Coordinate logistics, reminders, and non-clinical follow-up.",
            "Redirect clinical decisions to a clinician.",
        ],
        [
            "No diagnosis, treatment plan, or emergency minimization.",
            "Clinical content is routed to professional care.",
        ],
        {
            "concern": "stress and poor sleep",
            "red_flag_signal": "chest tightness during exertion",
            "requested_help": "what should I do tonight?",
        },
        "intake_summary",
        ["user_stated_concern", "non_clinical_context", "red_flags", "suggested_resource_type", "escalation_recommendation"],
    ),
    example(
        "gaming-playtest-to-design",
        "catalog",
        15,
        "Playtest-to-design",
        "Read playtest -> critique balance -> model economy -> preserve narrative",
        "A playtest shows players abandoning the second dungeon while economy telemetry shows gold inflation.",
        ["Playtest Reader", "Balance Critic", "Economy Modeler", "Narrative Keeper", "Design Diff Writer"],
        [
            "Extract signal from telemetry, feedback, and design docs.",
            "Identify mechanic imbalance and propose changes.",
            "Check loops, sinks, inflation, and progression.",
            "Review lore and story consistency.",
            "Write a build-to-build design diff.",
        ],
        ["Player anecdotes are separated from telemetry-backed findings."],
        {
            "build": "0.8.4",
            "telemetry": {"dungeon_2_abandonment": "48_percent", "gold_inflation": "31_percent"},
            "feedback": ["boss feels unfair", "crafting prices feel meaningless"],
        },
        "playtest_recap",
        ["player_pain_points", "balance_issues", "economy_risks", "narrative_conflicts", "proposed_changes", "build_to_build_diff"],
    ),
    example(
        "sales-b2b-pipeline",
        "catalog",
        16,
        "B2B pipeline",
        "Prospect -> qualify -> demo -> close honestly",
        "A sales team evaluates whether a healthcare prospect is ready for a technical demo.",
        ["Prospector", "Qualifier", "Demo Coach", "Closer", "Pipeline Reporter"],
        [
            "Research account context and buying signals.",
            "Score qualification and list missing facts.",
            "Create a personalized demo path.",
            "Handle objections within negotiation boundaries.",
            "Identify pipeline bottleneck and next step.",
        ],
        ["No-stretch policy: never exaggerate product capabilities."],
        {
            "account": "Acme Clinics",
            "signals": ["recent_security_audit", "new_vp_it", "budget_cycle_q4"],
            "methodology": "MEDDPICC",
        },
        "deal_brief",
        ["account_context", "qualification_score", "missing_facts", "demo_angle", "objections", "next_step", "go_no_go"],
    ),
    example(
        "education-mastery-learning",
        "catalog",
        17,
        "Mastery learning",
        "Tutor -> explain -> quiz -> grade -> update mastery",
        "A learner knows linear equations but struggles to apply slope-intercept form in word problems.",
        ["Tutor", "Explainer", "Quiz Master", "Grader", "Mastery Memory Updater"],
        [
            "Choose next concept from the mastery map.",
            "Explain at the right depth for the learner profile.",
            "Generate calibrated questions.",
            "Grade answers against a rubric.",
            "Update mastery memory and recommend next focus.",
        ],
        ["The tutor abstains instead of faking certainty."],
        {
            "learner_profile": "grade_8_algebra",
            "mastery_map": {"linear_equations": "partial", "slope_intercept_word_problems": "weak"},
            "session_goal": "diagnose misconception",
        },
        "learning_cycle_report",
        ["concept_taught", "explanation_level", "quiz_result", "misconceptions", "mastery_update", "next_recommendation"],
    ),
    example(
        "repo-maintainer-stewardship",
        "catalog",
        18,
        "Repo stewardship",
        "Triage diff -> benchmark -> release check -> security scan",
        "A release candidate changes CLI wiring, dependencies, and generated template files.",
        ["Maintainer", "Benchmarker", "Security Reviewer", "Release Drafter"],
        [
            "Identify changed areas, risks, and review order.",
            "Run performance and regression gates.",
            "Flag risky MCP grants, leaked secrets, and dangerous diffs.",
            "Draft release body and validate readiness gates.",
            "Produce release or no-release recommendation.",
        ],
        ["The recommendation is conservative and does not overstate readiness."],
        {
            "candidate": "v0.2.0-rc.1",
            "changed_areas": ["cli", "templates", "dependencies"],
            "required_gates": ["tests", "benchmarks", "security_scan", "release_notes"],
        },
        "maintainer_packet",
        ["changed_areas", "risk_map", "benchmark_result", "security_findings", "release_notes", "readiness_verdict"],
    ),
    example(
        "exotic-self-evolution",
        "catalog",
        19,
        "Self-evolution",
        "Hypothesize -> sandbox experiment -> record -> maybe federate",
        "A harness proposes changing retrieval weights after repeated low-confidence answers.",
        ["Hypothesizer", "Experimenter", "Witness Logger", "Federator"],
        [
            "Propose a falsifiable improvement with a declared metric.",
            "Run the experiment only in a sandbox.",
            "Write success or failure to a witness-signed evolution log.",
            "Preserve failed experiments as learning.",
            "Federate only vetted, non-sensitive improvements.",
        ],
        [
            "Self-evolution is opt-in and sandboxed.",
            "Production self-mutation and proxy-metric optimization require review.",
        ],
        {
            "hypothesis": "hybrid retrieval weight should increase sparse score from 0.35 to 0.45",
            "metric": "answer_faithfulness",
            "sandbox": "retrieval_eval_fixture_2026_06",
        },
        "evolution_record",
        ["hypothesis", "metric", "sandbox_config", "result", "keep_kill_decision", "rollback_path", "federation_eligibility"],
    ),
    example(
        "algorithmic-control-plane",
        "agentic",
        1,
        "Algorithmic control plane",
        "Model proposes; harness decides; algorithms verify",
        "A user asks the harness to update dependencies, but confidence, risk, cost, and verification gates must pass first.",
        ["Intent Classifier", "Planner", "Router", "Tool Broker", "Verifier", "Receipt Logger"],
        [
            "Classify intent, risk, expected cost, and verification strategy.",
            "Create a plan and route each step to the right worker or model.",
            "Broker tool access under policy.",
            "Verify outputs independently before applying results.",
            "Write receipt and memory update after verified completion.",
        ],
        ["Execution is blocked unless confidence, risk, cost, and verification gates pass."],
        {
            "request": "upgrade minor dependencies and open a patch",
            "risk_budget": "medium",
            "verification": ["unit_tests", "dependency_audit"],
        },
        "control_plane_receipt",
        ["intent", "risk", "plan", "tool_grants", "verification", "receipt_hash", "result"],
    ),
    example(
        "repo-genome-harness-plan",
        "agentic",
        2,
        "Repo genome to harness plan",
        "Static repo genome -> recommended harness plan",
        "A meta-harness analyzes a repository without executing code and recommends the safest generated harness shape.",
        ["Repo Scanner", "Risk Profiler", "Topology Recommender", "Plan Writer"],
        [
            "Scan repository structure, languages, tests, and release surfaces without execution.",
            "Score test confidence, MCP risk, and publish readiness.",
            "Recommend agent topology, tool surface, memory namespaces, and approvals.",
            "Emit a harness plan with constraints and required human gates.",
        ],
        ["Repo analysis does not execute repository code."],
        {
            "repository": "edge-intelligence-service",
            "allowed_analysis": ["static_files", "package_manifests", "ci_config"],
            "disallowed_analysis": ["running_tests", "network_calls"],
        },
        "repo_genome_plan",
        ["repo_profile", "agent_topology", "tool_surface", "risk_budget", "memory_namespaces", "recommended_vertical", "required_human_approvals"],
    ),
    example(
        "planner-executor-verifier",
        "agentic",
        3,
        "Planner executor verifier",
        "Planner -> executor -> verifier",
        "A coding harness must fix a bug while keeping the approver independent from the patch author.",
        ["Planner", "Executor", "Verifier"],
        [
            "Planner decomposes the issue into small steps and acceptance checks.",
            "Executor edits files or drafts the patch within the plan.",
            "Verifier runs tests and reviews the diff independently.",
            "Verifier rejects, requests retry, or approves with residual risk.",
        ],
        ["The same agent cannot create and approve the output."],
        {
            "bug": "cache returns stale data after tenant switch",
            "acceptance_checks": ["reproduction_test", "unit_tests", "diff_review"],
        },
        "verification_packet",
        ["plan", "patch_summary", "test_results", "diff_risks", "verifier_verdict"],
    ),
    example(
        "default-deny-tool-broker",
        "agentic",
        4,
        "Default-deny tool broker",
        "Governed tool surface with explicit grants",
        "An agent requests shell, network, and file-write access while diagnosing a failing build.",
        ["Tool Broker", "Policy Engine", "Agent Worker", "Audit Logger"],
        [
            "Declare requested tool, risk, timeout, and call budget.",
            "Evaluate request against default-deny policy.",
            "Require approval for dangerous or write-capable operations.",
            "Execute only approved calls and record the audit trail.",
        ],
        ["Network, shell, and file writes are denied unless explicitly granted."],
        {
            "requested_tools": ["shell:npm_test", "network:package_registry", "file_write:patch"],
            "context": "failing build diagnosis",
            "dirty_worktree": True,
        },
        "tool_broker_decision",
        ["tool_name", "needs", "risk", "approval", "timeout_ms", "max_calls_per_turn", "audit_record"],
    ),
    example(
        "test-first-coding-pod",
        "agentic",
        5,
        "Test-first coding pod",
        "Understand issue -> failing test -> patch -> tests -> diff review",
        "A repo-maintenance agent fixes a parsing regression by proving the failure before editing production code.",
        ["Issue Analyst", "Test Author", "Implementation Agent", "Reviewer", "Release-note Drafter"],
        [
            "Understand the issue and target behavior.",
            "Write the failing test that reproduces the issue.",
            "Patch only the code needed to pass the test.",
            "Run relevant and full validation gates.",
            "Review the diff and summarize release notes.",
        ],
        ["No production code is edited before a failing test exists."],
        {
            "issue": "markdown parser drops escaped dots in numbered headings",
            "test_target": "heading_parser",
            "validation": ["unit_test", "snapshot_test"],
        },
        "coding_pod_packet",
        ["issue_summary", "failing_test", "patch", "validation", "diff_review", "release_note"],
    ),
    example(
        "evidence-first-research",
        "agentic",
        6,
        "Evidence-first research",
        "Retriever -> source ranker -> claim extractor -> contradiction finder -> synthesizer -> citation verifier",
        "A research assistant must answer a technical market question with primary-source support.",
        ["Retriever", "Source Ranker", "Claim Extractor", "Contradiction Finder", "Synthesizer", "Citation Verifier"],
        [
            "Retrieve candidate sources for each sub-question.",
            "Rank each source for authority, recency, balance, and relevance.",
            "Extract claims and identify contradictions.",
            "Synthesize only supported claims.",
            "Verify every citation against the claim it supports.",
        ],
        ["The synthesizer cannot use claims that failed citation verification."],
        {
            "question": "Which open model licenses permit commercial fine-tuning?",
            "source_requirements": ["license_text", "official_docs"],
        },
        "research_quality_packet",
        ["answer", "source_ranking", "claim_table", "contradictions", "citation_verdicts", "confidence"],
    ),
    example(
        "memory-distillation",
        "agentic",
        7,
        "Memory distillation",
        "Retrieve -> judge -> distill -> consolidate",
        "A coding harness stores only durable lessons from a failed dependency upgrade, not the full noisy trace.",
        ["Memory Retriever", "Trajectory Judge", "Distiller", "Consolidator"],
        [
            "Retrieve relevant prior task traces and lessons.",
            "Judge whether the current trajectory produced useful learning.",
            "Distill durable patterns, failures, and verified decisions.",
            "Consolidate into namespace-specific memory with decay metadata.",
        ],
        ["Do not store raw sensitive task history when a distilled lesson is sufficient."],
        {
            "task_trace": "dependency upgrade failed due peer dependency conflict",
            "namespace": "repo-maintenance",
            "sensitivity": "internal_package_names",
        },
        "memory_update_packet",
        ["retrieved_context", "judge_verdict", "distilled_lesson", "namespace", "decay_policy", "excluded_raw_data"],
    ),
    example(
        "domain-judge-distill",
        "agentic",
        8,
        "Domain-specific judge and distill",
        "Domain judge -> domain distiller -> reusable lesson",
        "Different verticals evaluate success with their own domain-specific outcome criteria.",
        ["Domain Judge", "Distill Provider", "Memory Curator"],
        [
            "Apply domain-specific success criteria to the completed run.",
            "Separate domain verdict from generic task completion.",
            "Distill a reusable lesson for that vertical.",
            "Store the lesson in the correct namespace with evidence.",
        ],
        ["Generic success metrics cannot replace domain-specific judgment."],
        {
            "vertical": "research",
            "run_result": "answer passed grammar checks but had weak source diversity",
            "domain_metric": "citation_faithfulness_and_balance",
        },
        "domain_learning_packet",
        ["domain_verdict", "metric_evidence", "distilled_lesson", "namespace", "reuse_conditions"],
    ),
    example(
        "cost-aware-model-cascade",
        "agentic",
        9,
        "Cost-aware model cascade",
        "Cheap draft -> verify -> stronger retry only if needed -> record cost and quality",
        "A CI triage agent drafts issue labels cheaply and escalates only uncertain cases to a stronger model.",
        ["Cheap Drafter", "Verifier", "Escalation Router", "Cost Logger"],
        [
            "Attempt the task with the cheapest suitable model.",
            "Verify confidence, quality, and safety.",
            "Escalate to a stronger model only when verification fails or uncertainty is high.",
            "Record cost, latency, and quality outcome.",
        ],
        ["Escalation is evidence-driven, not automatic."],
        {
            "task": "label incoming GitHub issue",
            "cheap_model_confidence": 0.62,
            "escalation_threshold": 0.8,
        },
        "model_cascade_record",
        ["initial_model", "verification_result", "escalated_model", "cost", "latency", "quality_outcome"],
    ),
    example(
        "receipt-led-governance",
        "agentic",
        10,
        "Receipt-led governance",
        "Every meaningful action writes a tamper-evident receipt",
        "A harness performs a dependency audit and records all material inputs, outputs, tools, and verdicts.",
        ["Action Worker", "Tool Auditor", "Verifier", "Receipt Logger"],
        [
            "Hash inputs and planned outputs before action.",
            "Record agent, model, tool calls, cost, latency, risk, and verdict.",
            "Hash-chain the receipt to the previous receipt.",
            "Expose the receipt for audit and replay.",
        ],
        ["Material actions without receipts are treated as incomplete."],
        {
            "action": "dependency_audit",
            "previous_receipt_hash": "sha256:previous",
            "tool_calls": ["npm_audit"],
        },
        "governance_receipt",
        ["input_hash", "output_hash", "agent", "model", "tool_calls", "cost", "latency", "risk", "verdict", "previous_hash", "current_hash"],
    ),
    example(
        "ci-agent",
        "agentic",
        11,
        "CI agent",
        "Trigger -> bounded task -> GitHub API tools -> PR/comment/status output",
        "A GitHub Action reviews a pull request and posts a bounded genome report without arbitrary shell access.",
        ["Trigger Handler", "Bounded Task Runner", "GitHub Tool Broker", "Status Reporter"],
        [
            "Start from a CI trigger with declared permissions.",
            "Run a bounded, non-interactive task.",
            "Use GitHub API tools instead of arbitrary shell by default.",
            "Post PR comment, status, or release note output.",
        ],
        ["No arbitrary shell or broad token permissions in CI by default."],
        {
            "trigger": "pull_request_opened",
            "permissions": ["contents:read", "pull-requests:write"],
            "task": "repo_genome_report",
        },
        "ci_agent_output",
        ["trigger", "bounded_task", "tool_permissions", "findings", "posted_status", "residual_risk"],
    ),
    example(
        "human-approval-gate",
        "agentic",
        12,
        "Human approval gate",
        "Draft -> explain risk -> request approval -> execute approved action -> record receipt",
        "An agent wants to publish a package release after tests pass but before human release approval.",
        ["Drafting Agent", "Risk Explainer", "Approval Gate", "Executor", "Receipt Logger"],
        [
            "Draft the proposed action and explain risk.",
            "Request approval for the exact action.",
            "Execute only the approved operation.",
            "Record approval, execution, and receipt.",
        ],
        ["Dangerous actions execute only after explicit approval of the exact action."],
        {
            "proposed_action": "publish npm package",
            "risk": "irreversible public release",
            "approval_required": True,
        },
        "approval_gate_record",
        ["draft_action", "risk_explanation", "approval_request", "approved_action", "execution_result", "receipt"],
    ),
    example(
        "opt-in-self-evolution",
        "agentic",
        13,
        "Opt-in self-evolution",
        "Measure baseline -> small exploration -> evaluate -> adopt if better -> rollback on regression",
        "A harness tests a routing-weight change against historical tasks before adopting it.",
        ["Baseline Measurer", "Experiment Runner", "Evaluator", "Rollback Manager", "Audit Logger"],
        [
            "Measure current baseline on declared metrics.",
            "Run a small opt-in exploration in sandbox.",
            "Evaluate against baseline and regression thresholds.",
            "Adopt only if better, otherwise preserve failure learning.",
            "Write rollback path and audit log.",
        ],
        ["Adaptive tuning is opt-in and rollback-ready."],
        {
            "baseline_metric": "successful_verification_rate",
            "candidate_change": "increase code-review model threshold",
            "regression_threshold": "no_drop_above_1_percent",
        },
        "self_evolution_audit",
        ["baseline", "experiment", "evaluation", "adopt_reject_decision", "rollback_path", "audit_log"],
    ),
    example(
        "private-shared-federation",
        "agentic",
        14,
        "Private/shared federation",
        "Local confidential work -> distilled non-sensitive pattern -> signed sharing -> peer validation",
        "An enterprise team shares a generic failure pattern learned from internal incidents without exposing customer data.",
        ["Local Distiller", "Sensitivity Filter", "Signer", "Federation Publisher", "Peer Validator"],
        [
            "Distill non-sensitive pattern from confidential local work.",
            "Filter user data, secrets, and task history.",
            "Sign the reusable pattern and publish to an allowed namespace.",
            "Validate peer patterns before import.",
        ],
        ["Federation shares patterns, not user data."],
        {
            "local_lesson": "rollback runbooks need precomputed owner mapping",
            "sensitive_fields": ["customer_name", "incident_id", "internal_urls"],
            "federation_namespace": "patterns",
        },
        "federated_pattern_record",
        ["distilled_pattern", "excluded_sensitive_data", "signature", "namespace", "peer_validation", "import_decision"],
    ),
    example(
        "storm-article-synthesis",
        "agentic",
        15,
        "STORM article synthesis",
        "Discover perspectives -> ask multi-perspective questions -> retrieve and ground -> outline -> write sections -> audit citations",
        "A documentation team must produce a comprehensive, neutral overview article on an unfamiliar topic, grounded entirely in cited sources rather than model memory.",
        ["Perspective Discoverer", "Question Asker", "Grounded Expert", "Outline Architect", "Section Writer", "Citation Auditor"],
        [
            "Discover diverse perspectives by surveying related topics and articles.",
            "Drive multi-perspective question asking through simulated expert conversations.",
            "Convert questions into queries, retrieve trusted sources, and answer with citations.",
            "Generate and refine a hierarchical outline from internal knowledge and collected answers.",
            "Write each section grounded only in collected references with inline citations.",
            "Assemble the lead section, remove duplication, and verify every citation.",
        ],
        [
            "Article claims must be grounded in retrieved, cited sources, not in model memory.",
            "Untrusted or unverifiable sources are excluded before they ground any section.",
        ],
        {
            "topic": "post-quantum cryptography migration",
            "audience": "general technical readers",
            "perspectives": ["standards body", "enterprise security lead", "cryptography researcher"],
            "source_requirements": ["primary_standards", "peer_reviewed", "official_docs"],
        },
        "grounded_article_packet",
        ["topic", "perspectives", "outline", "article", "citations", "excluded_references", "confidence"],
        reference={
            "system": "STORM",
            "title": "Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models",
            "arxiv": "2402.14207",
            "url": "https://arxiv.org/abs/2402.14207",
        },
    ),
    example(
        "compilot-loop-autoscheduling",
        "agentic",
        16,
        "ComPilot loop auto-scheduling",
        "Analyze loop -> propose schedule -> legality gate -> compile and benchmark -> feed back and keep best",
        "A compiler optimization harness must speed up a nested loop kernel by letting an LLM propose schedule transformations that a compiler validates for legality and benchmarks for real speedup before any schedule is accepted.",
        ["Loop Analyzer", "Schedule Proposer", "Legality Checker", "Compiler Benchmarker", "Feedback Coordinator"],
        [
            "Analyze the loop nest IR, data dependencies, and baseline performance.",
            "Propose candidate schedule transformations such as tiling, fusion, interchange, and parallelization.",
            "Check each proposed schedule for legality with dependence analysis before it runs.",
            "Compile only legal schedules and benchmark real speedup against the baseline.",
            "Feed measured results back to the proposer, iterate within budget, and keep the best legal schedule.",
        ],
        [
            "Only legal, dependence-preserving schedules may be compiled or executed.",
            "Speedup claims must come from real compiler benchmarks, not from model estimates.",
        ],
        {
            "kernel": "gemm triple-nested matrix-multiply loop",
            "baseline": "scalar -O3 untiled loop nest",
            "allowed_transformations": ["tiling", "loop_fusion", "loop_interchange", "parallelization", "vectorization"],
            "metrics": ["baseline_runtime_ms", "best_runtime_ms", "geomean_speedup"],
            "budget": {"max_iterations": 12, "stop_after_no_improvement": 3},
        },
        "optimized_schedule_packet",
        ["baseline_profile", "proposed_transformations", "legality_verdict", "rejected_schedules", "speedup_evidence", "best_schedule", "iteration_summary"],
        reference={
            "system": "ComPilot",
            "title": "Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization",
            "arxiv": "2511.00592",
            "url": "https://arxiv.org/abs/2511.00592",
        },
    ),
]


def existing_source_headings() -> dict[tuple[str, int], str]:
    if not (PATTERNS / "catalog.json").exists():
        return {}

    catalog = json.loads((PATTERNS / "catalog.json").read_text(encoding="utf-8"))
    return {
        (item["section"], item["number"]): item["source_heading"]
        for item in catalog["examples"]
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def markdown_list(items: list[str], ordered: bool = False) -> str:
    lines = []
    for index, item in enumerate(items, start=1):
        prefix = f"{index}." if ordered else "-"
        lines.append(f"{prefix} {item}")
    return "\n".join(lines)


def expected_output(entry: dict) -> dict:
    return build_output(flow_payload(entry), entry["input"])


def flow_payload(entry: dict) -> dict:
    payload = {
        "id": entry["id"],
        "source": {
            "type": "local_catalog",
            "section": entry["section"],
            "number": entry["number"],
            "heading": entry["source_heading"],
        },
        "name": entry["name"],
        "pattern": entry["pattern"],
        "scenario": entry["scenario"],
        "workflow_steps": entry["workflow_steps"],
        "agents": entry["agents"],
        "policy_gates": entry["policy_gates"],
        "input_contract": {
            "file": "input.json",
            "description": "Concrete scenario input for this pattern example.",
        },
        "output_contract": entry["output_contract"],
        "run": {
            "command": f"python ../run_example.py {entry['id']}",
            "expected_stdout": "expected-output.json",
        },
        "memory_update": {
            "mode": "distill-only",
            "stores": ["verified decisions", "reusable failures", "domain lessons"],
            "excludes": ["raw sensitive data", "unsupported claims"],
        },
        "receipt": {
            "required": True,
            "records": ["input_hash", "workflow_steps", "policy_verdict", "output_hash", "reviewer_verdict"],
        },
    }
    if entry.get("reference") is not None:
        payload["reference"] = entry["reference"]
    return payload


def reference_section(entry: dict) -> str:
    reference = entry.get("reference")
    if not reference:
        return ""
    label = reference.get("system") or reference.get("title", "source")
    title = reference.get("title", label)
    url = reference.get("url")
    line = f"This pattern is adapted from **{label}**: {title}."
    if url:
        line += f"\n\nPaper: {url}"
    return f"\n## Reference\n\n{line}\n"


def readme(entry: dict) -> str:
    fields = entry["output_contract"]["required_fields"]
    return f"""# {entry["name"]}

Catalog entry: `{entry["section"]}` pattern {entry["number"]}

Source heading: {entry["source_heading"]}

Pattern: **{entry["pattern"]}**
{reference_section(entry)}
## Scenario

{entry["scenario"]}

## Flow

{markdown_list(entry["workflow_steps"], ordered=True)}

## Agent Roles

{markdown_list(entry["agents"])}

## Policy Gates

{markdown_list(entry["policy_gates"])}

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py {entry["id"]}
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py {entry["id"]} --check
```

## Expected Output

The flow should produce `{entry["output_contract"]["artifact_type"]}` with these required fields:

{markdown_list(fields)}

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
"""


def catalog_readme(entries: list[dict]) -> str:
    catalog_entries = [entry for entry in entries if entry["section"] == "catalog"]
    agentic_entries = [entry for entry in entries if entry["section"] == "agentic"]

    def section(title: str, items: list[dict]) -> str:
        rows = [f"## {title}", ""]
        for item in items:
            rows.append(f"- [`{item['id']}`](./{item['id']}/README.md) - {item['name']}")
        return "\n".join(rows)

    return f"""# Agentic Flow Examples

This directory contains one runnable-shape example for each catalog entry.

Each example directory contains:

- `README.md` - human-oriented walkthrough
- `flow.json` - machine-readable flow contract
- `input.json` - concrete scenario payload
- `expected-output.json` - expected artifact shape

Run any example from its directory with `python ../run_example.py <example-id>`, or from
this directory with `python run_example.py <example-id>`.

{section("Catalog Vertical And Base Patterns", catalog_entries)}

{section("Cross-Cutting Agentic Patterns", agentic_entries)}
"""


def status_file(entries: list[dict]) -> str:
    catalog_entries = [entry for entry in entries if entry["section"] == "catalog"]
    agentic_entries = [entry for entry in entries if entry["section"] == "agentic"]

    def lines(title: str, items: list[dict]) -> str:
        rows = [f"## {title}", ""]
        for item in items:
            rows.append(
                f"- [x] `{item['id']}` - {item['source_heading']} - "
                f"`patterns/{item['id']}/README.md`"
            )
        return "\n".join(rows)

    return f"""# Agentic Pattern Example Status

Source: local example catalog

Status: all documented patterns currently have generated example artifacts.

{lines("Catalog Vertical And Base Patterns", catalog_entries)}

{lines("Cross-Cutting Agentic Patterns", agentic_entries)}
"""


def build_entries() -> list[dict]:
    headings = existing_source_headings()
    entries = []
    seen = set()
    for spec in SPECS:
        key = (spec["section"], spec["number"])
        if spec["id"] in seen:
            raise ValueError(f"Duplicate example id: {spec['id']}")
        seen.add(spec["id"])
        entry = dict(spec)
        entry["source_heading"] = headings.get(key, spec["name"])
        entries.append(entry)

    return entries


def main() -> None:
    entries = build_entries()
    PATTERNS.mkdir(exist_ok=True)

    catalog = {
        "source": "local_example_catalog",
        "example_count": len(entries),
        "examples": entries,
    }
    write_json(PATTERNS / "catalog.json", catalog)
    (PATTERNS / "README.md").write_text(catalog_readme(entries), encoding="utf-8")
    STATUS.write_text(status_file(entries), encoding="utf-8")

    for entry in entries:
        example_dir = PATTERNS / entry["id"]
        example_dir.mkdir(exist_ok=True)
        (example_dir / "README.md").write_text(readme(entry), encoding="utf-8")
        write_json(example_dir / "flow.json", flow_payload(entry))
        write_json(example_dir / "input.json", entry["input"])
        write_json(example_dir / "expected-output.json", expected_output(entry))


if __name__ == "__main__":
    main()
