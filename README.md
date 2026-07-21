# AI Vibe Coding for Python Applications

**Course Code:** C179 · part of the [AI Vibe Coding Series](https://www.tertiarycourses.com.sg/ai-vibe-coding-series.html)
**Provider:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)
**Duration:** 3 days · 8 training hours per day · 9:30 am – 6:30 pm
**Register:** [AI Vibe Coding for Python Applications](https://www.tertiarycourses.com.sg/python-django-web-development-training.html)

A hands-on course in which learners build and deploy one real Python
application — **CardGuard**, a card-transaction fraud screening system — using an
AI coding assistant throughout.

This is a commercial short course. There is **no assessment** — learning is
reinforced through the labs, a Day 3 consolidation build and a course-wide recap.

## Courseware

Version **v1.0** · 22 July 2026

| Artifact | File |
|---|---|
| Slide deck (289 slides) | `courseware/AI Vibe Coding for Python Applications-v1.0.pptx` (+ `.pdf`) |
| Lesson Plan | `courseware/LP-AI Vibe Coding for Python Applications.docx` (+ `.pdf`) |
| Learner Guide | `courseware/LG-AI Vibe Coding for Python Applications.docx` (+ `.pdf`) |
| Learner Guide (Markdown mirror) | `LG-AI Vibe Coding for Python Applications.md` |
| Labs (20, 4 per topic) | `labs/topic1` … `labs/topic5` |
| Combined notebook | `labs/CardGuard-All-Labs.ipynb` |

Superseded versions are kept in `courseware/archive/`.

## Topics and learning outcomes

| Topic | Title | Labs |
|---|---|---|
| 1 | Vibe Coding Foundations | 1–4 |
| 2 | Object-Oriented Programming in Python | 5–8 |
| 3 | Data Analytics with pandas | 9–12 |
| 4 | Data Modelling with Pydantic and FastAPI | 13–16 |
| 5 | Packaging and Deployment | 17–20 |

- **LO1** — Apply vibe coding practices: a reproducible `uv` project, and an AI assistant used to scaffold, explain and refactor working code.
- **LO2** — Design and implement object-oriented Python: classes, encapsulation, inheritance and composition.
- **LO3** — Build data analytics pipelines with pandas: load, clean, transform, group and aggregate realistic datasets.
- **LO4** — Model and validate data with Pydantic and expose it through FastAPI with typed request and response models.
- **LO5** — Package and deploy a Python application: dependency locking, configuration, containerisation and a verified running service.

## The application learners build

A three-tier system, built up lab by lab:

```
Streamlit dashboard  ->  FastAPI service  ->  SQLite
   (analyst UI)          (typed endpoints)    (persistence)
                              ^
                    pandas analytics + rule engine
```

Transaction data is generated locally by `mockdata.py` with a fixed seed
(10,851 transactions, 40 cardholders, 42 seeded fraud cases), so every learner
and the trainer see identical numbers. No real cardholder data is used.

## Toolchain

Every lab uses [uv](https://docs.astral.sh/uv/). Verified on Python 3.12,
pandas 3.0, Streamlit 1.59, SQLite 3.47.

```bash
uv init cardguard && cd cardguard
uv python pin 3.12
uv add pandas pydantic fastapi 'uvicorn[standard]' streamlit httpx pytest
uv run python mockdata.py
```

> **Note** — pandas 3.0 enables Copy-on-Write by default. Chained assignment
> (`df[df.x > 1]['y'] = 0`) no longer mutates the frame, and AI assistants
> frequently generate the older pandas 1.x idiom. Verify generated pandas code
> against the installed version.

## Regenerating the courseware

The single source of truth lives in
`.claude/skills/non-wsq-courseware-build/build/`: `course_data.py` (metadata,
outcomes, topics, schedule) plus `data_domain1.py` … `data_domain5.py` (the 20
labs). Every artifact is generated from those files, so they cannot drift apart.

```bash
export COURSE_REPO="$PWD"
B=.claude/skills/non-wsq-courseware-build/build

bash $B/build_courseware.sh      # PPT + LP + LG, DOCX + PDF, with page-numbered TOCs
python3 $B/build_labs.py         # -> labs/ + the combined notebook
```

Individual generators (`build_slides.py`, `build_lesson_plan.py`,
`build_learner_guide.py`) can also be run on their own.

After any content change: bump `VERSION`, add a `VERSION_HISTORY` row in
`course_data.py`, move the superseded deck into `courseware/archive/`, and
re-run the QA audit:

```bash
python3 .claude/skills/non-wsq-courseware-qa/scan_prohibited.py
```

The audit fails the build if any WSQ, SSG/SkillsFuture, TRAQOM, funding,
digital-attendance or assessment content leaks into an artifact.

---

© 2026 Tertiary Infotech Academy Pte Ltd · www.tertiarycourses.com.sg
