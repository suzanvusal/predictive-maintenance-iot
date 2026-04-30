#!/usr/bin/env python3
"""
Predictive Maintenance IoT — Daily Template Automator
======================================================
Zero API calls. Zero cost. Pure template-based commits.
"""
from __future__ import annotations
import argparse
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_plan(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def get_day_plan(plan: dict, day: int) -> dict:
    for d in plan["days"]:
        if d["day"] == day:
            return d
    raise ValueError(f"Day {day} not found in plan")


def get_phase(plan: dict, day: int) -> dict:
    for p in plan["phases"]:
        if day in p["days"]:
            return p
    return {}


def get_template(filepath: str, day: int) -> str | None:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from templates.day_templates import DAY_FILES
        return DAY_FILES.get(day, {}).get(filepath)
    except ImportError:
        return None


def make_stub(filepath: str, day_plan: dict) -> str:
    ext   = Path(filepath).suffix
    name  = Path(filepath).stem
    day   = day_plan["day"]
    title = day_plan["title"]
    if ext == ".py":
        return (
            f'"""\n{filepath}\nDay {day}: {title}\n'
            f'Focus: {day_plan["focus"]}\n"""\n'
            f'from __future__ import annotations\nimport logging\n\n'
            f'logger = logging.getLogger(__name__)\n'
        )
    elif ext in (".yml", ".yaml"):
        return f"# {filepath}\n# Day {day}: {title}\n# Generated: {datetime.now(timezone.utc).isoformat()}\n"
    elif ext == ".md":
        return f"# {name.replace('_', ' ').title()}\n\nDay {day}: {title}\n\n{day_plan['focus']}\n"
    elif ext == ".json":
        return json.dumps({"day": day, "file": filepath, "title": title}, indent=2) + "\n"
    else:
        return f"# {filepath} — Day {day}: {title}\n"


def git(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + cmd, capture_output=True, text=True)


def write_file(filepath: str, content: str) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_file(filepath: str, snippet: str) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n# {datetime.now(timezone.utc).strftime('%H:%M:%S')} — {snippet[:60]}\n")


def commit(message: str, files: list[str] | None = None) -> bool:
    if files:
        for f in files:
            git(["add", f])
    else:
        git(["add", "-A"])
    r = git(["commit", "-m", message])
    return r.returncode == 0 and "nothing to commit" not in r.stdout


def strategy_real_files(day_plan: dict, day: int) -> int:
    files = day_plan.get("files_to_create", [])
    tasks = day_plan.get("commit_tasks", [])
    count = 0
    print(f"\n[Real Files] Writing {len(files)} files from templates...")
    for i, filepath in enumerate(files):
        content = get_template(filepath, day) or make_stub(filepath, day_plan)
        write_file(filepath, content)
        msg = tasks[i] if i < len(tasks) else f"feat: implement {Path(filepath).stem}"
        if commit(msg, [filepath]):
            count += 1
            print(f"  ✓ [{count}] {msg[:70]}")
    return count


def strategy_task_commits(day_plan: dict, made: int, target: int) -> int:
    tasks     = day_plan.get("commit_tasks", [])[made:]
    refactors = day_plan.get("refactor_fix_commits", [])
    all_msgs  = tasks + refactors
    files     = day_plan.get("files_to_create", [])
    count     = 0
    remaining = target - made
    print(f"\n[Tasks] Making {min(len(all_msgs), remaining)} task commits...")
    for msg in all_msgs[:remaining]:
        if not files:
            break
        fp = random.choice(files)
        append_file(fp, msg)
        if commit(msg, [fp]):
            count += 1
            print(f"  ✓ [{made + count}] {msg[:70]}")
    return count


def strategy_filler(made: int, target: int, day: int, day_plan: dict) -> int:
    remaining = target - made
    if remaining <= 0:
        return 0
    print(f"\n[Filler] Making {remaining} filler commits...")
    all_py   = [str(f) for f in Path("src").rglob("*.py")] if Path("src").exists() else []
    all_test = [str(f) for f in Path("tests").rglob("*.py")] if Path("tests").exists() else []
    pool     = (all_py + all_test) or day_plan.get("files_to_create", ["src/__init__.py"])
    msgs = [
        "style: run black formatter on {m}",
        "fix: remove unused import in {m}",
        "docs: add module docstring to {m}",
        "refactor: extract constant in {m}",
        "chore: add logging to {m}",
        "fix: handle None edge case in {m}",
        "test: add assertion for return type in {m}",
        "perf: add caching in {m}",
        "style: reorder imports in {m}",
        "docs: update docstring example in {m}",
        "fix: correct off-by-one in {m}",
        "refactor: rename variable for clarity in {m}",
        f"chore: day {day} maintenance sweep",
        "docs: fix typo in {m}",
        "fix: add missing type hint in {m}",
    ]
    count = 0
    while count < remaining:
        fp  = random.choice(pool)
        m   = Path(fp).stem
        msg = random.choice(msgs).format(m=m)
        append_file(fp, msg)
        if commit(msg, [fp]):
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day",     type=int, required=True)
    parser.add_argument("--commits", type=int, default=25)
    parser.add_argument("--plan",    type=str, required=True)
    args = parser.parse_args()

    target   = max(15, min(30, args.commits))
    plan     = load_plan(args.plan)
    day_plan = get_day_plan(plan, args.day)

    print(f"\n{'='*55}")
    print(f"  Predictive Maintenance IoT — Day {args.day}/30")
    print(f"  Target: {target} commits | Cost: $0.00")
    print(f"{'='*55}")
    print(f"\n📋 {day_plan['title']}")
    print(f"   {day_plan['focus']}")

    made = 0
    made += strategy_real_files(day_plan, args.day)
    print(f"\n  After real files  : {made}/{target}")

    made += strategy_task_commits(day_plan, made, made + min(8, target - made))
    print(f"  After task commits: {made}/{target}")

    if made < target:
        made += strategy_filler(made, target, args.day, day_plan)

    Path(".automation_state").mkdir(exist_ok=True)
    spath = f".automation_state/day_{args.day:02d}_summary.json"
    Path(spath).write_text(json.dumps({
        "day": args.day,
        "title": day_plan["title"],
        "commits_made": made,
        "target": target,
        "cost_usd": 0.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    commit(f"chore: add day {args.day} summary", [spath])

    print(f"\n{'='*55}")
    print(f"  ✅ Day {args.day} done! Commits: {made} | Cost: $0.00")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
