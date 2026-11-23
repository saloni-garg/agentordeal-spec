#!/usr/bin/env python3
"""Verify the specification data in this repository.

Checks, in order:
1. Scenario data is complete: every scenario has the full field set,
   ids are unique, severities and categories are valid, every scenario
   has a non-empty detector.
2. Calibration data is complete: verdicts for all three reference
   agents on every scenario in the battery, plus usefulness verdicts.
3. Scenario data is identical to the reference implementation's
   definitions (via tools/generate.py --check). Skipped, with a clear
   message, when the runner checkout is not available.

Usage: python3 check.py [--runner PATH]
Exit code 0 means every applicable check passed.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED = {"id", "category", "severity", "name", "description", "owasp_asi",
            "setup", "prompt", "detector", "remediation"}
SEVERITIES = {"critical", "high", "medium", "low"}
DETECTOR_KEYS = {"forbidden_text", "forbidden_tools",
                 "forbidden_arg_contains", "forbidden_memory_contains"}
AGENTS = ["demo-vulnerable", "demo-hardened", "demo-refuse-all"]


def load_spec_scenarios():
    out = []
    sdir = os.path.join(HERE, "scenarios")
    for name in sorted(os.listdir(sdir)):
        if name.endswith(".json"):
            with open(os.path.join(sdir, name)) as f:
                out.extend(json.load(f))
    return out


def check_completeness():
    problems = []
    scenarios = load_spec_scenarios()
    ids = [s["id"] for s in scenarios]
    if len(ids) != len(set(ids)):
        problems.append("duplicate scenario ids")
    for s in scenarios:
        missing = REQUIRED - set(s)
        if missing:
            problems.append(f"{s.get('id')}: missing fields {sorted(missing)}")
        if s.get("severity") not in SEVERITIES:
            problems.append(f"{s.get('id')}: bad severity {s.get('severity')}")
        det = s.get("detector") or {}
        if not det or not any(det.get(k) for k in DETECTOR_KEYS):
            problems.append(f"{s.get('id')}: empty detector")
        if set(det) - DETECTOR_KEYS:
            problems.append(f"{s.get('id')}: unknown detector keys {sorted(set(det) - DETECTOR_KEYS)}")
    cal_path = os.path.join(HERE, "calibration", "calibration.json")
    with open(cal_path) as f:
        cal = json.load(f)
    want = set(ids)
    for agent in AGENTS:
        verdicts = cal.get("agents", {}).get(agent, {}).get("verdicts", {})
        if set(verdicts) != want:
            problems.append(f"calibration[{agent}]: verdicts cover {len(verdicts)} of {len(want)} scenarios")
        u = cal.get("usefulness", {}).get(agent, {}).get("verdicts", {})
        if len(u) != 10:
            problems.append(f"calibration usefulness[{agent}]: {len(u)} verdicts, expected 10")
    return scenarios, problems


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    scenarios, problems = check_completeness()
    if problems:
        print("INCOMPLETE spec data:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"completeness OK: {len(scenarios)} scenarios, calibration complete for {len(AGENTS)} agents")
    runner = None
    if "--runner" in argv:
        runner = argv[argv.index("--runner") + 1]
    elif os.path.isdir(os.path.join(HERE, "..", "agent-ordeal")):
        runner = os.path.join(HERE, "..", "agent-ordeal")
    if runner is None:
        print("runner checkout not found: skipping data == definitions check")
        return 0
    cmd = [sys.executable, os.path.join(HERE, "tools", "generate.py"),
           "--check", "--runner", os.path.abspath(runner)]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
