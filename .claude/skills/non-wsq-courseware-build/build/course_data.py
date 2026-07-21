"""
SINGLE SOURCE OF TRUTH — C179 AI Vibe Coding for Python Applications (non-WSQ).

Mirrors the WSQ counterpart (Build and Deploy Python Applications with Vibe
Coding) 1:1 — same topic spine, same 20 labs, same depth — with the entire WSQ
layer removed:

  * no assessment of any kind (no WA/SAQ, no case study, no marking guide)
  * no SSG / SkillsFuture / WSQ funding or subsidy content
  * no TRAQOM survey, no digital attendance, no 75% attendance rule
  * no TGS- course reference — the plain non-WSQ code C179 is used

The 205 minutes freed on Day 3 by removing the assessment block are reallocated
into hands-on lab time, a consolidation build and an extended course recap.

Every artifact (PPT, LP, LG, LG.md) is generated from this module plus
data_domain1.py … data_domain5.py, so they stay 100% aligned.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "AI Vibe Coding for Python Applications"
SHORT_TITLE  = "AI Vibe Coding for Python Applications"
COURSE_CODE  = "C179"
VERSION      = "v1.0"
VERSION_DATE = "22 July 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 3
MODE         = "Instructor-led, hands-on practical labs"

DARK_THEME = False

# cover badge (top-right of the title slide)
BADGE_TOP   = "PYTHON"
BADGE_SUB   = "VIBE CODING"

# trainer profile card bullets (label, text)
TRAINER_BULLETS = [
    ("Role", "Principal Trainer, Tertiary Infotech Academy Pte. Ltd."),
    ("Expertise", "Python application development, AI-assisted (vibe) coding, data analytics and deployment."),
    ("Delivers", "Courses on Python, AI-assisted development, data engineering and software delivery."),
    ("Founder", "Founder and lead instructor at Tertiary Infotech / Tertiary Courses."),
]

ICE_BREAKER = [
    "Your name and organisation / role.",
    "Your experience with Python and with AI coding assistants (if any).",
    "What you want to build and deploy after this course.",
]

# closing slides
NEXT_STEPS_TITLE = "Where to Go Next"
_NEXT_STEP_ITEMS = [
    "Rebuild CardGuard from scratch on your own machine, using your AI assistant for every step.",
    "Add a new fraud rule and a matching pytest test, then redeploy the container.",
    "Swap SQLite for PostgreSQL — the repository layer is the only module that should change.",
    "Publish your image to a registry and deploy it to a cloud host.",
    "Practise the four-part prompt pattern on your own work: goal, constraints, inputs, expected output.",
]
# The deck expects a dict(title, items); the Learner Guide expects a plain list.
NEXT_STEPS = dict(title=NEXT_STEPS_TITLE, items=_NEXT_STEP_ITEMS)
THANK_YOU_LINE = "You can now build, test and deploy a real Python application with AI assistance."
THANK_YOU_KICKER = "KEEP BUILDING"

# ------------------------------------------------------------------ toolchain
TOOLCHAIN = dict(
    pkg_manager="uv",
    init="uv init <lab-folder>",
    add="uv add pandas pydantic fastapi streamlit",
    run="uv run python main.py",
    run_api="uv run uvicorn main:app --reload",
    run_ui="uv run streamlit run app.py",
    note="uv creates .venv and uv.lock automatically; learners never activate a venv by hand.",
    versions="Verified on uv, Python 3.12, pandas 3.0, streamlit 1.59. pandas 3.0 enables "
             "Copy-on-Write by default — chained assignment no longer mutates in place, and "
             "AI assistants frequently generate the older pandas 1.x idiom. Always verify "
             "generated pandas code against the installed version.",
)

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Apply vibe coding practices — set up a reproducible Python project with uv, and use an AI coding assistant to scaffold, explain and refactor working code.",
    "LO2: Design and implement object-oriented Python — classes, encapsulation, inheritance and composition — using AI-assisted conversational design.",
    "LO3: Build data analytics pipelines with pandas — load, clean, transform, group and aggregate realistic datasets into reportable results.",
    "LO4: Model and validate data with Pydantic and expose it through a FastAPI application with typed request and response models.",
    "LO5: Package and deploy a Python application — dependency locking, configuration, containerisation and a running deployed service.",
]
LO_TITLES = [
    "Vibe Coding",
    "Object-Oriented Python",
    "pandas Analytics",
    "Pydantic & FastAPI",
    "Package & Deploy",
]

# ------------------------------------------------------------------ topics
# `weighting` is deliberately omitted — a non-WSQ course has no exam to weight.
TOPICS = [
    dict(num=1, code="01",
         title="Vibe Coding Foundations",
         subtitle="uv Projects · AI Coding Assistants · Prompting Patterns · AI-Assisted Refactoring",
         concepts=[
            "Vibe coding is directing an AI assistant to write code you specify, review and own — you remain accountable for correctness.",
            "uv manages the interpreter, virtual environment and locked dependencies: uv init, uv add, uv run.",
            "Effective prompts state the goal, the constraints, the inputs and the expected output — vague prompts produce plausible but wrong code.",
            "Always read and run AI-generated code before trusting it; refactoring conversationally is faster than rewriting by hand.",
         ]),
    dict(num=2, code="02",
         title="Object-Oriented Programming in Python",
         subtitle="Classes · Encapsulation · Inheritance · Composition · Dunder Methods",
         concepts=[
            "A class bundles data (attributes) with the behaviour that operates on it (methods); an object is one instance of it.",
            "Encapsulation hides internal state behind methods and properties so callers depend on behaviour, not layout.",
            "Inheritance models 'is-a' and shares behaviour; composition models 'has-a' and is usually the more flexible default.",
            "Dunder methods (__init__, __repr__, __eq__) integrate your classes with Python's built-in operators and printing.",
         ]),
    dict(num=3, code="03",
         title="Data Analytics with pandas",
         subtitle="DataFrames · Cleaning · Transformation · GroupBy · Aggregation · Reporting",
         concepts=[
            "A DataFrame is a labelled 2-D table; a Series is one column. Most analytics is selecting, filtering and reshaping these.",
            "Real data is dirty: missing values, wrong dtypes and duplicates must be handled explicitly before analysis.",
            "split-apply-combine (groupby then aggregate) answers most business questions about a dataset.",
            "An analytics pipeline should be a set of small, testable functions — not one long script.",
         ]),
    dict(num=4, code="04",
         title="Data Modelling with Pydantic and FastAPI",
         subtitle="Typed Models · Validation · Endpoints · Request/Response Schemas · Auto Docs",
         concepts=[
            "Pydantic models declare the shape of data with Python type hints and validate it at runtime, failing fast on bad input.",
            "FastAPI turns typed Python functions into HTTP endpoints, deriving validation and OpenAPI docs from the annotations.",
            "Separate request models from response models so the API contract is explicit and safe to change.",
            "The analytics layer stays plain Python; FastAPI is a thin transport layer over it.",
         ]),
    dict(num=5, code="05",
         title="Packaging and Deployment",
         subtitle="uv Lockfiles · Configuration · Containers · Deploying a Service",
         concepts=[
            "uv.lock pins exact versions so the application installs identically in development and production.",
            "Configuration belongs in environment variables, never hard-coded — secrets must never be committed.",
            "A container image bundles the interpreter, dependencies and application code into one deployable artifact.",
            "A deployment is not done until the running service has been verified with a real request against a health endpoint.",
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Vibe Coding Foundations & Object-Oriented Python",
    2: "Data Analytics with pandas, Pydantic & FastAPI",
    3: "FastAPI, Packaging, Deployment & Consolidation",
}

# ------------------------------------------------------------------ schedule
# kind: admin | topic | lab | break | lunch | recap   (NEVER "assess")
# Each day totals exactly 480 training minutes (lunch excluded).
#
# Day 3 devotes its full afternoon to deeper hands-on lab time, an end-to-end
# consolidation build and an extended course-wide recap.
def SCHEDULE(lab_titles):
    return {
     1: (DAY_THEMES[1], [
        ("9:30","10:00",30,"admin","Welcome, course introduction, ground rules and ice-breaker"),
        ("10:00","10:45",45,"topic",f"Topic 1 — {TOPICS[0]['title']}: {TOPICS[0]['subtitle']} (concepts + demo)"),
        ("10:45","11:00",15,"break","Tea break"),
        ("11:00","13:00",120,"lab","Hands-on: "+lab_titles([1,2,3])),
        ("13:00","14:00",60,"lunch","Lunch break"),
        ("14:00","15:30",90,"lab","Hands-on: "+lab_titles([4])+f". Topic 2 — {TOPICS[1]['title']}: {TOPICS[1]['subtitle']} (concepts)"),
        ("15:30","15:45",15,"break","Tea break"),
        ("15:45","18:15",150,"lab","Hands-on: "+lab_titles([5,6,7,8])),
        ("18:15","18:30",15,"recap","Day 1 recap and Q&A"),
     ]),
     2: (DAY_THEMES[2], [
        ("9:30","9:45",15,"recap","Day 1 recap and Q&A"),
        ("9:45","10:45",60,"topic",f"Topic 3 — {TOPICS[2]['title']}: {TOPICS[2]['subtitle']} (concepts + demo)"),
        ("10:45","11:00",15,"break","Tea break"),
        ("11:00","13:00",120,"lab","Hands-on: "+lab_titles([9,10])),
        ("13:00","14:00",60,"lunch","Lunch break"),
        ("14:00","15:30",90,"lab","Hands-on: "+lab_titles([11,12])),
        ("15:30","15:45",15,"break","Tea break"),
        ("15:45","18:15",150,"lab",f"Topic 4 — {TOPICS[3]['title']}: {TOPICS[3]['subtitle']} (concepts). Hands-on: "+lab_titles([13,14])),
        ("18:15","18:30",15,"recap","Day 2 recap and Q&A"),
     ]),
     3: (DAY_THEMES[3], [
        ("9:30","9:45",15,"recap","Day 2 recap and Q&A"),
        ("9:45","11:00",75,"lab","Hands-on: "+lab_titles([15,16])),
        ("11:00","11:15",15,"break","Tea break"),
        ("11:15","13:00",105,"lab",f"Topic 5 — {TOPICS[4]['title']}: {TOPICS[4]['subtitle']} (concepts). Hands-on: "+lab_titles([17])),
        ("13:00","14:00",60,"lunch","Lunch break"),
        ("14:00","15:45",105,"lab","Hands-on: "+lab_titles([18,19,20])),
        ("15:45","16:00",15,"break","Tea break"),
        ("16:00","17:30",90,"lab","Consolidation build: rebuild the CardGuard stack end-to-end from a clean checkout — uv sync, run the analytics pipeline, start the FastAPI service and the Streamlit dashboard, then containerise and verify the health endpoint. Trainer-supported, working individually."),
        ("17:30","18:30",60,"recap","Course-wide recap and Q&A: the four-part prompt pattern, the OOP/analytics/API/deployment spine, common AI-generated defects and how each was caught, and a guided walkthrough of where to take CardGuard next."),
     ]),
    }

# ------------------------------------------------------------------ optional deck content
COURSE_OVERVIEW = dict(
    section_title="Course Fundamentals",
    concepts_title="Key Concepts",
    concepts=[
        ("Vibe Coding", "Directing an AI assistant to write code you specify, review and own. The assistant accelerates you; it does not absolve you of correctness."),
        ("Reproducible Projects", "uv manages the interpreter, the virtual environment and a lockfile, so the project installs identically on every machine."),
        ("Prompt Specification", "State the goal, the constraints, the inputs and the expected output. Vague prompts produce plausible but wrong code."),
        ("Review Discipline", "Read and run generated code before trusting it. Test the boundaries the prompt specified — that is where generated code fails."),
    ],
    framework_title="The Four-Part Prompt Pattern",
    framework=[
        ("Goal", "What the code must accomplish, in one sentence."),
        ("Constraints", "Rules, thresholds, limits and error behaviour the code must honour."),
        ("Inputs", "The exact parameters and their types."),
        ("Expected Output", "The return shape and what it means."),
    ],
    statement=dict(
        headline="The assistant writes the code. You own the correctness.",
        body="Every lab in this course ends with a verification step, because generated code that looks right and is wrong is the defining risk of AI-assisted development.",
        kicker="KEY IDEA"),
    pillars_title="What You'll Build",
    pillars=[
        ("CardGuard — a fraud screening system", [
            "A three-tier application built up lab by lab",
            "Streamlit dashboard over a FastAPI service over SQLite",
            "pandas analytics and a rule-based risk engine",
        ]),
        ("Production practices", [
            "Locked dependencies with uv.lock",
            "Typed request/response models with Pydantic",
            "A container image with a verified health endpoint",
        ]),
    ],
    arc_title="How Every Lab Progresses",
    arc=[
        "Specify the change with a four-part prompt.",
        "Generate the code with your AI assistant.",
        "Read every line before you run it.",
        "Run it and test the boundaries.",
        "Correct what the assistant got wrong.",
    ],
)

LAB_SHOTS = {}

# ------------------------------------------------------------------ optional LG content
LG_INTRO = (
    "This guide accompanies AI Vibe Coding for Python Applications (C179), a "
    "three-day hands-on course in which you build and deploy one real Python "
    "application — CardGuard, a card-transaction fraud screening system — using "
    "an AI coding assistant throughout."
)
LG_INTRO2 = (
    "The twenty labs are cumulative: each one extends the same application, so by "
    "the end you have a working three-tier system you built yourself. Every lab "
    "finishes with a verification step, because the central discipline of vibe "
    "coding is proving that the generated code actually does what you specified."
)
LG_SETUP = dict(
    needs=[
        "A laptop with administrative rights to install software.",
        "Python 3.12 and uv (the labs install uv in Lab 1).",
        "An AI coding assistant — Claude, GitHub Copilot or Cursor.",
        "A terminal and a code editor (VS Code recommended).",
    ],
    verify_text="Confirm your setup before you begin Lab 1.",
    verify_code="$ uv --version\n$ python3 --version",
    conventions=[
        "Placeholders such as <VALUE> are replaced with your own values.",
        "Commands prefixed with $ are typed into your terminal.",
        "Every lab ends with a 'Test it' step — do not skip it.",
    ],
)
LAB_NOTE = (
    "All transaction data in these labs is generated locally by mockdata.py with a "
    "fixed seed. No real cardholder data is used at any point. Use only accounts "
    "and data you are authorised to use."
)
LG_WRAPUP = dict(
    title="Wrap-Up",
    intro="Over three days you built and deployed a complete Python application with an AI assistant at your side.",
    sections=[
        dict(title="What you built", bullets=[
            "A reproducible uv project with locked dependencies.",
            "An object-oriented domain model for cards, transactions and rules.",
            "A pandas analytics pipeline that cleans, groups and aggregates transaction data.",
            "A FastAPI service with typed Pydantic request and response models.",
            "A Streamlit dashboard and a containerised, verified deployment.",
        ]),
        dict(title="The habits that matter", bullets=[
            "Specify before you generate: goal, constraints, inputs, expected output.",
            "Read every generated line before running it.",
            "Test the boundaries — thresholds, empty inputs and error paths.",
            "Keep the analytics layer plain Python so it stays testable.",
            "Never commit secrets; configuration belongs in environment variables.",
        ]),
    ],
)
LG_NEXT_STEPS = _NEXT_STEP_ITEMS
LG_GLOSSARY = [
    ("Vibe coding", "Directing an AI coding assistant to produce code that you specify, review, test and own."),
    ("uv", "A fast Python package and project manager that handles the interpreter, virtual environment and a lockfile."),
    ("uv.lock", "A lockfile pinning the exact resolved version of every dependency so installs are reproducible."),
    ("DataFrame", "A labelled two-dimensional table in pandas; a Series is a single column of one."),
    ("Copy-on-Write", "The pandas 3.0 default under which chained assignment no longer mutates the original frame."),
    ("split-apply-combine", "The groupby-then-aggregate pattern that answers most questions about a dataset."),
    ("Encapsulation", "Hiding internal state behind methods and properties so callers depend on behaviour, not layout."),
    ("Composition", "Modelling a 'has-a' relationship by holding another object, usually preferred over inheritance."),
    ("Dunder method", "A double-underscore special method such as __init__ or __repr__ that hooks into Python's built-in behaviour."),
    ("Pydantic", "A library that declares data shapes with type hints and validates them at runtime."),
    ("FastAPI", "A Python web framework that derives validation and OpenAPI documentation from type annotations."),
    ("Container image", "A bundle of interpreter, dependencies and application code that runs identically anywhere."),
    ("Health endpoint", "A lightweight endpoint used to verify that a deployed service is actually running."),
]

# ------------------------------------------------------------------ version history
VERSION_HISTORY = [
    ("1.0", VERSION_DATE,
     "Initial release of course C179 — 3 days, 5 topics and 20 hands-on labs "
     "building the CardGuard fraud-screening application with an AI coding "
     "assistant. Day 3 closes with an end-to-end consolidation build and an "
     "extended course-wide recap.",
     TRAINER),
]
