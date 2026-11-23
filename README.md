# AgentOrdeal

**A reproducible benchmark for autonomous agent security.**

AgentOrdeal is a benchmark, not a scanner. It defines a fixed,
versioned battery of adversarial scenarios for autonomous agents --
prompt injection, tool misuse, data exfiltration, memory poisoning,
goal hijacking, and MCP attacks -- a deterministic metric over what an
agent observably does, and a calibration protocol that lets any
implementation prove it measures the same thing.

Implementations come and go; the benchmark is the standard. The
reference implementation is the `agent-ordeal` runner. Independent
implementations are welcome and expected: conformance is defined by
the specification, not by using any particular code.

## Report a score

```
AgentOrdeal-1.0 / battery=1.2.0 / seed=42 / score=91.3
```

That string -- specification version, battery version, seed, score --
is the whole citation. A score without its battery version is not an
AgentOrdeal result. See `SPEC.md` section 4.

## Claim conformance

An implementation may state:

> Supports AgentOrdeal 1.0 (battery 1.2.0), calibration-verified.

if and only if it satisfies `SPEC.md` section 5: unaltered battery
data, the exact detector and scoring rules of `scoring/`, a full pass
of the calibration protocol in `calibration/`, and scorecards carrying
the `specification` field and citation string.

## Repository layout

- `SPEC.md` -- the AgentOrdeal Specification 1.0: task, metric,
  citation format, conformance.
- `scenarios/` -- the battery as implementation-independent data, one
  JSON file per category. Generated from the reference implementation
  by `tools/generate.py`; never edited by hand.
- `scoring/` -- scoring rules, severity weights, grade boundaries, and
  the detector definitions, stated precisely enough to reimplement.
- `calibration/` -- the calibration protocol and the pinned verdicts
  for the three reference agents.
- `VERSIONING.md` -- the stability policy: released batteries are
  immutable, scores are never silently changed, old batteries remain
  runnable and citable indefinitely.
- `CHANGELOG.md` -- battery and specification changes, with mapping
  notes between battery versions.
- `check.py` -- verifies the spec data is complete and identical to
  the reference implementation's definitions.

## Current versions

- Specification: **1.0**
- Battery: **1.2.0** -- 91 security scenarios (plus the separate
  10-task usefulness battery used by the combined grade)

## License

MIT. See [LICENSE](LICENSE).
