# Changelog

## Rename -- 2026-11-22

The benchmark was renamed from **AgentGauntlet** to **AgentOrdeal**
before its first public release (runner iteration 22). This repository
was `agentgauntlet-spec`, now `agentordeal-spec`. Specification
version stays 1.0 and battery stays 1.2.0: the rename changes no
scenario, detector, scoring rule, or score. The citation format is
now `AgentOrdeal-1.0 / battery=1.2.0 / seed=42 / score=91.3`.

Battery and specification changes for AgentOrdeal. Every entry names
the battery version, what changed, and the mapping to the previous
battery. Released batteries are immutable (see VERSIONING.md); this
file is the record, not a place where history gets revised.

## Specification 1.0 -- 2026-11-22

The first specification-tracked release. The benchmark is split out of
the reference implementation (`agent-ordeal` runner) into this
repository: SPEC.md defines the task, the metric, the citation format,
and the conformance requirements independently of any code.

- Specification version: 1.0 (initial).
- Conformance claim format introduced: "Supports AgentOrdeal 1.0
  (battery X.Y.Z), calibration-verified."
- Citation format introduced:
  `AgentOrdeal-1.0 / battery=1.2.0 / seed=42 / score=91.3`.

## Battery 1.2.0 -- shipped with runner 0.4.0

First battery tracked by the specification.

- 91 security scenarios: 16 prompt_injection, 19 tool_misuse,
  16 data_exfiltration, 16 memory_poisoning, 16 goal_hijacking,
  8 mcp_security.
- Mapping from battery 1.1.0 (runner-internal): identical scenario set
  plus TM-17, TM-18, TM-19 (Unexpected Code Execution scenarios closing
  the OWASP ASI05 thin spot, 1 -> 4 scenarios). No scenario removed or
  renumbered; all 1.1.0 ids keep their meaning.
- Calibration: pinned verdicts for the three reference agents
  (demo-vulnerable, demo-hardened, demo-refuse-all) on all 91
  scenarios, plus the 10-task usefulness battery, in
  `calibration/calibration.json`.

## Battery history before the specification split

- 1.1.0 (runner 0.2.0): 88 scenarios; mcp_security category added;
  multi-turn, encoded, and document-carried payloads added.
- 1.0.0 (runner 0.1.0): 40 scenarios, 8 per category across the
  original five categories.
