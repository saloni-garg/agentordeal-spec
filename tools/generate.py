#!/usr/bin/env python3
"""Generate the specification's data files from the reference implementation.

The scenario battery and the calibration set in this repository are
GENERATED from the reference runner (agent-ordeal) so the specification
data can never silently drift from the definitions the reference
implementation runs. Do not edit scenarios/*.json or
calibration/calibration.json by hand -- edit the runner's scenario
definitions, regenerate, and commit both.

Usage:
    python3 tools/generate.py [--check] [--runner PATH]

--runner defaults to the sibling checkout ../agent-ordeal, or the
AGENTORDEAL_RUNNER environment variable. --check regenerates in
memory and exits non-zero if any committed file differs.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_ROOT = os.path.dirname(HERE)

SPEC_VERSION = "1.0"


def load_runner(runner_path):
    sys.path.insert(0, runner_path)
    # Drop any previously imported agentordeal package from another location.
    for mod in [m for m in list(sys.modules) if m == "agentordeal" or m.startswith("agentordeal.")]:
        del sys.modules[mod]
    from agentordeal.scenarios import load_scenarios, BATTERY_VERSION
    return load_scenarios(), BATTERY_VERSION, runner_path


def scenario_files(scenarios):
    """{filename: content} for scenarios/<category>.json, one file per category."""
    by_cat = {}
    for sc in scenarios:
        by_cat.setdefault(sc["category"], []).append(sc)
    files = {}
    for cat in sorted(by_cat):
        data = sorted(by_cat[cat], key=lambda s: s["id"])
        files[f"scenarios/{cat}.json"] = json.dumps(data, indent=1, sort_keys=True) + "\n"
    return files


def calibration_file(runner_path, battery_version):
    fixture = os.path.join(runner_path, "tests", "fixtures", "calibration.json")
    with open(fixture) as f:
        cal = json.load(f)
    if cal.get("battery_version") != battery_version:
        raise SystemExit(f"calibration fixture battery {cal.get('battery_version')} "
                         f"!= runner battery {battery_version}; regenerate the fixture first")
    out = {
        "spec_version": SPEC_VERSION,
        "battery_version": battery_version,
        "reference_agents": {
            "demo-vulnerable": "Rule-based naive agent: obeys injected instructions, "
                               "reveals its canary, calls named dangerous tools, stores "
                               "what it is told to remember. Defined in the reference "
                               "implementation (agentordeal/adapters/demo.py).",
            "demo-hardened": "Rule-based hardened agent: treats attack signals as "
                             "untrusted, refuses, leaks nothing, still completes benign "
                             "control tasks. Defined in the reference implementation.",
            "demo-refuse-all": "Refuses every request, benign or not. Exists to prove "
                               "the usefulness gate: perfect security verdicts, zero "
                               "usefulness, combined grade capped at D.",
        },
        "agents": cal["agents"],
        "usefulness": cal["usefulness"],
    }
    return {"calibration/calibration.json": json.dumps(out, indent=1, sort_keys=True) + "\n"}


def expected_files(runner_path):
    scenarios, battery_version, _ = load_runner(runner_path)
    files = scenario_files(scenarios)
    files.update(calibration_file(runner_path, battery_version))
    return files, battery_version, len(scenarios)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true", help="verify committed files match the runner definitions")
    p.add_argument("--runner", default=os.environ.get(
        "AGENTORDEAL_RUNNER", os.path.join(SPEC_ROOT, "..", "agent-ordeal")))
    a = p.parse_args(argv)
    runner_path = os.path.abspath(a.runner)
    files, battery_version, n = expected_files(runner_path)
    if a.check:
        bad = []
        for rel, content in sorted(files.items()):
            path = os.path.join(SPEC_ROOT, rel)
            if not os.path.exists(path) or open(path).read() != content:
                bad.append(rel)
        if bad:
            print("DRIFT: spec data differs from runner definitions:", *bad, sep="\n  ")
            return 1
        print(f"OK: spec data == runner definitions (battery {battery_version}, {n} scenarios)")
        return 0
    for rel, content in sorted(files.items()):
        path = os.path.join(SPEC_ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
    print(f"generated {len(files)} files (battery {battery_version}, {n} scenarios)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
