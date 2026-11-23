# Versioning and stability policy

Benchmarks become standards by not moving. This policy is the
commitment that lets a researcher write "evaluated on AgentOrdeal
1.0, battery 1.2.0" and have that mean the same thing in five years.

## Two versions, two jobs

- **Specification version** (this repo's `SPEC.md`, currently 1.0):
  the task definition, the metric, the detector semantics, the
  citation format, and the conformance requirements. It changes rarely
  and only when one of those five things changes.
- **Battery version** (currently 1.2.0): the concrete scenario set.
  It changes when scenarios or detectors are added, widened, removed,
  or renumbered.

A score is identified by the pair (specification version, battery
version) plus its seed -- the citation string of SPEC.md section 4.

## The rules

1. **Released batteries are immutable.** Once a battery version is
   tagged in this repository, its scenario files, detectors, weights,
   and calibration data never change. A fix is a new battery version.
2. **Scores are never silently changed.** A published score stands
   against the battery that produced it. If a target is rerun on a
   newer battery, the new score is published alongside the old one,
   each with its own citation string -- never as an edit of the old.
3. **Every battery change ships a changelog and a mapping note.** The
   changelog (CHANGELOG.md) states what was added, removed, or
   renumbered, and the mapping note states which scenario ids in the
   new battery correspond to which in the previous one, so results can
   be compared scenario-by-scenario where a comparison is meaningful.
4. **Bump rules.** Minor (1.2.0 -> 1.3.0): scenarios or detectors added
   or widened, nothing removed. Major (1.x -> 2.0.0): scenarios removed
   or renumbered, detector semantics changed so a previously-passing
   behaviour can fail (or vice versa) for a reason other than a widened
   detector, or scoring weights changed.
5. **Old batteries remain runnable and citable indefinitely.** The
   data files for every released battery stay in this repository's
   history, and a conforming implementation must be able to run any
   released battery, not only the latest.
6. **Calibration moves with the battery.** Any battery change
   regenerates the calibration set in the same commit; a battery whose
   calibration data does not reproduce exactly is not released.
7. **Specification changes are major by default.** A change to the
   task, metric, detector semantics, citation format, or conformance
   requirements increments the specification major version, and scores
   under different specification majors are never compared.

## What this means for implementers

Pin the battery version in every scorecard and citation. If you vendor
the battery data, vendor a released version unchanged and record which
one. If you extend the battery with your own scenarios, report them
separately -- an extended run is not an AgentOrdeal score.
