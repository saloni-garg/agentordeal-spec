# Calibration protocol

Calibration is how an implementation proves it measures the same
benchmark as everyone else. The calibration set pins the exact
behaviour of three **reference agents** -- deterministic, rule-based
agents defined in the reference implementation
(`agentordeal/adapters/demo.py` in the runner repository):

- **demo-vulnerable** -- a naive agent: it obeys injected instructions,
  reveals its canary, calls named dangerous tools, and stores what it
  is told to remember.
- **demo-hardened** -- a hardened agent: it treats attack signals as
  untrusted, refuses, leaks nothing, and still completes benign tasks.
- **demo-refuse-all** -- it refuses everything. Its role is to prove
  the usefulness gate: perfect security verdicts, zero usefulness,
  combined grade capped at D.

## The data

`calibration.json` (generated -- see `tools/generate.py`) contains, for
the stated battery version:

- `agents.<name>.verdicts` -- the expected pass/fail verdict for every
  one of the battery's scenarios (all 91 for battery 1.2.0);
- `agents.<name>.score` / `.grade` -- the expected weighted score and
  grade;
- `usefulness.<name>.verdicts` -- the expected verdicts on the 10-task
  usefulness battery.

## The protocol

A new implementation proves conformance as follows:

1. Implement the three reference agents exactly as defined in the
   reference implementation (they are small and deterministic by
   design; port them, do not approximate them).
2. Run the full battery from `scenarios/` against each agent, with
   the detector and scoring rules of `scoring/`.
3. Compare every verdict, score, and grade against
   `calibration.json`. **Exact match on all of them is required.**
   A single differing verdict means the implementation is measuring
   something else -- most often a detector edge (substring semantics,
   argument serialisation, memory joining) or a multi-turn aggregation
   difference.
4. Run the usefulness battery the same way and compare those verdicts
   too, including the refuse-all agent's combined-grade cap.

Passing implementations may use the conformance claim format in
`SPEC.md` section 5. The reference implementation runs this protocol
as a test (`agentordeal.calibration.check_conformance`) on every change;
any battery or detector change that alters a verdict must regenerate
the calibration data and bump the battery version in the same commit.
