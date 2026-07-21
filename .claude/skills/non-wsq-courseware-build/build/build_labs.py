#!/usr/bin/env python3
"""Generate labs/ from the same single source that drives the PPT, LP and LG.

Produces, for each of the 20 labs:
  labs/topicN/labNN_<slug>/README.md   - goal, steps, verification
  labs/topicN/labNN_<slug>/*.py        - the runnable code from each step
and one combined notebook:
  labs/CardGuard-All-Labs.ipynb
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import course_data as C

# Domains are discovered dynamically so the course can have any number of them,
# matching the rest of the non-WSQ engine.
import glob as _glob, importlib
def _load_domains():
    acts = []
    for f in sorted(_glob.glob(os.path.join(HERE, "data_domain[0-9]*.py")),
                    key=lambda p: int("".join(c for c in os.path.basename(p) if c.isdigit()) or 0)):
        n = "".join(c for c in os.path.basename(f) if c.isdigit())
        acts += getattr(importlib.import_module(os.path.basename(f)[:-3]), f"DOMAIN{n}", [])
    return acts

LABS = _load_domains()

# The labs live in the course repo, not beside this skill.
def _find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))

OUT = os.path.join(_find_repo(HERE), "labs")


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return re.sub(r"_+", "_", s)[:48]


def norm(steps):
    """Steps may be (instr, code) or bare (instr,) / instr."""
    out = []
    for s in steps:
        if isinstance(s, (tuple, list)):
            out.append((s[0], s[1] if len(s) > 1 else ""))
        else:
            out.append((s, ""))
    return out


def is_python(code: str) -> bool:
    """True when the snippet is a Python file rather than a shell command."""
    if not code.strip():
        return False
    head = code.lstrip()
    if head.startswith("#") and (".py" in head.split("\n")[0]):
        return True
    shell_starts = ("uv ", "curl", "docker", "git ", "open ", "grep", "for ",
                    "cd ", "cp ", "rm ", "ls ", "mkdir", "sleep", "#!")
    return not head.startswith(shell_starts)


def write_lab(lab) -> dict:
    topic_dir = os.path.join(OUT, f"topic{lab['topic']}")
    lab_dir = os.path.join(topic_dir, f"lab{lab['num']:02d}_{slug(lab['title'])}")
    os.makedirs(lab_dir, exist_ok=True)
    steps = norm(lab["steps"])

    # ---- README
    lines = [f"# Lab {lab['num']} — {lab['title']}", "",
             f"**Topic {lab['topic']}** · {lab['objective']}", "",
             f"{lab['desc']}", "",
             f"- **You will build:** {lab['build']}",
             f"- **Tools:** {lab['services']}", "",
             "## Steps", ""]
    for i, (instr, code) in enumerate(steps, 1):
        lines.append(f"{i}. {instr}")
        if code:
            lang = "python" if is_python(code) else "bash"
            lines += ["", f"   ```{lang}", *[f"   {l}" for l in code.split("\n")],
                      "   ```", ""]
    lines += ["", "## Verify", "", lab["test"], ""]
    with open(os.path.join(lab_dir, "README.md"), "w") as f:
        f.write("\n".join(lines))

    # ---- python files (one per python snippet, named from the # header if present)
    # Several snippets in one lab may target the SAME filename, so the first write
    # truncates and later ones append. `written` tracks that per build — without it
    # the files are opened in append mode across RUNS too, so a rebuild stacks the
    # new content underneath the old (which is how lab01/main.py ended up holding
    # both the retired payroll example and its CardGuard replacement).
    py_count = 0
    written = set()
    for i, (instr, code) in enumerate(steps, 1):
        if not is_python(code):
            continue
        first = code.lstrip().split("\n")[0]
        m = re.match(r"#\s*([\w./-]+\.py)", first)
        name = os.path.basename(m.group(1)) if m else f"step{i:02d}_{slug(instr)[:32]}.py"
        body = code if code.lstrip().startswith("#") else f"# {instr}\n{code}"
        with open(os.path.join(lab_dir, name), "a" if name in written else "w") as f:
            f.write(body.rstrip() + "\n\n")
        written.add(name)
        py_count += 1

    # ---- shell script of the commands, so a learner can replay the lab
    sh = [f"#!/usr/bin/env bash", f"# Lab {lab['num']} — {lab['title']}",
          "set -euo pipefail", ""]
    for i, (instr, code) in enumerate(steps, 1):
        if code and not is_python(code):
            sh += [f"# {i}. {instr}", code, ""]
    if len(sh) > 4:
        p = os.path.join(lab_dir, "commands.sh")
        with open(p, "w") as f:
            f.write("\n".join(sh))
        os.chmod(p, 0o755)

    return dict(dir=lab_dir, py=py_count, steps=len(steps))


def cell_md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.split("\n")}


def cell_code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.split("\n")}


def build_notebook():
    cells = [cell_md(
        f"# {C.TITLE}\n\n"
        f"**{C.COURSE_CODE}** · {C.ORG}\n\n"
        f"All {len(LABS)} labs in one notebook. Every lab builds one application: "
        "**CardGuard**, a card-transaction fraud screening system.\n\n"
        "Run the setup cell first, then work through the topics in order.")]

    cells.append(cell_md("## Setup\n\nInstall the toolchain and generate the "
                         "deterministic dataset used by every lab."))
    cells.append(cell_code(
        "# One-time setup (uv manages the environment)\n"
        "!uv add pandas pydantic fastapi 'uvicorn[standard]' streamlit httpx pytest\n"
        "!uv run python mockdata.py"))

    by_topic = {t["num"]: t for t in C.TOPICS}
    current = None
    for lab in LABS:
        if lab["topic"] != current:
            current = lab["topic"]
            t = by_topic[current]
            cells.append(cell_md(
                f"---\n\n# Topic {t['code']} — {t['title']}\n\n"
                f"*{t['subtitle']}*\n\n"
                + "\n".join(f"- {c}" for c in t["concepts"])))
        cells.append(cell_md(
            f"## Lab {lab['num']} — {lab['title']}\n\n"
            f"**Objective:** {lab['objective']}\n\n{lab['desc']}\n\n"
            f"**You will build:** {lab['build']}"))
        for i, (instr, code) in enumerate(norm(lab["steps"]), 1):
            cells.append(cell_md(f"**Step {i}.** {instr}"))
            if code:
                cells.append(cell_code(code if is_python(code)
                                       else "\n".join(f"!{l}" for l in code.split("\n")
                                                      if l.strip())))
        cells.append(cell_md(f"> **Verify:** {lab['test']}"))

    nb = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"}},
        "nbformat": 4, "nbformat_minor": 5}
    path = os.path.join(OUT, "CardGuard-All-Labs.ipynb")
    with open(path, "w") as f:
        json.dump(nb, f, indent=1)
    return path, len(cells)


def build_index(results):
    lines = [f"# Labs — {C.TITLE}", "",
             f"{len(LABS)} hands-on labs building **CardGuard**, a card-transaction "
             "fraud screening system.", "",
             "Every lab uses `uv`. Run the combined notebook "
             "[CardGuard-All-Labs.ipynb](CardGuard-All-Labs.ipynb) or work through "
             "the per-lab folders below.", "",
             "| Lab | Topic | Title | Objective |", "|---|---|---|---|"]
    by_topic = {t["num"]: t["title"] for t in C.TOPICS}
    for lab in LABS:
        rel = os.path.relpath(results[lab["num"]]["dir"], OUT)
        lines.append(f"| {lab['num']} | {by_topic[lab['topic']]} | "
                     f"[{lab['title']}]({rel}/README.md) | {lab['objective']} |")
    lines += ["", "## Setup", "",
              "```bash", "uv add pandas pydantic fastapi 'uvicorn[standard]' streamlit httpx pytest",
              "uv run python mockdata.py", "```", ""]
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    results = {}
    for lab in LABS:
        results[lab["num"]] = write_lab(lab)
    nb_path, n_cells = build_notebook()
    build_index(results)
    total_py = sum(r["py"] for r in results.values())
    total_steps = sum(r["steps"] for r in results.values())
    print(f"Labs written : {len(LABS)}")
    print(f"  steps      : {total_steps}")
    print(f"  python files: {total_py}")
    print(f"Notebook     : {nb_path} ({n_cells} cells)")
