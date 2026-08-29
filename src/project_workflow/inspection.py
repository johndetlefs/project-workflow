"""Canonical Project Workflow inspection runtime."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .contracts import (
    CANONICAL_INIT_COMMAND,
    CANONICAL_UPGRADE_COMMAND,
    COORDINATION_BOUNDARIES,
    COORDINATION_DRIFT_CLASSIFICATIONS,
    COORDINATION_FILENAME,
    CURRENT_ASSET_VERSION,
    CURRENT_PACKAGE_VERSION,
    CURRENT_SCHEMA_VERSION,
    DOCTOR_OUTPUT_SCHEMA_VERSION,
    EPIC_CHILD_GATED_STATUSES,
    EPIC_ID_PREFIX,
    EPIC_TRACKER_STATUSES,
    FIX_CLASSIFICATIONS,
    FIX_ID_PREFIX,
    FIX_MODES,
    FIX_SEVERITIES,
    GLOBAL_TRACKER_COLUMNS,
    OPERATIONAL_STATUS_ACTION_PRECEDENCE,
    OPERATIONAL_STATUS_SCHEMA_VERSION,
    PROMPT_FILES,
    STRUCTURED_EVIDENCE_FILENAME,
    TRACKER_STATUSES,
    DoctorEvaluation,
    DoctorIssue,
    OperationalStatusAction,
    OperationalStatusFact,
    OperationalStatusFinding,
    OperationalStatusInspection,
    OperationalStatusProofLayer,
    OperationalStatusRepository,
    OperationalStatusSnapshot,
    OperationalStatusSource,
    OperationalStatusValue,
    OperationalStatusWorkItem,
    WorkflowConfig,
    WorkspaceRepository,
    _OperationalStatusActionCandidate,
)
from .coordination import (
    _coordination_preflight_payload,
    _coordination_required_text,
    _coordination_state_path,
    _coordination_status_payload,
    _coordination_validate_state,
    _execution_control_projection,
    _execution_fixed_release_projection,
    _execution_qa_projection,
    _execution_validate_control,
    _verification_campaign_projection,
)
from .lifecycle import (
    _add_issue,
    _approval_envelope_issues,
    _backlog_path,
    _backlog_rows,
    _backlog_validation_issues,
    _doctor_check_implementation_ac_mapping,
    _epic_requirements_readiness_issues,
    _epic_tracker_rows,
    _fix_closeout_issues,
    _fix_non_delivery_closeout_issues,
    _fix_triage_issues,
    _global_tracker_rows,
    _has_epic_acceptance_audit_evidence,
    _has_qa_review_evidence,
    _inspect_operational_active_work,
    _intent_audit_evaluation,
    _intent_audit_path,
    _intent_contract_mode,
    _intent_qa_review_issues,
    _is_discovery_work,
    _legacy_adoption_evidence_untrusted,
    _load_structured_evidence,
    _operational_epic_child_documents,
    _operational_item_proof_layers,
    _operational_status_artifact,
    _operational_status_document_source,
    _operational_status_fact,
    _operational_work_item_facts,
    _operational_work_item_paths,
    _parse_markdown_table,
    _repository_evidence_issues,
    _repository_evidence_rows,
    _repository_scope_issues,
    _repository_scope_values,
    _requirements_approval_issues_for_path,
    _resolve_epic_dir,
    _status_requires_task_readiness,
    _structured_evidence_issues,
    _task_readiness_issues,
    _triggered_proof_recipes,
    _validation_impact_from_text,
)
from .repository import (
    _clean_markdown_cell_path,
    _decomposition_plan_authority_issues,
    _decomposition_plan_path,
    _epic_contract_issues_for_path,
    _epic_contract_path,
    _extract_ac_ids,
    _extract_parent_ac_coverage,
    _extract_workflow_ref_ids,
    _fix_value_missing,
    _fix_values,
    _is_generated_content,
    _legacy_truncated_child_charter_issues,
    _load_workflow_config,
    _markdown_section,
    _operational_git_optional,
    _repository_compatibility,
    _task_prefix_from_id,
    _valid_epic_id,
    _valid_fix_id,
    _valid_task_id,
    _with_generated_marker,
    _workflow_config_path,
    _workflow_manifest_path,
)


def _operational_status_source_payload(source: OperationalStatusSource) -> dict[str, str]:
    return {
        "kind": source.kind,
        "artifact": source.artifact,
        "detail": source.detail,
    }


def _operational_status_value_payload(value: OperationalStatusValue) -> dict[str, object]:
    return {
        "state": value.state,
        "summary": value.summary,
        "sources": [_operational_status_source_payload(source) for source in value.sources],
        "facts": [
            {
                "key": fact.key,
                "value": list(fact.value) if isinstance(fact.value, tuple) else fact.value,
            }
            for fact in value.facts
        ],
    }


def _operational_status_repository_payload(
    repository: OperationalStatusRepository,
) -> dict[str, object]:
    return {
        "id": repository.repository_id,
        "path": repository.path,
        "role": repository.role,
        "authority": repository.authority,
        "git": _operational_status_value_payload(repository.git),
        "evidence": [
            {
                "key": fact.key,
                "value": list(fact.value) if isinstance(fact.value, tuple) else fact.value,
            }
            for fact in repository.evidence
        ],
        "sources": [_operational_status_source_payload(source) for source in repository.sources],
    }


def _operational_status_work_item_payload(
    work_item: OperationalStatusWorkItem,
) -> dict[str, object]:
    return {
        "id": work_item.item_id,
        "title": work_item.title,
        "kind": work_item.kind,
        "lifecycle": work_item.lifecycle,
        "operational_meaning": work_item.operational_meaning,
        "sources": [_operational_status_source_payload(source) for source in work_item.sources],
        "facts": [
            {
                "key": fact.key,
                "value": list(fact.value) if isinstance(fact.value, tuple) else fact.value,
            }
            for fact in work_item.facts
        ],
        "proof_layers": [
            {
                "name": layer.name,
                "state": layer.state,
                "summary": layer.summary,
                "sources": [_operational_status_source_payload(source) for source in layer.sources],
            }
            for layer in work_item.proof_layers
        ],
        "delivery": (
            _operational_status_value_payload(work_item.delivery)
            if work_item.delivery is not None
            else None
        ),
    }


def _operational_status_finding_payload(
    finding: OperationalStatusFinding,
) -> dict[str, object]:
    return {
        "code": finding.code,
        "severity": finding.severity,
        "message": finding.message,
        "sources": [_operational_status_source_payload(source) for source in finding.sources],
    }


def _operational_status_action_payload(
    action: OperationalStatusAction,
) -> dict[str, object]:
    return {
        "code": action.code,
        "title": action.title,
        "responsible_party": action.responsible_party,
        "reason": action.reason,
        "command": action.command,
        "request": action.request,
        "sources": [_operational_status_source_payload(source) for source in action.sources],
    }


def operational_status_payload(snapshot: OperationalStatusSnapshot) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": OPERATIONAL_STATUS_SCHEMA_VERSION,
        "root": snapshot.root,
        "installation": _operational_status_value_payload(snapshot.installation),
        "git": _operational_status_value_payload(snapshot.git),
        "health": _operational_status_value_payload(snapshot.health),
        "proof": _operational_status_value_payload(snapshot.proof),
        "delivery": _operational_status_value_payload(snapshot.delivery),
        "active_work": [
            _operational_status_work_item_payload(work_item) for work_item in snapshot.active_work
        ],
        "findings": [_operational_status_finding_payload(finding) for finding in snapshot.findings],
        "blockers": [_operational_status_finding_payload(blocker) for blocker in snapshot.blockers],
        "primary_action": (
            _operational_status_action_payload(snapshot.primary_action)
            if snapshot.primary_action is not None
            else None
        ),
        "secondary_actions": [
            _operational_status_action_payload(action) for action in snapshot.secondary_actions
        ],
    }
    if snapshot.workspace_authority is not None:
        payload["workspace"] = {
            "enabled": True,
            "authority_repository": snapshot.workspace_authority,
        }
        payload["repositories"] = [
            _operational_status_repository_payload(repository)
            for repository in snapshot.repositories
        ]
    return payload


def operational_status_inspection_payload(
    inspection: OperationalStatusInspection,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "installation": _operational_status_value_payload(inspection.installation),
        "git": _operational_status_value_payload(inspection.git),
        "active_work": [
            _operational_status_work_item_payload(work_item) for work_item in inspection.active_work
        ],
        "findings": [
            _operational_status_finding_payload(finding) for finding in inspection.findings
        ],
    }
    if inspection.workspace_authority is not None:
        payload["workspace"] = {
            "enabled": True,
            "authority_repository": inspection.workspace_authority,
        }
        payload["repositories"] = [
            _operational_status_repository_payload(repository)
            for repository in inspection.repositories
        ]
    return payload


def _inspect_operational_installation(root: Path) -> OperationalStatusValue:
    compatibility = _repository_compatibility(root)
    workflow_source = OperationalStatusSource(
        "repository-compatibility",
        ".project-workflow",
        compatibility.reason,
    )
    manifest_path = _workflow_manifest_path(root)
    sources = [workflow_source]
    if manifest_path.exists():
        sources.append(
            OperationalStatusSource(
                "manifest",
                _operational_status_artifact(root, manifest_path),
            )
        )

    facts: list[OperationalStatusFact] = [
        _operational_status_fact("compatibility_reason", compatibility.reason),
        _operational_status_fact("helper_package_version", CURRENT_PACKAGE_VERSION),
        _operational_status_fact("helper_asset_version", CURRENT_ASSET_VERSION),
        _operational_status_fact("helper_schema_version", CURRENT_SCHEMA_VERSION),
        _operational_status_fact("manifest_present", manifest_path.exists()),
        _operational_status_fact("manifest_parsed", compatibility.manifest is not None),
    ]
    if compatibility.manifest is not None:
        manifest = compatibility.manifest
        facts.extend(
            (
                _operational_status_fact("manifest_version", manifest.manifest_version),
                _operational_status_fact("package_version", manifest.package_version),
                _operational_status_fact("asset_version", manifest.asset_version),
                _operational_status_fact("schema_version", manifest.schema_version),
                _operational_status_fact("applied_migrations", manifest.applied_migrations),
            )
        )
    if compatibility.state in {"upgradeable", "legacy-unversioned"}:
        facts.append(_operational_status_fact("upgrade_command", CANONICAL_UPGRADE_COMMAND))

    summaries = {
        "current": "Installed project-workflow contract is current.",
        "upgradeable": "Installed project-workflow contract can be upgraded.",
        "legacy-unversioned": "Recognized project-workflow installation has no version manifest.",
        "unsupported-future": "Repository contract is newer than this helper supports.",
        "invalid": "Repository contract is invalid or cannot be classified safely.",
        "not-initialized": "Repository is not initialized with project-workflow.",
    }
    return OperationalStatusValue(
        "installation",
        compatibility.state,
        summaries[compatibility.state],
        tuple(sources),
        tuple(facts),
    )


def _inspect_operational_git(
    root: Path,
    *,
    source_artifact: str = ".git",
    source_detail: str = "read-only local Git inspection",
    repository_id: str | None = None,
) -> tuple[OperationalStatusValue, tuple[OperationalStatusFinding, ...]]:
    source = OperationalStatusSource("git", source_artifact, source_detail)
    repository_label = (
        f"Workspace repository '{repository_id}'" if repository_id is not None else "Git worktree"
    )
    top_level = _operational_git_optional(["rev-parse", "--show-toplevel"], root)
    if top_level is None:
        finding = OperationalStatusFinding(
            "PW_STATUS_GIT_UNAVAILABLE",
            "warning",
            f"{repository_label} state is unavailable because its root is not a readable "
            "Git worktree.",
            (source,),
        )
        return (
            OperationalStatusValue(
                "git",
                "unavailable",
                "Local Git state is unavailable.",
                (source,),
                (_operational_status_fact("available", False),),
            ),
            (finding,),
        )

    branch = _operational_git_optional(["symbolic-ref", "--quiet", "--short", "HEAD"], root)
    head = _operational_git_optional(["rev-parse", "HEAD"], root)
    upstream = _operational_git_optional(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], root
    )
    porcelain = _operational_git_optional(["status", "--porcelain"], root)
    findings: list[OperationalStatusFinding] = []
    resolved_root = str(root.resolve())
    resolved_top = str(Path(top_level).resolve())
    if resolved_top != resolved_root:
        findings.append(
            OperationalStatusFinding(
                "PW_STATUS_GIT_ROOT_MISMATCH",
                "error",
                f"{repository_label} requested root {resolved_root} differs from Git "
                f"worktree root {resolved_top}.",
                (source,),
            )
        )
    if head is None:
        findings.append(
            OperationalStatusFinding(
                "PW_STATUS_GIT_HEAD_UNAVAILABLE",
                "warning",
                f"{repository_label} has no readable HEAD commit.",
                (source,),
            )
        )
    if porcelain is None:
        findings.append(
            OperationalStatusFinding(
                "PW_STATUS_GIT_STATUS_UNAVAILABLE",
                "warning",
                f"{repository_label} cleanliness could not be determined.",
                (source,),
            )
        )

    clean = porcelain == "" if porcelain is not None else None
    detached = branch is None and head is not None
    if head is None or porcelain is None:
        state = "unavailable"
        summary = "Git worktree state is only partially available."
    elif detached:
        state = "detached"
        summary = f"Git HEAD is detached at {head[:12]}."
    elif clean is False:
        state = "dirty"
        summary = f"Git branch {branch} has uncommitted changes."
    else:
        state = "clean"
        summary = f"Git branch {branch} is clean."

    facts = (
        _operational_status_fact("available", True),
        _operational_status_fact("top_level", resolved_top),
        _operational_status_fact("branch", branch),
        _operational_status_fact("detached", detached),
        _operational_status_fact("head", head),
        _operational_status_fact("upstream", upstream),
        _operational_status_fact("clean", clean),
    )
    return OperationalStatusValue("git", state, summary, (source,), facts), tuple(findings)


def _workspace_git_state_findings(
    repository: WorkspaceRepository,
    git: OperationalStatusValue,
) -> tuple[OperationalStatusFinding, ...]:
    source = git.sources[0]
    if git.state == "dirty":
        return (
            OperationalStatusFinding(
                "PW_STATUS_WORKSPACE_REPOSITORY_DIRTY",
                "error",
                f"Workspace repository '{repository.repository_id}' has uncommitted changes.",
                (source,),
            ),
        )
    if git.state == "detached":
        return (
            OperationalStatusFinding(
                "PW_STATUS_WORKSPACE_REPOSITORY_DETACHED",
                "error",
                f"Workspace repository '{repository.repository_id}' has a detached HEAD.",
                (source,),
            ),
        )
    if git.state == "unavailable":
        return (
            OperationalStatusFinding(
                "PW_STATUS_WORKSPACE_REPOSITORY_UNAVAILABLE",
                "error",
                f"Workspace repository '{repository.repository_id}' Git state is unavailable.",
                (source,),
            ),
        )
    return ()


def inspect_operational_status_repository(
    root: Path,
    *,
    repository_id: str | None = None,
) -> OperationalStatusInspection:
    inspected_root = root.resolve()
    installation = _inspect_operational_installation(inspected_root)
    config = _load_workflow_config(inspected_root)
    if config.workspace is None:
        if repository_id is not None:
            raise SystemExit(
                "The --repository selector requires a workspace declaration in "
                ".project-workflow/config.json."
            )
        git, git_findings = _inspect_operational_git(inspected_root)
        repositories: tuple[OperationalStatusRepository, ...] = ()
        workspace_authority = None
    else:
        workspace = config.workspace
        selected_repositories: tuple[WorkspaceRepository, ...]
        if repository_id is not None:
            try:
                selected_repositories = (workspace.repository(repository_id),)
            except KeyError as exc:
                registered = ", ".join(
                    repository.repository_id for repository in workspace.repositories
                )
                raise SystemExit(
                    f"Unknown workspace repository '{repository_id}'. Registered: {registered}."
                ) from exc
        else:
            selected_repositories = workspace.repositories
        repository_records: list[OperationalStatusRepository] = []
        repository_findings: list[OperationalStatusFinding] = []
        authority_git: OperationalStatusValue | None = None
        for repository in selected_repositories:
            source_artifact = ".git" if repository.path == "." else f"{repository.path}/.git"
            repository_git, findings = _inspect_operational_git(
                repository.resolved_path,
                source_artifact=source_artifact,
                source_detail=f"workspace repository {repository.repository_id}",
                repository_id=repository.repository_id,
            )
            repository_records.append(
                OperationalStatusRepository(
                    repository.repository_id,
                    repository.path,
                    repository.role,
                    repository.repository_id == workspace.authority_repository,
                    repository_git,
                    (),
                    (
                        OperationalStatusSource(
                            "workspace-config",
                            ".project-workflow/config.json",
                            f"registration for {repository.repository_id}",
                        ),
                    ),
                )
            )
            repository_findings.extend(findings)
            repository_findings.extend(_workspace_git_state_findings(repository, repository_git))
            if repository.repository_id == workspace.authority_repository:
                authority_git = repository_git
        if authority_git is None:
            authority = workspace.repository(workspace.authority_repository)
            authority_artifact = ".git" if authority.path == "." else f"{authority.path}/.git"
            authority_git, findings = _inspect_operational_git(
                authority.resolved_path,
                source_artifact=authority_artifact,
                source_detail=f"workspace authority repository {authority.repository_id}",
                repository_id=authority.repository_id,
            )
            repository_findings.extend(findings)
        git = authority_git
        git_findings = tuple(repository_findings)
        repositories = tuple(repository_records)
        workspace_authority = workspace.authority_repository
    active_work, work_findings = _inspect_operational_active_work(inspected_root)
    return OperationalStatusInspection(
        installation,
        git,
        active_work,
        (*git_findings, *work_findings),
        workspace_authority,
        repositories,
    )


def _operational_status_unique_sources(
    sources: list[OperationalStatusSource],
) -> tuple[OperationalStatusSource, ...]:
    return tuple(dict.fromkeys(sources))


def _operational_repository_evidence(
    root: Path,
    repositories: tuple[OperationalStatusRepository, ...],
    work_items: tuple[OperationalStatusWorkItem, ...],
) -> tuple[OperationalStatusRepository, ...]:
    enriched: list[OperationalStatusRepository] = []
    for repository in repositories:
        primary_work: list[str] = []
        touched_work: list[str] = []
        branch_pr: list[str] = []
        validation: list[str] = []
        delivery: list[str] = []
        evidence: list[str] = []
        sources: list[OperationalStatusSource] = []
        for item in work_items:
            requirements_path, implementation_path, _epic_dir = _operational_work_item_paths(
                root, item
            )
            scope_path = implementation_path if item.kind == "fix" else requirements_path
            if scope_path is None or not scope_path.exists():
                continue
            requirements_text = scope_path.read_text(encoding="utf-8")
            primary, touched = _repository_scope_values(requirements_text)
            if repository.repository_id not in touched:
                continue
            touched_work.append(item.item_id)
            if primary == repository.repository_id:
                primary_work.append(item.item_id)
            sources.append(
                OperationalStatusSource(
                    "implementation" if item.kind == "fix" else "requirements",
                    _operational_status_artifact(root, scope_path),
                    f"repository scope for {item.item_id}",
                )
            )
            if implementation_path is None or not implementation_path.exists():
                continue
            rows = _repository_evidence_rows(implementation_path.read_text(encoding="utf-8"))
            row = rows.get(repository.repository_id)
            if row is None:
                continue
            branch_pr.append(f"{item.item_id}: {row['branch_pr']}")
            validation.append(f"{item.item_id}: {row['validation']}")
            delivery.append(f"{item.item_id}: {row['delivery']}")
            evidence.append(f"{item.item_id}: {row['evidence']}")
            sources.append(
                OperationalStatusSource(
                    "repository-evidence",
                    _operational_status_artifact(root, implementation_path),
                    f"repository evidence for {item.item_id}",
                )
            )
        facts: list[OperationalStatusFact] = []
        for key, values in (
            ("primary_work", primary_work),
            ("touched_work", touched_work),
            ("branch_pr", branch_pr),
            ("validation", validation),
            ("delivery", delivery),
            ("evidence_artifacts", evidence),
        ):
            if values:
                facts.append(_operational_status_fact(key, tuple(values)))
        enriched.append(
            OperationalStatusRepository(
                repository.repository_id,
                repository.path,
                repository.role,
                repository.authority,
                repository.git,
                tuple(facts),
                _operational_status_unique_sources([*repository.sources, *sources]),
            )
        )
    return tuple(enriched)


def _workspace_repository_evidence_findings(
    repositories: tuple[OperationalStatusRepository, ...],
) -> tuple[OperationalStatusFinding, ...]:
    findings: list[OperationalStatusFinding] = []
    for repository in repositories:
        live_branch = next(
            (fact.value for fact in repository.git.facts if fact.key == "branch"),
            None,
        )
        branch_records = next(
            (fact.value for fact in repository.evidence if fact.key == "branch_pr"),
            (),
        )
        if not isinstance(live_branch, str) or not isinstance(branch_records, tuple):
            continue
        for record in branch_records:
            _item_id, separator, recorded_state = record.partition(":")
            if not separator:
                continue
            expected_branch = recorded_state.strip()
            if expected_branch.lower().startswith("branch "):
                expected_branch = expected_branch[7:].strip().strip("`")
            if not re.fullmatch(r"[A-Za-z0-9._/-]+", expected_branch):
                continue
            if expected_branch == live_branch:
                continue
            sources = _operational_status_unique_sources(
                [*repository.git.sources, *repository.sources]
            )
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_WORKSPACE_REPOSITORY_BRANCH_MISMATCH",
                    "error",
                    f"Workspace repository '{repository.repository_id}' is on branch "
                    f"'{live_branch}' but recorded work expects '{expected_branch}'.",
                    sources,
                )
            )
    return tuple(findings)


def _operational_relevant_repository_ids(
    root: Path,
    work_items: tuple[OperationalStatusWorkItem, ...],
) -> set[str]:
    repository_ids: set[str] = set()
    for item in work_items:
        requirements_path, implementation_path, _epic_dir = _operational_work_item_paths(root, item)
        scope_path = implementation_path if item.kind == "fix" else requirements_path
        if scope_path is None or not scope_path.exists():
            continue
        _primary, touched = _repository_scope_values(scope_path.read_text(encoding="utf-8"))
        repository_ids.update(touched)
    return repository_ids


def _operational_aggregate_proof_state(
    layers: tuple[OperationalStatusProofLayer, ...],
) -> str:
    by_name = {layer.name: layer.state for layer in layers}
    state = "declared"
    if by_name.get("requirements-approval") not in {"pass", "not-required"}:
        return state
    state = "approved"
    if by_name.get("readiness") not in {"pass", "not-required"}:
        return state
    state = "ready"
    if by_name.get("implementation") != "pass":
        return state
    state = "implementation-recorded"
    if by_name.get("qa-review") != "pass" or by_name.get("parent-acceptance") not in {
        "pass",
        "not-required",
    }:
        return state
    state = "repository-validated"
    if by_name.get("structured-evidence") == "pass":
        return "recorded-evidence"
    return state


def _operational_outcome_states(root: Path, item: OperationalStatusWorkItem) -> tuple[str, str]:
    requirements_path, implementation_path, epic_dir = _operational_work_item_paths(root, item)
    if requirements_path is None:
        return "not-recorded", "not-recorded"
    requirements_text = (
        requirements_path.read_text(encoding="utf-8") if requirements_path.exists() else ""
    )
    implementation_text = (
        implementation_path.read_text(encoding="utf-8")
        if implementation_path is not None and implementation_path.exists()
        else ""
    )
    if "user-outcome-journey" not in _triggered_proof_recipes(
        requirements_text, implementation_text
    ):
        return "not-required", "not-required"
    if item.kind == "epic" and epic_dir is not None:
        journey_records: list[dict[str, object]] = []
        for row, child_requirements, child_implementation in _operational_epic_child_documents(
            root, epic_dir
        ):
            child_requirements_text = child_requirements.read_text(encoding="utf-8")
            child_implementation_text = child_implementation.read_text(encoding="utf-8")
            if "user-outcome-journey" not in _triggered_proof_recipes(
                child_requirements_text, child_implementation_text
            ):
                continue
            if _structured_evidence_issues(
                requirements_path=child_requirements,
                implementation_path=child_implementation,
                include_explicit_nonpassing=True,
                parent_ac_ids=_extract_ac_ids(_extract_parent_ac_coverage(row)),
            ):
                return "invalid", "unknown"
            records, load_issues = _load_structured_evidence(
                child_implementation.parent / STRUCTURED_EVIDENCE_FILENAME
            )
            if load_issues:
                return "invalid", "unknown"
            journey_records.extend(
                record
                for record in records
                if record.get("recipe") == "user-outcome-journey"
                and str(record.get("status", "")).strip().lower() == "pass"
            )
    elif implementation_path is not None:
        records, load_issues = _load_structured_evidence(
            implementation_path.parent / STRUCTURED_EVIDENCE_FILENAME
        )
        if load_issues:
            return "not-recorded", "unknown"
        journey_records = [
            record
            for record in records
            if record.get("recipe") == "user-outcome-journey"
            and str(record.get("status", "")).strip().lower() == "pass"
        ]
    else:
        return "not-recorded", "unknown"
    if not journey_records:
        return "not-recorded", "unknown"
    if implementation_path is not None and _structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
        include_explicit_nonpassing=True,
    ):
        return "invalid", "unknown"
    required_acceptance_states = {
        str(record.get("owner_acceptance_status", "")).strip().lower()
        for record in journey_records
        if record.get("owner_acceptance_required") is True
    }
    if "pending" in required_acceptance_states:
        return "outcome-proven", "ready-for-owner-acceptance"
    if required_acceptance_states and required_acceptance_states == {"accepted"}:
        return "outcome-proven", "owner-accepted"
    return "outcome-proven", "not-required"


def classify_operational_proof(
    root: Path,
    work_items: tuple[OperationalStatusWorkItem, ...],
) -> tuple[OperationalStatusValue, tuple[OperationalStatusWorkItem, ...]]:
    classified: list[OperationalStatusWorkItem] = []
    aggregate_states: list[str] = []
    all_sources: list[OperationalStatusSource] = []
    state_rank = {
        "unknown": 0,
        "not-recorded": 1,
        "declared": 2,
        "approved": 3,
        "ready": 4,
        "implementation-recorded": 5,
        "repository-validated": 6,
        "recorded-evidence": 7,
    }
    for item in work_items:
        layers = _operational_item_proof_layers(root, item)
        aggregate_state = _operational_aggregate_proof_state(layers)
        aggregate_states.append(aggregate_state)
        all_sources.extend(source for layer in layers for source in layer.sources)
        item_facts = tuple(
            fact
            for fact in item.facts
            if fact.key
            not in {
                "aggregate_proof_state",
                "outcome_proof_state",
                "owner_acceptance_state",
            }
        ) + (_operational_status_fact("aggregate_proof_state", aggregate_state),)
        outcome_state, owner_acceptance_state = _operational_outcome_states(root, item)
        item_facts = item_facts + (
            _operational_status_fact("outcome_proof_state", outcome_state),
            _operational_status_fact("owner_acceptance_state", owner_acceptance_state),
        )
        classified.append(
            OperationalStatusWorkItem(
                item.item_id,
                item.title,
                item.kind,
                item.lifecycle,
                item.operational_meaning,
                item.sources,
                item_facts,
                layers,
                item.delivery,
            )
        )
    if not classified:
        aggregate = "not-recorded"
        summary = "No active work item proof is recorded."
        sources: tuple[OperationalStatusSource, ...] = (
            OperationalStatusSource("global-tracker", ".project-workflow/TRACKER.md"),
        )
    else:
        aggregate = min(aggregate_states, key=lambda value: state_rank[value])
        summary = f"Weakest active work proof state is {aggregate}."
        sources = _operational_status_unique_sources(all_sources)
    return (
        OperationalStatusValue("proof", aggregate, summary, sources),
        tuple(classified),
    )


def classify_operational_health(
    root: Path,
    *,
    strict: bool = False,
) -> tuple[OperationalStatusValue, tuple[OperationalStatusFinding, ...]]:
    issues = run_doctor(root)
    accepted = _accepted_doctor_warning_fingerprints(root)
    evaluation = _evaluate_doctor(
        issues,
        root=root,
        strict=strict,
        accepted_fingerprints=accepted,
    )
    source = OperationalStatusSource("doctor", ".project-workflow", "Doctor evaluation")
    facts = (
        _operational_status_fact("strict", strict),
        _operational_status_fact("total_count", len(evaluation.issues)),
        _operational_status_fact("visible_count", len(evaluation.visible_issues)),
        _operational_status_fact("accepted_count", len(evaluation.accepted_issues)),
        _operational_status_fact("current_count", len(evaluation.current_issues)),
        _operational_status_fact("legacy_count", len(evaluation.legacy_issues)),
        _operational_status_fact("blocking_count", len(evaluation.blocking_issues)),
    )
    health = OperationalStatusValue(
        "health",
        evaluation.status,
        (
            "Doctor found no visible issues."
            if evaluation.status == "pass"
            else f"Doctor reports {len(evaluation.visible_issues)} visible issue(s)."
        ),
        (source,),
        facts,
    )
    findings = tuple(
        OperationalStatusFinding(
            issue.code,
            "error" if issue in evaluation.blocking_issues else "warning",
            issue.message,
            (
                OperationalStatusSource(
                    "doctor",
                    _doctor_issue_path_for_fingerprint(issue, root),
                    f"owner {issue.remediation_owner}; mechanical {str(issue.mechanically_upgradeable).lower()}",
                ),
            ),
        )
        for issue in evaluation.visible_issues
    )
    return health, findings


def _operational_delivery_receipt_paths(
    root: Path,
    item: OperationalStatusWorkItem,
) -> tuple[Path, ...]:
    item_facts = _operational_work_item_facts(item)
    candidates: list[Path] = []
    explicit = item_facts.get("delivery_receipt")
    if isinstance(explicit, str) and explicit:
        candidates.append(root / explicit)
    _requirements_path, implementation_path, _epic_dir = _operational_work_item_paths(root, item)
    if implementation_path is not None:
        evidence_path = implementation_path.parent / STRUCTURED_EVIDENCE_FILENAME
        if evidence_path.exists():
            try:
                payload = json.loads(evidence_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                payload = {}
            records = payload.get("claims", []) if isinstance(payload, dict) else []
            if isinstance(records, list):
                for record in records:
                    if not isinstance(record, dict):
                        continue
                    if str(record.get("status", "")).strip().lower() != "pass":
                        continue
                    artifact = record.get("evidence_artifact")
                    if not isinstance(artifact, str) or not artifact.strip():
                        continue
                    if re.match(r"^[a-z][a-z0-9+.-]*://", artifact, flags=re.IGNORECASE):
                        continue
                    candidate = Path(artifact)
                    if not candidate.is_absolute():
                        candidate = implementation_path.parent / candidate
                    candidates.append(candidate)
    return tuple(dict.fromkeys(candidates))


def _operational_receipt_state(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return None
    deployment = payload.get("deployment")
    if (
        isinstance(deployment, dict)
        and deployment.get("status") in {"verified", "deployed"}
        and all(deployment.get(key) for key in ("target", "source", "observed_at", "result"))
    ):
        return "deployed"
    release = payload.get("release")
    if not isinstance(release, dict) or not release.get("version"):
        return None
    publication = release.get("publication")
    if (
        isinstance(publication, dict)
        and publication.get("status") in {"verified", "published"}
        and all(publication.get(key) for key in ("target", "source", "observed_at", "result"))
    ):
        return "published"
    return "released"


def classify_operational_delivery(
    root: Path,
    item: OperationalStatusWorkItem,
) -> tuple[OperationalStatusValue, tuple[OperationalStatusFinding, ...]]:
    tracker_source = item.sources[0]
    if item.lifecycle != "Complete":
        return (
            OperationalStatusValue(
                "delivery",
                "not-recorded",
                "Non-terminal work has no completed delivery state.",
                (tracker_source,),
            ),
            (),
        )

    state = "repository-complete"
    summary = "Repository workflow completion is recorded."
    sources: list[OperationalStatusSource] = [tracker_source]
    findings: list[OperationalStatusFinding] = []
    item_facts = _operational_work_item_facts(item)
    tracker_branch = item_facts.get("tracker_branch")
    if isinstance(tracker_branch, str) and tracker_branch:
        remote_default = _operational_git_optional(
            ["symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"], root
        )
        target = remote_default or next(
            (
                candidate
                for candidate in ("main", "master")
                if _operational_git_optional(["rev-parse", "--verify", candidate], root) is not None
            ),
            None,
        )
        if (
            target is not None
            and _operational_git_optional(
                ["merge-base", "--is-ancestor", tracker_branch, target], root
            )
            is not None
        ):
            state = "integrated"
            summary = f"Git proves {tracker_branch} is contained in {target}."
            sources.append(OperationalStatusSource("git", ".git", f"{tracker_branch} -> {target}"))

    for receipt_path in _operational_delivery_receipt_paths(root, item):
        receipt_source = OperationalStatusSource(
            "delivery-receipt",
            _operational_status_artifact(root, receipt_path),
        )
        if not receipt_path.exists():
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_DELIVERY_RECEIPT_MISSING",
                    "warning",
                    "The referenced delivery receipt does not exist.",
                    (receipt_source,),
                )
            )
            continue
        try:
            receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_DELIVERY_RECEIPT_INVALID",
                    "warning",
                    f"Delivery receipt is unavailable or malformed: {exc}",
                    (receipt_source,),
                )
            )
            continue
        receipt_state = _operational_receipt_state(receipt_payload)
        if receipt_state is None:
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_DELIVERY_RECEIPT_INVALID",
                    "warning",
                    "Delivery receipt lacks a recognized release or deployment record.",
                    (receipt_source,),
                )
            )
            continue
        receipt_rank = {"released": 1, "published": 2, "deployed": 3}
        current_rank = receipt_rank.get(state, 0)
        if receipt_rank[receipt_state] >= current_rank:
            state = receipt_state
            summary = f"Repository-local receipt records {receipt_state} delivery."
            sources.append(receipt_source)
    return (
        OperationalStatusValue(
            "delivery",
            state,
            summary,
            _operational_status_unique_sources(sources),
        ),
        tuple(findings),
    )


def _operational_action(
    code: str,
    title: str,
    responsible_party: str,
    reason: str,
    sources: tuple[OperationalStatusSource, ...],
    *,
    command: str | None = None,
    request: str | None = None,
) -> OperationalStatusAction:
    return OperationalStatusAction(
        code,
        title,
        responsible_party,
        reason,
        sources,
        command,
        request,
    )


def _operational_action_candidate(
    precedence: str,
    action: OperationalStatusAction,
    *,
    work_order: int = 0,
    item_id: str = "",
) -> _OperationalStatusActionCandidate:
    return _OperationalStatusActionCandidate(
        precedence,
        work_order,
        item_id,
        action,
    )


def _operational_installation_action(
    installation: OperationalStatusValue,
) -> _OperationalStatusActionCandidate | None:
    sources = installation.sources or (
        OperationalStatusSource("repository-compatibility", ".project-workflow"),
    )
    if installation.state in {"upgradeable", "legacy-unversioned"}:
        action = _operational_action(
            "PW_STATUS_UPGRADE_REQUIRED",
            "Upgrade project-workflow",
            "agent",
            installation.summary,
            sources,
            command=CANONICAL_UPGRADE_COMMAND,
        )
    elif installation.state == "not-initialized":
        action = _operational_action(
            "PW_STATUS_INIT_REQUIRED",
            "Initialize project-workflow",
            "agent",
            installation.summary,
            sources,
            command=CANONICAL_INIT_COMMAND,
        )
    elif installation.state == "helper-limited":
        action = _operational_action(
            "PW_STATUS_HELPER_UPGRADE_REQUIRED",
            "Use the current project-workflow helper",
            "agent",
            installation.summary,
            sources,
            command=CANONICAL_UPGRADE_COMMAND,
        )
    elif installation.state == "unsupported-future":
        action = _operational_action(
            "PW_STATUS_UNSUPPORTED_FUTURE",
            "Use a compatible helper",
            "owner",
            installation.summary,
            sources,
            request=(
                "Select a project-workflow helper version that supports the repository's "
                "newer contract before making workflow changes."
            ),
        )
    elif installation.state in {"invalid", "unknown"}:
        action = _operational_action(
            "PW_STATUS_INSTALLATION_INVALID",
            "Repair installation identity",
            "owner",
            installation.summary,
            sources,
            request=(
                "Review the manifest and repository contract, decide the authoritative "
                "version, and repair the invalid installation before continuing."
            ),
        )
    else:
        return None
    return _operational_action_candidate("installation-safety", action)


def _operational_finding_candidates(
    findings: tuple[OperationalStatusFinding, ...],
) -> list[_OperationalStatusActionCandidate]:
    candidates: list[_OperationalStatusActionCandidate] = []
    for order, finding in enumerate(findings):
        if finding.severity != "error":
            continue
        detail = " ".join(source.detail.lower() for source in finding.sources)
        responsible_party = "owner" if "owner owner" in detail else "agent"
        candidates.append(
            _operational_action_candidate(
                "blocking-current-finding",
                _operational_action(
                    "PW_STATUS_REPAIR_BLOCKER",
                    f"Resolve {finding.code}",
                    responsible_party,
                    finding.message,
                    finding.sources,
                    request=(
                        f"Resolve {finding.code} at its cited source, then rerun "
                        "`project doctor --strict` and `project status`."
                    ),
                ),
                work_order=order,
                item_id=finding.code,
            )
        )
    return candidates


def _operational_item_layer_map(
    item: OperationalStatusWorkItem,
) -> dict[str, OperationalStatusProofLayer]:
    return {layer.name: layer for layer in item.proof_layers}


def _operational_validation_impact_action(
    root: Path,
    item: OperationalStatusWorkItem,
    work_order: int,
) -> _OperationalStatusActionCandidate | None:
    _requirements_path, implementation_path, _epic_dir = _operational_work_item_paths(root, item)
    if implementation_path is None or not implementation_path.exists():
        return None
    decision, issues = _validation_impact_from_text(implementation_path.read_text(encoding="utf-8"))
    if issues:
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_VALIDATION_IMPACT_INVALID",
                f"Repair validation impact for {item.item_id}",
                "agent",
                "Validation impact decision is invalid: " + "; ".join(issues),
                (
                    _operational_status_document_source(
                        root,
                        "implementation",
                        implementation_path,
                        item.sources[0],
                    ),
                ),
                request=(
                    "Record one coherent unaffected, affected, or ambiguous decision; "
                    "do not start validation or review while the decision is invalid."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    if decision is None:
        return None
    classification = str(decision["classification"])
    verdict = str(decision["validation_verdict"])
    source = (
        _operational_status_document_source(
            root,
            "implementation",
            implementation_path,
            item.sources[0],
        ),
    )
    if classification == "ambiguous":
        return _operational_action_candidate(
            "owner-decision",
            _operational_action(
                "PW_STATUS_VALIDATION_IMPACT_CLARIFICATION_REQUIRED",
                f"Clarify validation impact for {item.item_id}",
                "owner",
                "The later change cannot yet be tied to a specific prior proof layer.",
                source,
                request=(
                    "Identify the exact prior proof that the later change can invalidate, "
                    "or confirm that it is unaffected. Do not investigate further first."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    if classification == "affected" and verdict != "pass":
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_AFFECTED_VALIDATION_REQUIRED",
                f"Validate affected proof for {item.item_id}",
                "agent",
                (
                    "The recorded later change invalidates only: "
                    + ", ".join(str(value) for value in decision["affected_proof_layers"])
                    + f"; validation verdict is {verdict}."
                ),
                source,
                request=(
                    "Run the named affected validation once, update its verdict, then stop "
                    "validation work. This decision does not authorize independent QA."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    return None


def _operational_coordination_action(
    root: Path,
    item: OperationalStatusWorkItem,
    work_order: int,
) -> _OperationalStatusActionCandidate | None:
    try:
        path = _coordination_state_path(root, item.item_id)
    except ValueError:
        return None
    if not path.is_file():
        return None
    source = (
        OperationalStatusSource(
            "coordination-state",
            _operational_status_artifact(root, path),
            "durable Coordinator authority and next action",
        ),
    )
    try:
        status = _coordination_status_payload(root, item.item_id)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return _operational_action_candidate(
            "blocking-current-finding",
            _operational_action(
                "PW_STATUS_COORDINATION_INVALID",
                f"Repair coordination state for {item.item_id}",
                "agent",
                str(exc),
                source,
                request="Repair the cited durable state, then rerun coordinate status and Doctor.",
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    contract_state = str(status["contract_state"])
    if contract_state not in {"current", "compatible"}:
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_COORDINATION_HANDOFF_REQUIRED",
                f"Load Coordinator contract for {item.item_id}",
                "agent",
                f"Declared physical-context contract is {contract_state}; explicitly load the applicable contract.",
                source,
                command=(
                    f"./.project-workflow/cli/workflow coordinate preflight --id {item.item_id}"
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    last_boundary = status.get("last_boundary")
    if isinstance(last_boundary, dict) and last_boundary.get("classification") == "drift-detected":
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_COORDINATION_BLOCKED",
                f"Resolve affected coordination branch for {item.item_id}",
                "agent",
                str(status["next_action"]),
                source,
                command=(f"./.project-workflow/cli/workflow coordinate status --id {item.item_id}"),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    checkpoint = status.get("outcome_checkpoint")
    if isinstance(checkpoint, dict) and checkpoint.get("status") in {"pending", "fail"}:
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_COORDINATION_CHECKPOINT",
                f"Resolve outcome checkpoint for {item.item_id}",
                "agent",
                str(status["next_action"]),
                source,
                command=f"./.project-workflow/cli/workflow coordinate status --id {item.item_id}",
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    verification = status.get("verification")
    if isinstance(verification, dict):
        operational_state = verification.get("operational_state")
        if operational_state == "blocked":
            return _operational_action_candidate(
                "blocking-current-finding",
                _operational_action(
                    "PW_STATUS_VERIFICATION_BLOCKED",
                    f"Resolve material verification for {item.item_id}",
                    "agent",
                    str(verification["next_action"]),
                    source,
                    command=(
                        "./.project-workflow/cli/workflow coordinate "
                        f"verification-preflight --id {item.item_id} "
                        "--material-verification yes"
                    ),
                ),
                work_order=work_order,
                item_id=item.item_id,
            )
        if operational_state == "verification-required":
            return _operational_action_candidate(
                "missing-workflow-gate",
                _operational_action(
                    "PW_STATUS_VERIFICATION_REQUIRED",
                    f"Complete material verification for {item.item_id}",
                    "agent",
                    str(verification["next_action"]),
                    source,
                    command=(
                        "./.project-workflow/cli/workflow coordinate "
                        f"verification-preflight --id {item.item_id} "
                        "--material-verification yes"
                    ),
                ),
                work_order=work_order,
                item_id=item.item_id,
            )
    return None


def _operational_item_action(
    root: Path,
    item: OperationalStatusWorkItem,
    work_order: int,
) -> _OperationalStatusActionCandidate | None:
    layers = _operational_item_layer_map(item)
    facts = _operational_work_item_facts(item)
    owner_epic = facts.get("owner_epic")
    fallback_sources = item.sources

    if item.lifecycle == "Blocked":
        return _operational_action_candidate(
            "blocking-current-finding",
            _operational_action(
                "PW_STATUS_BLOCKER_DECISION_REQUIRED",
                f"Resolve blocker for {item.item_id}",
                "owner",
                f"{item.item_id} is explicitly Blocked.",
                fallback_sources,
                request=(
                    f"Record the decision or changed condition that unblocks {item.item_id}, "
                    "then move it to the appropriate prior lifecycle state."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    coordination_action = _operational_coordination_action(root, item, work_order)
    if coordination_action is not None:
        return coordination_action

    if item.kind == "epic-child" and item.lifecycle == "Proposed" and owner_epic:
        return _operational_action_candidate(
            "lifecycle-progress",
            _operational_action(
                "PW_STATUS_APPROVE_EPIC_CHILD",
                f"Approve {item.item_id}",
                "agent",
                "The child is authorized by the parent decomposition and remains Proposed.",
                fallback_sources,
                command=(
                    f"./.project-workflow/cli/workflow epic approve --epic-id "
                    f"{owner_epic} --id {item.item_id}"
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    if item.kind == "epic-child" and item.lifecycle == "Approved" and owner_epic:
        return _operational_action_candidate(
            "lifecycle-progress",
            _operational_action(
                "PW_STATUS_SCAFFOLD_EPIC_CHILD",
                f"Scaffold {item.item_id}",
                "agent",
                "The approved child has not been scaffolded.",
                fallback_sources,
                command=(
                    f"./.project-workflow/cli/workflow epic scaffold-child --epic-id "
                    f"{owner_epic} --id {item.item_id}"
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    approval = layers.get("requirements-approval")
    if approval is not None and approval.state not in {"pass", "not-required"}:
        return _operational_action_candidate(
            "owner-decision",
            _operational_action(
                "PW_STATUS_REQUIREMENTS_APPROVAL_REQUIRED",
                f"Approve requirements for {item.item_id}",
                "owner",
                approval.summary,
                approval.sources,
                request=(
                    f"Review and approve the requirements and acceptance criteria envelope "
                    f"for {item.item_id}."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    if item.kind == "fix" and item.lifecycle == "To Do":
        return _operational_action_candidate(
            "lifecycle-progress",
            _operational_action(
                "PW_STATUS_TRIAGE_FIX",
                f"Triage {item.item_id}",
                "agent",
                "The Fix remains in To Do and must pass its triage gate.",
                fallback_sources,
                command=f"./.project-workflow/cli/workflow fix triage --id {item.item_id}",
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    readiness = layers.get("readiness")
    if readiness is not None and readiness.state not in {"pass", "not-required"}:
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_READINESS_REQUIRED",
                f"Repair readiness for {item.item_id}",
                "agent",
                readiness.summary,
                readiness.sources,
                request=(
                    f"Complete the cited readiness requirements for {item.item_id}, then "
                    "run its supported readiness command."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    implementation = layers.get("implementation")
    if (
        implementation is not None
        and implementation.state != "pass"
        and item.lifecycle in {"In Progress", "Testing", "Review", "Closeout", "Complete"}
    ):
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_IMPLEMENTATION_REQUIRED",
                f"Complete implementation for {item.item_id}",
                "agent",
                implementation.summary,
                implementation.sources,
                request=(
                    f"Finish and record the implementation work for {item.item_id} before "
                    "advancing its lifecycle."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    impact_action = _operational_validation_impact_action(root, item, work_order)
    if impact_action is not None:
        return impact_action

    qa = layers.get("qa-review")
    if qa is not None and qa.state != "pass" and item.lifecycle in {"Review", "Complete"}:
        if qa.state == "not-required":
            qa = None
    if (
        qa is not None
        and qa.state not in {"pass", "not-required"}
        and item.lifecycle in {"Review", "Complete"}
    ):
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_QA_REQUIRED",
                f"Run required review for {item.item_id}",
                "agent",
                qa.summary,
                qa.sources,
                request=(
                    "Complete only the QA gate already required by the approved work item. "
                    "A validation-impact decision never creates or broadens QA."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    acceptance = layers.get("parent-acceptance")
    if (
        acceptance is not None
        and acceptance.state not in {"pass", "not-required"}
        and item.lifecycle in {"Review", "Closeout", "Complete"}
    ):
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_PARENT_ACCEPTANCE_REQUIRED",
                f"Record acceptance for {item.item_id}",
                "agent",
                acceptance.summary,
                acceptance.sources,
                request=(
                    f"Record the cited parent acceptance evidence for {item.item_id} before "
                    "completion."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    evidence = layers.get("structured-evidence")
    if (
        evidence is not None
        and evidence.state not in {"pass", "not-required"}
        and item.lifecycle in {"Review", "Closeout", "Complete"}
    ):
        return _operational_action_candidate(
            "missing-workflow-gate",
            _operational_action(
                "PW_STATUS_STRUCTURED_EVIDENCE_REQUIRED",
                f"Collect evidence for {item.item_id}",
                "external-authority",
                evidence.summary,
                evidence.sources,
                request=(
                    f"Collect and record passing evidence for every triggered proof recipe "
                    f"owned by {item.item_id}."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    command: str | None = None
    code = ""
    title = ""
    reason = f"{item.item_id} is ready for its next legal lifecycle transition."
    if item.kind == "epic-child" and owner_epic:
        transitions = {
            "In Progress": ("PW_STATUS_TEST_EPIC_CHILD", "Move child to Testing", "Testing"),
            "Testing": ("PW_STATUS_REVIEW_EPIC_CHILD", "Move child to Review", "Review"),
            "Review": ("PW_STATUS_COMPLETE_EPIC_CHILD", "Complete child", "Complete"),
        }
        if item.lifecycle in transitions:
            code, title, target = transitions[item.lifecycle]
            command = (
                f"./.project-workflow/cli/workflow epic status --epic-id {owner_epic} "
                f"--id {item.item_id} --to {target}"
            )
    elif item.kind == "epic":
        transitions = {
            "To Do": ("PW_STATUS_ANALYSE_EPIC", "Begin Epic analysis", "Analysing"),
            "Analysing": ("PW_STATUS_READY_EPIC", "Mark Epic ready", "Ready"),
            "Ready": ("PW_STATUS_START_EPIC", "Start Epic", "In Progress"),
            "In Progress": ("PW_STATUS_CLOSEOUT_EPIC", "Begin Epic closeout", "Closeout"),
        }
        if item.lifecycle in transitions:
            code, title, target = transitions[item.lifecycle]
            command = (
                f"./.project-workflow/cli/workflow epic lifecycle --epic-id "
                f"{item.item_id} --to '{target}'"
            )
        elif item.lifecycle == "Closeout":
            code = "PW_STATUS_COMPLETE_EPIC"
            title = "Complete Epic closeout"
            command = f"./.project-workflow/cli/workflow epic closeout --epic-id {item.item_id}"
    elif item.kind == "fix":
        transitions = {
            "Ready": ("PW_STATUS_START_FIX", "Start Fix", "In Progress"),
            "In Progress": ("PW_STATUS_TEST_FIX", "Move Fix to Testing", "Testing"),
            "Testing": ("PW_STATUS_REVIEW_FIX", "Move Fix to Review", "Review"),
        }
        if item.lifecycle in transitions:
            code, title, target = transitions[item.lifecycle]
            command = (
                f"./.project-workflow/cli/workflow fix status --id {item.item_id} --to '{target}'"
            )
    else:
        transitions = {
            "To Do": ("PW_STATUS_ANALYSE_TASK", "Begin task analysis", "Analysing"),
            "Analysing": ("PW_STATUS_READY_TASK", "Mark task ready", "Ready"),
            "Ready": ("PW_STATUS_START_TASK", "Start task", "In Progress"),
            "Plan Confirmed": ("PW_STATUS_START_TASK", "Start task", "In Progress"),
            "In Progress": ("PW_STATUS_TEST_TASK", "Move task to Testing", "Testing"),
            "Testing": ("PW_STATUS_REVIEW_TASK", "Move task to Review", "Review"),
            "Review": ("PW_STATUS_COMPLETE_TASK", "Complete task", "Complete"),
        }
        if item.lifecycle in transitions:
            code, title, target = transitions[item.lifecycle]
            command = (
                f"./.project-workflow/cli/workflow task status --id {item.item_id} --to '{target}'"
            )
    if command is not None:
        return _operational_action_candidate(
            "lifecycle-progress",
            _operational_action(
                code,
                f"{title}: {item.item_id}",
                "agent",
                reason,
                fallback_sources,
                command=command,
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    if item.kind == "fix" and item.lifecycle == "Review":
        return _operational_action_candidate(
            "lifecycle-progress",
            _operational_action(
                "PW_STATUS_CLOSE_FIX",
                f"Close Fix: {item.item_id}",
                "agent",
                "The Fix reached Review and its recorded proof gates pass.",
                fallback_sources,
                request=(
                    f"Record disposition, decision, closing identity, and verification for "
                    f"{item.item_id}, then run the supported `fix close` command with those "
                    "values."
                ),
            ),
            work_order=work_order,
            item_id=item.item_id,
        )

    if item.delivery is not None and item.delivery.state in {
        "repository-complete",
        "integrated",
        "released",
        "published",
    }:
        delivery_requests = {
            "repository-complete": ("Authorize and record branch integration.", "owner"),
            "integrated": ("Create and record the intended release.", "owner"),
            "released": ("Verify and record public publication.", "external-authority"),
            "published": ("Verify and record the intended deployment.", "external-authority"),
        }
        request, party = delivery_requests[item.delivery.state]
        return _operational_action_candidate(
            "delivery-follow-up",
            _operational_action(
                "PW_STATUS_DELIVERY_FOLLOW_UP",
                f"Advance delivery for {item.item_id}",
                party,
                item.delivery.summary,
                item.delivery.sources or fallback_sources,
                request=request,
            ),
            work_order=work_order,
            item_id=item.item_id,
        )
    return None


def _operational_backlog_candidate(
    root: Path,
) -> _OperationalStatusActionCandidate | None:
    backlog_path = root / ".project-workflow" / "BACKLOG.md"
    if not backlog_path.exists():
        return None
    issues: list[DoctorIssue] = []
    source = OperationalStatusSource("backlog", ".project-workflow/BACKLOG.md")
    try:
        rows = _backlog_rows(backlog_path, issues=issues)
    except (OSError, SystemExit):
        rows = []
        issues.append(
            DoctorIssue(
                "PW_BACKLOG_INVALID",
                "error",
                str(backlog_path),
                "Backlog cannot be parsed using the required schema.",
                "agent",
                False,
            )
        )
    if issues:
        return _operational_action_candidate(
            "blocking-current-finding",
            _operational_action(
                "PW_STATUS_BACKLOG_INVALID",
                "Repair backlog structure",
                "agent",
                f"Backlog parsing found {len(issues)} issue(s).",
                (source,),
                request="Repair the cited backlog rows, then rerun backlog validation.",
            ),
        )
    eligible = [
        (order, row)
        for order, row in enumerate(rows)
        if row.get("Status") in {"Accepted", "Proposed"} and not row.get("Promoted To", "").strip()
    ]
    if not eligible:
        return None
    priority_rank = {"High": 0, "Medium": 1, "Low": 2, "Unset": 3}
    order, row = min(
        eligible,
        key=lambda entry: (
            priority_rank.get(entry[1].get("Priority", "Unset"), 4),
            entry[0],
        ),
    )
    row_id = row.get("ID", "").strip()
    title = row.get("Title", "").strip() or row_id
    return _operational_action_candidate(
        "backlog-selection",
        _operational_action(
            "PW_STATUS_SELECT_BACKLOG_ITEM",
            f"Select backlog item {row_id}",
            "owner",
            (
                f"{row_id} is the highest recorded actionable backlog item "
                f"({row.get('Priority', 'Unset')}, file order {order + 1})."
            ),
            (source,),
            request=(f"Confirm whether to promote or otherwise advance {row_id}: {title}."),
        ),
        work_order=order,
        item_id=row_id,
    )


def resolve_operational_actions(
    root: Path,
    *,
    installation: OperationalStatusValue,
    work_items: tuple[OperationalStatusWorkItem, ...],
    findings: tuple[OperationalStatusFinding, ...] = (),
    focus_id: str | None = None,
) -> tuple[OperationalStatusAction, tuple[OperationalStatusAction, ...]]:
    candidates: list[_OperationalStatusActionCandidate] = []
    installation_candidate = _operational_installation_action(installation)
    if installation_candidate is not None:
        candidates.append(installation_candidate)
    candidates.extend(_operational_finding_candidates(findings))

    selected_work = tuple(
        item for item in work_items if focus_id is None or item.item_id == focus_id
    )
    for order, item in enumerate(selected_work):
        candidate = _operational_item_action(root, item, order)
        if candidate is not None:
            candidates.append(candidate)

    if focus_id is not None and not selected_work:
        candidates.append(
            _operational_action_candidate(
                "blocking-current-finding",
                _operational_action(
                    "PW_STATUS_FOCUS_NOT_FOUND",
                    f"Locate work item {focus_id}",
                    "agent",
                    f"The active operational projection contains no item named {focus_id}.",
                    (OperationalStatusSource("global-tracker", ".project-workflow/TRACKER.md"),),
                    request=(
                        f"Check the item ID and its tracker lifecycle, then rerun status for "
                        f"{focus_id}."
                    ),
                ),
                item_id=focus_id,
            )
        )
    elif not selected_work:
        backlog_candidate = _operational_backlog_candidate(root)
        if backlog_candidate is not None:
            candidates.append(backlog_candidate)

    if not candidates:
        candidates.append(
            _operational_action_candidate(
                "no-action",
                _operational_action(
                    "PW_STATUS_NO_ACTION",
                    "No repository action is required",
                    "owner",
                    "No compatibility blocker, active-work gate, or actionable backlog item was found.",
                    (OperationalStatusSource("global-tracker", ".project-workflow/TRACKER.md"),),
                    request="Select a future outcome when more work is desired.",
                ),
            )
        )

    rank = {name: index for index, name in enumerate(OPERATIONAL_STATUS_ACTION_PRECEDENCE)}
    ordered = sorted(
        candidates,
        key=lambda candidate: (
            rank[candidate.precedence],
            candidate.work_order,
            candidate.item_id,
            candidate.action.code,
        ),
    )
    unique: list[OperationalStatusAction] = []
    seen: set[tuple[str, str, str | None, str | None, tuple[str, ...]]] = set()
    for candidate in ordered:
        action = candidate.action
        identity = (
            action.code,
            action.title,
            action.command,
            action.request,
            tuple(source.artifact for source in action.sources),
        )
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(action)
    return unique[0], tuple(unique[1:])


def _operational_aggregate_delivery(
    work_items: tuple[OperationalStatusWorkItem, ...],
) -> OperationalStatusValue:
    values = tuple(item.delivery for item in work_items if item.delivery is not None)
    if not values:
        return OperationalStatusValue(
            "delivery",
            "not-recorded",
            "No selected work item has a recorded delivery state.",
            (OperationalStatusSource("global-tracker", ".project-workflow/TRACKER.md"),),
        )
    rank = {
        "unknown": 0,
        "not-recorded": 1,
        "repository-complete": 2,
        "integrated": 3,
        "released": 4,
        "published": 5,
        "deployed": 6,
    }
    weakest = min(values, key=lambda value: rank[value.state])
    sources = _operational_status_unique_sources(
        [source for value in values for source in value.sources]
    )
    return OperationalStatusValue(
        "delivery",
        weakest.state,
        f"Weakest selected work delivery state is {weakest.state}.",
        sources,
    )


def build_operational_status_snapshot(
    root: Path,
    *,
    strict: bool = False,
    focus_id: str | None = None,
    repository_id: str | None = None,
) -> OperationalStatusSnapshot:
    inspected_root = root.resolve()
    inspection = inspect_operational_status_repository(
        inspected_root,
        repository_id=repository_id,
    )
    selected = tuple(
        item for item in inspection.active_work if focus_id is None or item.item_id == focus_id
    )
    selected_repositories = inspection.repositories
    if inspection.workspace_authority is not None and focus_id is not None:
        relevant_repository_ids = _operational_relevant_repository_ids(
            inspected_root,
            selected,
        )
        if repository_id is not None and relevant_repository_ids:
            if repository_id not in relevant_repository_ids:
                raise SystemExit(
                    f"Workspace repository '{repository_id}' is not in the recorded scope "
                    f"for active work item '{focus_id}'."
                )
        elif relevant_repository_ids:
            selected_repositories = tuple(
                repository
                for repository in selected_repositories
                if repository.repository_id in relevant_repository_ids
            )
    proof, proof_work = classify_operational_proof(inspected_root, selected)
    health, health_findings = classify_operational_health(inspected_root, strict=strict)
    delivered_work: list[OperationalStatusWorkItem] = []
    delivery_findings: list[OperationalStatusFinding] = []
    for item in proof_work:
        delivery, item_findings = classify_operational_delivery(inspected_root, item)
        delivery_findings.extend(item_findings)
        item_facts = item.facts
        item_sources = item.sources
        owner_epic = next(
            (str(fact.value) for fact in item.facts if fact.key == "owner_epic" and fact.value),
            None,
        )
        intent_epic_id = item.item_id if item.kind == "epic" else owner_epic
        if intent_epic_id:
            try:
                intent_epic_dir = _resolve_epic_dir(
                    inspected_root / ".project-workflow" / "tasks", intent_epic_id
                )
                intent_requirements = (intent_epic_dir / "REQUIREMENTS.md").read_text(
                    encoding="utf-8"
                )
                if _intent_contract_mode(intent_requirements) == "full":
                    intent_evaluation = _intent_audit_evaluation(intent_epic_dir)
                    item_facts = item_facts + (
                        _operational_status_fact(
                            "intent_audit_state", str(intent_evaluation["state"])
                        ),
                    )
                    item_sources = item_sources + (
                        OperationalStatusSource(
                            "intent-audit",
                            _operational_status_artifact(
                                inspected_root, _intent_audit_path(intent_epic_dir)
                            ),
                            str(intent_evaluation["state"]),
                        ),
                    )
            except (OSError, SystemExit):
                pass
        delivered_work.append(
            OperationalStatusWorkItem(
                item.item_id,
                item.title,
                item.kind,
                item.lifecycle,
                item.operational_meaning,
                item_sources,
                item_facts,
                item.proof_layers,
                delivery,
            )
        )
    work_items = tuple(delivered_work)
    repositories = _operational_repository_evidence(
        inspected_root,
        selected_repositories,
        work_items,
    )
    delivery = _operational_aggregate_delivery(work_items)
    workspace_evidence_findings = _workspace_repository_evidence_findings(repositories)
    findings = tuple(
        [
            *inspection.findings,
            *health_findings,
            *delivery_findings,
            *workspace_evidence_findings,
        ]
    )
    blockers = tuple(finding for finding in findings if finding.severity == "error")
    primary, secondary = resolve_operational_actions(
        inspected_root,
        installation=inspection.installation,
        work_items=work_items,
        findings=findings,
        focus_id=focus_id,
    )
    return OperationalStatusSnapshot(
        str(inspected_root),
        inspection.installation,
        inspection.git,
        health,
        proof,
        delivery,
        work_items,
        findings,
        blockers,
        primary,
        secondary,
        inspection.workspace_authority,
        repositories,
    )


def _operational_status_fact_value(
    value: OperationalStatusValue,
    key: str,
    default: object = None,
) -> object:
    return next((fact.value for fact in value.facts if fact.key == key), default)


def _operational_human_sources(
    snapshot: OperationalStatusSnapshot,
) -> tuple[OperationalStatusSource, ...]:
    sources: list[OperationalStatusSource] = []
    for value in (
        snapshot.installation,
        snapshot.git,
        snapshot.health,
        snapshot.proof,
        snapshot.delivery,
    ):
        sources.extend(value.sources)
    for repository in snapshot.repositories:
        sources.extend(repository.git.sources)
        sources.extend(repository.sources)
    for item in snapshot.active_work:
        sources.extend(item.sources)
        for layer in item.proof_layers:
            sources.extend(layer.sources)
        if item.delivery is not None:
            sources.extend(item.delivery.sources)
    for finding in (*snapshot.findings, *snapshot.blockers):
        sources.extend(finding.sources)
    if snapshot.primary_action is not None:
        sources.extend(snapshot.primary_action.sources)
    for action in snapshot.secondary_actions:
        sources.extend(action.sources)
    return _operational_status_unique_sources(sources)


def render_operational_status_human(snapshot: OperationalStatusSnapshot) -> str:
    action = snapshot.primary_action
    if action is None:
        raise ValueError("Operational status snapshot requires a primary action.")
    lines = [
        "Next action",
        f"- [{action.code}] {action.title}",
        f"- Responsible: {action.responsible_party}",
        f"- Why: {action.reason}",
        (
            f"- Run: {action.command}"
            if action.command is not None
            else f"- Request: {action.request}"
        ),
        "",
        "Status",
        f"- Installation: {snapshot.installation.state} — {snapshot.installation.summary}",
        f"- Git: {snapshot.git.state} — {snapshot.git.summary}",
        (
            f"- Health: {snapshot.health.state} — {snapshot.health.summary} "
            f"(accepted warnings: "
            f"{_operational_status_fact_value(snapshot.health, 'accepted_count', 0)})"
        ),
        f"- Proof: {snapshot.proof.state} — {snapshot.proof.summary}",
        f"- Delivery: {snapshot.delivery.state} — {snapshot.delivery.summary}",
    ]
    if snapshot.workspace_authority is not None:
        lines.extend(("", "Workspace repositories"))
        for repository in snapshot.repositories:
            authority = " (authority)" if repository.authority else ""
            lines.append(
                f"- {repository.repository_id}{authority} [{repository.role}] "
                f"{repository.path} — Git {repository.git.state}: {repository.git.summary}"
            )
    lines.extend(("", "Active work"))
    if snapshot.active_work:
        for item in snapshot.active_work:
            aggregate_proof = next(
                (fact.value for fact in item.facts if fact.key == "aggregate_proof_state"),
                "not-recorded",
            )
            delivery_state = item.delivery.state if item.delivery is not None else "unknown"
            intent_state = next(
                (fact.value for fact in item.facts if fact.key == "intent_audit_state"),
                None,
            )
            intent_suffix = f"; intent {intent_state}" if intent_state else ""
            outcome_state = next(
                (fact.value for fact in item.facts if fact.key == "outcome_proof_state"),
                "not-recorded",
            )
            owner_acceptance_state = next(
                (fact.value for fact in item.facts if fact.key == "owner_acceptance_state"),
                "not-recorded",
            )
            lines.append(
                f"- {item.item_id} [{item.lifecycle}] {item.title} — "
                f"proof {aggregate_proof}; outcome {outcome_state}; owner acceptance "
                f"{owner_acceptance_state}; delivery {delivery_state}{intent_suffix}"
            )
    else:
        lines.append("- None selected or active.")

    lines.extend(("", "Findings"))
    if snapshot.findings:
        lines.extend(
            f"- {finding.severity}: {finding.code} — {finding.message}"
            for finding in snapshot.findings
        )
    else:
        lines.append("- None.")

    lines.extend(("", "Secondary actions"))
    if snapshot.secondary_actions:
        for secondary in snapshot.secondary_actions:
            instruction = secondary.command or secondary.request
            lines.append(
                f"- [{secondary.code}] {secondary.title} "
                f"({secondary.responsible_party}): {instruction}"
            )
    else:
        lines.append("- None.")

    lines.extend(("", "Sources"))
    lines.extend(
        f"- {source.kind}: {source.artifact}" + (f" — {source.detail}" if source.detail else "")
        for source in _operational_human_sources(snapshot)
    )
    return "\n".join(lines) + "\n"


def _doctor_check_source_mirrors(root: Path, issues: list[DoctorIssue]) -> None:
    def matches_packaged(local_path: Path, packaged_path: Path) -> bool:
        local_content = local_path.read_text(encoding="utf-8")
        packaged_content = packaged_path.read_text(encoding="utf-8")
        return local_content in {
            packaged_content,
            _with_generated_marker(local_path, packaged_content),
        }

    dev_prompts_dir = root / ".github" / "prompts"
    packaged_prompts_dir = root / "src" / "project_workflow" / "prompts"
    if dev_prompts_dir.exists() and packaged_prompts_dir.exists():
        for prompt_file in PROMPT_FILES:
            dev_path = dev_prompts_dir / prompt_file
            packaged_path = packaged_prompts_dir / prompt_file
            if not dev_path.exists():
                _add_issue(issues, "error", dev_path, "Development prompt is missing.")
                continue
            if not packaged_path.exists():
                _add_issue(issues, "error", packaged_path, "Packaged prompt is missing.")
                continue
            if not matches_packaged(dev_path, packaged_path):
                _add_issue(
                    issues,
                    "error",
                    dev_path,
                    f"Prompt differs from packaged mirror: {packaged_path}",
                )

    local_cli_dir = root / ".project-workflow" / "cli"
    packaged_template_dir = root / "src" / "project_workflow" / "templates"
    mirror_pairs = (
        (
            local_cli_dir / "workflow.py",
            packaged_template_dir / "workflow.py",
            "Local workflow CLI differs from packaged template",
        ),
        (
            local_cli_dir / "workflow",
            packaged_template_dir / "workflow",
            "Local workflow CLI differs from packaged template",
        ),
        (
            local_cli_dir / "adapter_common.py",
            root / "src/project_workflow/adapter_common.py",
            "Local adapter foundation differs from packaged source",
        ),
        (
            local_cli_dir / "codex_adapter.py",
            root / "src/project_workflow/codex_adapter.py",
            "Local Codex adapter differs from packaged source",
        ),
        (
            local_cli_dir / "claude_adapter.py",
            root / "src/project_workflow/claude_adapter.py",
            "Local Claude adapter differs from packaged source",
        ),
        (
            local_cli_dir
            / "claude_plugin/project-workflow-execution-control/.claude-plugin/plugin.json",
            root / "src/project_workflow/claude_plugin/project-workflow-execution-control/"
            ".claude-plugin/plugin.json",
            "Local Claude plugin manifest differs from packaged source",
        ),
        (
            local_cli_dir / "claude_plugin/project-workflow-execution-control/hooks/hooks.json",
            root / "src/project_workflow/claude_plugin/project-workflow-execution-control/"
            "hooks/hooks.json",
            "Local Claude hooks differ from packaged source",
        ),
        (
            local_cli_dir / "claude_plugin/project-workflow-execution-control/scripts/"
            "project-workflow-claude-hook",
            root / "src/project_workflow/claude_plugin/project-workflow-execution-control/scripts/"
            "project-workflow-claude-hook",
            "Local Claude hook launcher differs from packaged source",
        ),
        (
            root / ".agents/skills/project-delegate/SKILL.md",
            root / "src/project_workflow/codex/skills/project-delegate/SKILL.md",
            "Installed Codex Delegate skill differs from packaged source",
        ),
        (
            root / ".agents/skills/project-coordinator/SKILL.md",
            root / "src/project_workflow/codex/skills/project-coordinator/SKILL.md",
            "Installed Codex Coordinator skill differs from packaged source",
        ),
        (
            root / ".agents/skills/project-clarify/SKILL.md",
            root / "src/project_workflow/codex/skills/project-clarify/SKILL.md",
            "Installed Codex Clarify skill differs from packaged source",
        ),
    )
    for local_path, packaged_path, mismatch_label in mirror_pairs:
        if not local_path.exists() or not packaged_path.exists():
            continue
        if not matches_packaged(local_path, packaged_path):
            _add_issue(
                issues,
                "error",
                local_path,
                f"{mismatch_label}: {packaged_path}",
            )


def _doctor_check_delegate_semantics(root: Path, issues: list[DoctorIssue]) -> None:
    required = (
        "task or epic",
        "verified",
        "unsupported",
        "unknown",
        "available child",
        "coordinator",
        "descendants",
        "unrelated",
        "independent qa",
    )
    candidates = (
        root / "src/project_workflow/prompts/Delegate.prompt.md",
        root / "src/project_workflow/codex/skills/project-delegate/SKILL.md",
        root / ".github/prompts/Delegate.prompt.md",
        root / ".agents/skills/project-delegate/SKILL.md",
        root / ".claude/agents/project-delegate.md",
        root / ".cursor/agents/project-delegate.md",
    )
    for path in candidates:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        if relative.startswith(
            (".agents/skills/", ".github/prompts/")
        ) and not _is_generated_content(text):
            # A user-owned active collision is reported by the pending-update check.
            continue
        lowered = text.lower()
        missing = [term for term in required if term not in lowered]
        stale = any(
            term in lowered
            for term in (
                "workers:4",
                "worker limit",
                "on first work-item failure",
                "enter fail-fast mode",
            )
        )
        placeholder_leak = relative.startswith((".claude/agents/", ".cursor/agents/")) and (
            "${input:" in text
        )
        if missing or stale or placeholder_leak:
            details = []
            if missing:
                details.append("missing " + ", ".join(missing))
            if stale:
                details.append("contains stale fixed-capacity or blanket-failure guidance")
            if placeholder_leak:
                details.append("contains GitHub Copilot input placeholders")
            _add_issue(
                issues,
                "error",
                path,
                "Delegate semantic asset is invalid: " + "; ".join(details) + ".",
                code="PW_GENERATED_ASSET_DRIFT",
                remediation_owner="project-workflow",
                mechanically_upgradeable=True,
            )


def _doctor_check_coordinator_clarify_semantics(root: Path, issues: list[DoctorIssue]) -> None:
    contracts = (
        (
            "Coordinator",
            (
                "single owner-facing",
                "only writer",
                "smallest sufficient",
                "bounded packet",
                "independent qa",
                "stop after sufficient proof",
                "one full minor release",
            ),
            (
                root / "src/project_workflow/prompts/Coordinator.prompt.md",
                root / "src/project_workflow/codex/skills/project-coordinator/SKILL.md",
                root / ".github/prompts/Coordinator.prompt.md",
                root / ".agents/skills/project-coordinator/SKILL.md",
                root / ".claude/agents/project-coordinator.md",
                root / ".cursor/agents/project-coordinator.md",
            ),
        ),
        (
            "Clarify",
            (
                "pre-approval",
                "post-plan",
                "drift-ambiguity",
                "epic parent",
                "inside-envelope",
                "drift-detected",
                "approved-change",
                "not periodic",
                "does not monitor",
            ),
            (
                root / "src/project_workflow/prompts/Clarify.prompt.md",
                root / "src/project_workflow/codex/skills/project-clarify/SKILL.md",
                root / ".github/prompts/Clarify.prompt.md",
                root / ".agents/skills/project-clarify/SKILL.md",
                root / ".claude/agents/project-clarify.md",
                root / ".cursor/agents/project-clarify.md",
            ),
        ),
    )
    for label, required, candidates in contracts:
        for path in candidates:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            relative = path.relative_to(root).as_posix()
            if relative.startswith(
                (".agents/skills/", ".github/prompts/")
            ) and not _is_generated_content(text):
                continue
            lowered = " ".join(text.lower().split())
            missing = [term for term in required if term not in lowered]
            placeholder_leak = relative.startswith((".claude/agents/", ".cursor/agents/")) and (
                "${input:" in text
            )
            if missing or placeholder_leak:
                details = []
                if missing:
                    details.append("missing " + ", ".join(missing))
                if placeholder_leak:
                    details.append("contains GitHub Copilot input placeholders")
                _add_issue(
                    issues,
                    "error",
                    path,
                    f"{label} semantic asset is invalid: " + "; ".join(details) + ".",
                    code="PW_GENERATED_ASSET_DRIFT",
                    remediation_owner="project-workflow",
                    mechanically_upgradeable=True,
                )

    compatibility = _repository_compatibility(root)
    if compatibility.manifest is not None and compatibility.manifest.asset_version >= 2:
        ignore_path = root / ".project-workflow/.gitignore"
        ignore_text = ignore_path.read_text(encoding="utf-8") if ignore_path.is_file() else ""
        if "runtime/delegations/" not in {line.strip() for line in ignore_text.splitlines()}:
            _add_issue(
                issues,
                "error",
                ignore_path,
                "Delegate runtime handles are not protected by the managed workflow ignore.",
                code="PW_GENERATED_ASSET_DRIFT",
                remediation_owner="project-workflow",
                mechanically_upgradeable=True,
            )


def _doctor_check_coordination_state(root: Path, issues: list[DoctorIssue]) -> None:
    tasks_dir = root / ".project-workflow" / "tasks"
    if not tasks_dir.is_dir():
        return
    for path in sorted(tasks_dir.rglob(COORDINATION_FILENAME)):
        target_id = path.parent.name.split("-", 2)[:2]
        expected_id = "-".join(target_id) if len(target_id) == 2 else ""
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            _coordination_validate_state(payload, target_id=expected_id or None)
            actual_id = str(payload["target_id"])
            decisions = payload["boundary_decisions"]
            assert isinstance(decisions, list)
            for decision in decisions:
                if not isinstance(decision, dict):
                    raise ValueError("boundary_decisions entries must be objects.")
                if decision.get("boundary") not in COORDINATION_BOUNDARIES:
                    raise ValueError("boundary_decisions contains an unknown boundary.")
                classification = decision.get("classification")
                if classification not in COORDINATION_DRIFT_CLASSIFICATIONS:
                    raise ValueError("boundary_decisions contains an unknown classification.")
                if classification == "approved-change" and not decision.get("amendment_identity"):
                    raise ValueError("approved-change decision is missing amendment_identity.")
                _coordination_required_text(
                    decision.get("intent_identity"), "boundary_decisions.intent_identity"
                )
                _coordination_required_text(
                    decision.get("source_revision"), "boundary_decisions.source_revision"
                )
                source_identity = decision.get("source_identity")
                if source_identity is not None and (
                    not isinstance(source_identity, str)
                    or not re.fullmatch(r"sha256:[0-9a-f]{64}", source_identity)
                ):
                    raise ValueError("boundary_decisions.source_identity is invalid.")
            preflight = _coordination_preflight_payload(root, actual_id, payload)
            if preflight["contract_state"] not in {"current", "compatible"}:
                _add_issue(
                    issues,
                    "warning",
                    path,
                    "Coordination context contract is "
                    f"{preflight['contract_state']}; explicitly load and declare the applicable "
                    "contract before affected work continues.",
                    code="PW_WORKFLOW_INVALID",
                    remediation_owner="agent",
                    mechanically_upgradeable=False,
                )
            campaign = payload.get("verification_campaign")
            if isinstance(campaign, dict) or payload.get("verification_requirement") is not None:
                projection = _verification_campaign_projection(root, actual_id, payload)
                if projection["campaign_current"] is False:
                    raw_reasons = projection["reasons"]
                    assert isinstance(raw_reasons, list)
                    _add_issue(
                        issues,
                        "error",
                        path,
                        "Verification campaign is stale: "
                        + "; ".join(str(reason) for reason in raw_reasons)
                        + ".",
                        code="PW_WORKFLOW_INVALID",
                        remediation_owner="agent",
                        mechanically_upgradeable=False,
                    )
                elif projection["operational_state"] in {
                    "verification-required",
                    "blocked",
                }:
                    _add_issue(
                        issues,
                        "warning",
                        path,
                        "Material verification is "
                        f"{projection['operational_state']}: {projection['next_action']}",
                        code="PW_WORKFLOW_INVALID",
                        remediation_owner="agent",
                        mechanically_upgradeable=False,
                    )
            execution_control = payload.get("execution_control")
            if execution_control is not None:
                _execution_validate_control(execution_control, work_id=actual_id)
                execution = _execution_control_projection(root, actual_id, "material-execution")
                if execution["state"] == "blocked":
                    _add_issue(
                        issues,
                        "warning",
                        path,
                        "Material execution is blocked: "
                        f"{execution['reason']}. {execution['next_action']}",
                        code="PW_WORKFLOW_INVALID",
                        remediation_owner="agent",
                        mechanically_upgradeable=False,
                    )
            qa_campaign = _execution_qa_projection(payload.get("execution_qa"), actual_id)
            if isinstance(qa_campaign, dict) and qa_campaign["state"] == "blocked":
                _add_issue(
                    issues,
                    "warning",
                    path,
                    "Execution QA campaign is blocked: " + str(qa_campaign["next_action"]),
                    code="PW_WORKFLOW_INVALID",
                    remediation_owner="agent",
                    mechanically_upgradeable=False,
                )
            fixed_release = _execution_fixed_release_projection(
                root, payload.get("fixed_release"), actual_id
            )
            if isinstance(fixed_release, dict) and fixed_release["state"] in {
                "blocked",
                "terminal-fail",
            }:
                _add_issue(
                    issues,
                    "warning",
                    path,
                    f"Fixed release is {fixed_release['state']}: {fixed_release['next_action']}",
                    code="PW_WORKFLOW_INVALID",
                    remediation_owner="agent",
                    mechanically_upgradeable=False,
                )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            _add_issue(
                issues,
                "error",
                path,
                f"Coordination state is invalid: {exc}",
                code="PW_WORKFLOW_INVALID",
                remediation_owner="agent",
                mechanically_upgradeable=False,
            )


def _doctor_check_pending_generated_updates(root: Path, issues: list[DoctorIssue]) -> None:
    checked_roots = (
        root / ".project-workflow" / "cli",
        root / ".github" / "prompts",
        root / ".claude" / "agents",
        root / ".agents" / "skills",
        root / ".cursor" / "agents",
        root / ".cursor" / "rules",
    )
    for checked_root in checked_roots:
        if not checked_root.exists():
            continue
        for path in sorted(checked_root.rglob("*")):
            if ".new" not in path.name:
                continue
            _add_issue(
                issues,
                "warning",
                path,
                "Generated project-workflow update is pending because init preserved an unmarked existing file.",
            )


def _doctor_check_namespace_config(root: Path, issues: list[DoctorIssue]) -> WorkflowConfig | None:
    config_path = _workflow_config_path(root)
    try:
        return _load_workflow_config(root)
    except SystemExit as exc:
        _add_issue(issues, "error", config_path, str(exc))
        return None


def _doctor_check_workspace_authority(
    root: Path,
    config: WorkflowConfig | None,
    issues: list[DoctorIssue],
) -> None:
    if config is None or config.workspace is None:
        return
    for repository in config.workspace.repositories:
        if repository.repository_id == config.workspace.authority_repository:
            continue
        workflow_path = repository.resolved_path / ".project-workflow"
        if workflow_path.exists():
            _add_issue(
                issues,
                "error",
                workflow_path,
                f"Registered non-authority repository '{repository.repository_id}' contains "
                "a competing .project-workflow state. Remove or archive the child workflow "
                "state outside the repository and keep the parent authority authoritative.",
                code="PW_WORKSPACE_AUTHORITY_CONFLICT",
                remediation_owner="owner",
                mechanically_upgradeable=False,
            )


def _doctor_check_row_namespace(
    row_id: str,
    *,
    config: WorkflowConfig | None,
    path: Path,
    issues: list[DoctorIssue],
) -> None:
    if config is None:
        return
    prefix = _task_prefix_from_id(row_id)
    if prefix is None or prefix in {EPIC_ID_PREFIX, FIX_ID_PREFIX}:
        return
    if prefix not in config.task_id_prefixes:
        _add_issue(
            issues,
            "warning",
            path,
            f"{row_id} uses unconfigured task ID prefix '{prefix}'. "
            f"Configured prefixes: {', '.join(config.task_id_prefixes)}.",
        )


def _doctor_check_row_id_format(
    row_id: str,
    *,
    config: WorkflowConfig | None,
    path: Path,
    issues: list[DoctorIssue],
    task_only: bool = False,
) -> None:
    if config is None:
        return
    if not task_only and row_id.startswith(f"{EPIC_ID_PREFIX}-"):
        if not _valid_epic_id(row_id, config=config):
            _add_issue(issues, "error", path, f"{row_id} has invalid epic ID format.")
        return
    if not task_only and row_id.startswith(f"{FIX_ID_PREFIX}-"):
        if not _valid_fix_id(row_id, config=config):
            _add_issue(issues, "error", path, f"{row_id} has invalid Fix ID format.")
        return

    prefix = _task_prefix_from_id(row_id)
    if prefix is None:
        _add_issue(issues, "error", path, f"{row_id} has invalid task ID format.")
        return
    if prefix in config.task_id_prefixes and not _valid_task_id(row_id, config=config):
        _add_issue(issues, "error", path, f"{row_id} has invalid task ID format.")


def _doctor_check_duplicate_tracker_ids(root: Path, issues: list[DoctorIssue]) -> None:
    workflow_dir = root / ".project-workflow"
    tracker_paths = [workflow_dir / "TRACKER.md"]
    tasks_dir = workflow_dir / "tasks"
    if tasks_dir.exists():
        tracker_paths.extend(sorted(tasks_dir.glob(f"{EPIC_ID_PREFIX}-*/TRACKER.md")))

    seen: dict[str, Path] = {}
    reported: set[str] = set()
    for tracker_path in tracker_paths:
        if not tracker_path.exists():
            continue
        try:
            if tracker_path.name == "TRACKER.md" and tracker_path.parent == workflow_dir:
                _lines, _header_idx, rows = _global_tracker_rows(tracker_path)
            else:
                _lines, _header_idx, rows = _epic_tracker_rows(tracker_path)
        except SystemExit:
            continue
        for row in rows:
            row_id = row.get("ID", "").strip()
            if not row_id:
                continue
            if row_id in seen and row_id not in reported:
                _add_issue(
                    issues,
                    "error",
                    tracker_path,
                    f"Duplicate workflow ID '{row_id}' also appears in {seen[row_id]}.",
                )
                reported.add(row_id)
            else:
                seen[row_id] = tracker_path


def _doctor_check_task_doc(
    *,
    root: Path,
    docs_rel: str,
    status: str,
    row_id: str,
    issues: list[DoctorIssue],
    parent_requirements_path: Path | None = None,
) -> None:
    if not docs_rel:
        _add_issue(issues, "warning", ".project-workflow/TRACKER.md", f"{row_id} has no docs path.")
        return

    docs_path = root / ".project-workflow" / docs_rel
    if not docs_path.exists():
        _add_issue(issues, "error", docs_path, f"{row_id} docs path does not exist.")
        return

    try:
        docs_text = docs_path.read_text(encoding="utf-8")
    except OSError as exc:
        _add_issue(issues, "error", docs_path, f"Could not read docs for {row_id}: {exc}")
        return

    requirements_path = docs_path.parent / "REQUIREMENTS.md"
    requirements_text: str | None = None
    if requirements_path.exists():
        requirements_text = requirements_path.read_text(encoding="utf-8")
    has_completion_evidence = _has_qa_review_evidence(
        docs_text,
        requirements_text=requirements_text,
    ) or _has_epic_acceptance_audit_evidence(docs_path, row_id)
    if status == "Complete" and not has_completion_evidence:
        _add_issue(
            issues,
            "warning",
            docs_path,
            f"{row_id} is Complete but lacks non-placeholder QA/code-review evidence.",
        )
    if status == "Complete":
        for intent_qa_issue in _intent_qa_review_issues(docs_text):
            _add_issue(
                issues,
                "warning",
                docs_path,
                f"{row_id} intent-adversarial QA: {intent_qa_issue}.",
            )

    if requirements_text is not None and status in ("Review", "Complete"):
        if _legacy_adoption_evidence_untrusted(requirements_text):
            _add_issue(
                issues,
                "warning",
                requirements_path,
                f"{row_id} adopted legacy evidence is untrusted until refreshed.",
            )
    if (
        requirements_path.exists()
        and docs_path.name == "IMPLEMENTATION.md"
        and status
        in (
            "Review",
            "Complete",
        )
    ):
        parent_ac_ids: set[str] | None = None
        if parent_requirements_path is not None:
            parent_section = _markdown_section(docs_text, "Parent AC Coverage")
            parent_ac_ids = _extract_ac_ids(parent_section)
        for evidence_issue in _structured_evidence_issues(
            requirements_path=requirements_path,
            implementation_path=docs_path,
            parent_ac_ids=parent_ac_ids,
            include_explicit_nonpassing=status != "Complete",
        ):
            _add_issue(
                issues,
                "error",
                docs_path,
                f"{row_id} {evidence_issue}",
            )
        for repository_issue in _repository_evidence_issues(
            root,
            requirements_text or "",
            docs_text,
        ):
            _add_issue(
                issues,
                "error",
                docs_path,
                f"{row_id} {repository_issue}",
            )
    if parent_requirements_path is not None and status in (
        "Approved",
        "In Progress",
        "Testing",
        "Review",
        "Complete",
    ):
        for approval_issue in _requirements_approval_issues_for_path(
            parent_requirements_path,
            require_decomposition=True,
        ):
            _add_issue(
                issues,
                "warning",
                parent_requirements_path,
                f"{row_id} parent approval envelope: {approval_issue}",
            )
        if status != "Complete" and requirements_text is not None:
            for charter_issue in _legacy_truncated_child_charter_issues(
                epic_dir=parent_requirements_path.parent,
                requirements_text=requirements_text,
                implementation_text=docs_text,
            ):
                _add_issue(
                    issues,
                    "error",
                    docs_path,
                    f"{row_id} child charter integrity: {charter_issue}",
                )
    elif requirements_text is not None and not _is_discovery_work(requirements_text, docs_text):
        approval_required = False
        require_decomposition = False
        require_implementation = False
        if row_id.startswith(f"{EPIC_ID_PREFIX}-"):
            approval_required = status in ("Ready", "In Progress", "Closeout", "Complete")
            require_decomposition = approval_required
        else:
            approval_required = _status_requires_task_readiness(status)
            require_implementation = approval_required
        if approval_required:
            for approval_issue in _approval_envelope_issues(
                requirements_text,
                require_decomposition=require_decomposition,
                require_implementation=require_implementation,
            ):
                _add_issue(
                    issues,
                    "warning",
                    requirements_path,
                    f"{row_id} approval envelope: {approval_issue}",
                )
    if status not in ("To Do", "N/A") and requirements_text is not None:
        if "____" in requirements_text:
            _add_issue(
                issues,
                "warning",
                requirements_path,
                f"{row_id} has active status '{status}' but requirements still contain placeholders.",
            )
    if (
        docs_path.name == "IMPLEMENTATION.md"
        and status != "Complete"
        and _status_requires_task_readiness(status)
    ):
        if requirements_text is not None:
            for readiness_issue in _task_readiness_issues(
                requirements_text=requirements_text,
                implementation_text=docs_text,
            ):
                _add_issue(
                    issues,
                    "warning",
                    docs_path,
                    f"{row_id} readiness gate: {readiness_issue}",
                )
    if (
        docs_path.name == "IMPLEMENTATION.md"
        and requirements_text is not None
        and _status_requires_task_readiness(status)
    ):
        for repository_issue in _repository_scope_issues(root, requirements_text):
            _add_issue(
                issues,
                "error",
                requirements_path,
                f"{row_id} repository scope: {repository_issue}",
            )
    if docs_path.name == "REQUIREMENTS.md" and row_id.startswith(f"{EPIC_ID_PREFIX}-"):
        if status not in ("To Do", "N/A"):
            for readiness_issue in _epic_requirements_readiness_issues(docs_text):
                _add_issue(
                    issues,
                    "warning",
                    docs_path,
                    f"{row_id} epic readiness gate: {readiness_issue}",
                )

    _doctor_check_implementation_ac_mapping(
        docs_path=docs_path,
        docs_text=docs_text,
        status=status,
        row_id=row_id,
        issues=issues,
    )


def _doctor_check_fix_doc(
    *,
    root: Path,
    docs_rel: str,
    status: str,
    row_id: str,
    config: WorkflowConfig | None,
    issues: list[DoctorIssue],
) -> None:
    fix_path = root / ".project-workflow" / docs_rel
    if fix_path.name != "FIX.md" or not fix_path.exists():
        _add_issue(issues, "error", fix_path, f"{row_id} must point to an existing FIX.md.")
        return
    try:
        fix_text = fix_path.read_text(encoding="utf-8")
    except OSError as exc:
        _add_issue(issues, "error", fix_path, f"Could not read {row_id}: {exc}")
        return
    summary = _fix_values(fix_text, "Summary")
    for heading in (
        "Summary",
        "Report",
        "Routing",
        "Classification",
        "Related Work",
        "Risk",
        "Fix Plan",
        "Verification",
        "Outcome",
    ):
        if not _markdown_section(fix_text, heading):
            _add_issue(issues, "error", fix_path, f"{row_id} is missing `## {heading}`.")
    if summary.get("fix") != row_id:
        _add_issue(issues, "error", fix_path, f"Summary Fix ID does not match {row_id}.")
    if summary.get("status") != status:
        _add_issue(
            issues,
            "error",
            fix_path,
            f"Summary status '{summary.get('status', '')}' does not match tracker '{status}'.",
        )
    classification = _fix_values(fix_text, "Classification")
    classification_type = classification.get("type")
    if (
        not _fix_value_missing(classification_type)
        and classification_type not in FIX_CLASSIFICATIONS
    ):
        _add_issue(
            issues,
            "error",
            fix_path,
            f"{row_id} has invalid classification Type '{classification_type}'.",
        )
    mode = classification.get("mode")
    if not _fix_value_missing(mode) and mode not in FIX_MODES:
        _add_issue(issues, "error", fix_path, f"{row_id} has invalid Mode '{mode}'.")
    severity = classification.get("severity")
    if not _fix_value_missing(severity) and severity not in FIX_SEVERITIES:
        _add_issue(issues, "error", fix_path, f"{row_id} has invalid Severity '{severity}'.")
    if status in {"Ready", "In Progress", "Testing", "Review", "Complete"}:
        try:
            triage_issues = _fix_triage_issues(
                root,
                fix_text,
                require_active_disposition=status != "Complete",
            )
        except SystemExit as exc:
            triage_issues = [str(exc)]
        for triage_issue in triage_issues:
            _add_issue(issues, "error", fix_path, f"{row_id} triage: {triage_issue}.")
    if status in {"Review", "Complete"}:
        for repository_issue in _repository_evidence_issues(
            root,
            fix_text,
            fix_text,
        ):
            _add_issue(
                issues,
                "error",
                fix_path,
                f"{row_id} {repository_issue}",
            )
    if status == "Complete":
        for closeout_issue in _fix_closeout_issues(root, fix_text):
            _add_issue(issues, "error", fix_path, f"{row_id} closeout: {closeout_issue}.")
    if status == "N/A":
        for closeout_issue in _fix_non_delivery_closeout_issues(fix_text):
            _add_issue(issues, "error", fix_path, f"{row_id} closeout: {closeout_issue}.")
    related = _fix_values(fix_text, "Related Work")
    refs = (
        _extract_workflow_ref_ids(related.get("originating work", ""), config=config)
        if config is not None
        else set()
    )
    if refs:
        tracker_path = root / ".project-workflow" / "TRACKER.md"
        try:
            _lines, _header_idx, tracker_rows = _global_tracker_rows(tracker_path)
            known_ids = {row["ID"] for row in tracker_rows}
        except SystemExit:
            known_ids = set()
        for ref in sorted(refs - known_ids):
            _add_issue(
                issues,
                "warning",
                fix_path,
                f"{row_id} related work reference '{ref}' is not in the local global tracker.",
            )


def _doctor_check_global_tracker(
    root: Path, issues: list[DoctorIssue], *, config: WorkflowConfig | None
) -> None:
    workflow_dir = root / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        _add_issue(issues, "error", tracker_path, "Global tracker is missing.")
        return

    rows = _parse_markdown_table(
        tracker_path,
        expected_columns=GLOBAL_TRACKER_COLUMNS,
        issues=issues,
        label="Global tracker",
    )
    for row in rows:
        row_id = row["ID"]
        _doctor_check_row_id_format(row_id, config=config, path=tracker_path, issues=issues)
        _doctor_check_row_namespace(row_id, config=config, path=tracker_path, issues=issues)
        status = row["Status"]
        if status not in TRACKER_STATUSES:
            _add_issue(
                issues,
                "error",
                tracker_path,
                f"{row_id} has invalid status '{status}'.",
            )
        docs_rel = _clean_markdown_cell_path(row["Docs"])
        if row_id.startswith(f"{FIX_ID_PREFIX}-"):
            _doctor_check_fix_doc(
                root=root,
                docs_rel=docs_rel,
                status=status,
                row_id=row_id,
                config=config,
                issues=issues,
            )
        else:
            _doctor_check_task_doc(
                root=root,
                docs_rel=docs_rel,
                status=status,
                row_id=row_id,
                issues=issues,
            )


def _doctor_check_backlog(
    root: Path, issues: list[DoctorIssue], *, config: WorkflowConfig | None
) -> None:
    backlog_path = _backlog_path(root)
    if not backlog_path.exists():
        return
    if config is None:
        return
    issues.extend(_backlog_validation_issues(root, backlog_path, config=config))


def _doctor_check_epic_trackers(
    root: Path, issues: list[DoctorIssue], *, config: WorkflowConfig | None
) -> None:
    tasks_dir = root / ".project-workflow" / "tasks"
    if not tasks_dir.exists():
        return

    for epic_tracker_path in sorted(tasks_dir.glob(f"{EPIC_ID_PREFIX}-*/TRACKER.md")):
        try:
            _lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
        except SystemExit as exc:
            _add_issue(issues, "error", epic_tracker_path, str(exc))
            continue
        parent_requirements_path = epic_tracker_path.parent / "REQUIREMENTS.md"
        parent_approval_issues = _requirements_approval_issues_for_path(
            parent_requirements_path,
            require_decomposition=True,
        )
        authority_severity = "warning" if parent_approval_issues else "error"
        for contract_issue in _epic_contract_issues_for_path(epic_tracker_path.parent):
            _add_issue(
                issues,
                authority_severity,
                _epic_contract_path(epic_tracker_path.parent),
                f"{epic_tracker_path.parent.name} epic contract: {contract_issue}",
            )
        active_audit_statuses = {row.get("Status", "") for row in rows} & {
            "In Progress",
            "Testing",
            "Review",
            "Complete",
        }
        parent_requirements_text = (
            parent_requirements_path.read_text(encoding="utf-8")
            if parent_requirements_path.exists()
            else ""
        )
        if active_audit_statuses and _intent_contract_mode(parent_requirements_text) == "full":
            audit_evaluation = _intent_audit_evaluation(epic_tracker_path.parent)
            if audit_evaluation["state"] != "current":
                severity = "error" if active_audit_statuses & {"Review", "Complete"} else "warning"
                _add_issue(
                    issues,
                    severity,
                    _intent_audit_path(epic_tracker_path.parent),
                    f"{epic_tracker_path.parent.name} intent audit is "
                    f"{audit_evaluation['state']}; run `epic intent-audit --epic-id "
                    f"{epic_tracker_path.parent.name.split('-', 2)[0]}-"
                    f"{epic_tracker_path.parent.name.split('-', 2)[1]}` and refresh the "
                    "sourced semantic review.",
                    code="PW_INTENT_AUDIT_NOT_CURRENT",
                    remediation_owner="agent",
                    mechanically_upgradeable=False,
                )
        for row in rows:
            row_id = row["ID"]
            _doctor_check_row_id_format(
                row_id,
                config=config,
                path=epic_tracker_path,
                issues=issues,
                task_only=True,
            )
            _doctor_check_row_namespace(
                row_id, config=config, path=epic_tracker_path, issues=issues
            )
            status = row["Status"]
            if status not in EPIC_TRACKER_STATUSES:
                _add_issue(
                    issues,
                    "error",
                    epic_tracker_path,
                    f"{row_id} has invalid epic status '{status}'.",
                )
            if status in EPIC_CHILD_GATED_STATUSES:
                for authority_issue in _decomposition_plan_authority_issues(
                    epic_dir=epic_tracker_path.parent,
                    row=row,
                ):
                    _add_issue(
                        issues,
                        authority_severity,
                        _decomposition_plan_path(epic_tracker_path.parent),
                        f"{row_id} decomposition authority: {authority_issue}",
                    )
            docs_rel = _clean_markdown_cell_path(row["Docs"])
            if not docs_rel and status in (
                "Approved",
                "In Progress",
                "Testing",
                "Review",
                "Complete",
            ):
                for approval_issue in parent_approval_issues:
                    _add_issue(
                        issues,
                        "warning",
                        parent_requirements_path,
                        f"{row_id} parent approval envelope: {approval_issue}",
                    )
            if docs_rel:
                _doctor_check_task_doc(
                    root=root,
                    docs_rel=docs_rel,
                    status=status,
                    row_id=row_id,
                    issues=issues,
                    parent_requirements_path=epic_tracker_path.parent / "REQUIREMENTS.md",
                )


def _doctor_check_repository_compatibility(root: Path, issues: list[DoctorIssue]) -> None:
    compatibility = _repository_compatibility(root)
    manifest_path = _workflow_manifest_path(root)
    if compatibility.state == "current":
        return
    if compatibility.state == "legacy-unversioned":
        _add_issue(
            issues,
            "warning",
            manifest_path,
            "Repository is a recognized pre-versioned project-workflow installation; "
            "run `project upgrade` to plan the schema migration.",
            code="PW_REPOSITORY_LEGACY_UNVERSIONED",
            remediation_owner="project-workflow",
            mechanically_upgradeable=True,
        )
    elif compatibility.state == "upgradeable":
        schema_behind = compatibility.reason in {"schema-behind", "assets-and-schema-behind"}
        _add_issue(
            issues,
            "warning",
            manifest_path,
            (
                "Repository schema is behind; run `project upgrade` to plan the migration."
                if schema_behind
                else "Generated assets are behind; run canonical `project init` to refresh them."
            ),
            code=(
                "PW_REPOSITORY_SCHEMA_BEHIND" if schema_behind else "PW_REPOSITORY_ASSETS_BEHIND"
            ),
            remediation_owner="project-workflow",
            mechanically_upgradeable=True,
        )
    elif compatibility.state == "unsupported-future":
        _add_issue(
            issues,
            "error",
            manifest_path,
            f"Repository uses an unsupported future contract: {compatibility.reason}.",
            code="PW_REPOSITORY_UNSUPPORTED_FUTURE",
            remediation_owner="owner",
            mechanically_upgradeable=False,
        )
    elif compatibility.state == "invalid":
        _add_issue(
            issues,
            "error",
            manifest_path,
            f"Repository manifest is invalid: {compatibility.reason}.",
            code="PW_REPOSITORY_INVALID",
            remediation_owner="owner",
            mechanically_upgradeable=False,
        )
    else:
        _add_issue(
            issues,
            "error",
            manifest_path,
            "Repository is not initialized; run canonical `project init`.",
            code="PW_REPOSITORY_NOT_INITIALIZED",
            remediation_owner="project-workflow",
            mechanically_upgradeable=True,
        )


def run_doctor(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    _doctor_check_repository_compatibility(root, issues)
    config = _doctor_check_namespace_config(root, issues)
    _doctor_check_workspace_authority(root, config, issues)
    _doctor_check_source_mirrors(root, issues)
    _doctor_check_delegate_semantics(root, issues)
    _doctor_check_coordinator_clarify_semantics(root, issues)
    _doctor_check_coordination_state(root, issues)
    _doctor_check_pending_generated_updates(root, issues)
    _doctor_check_backlog(root, issues, config=config)
    _doctor_check_duplicate_tracker_ids(root, issues)
    _doctor_check_global_tracker(root, issues, config=config)
    _doctor_check_epic_trackers(root, issues, config=config)
    return issues


def _doctor_issue_is_blocking(issue: DoctorIssue, *, strict: bool) -> bool:
    return issue.severity == "error" or (strict and issue.severity == "warning")


def _doctor_issue_is_legacy(issue: DoctorIssue) -> bool:
    if issue.severity != "warning":
        return False
    path_text = str(issue.path)
    if ".project-workflow/tasks/APP-" in path_text:
        return True
    if "uses unconfigured task ID prefix 'APP'" in issue.message:
        return True
    match = re.search(r"\.project-workflow/tasks/EPIC-(\d+)-", path_text)
    return bool(match and int(match.group(1)) < 3)


def _doctor_issue_path_for_fingerprint(issue: DoctorIssue, root: Path) -> str:
    issue_path = Path(issue.path)
    if issue_path.is_absolute():
        try:
            return issue_path.relative_to(root).as_posix()
        except ValueError:
            return issue_path.as_posix()
    return str(issue.path).replace("\\", "/")


def _doctor_issue_fingerprint(issue: DoctorIssue, root: Path) -> str:
    payload = "\n".join(
        (
            issue.severity,
            _doctor_issue_path_for_fingerprint(issue, root),
            issue.message,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _accepted_doctor_warning_fingerprints(root: Path) -> dict[str, str]:
    try:
        return _load_workflow_config(root).accepted_doctor_warnings
    except SystemExit:
        return {}


def _doctor_issue_is_accepted(
    issue: DoctorIssue, *, root: Path, accepted_fingerprints: dict[str, str]
) -> bool:
    return _doctor_issue_fingerprint(issue, root) in accepted_fingerprints


def _evaluate_doctor(
    issues: list[DoctorIssue],
    *,
    root: Path,
    strict: bool,
    accepted_fingerprints: dict[str, str],
) -> DoctorEvaluation:
    accepted_issues = tuple(
        issue
        for issue in issues
        if _doctor_issue_is_accepted(
            issue,
            root=root,
            accepted_fingerprints=accepted_fingerprints,
        )
    )
    visible_issues = tuple(
        issue
        for issue in issues
        if not _doctor_issue_is_accepted(
            issue,
            root=root,
            accepted_fingerprints=accepted_fingerprints,
        )
    )
    blocking_issues = tuple(
        issue for issue in visible_issues if _doctor_issue_is_blocking(issue, strict=strict)
    )
    current_issues = tuple(issue for issue in visible_issues if not _doctor_issue_is_legacy(issue))
    legacy_issues = tuple(issue for issue in visible_issues if _doctor_issue_is_legacy(issue))
    return DoctorEvaluation(
        issues=tuple(issues),
        visible_issues=visible_issues,
        accepted_issues=accepted_issues,
        blocking_issues=blocking_issues,
        current_issues=current_issues,
        legacy_issues=legacy_issues,
        strict=strict,
    )


def _doctor_effective_severity(
    issue: DoctorIssue,
    *,
    strict: bool,
    accepted: bool,
) -> str:
    if accepted:
        return "accepted"
    if strict and issue.severity == "warning":
        return "error"
    return issue.severity


def _doctor_issue_record(
    issue: DoctorIssue,
    *,
    root: Path,
    strict: bool,
    accepted_fingerprints: dict[str, str],
) -> dict[str, object]:
    fingerprint = _doctor_issue_fingerprint(issue, root)
    accepted = fingerprint in accepted_fingerprints
    return {
        "code": issue.code,
        "severity": issue.severity,
        "effective_severity": _doctor_effective_severity(
            issue,
            strict=strict,
            accepted=accepted,
        ),
        "artifact": _doctor_issue_path_for_fingerprint(issue, root),
        "message": issue.message,
        "remediation_owner": issue.remediation_owner,
        "mechanically_upgradeable": issue.mechanically_upgradeable,
        "accepted": accepted,
        "accepted_reason": accepted_fingerprints.get(fingerprint, ""),
        "legacy": _doctor_issue_is_legacy(issue),
        "fingerprint": fingerprint,
    }


def _doctor_json_payload(
    evaluation: DoctorEvaluation,
    *,
    root: Path,
    accepted_fingerprints: dict[str, str],
) -> dict[str, object]:
    return {
        "schema_version": DOCTOR_OUTPUT_SCHEMA_VERSION,
        "root": str(root),
        "strict": evaluation.strict,
        "status": evaluation.status,
        "summary": {
            "total": len(evaluation.issues),
            "visible": len(evaluation.visible_issues),
            "accepted": len(evaluation.accepted_issues),
            "errors": sum(
                _doctor_effective_severity(
                    issue,
                    strict=evaluation.strict,
                    accepted=False,
                )
                == "error"
                for issue in evaluation.visible_issues
            ),
            "warnings": sum(
                _doctor_effective_severity(
                    issue,
                    strict=evaluation.strict,
                    accepted=False,
                )
                == "warning"
                for issue in evaluation.visible_issues
            ),
            "legacy": len(evaluation.legacy_issues),
            "blocking": len(evaluation.blocking_issues),
        },
        "findings": [
            _doctor_issue_record(
                issue,
                root=root,
                strict=evaluation.strict,
                accepted_fingerprints=accepted_fingerprints,
            )
            for issue in evaluation.issues
        ],
    }


def _format_doctor_issue(
    issue: DoctorIssue,
    *,
    root: Path,
    strict: bool,
    accepted_fingerprints: dict[str, str],
    accepted: bool = False,
) -> str:
    if accepted:
        severity = "accepted"
    elif _doctor_issue_is_legacy(issue):
        severity = "error" if strict and issue.severity == "warning" else "legacy warning"
    else:
        severity = "error" if strict and issue.severity == "warning" else issue.severity
    fingerprint = _doctor_issue_fingerprint(issue, root)
    reason = accepted_fingerprints.get(fingerprint, "")
    reason_text = f" (accepted: {reason})" if accepted and reason else ""
    mechanical = "yes" if issue.mechanically_upgradeable else "no"
    return (
        f"{severity.upper()}: {issue.path}: {issue.message} "
        f"[code: {issue.code}] [owner: {issue.remediation_owner}] "
        f"[mechanical: {mechanical}] [fingerprint: {fingerprint}]{reason_text}"
    )
