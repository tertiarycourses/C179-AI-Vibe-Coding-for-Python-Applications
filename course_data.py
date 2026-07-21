"""
SINGLE SOURCE OF TRUTH for the TGS-2019504591 courseware.

Every artifact — the slide deck (PPT), Lesson Plan (LP), Learner Guide (LG)
and the labs/ folder — is generated from (or aligned to) the data in this
module, so titles, topic numbering, activities, learning outcomes and the
schedule can never drift apart.

Edit here, then re-run build_slides.py / build_lesson_plan.py /
build_learner_guide.py.
"""

# ------------------------------------------------------------------ metadata
TITLE       = "Build and Deploy Python Applications with Vibe Coding"
SHORT_TITLE = "Build and Deploy Python Apps with Vibe Coding"
COURSE_CODE = "TGS-2019504591"
VERSION     = "v1.6"
VERSION_DATE = "20 July 2026"
ORG         = "Tertiary Infotech Academy Pte Ltd"

# Document Version Control Record (version, date, summary, author)
VERSIONS = [
    ("1.0", "20 July 2026",
     "Initial release — 5 topics, 20 labs, CardGuard fraud-screening application.",
     "Dr. Alfred Ang"),
    ("1.1", "20 July 2026",
     "Corrected all framing content to the Python / vibe-coding syllabus: learning "
     "outcomes, core-concepts section, trainer profile, lesson-plan schedule "
     "(9:30am-6:30pm), lab references (20 labs) and closing slides now render from "
     "course_data. Added Quick Command Reference and Support sections to the Learner "
     "Guide.", "Dr. Alfred Ang"),
    ("1.2", "20 July 2026",
     "Rebuilt the lab step slides: code now renders in a dark card sized to its "
     "content with a side-by-side explanation column, long snippets continue onto "
     "further slides, and the instruction text no longer overlaps the code. Added "
     "cover logos; replaced the exam-weighting kicker; Briefing for Assessment is "
     "now a visual tile grid.", "Dr. Alfred Ang"),
    ("1.3", "20 July 2026",
     "Fixed the lab code slides properly: code is wrapped to the card width so it "
     "can no longer render outside the dark card, and wrapped continuation lines "
     "keep their indentation instead of resetting to column 0. Lab kickers now show "
     "the lab number only (they were truncated mid-word). Replaced the LMS/TMS text "
     "link with a portal screenshot slide.", "Dr. Alfred Ang"),
    ("1.4", "20 July 2026",
     "Course-portal screenshot is now scaled to fit inside its card (it previously "
     "overhung the card and collided with the caption), and the caption sits below "
     "the card.", "Dr. Alfred Ang"),
    ("1.5", "20 July 2026",
     "Re-authored Labs 1 and 2 onto the CardGuard application. They previously "
     "built an unrelated payroll/CPF tool while every other lab built CardGuard, so "
     "learners were told to work inside a payroll project in Lab 1 and inside the "
     "cardguard project from Lab 5. Lab 1 now initialises the cardguard project and "
     "loads transactions; Lab 2 teaches the same prompting pattern against a "
     "transaction risk-scoring function.", "Dr. Alfred Ang"),
    ("1.6", "20 July 2026",
     "Aligned the courseware with the new v17 assessment set: the practical "
     "instrument is a Case Study (CS, 80 minutes), not a Practical Performance "
     "(PP), and the WA is 50 minutes — corrected on the deck, the lesson plan and "
     "the learner guide. Code snippets now wrap on token boundaries so long "
     "pandas chains no longer split a string literal mid-word, and the "
     "explanation column no longer shows OOP notes beside Streamlit or Docker "
     "code.", "Dr. Alfred Ang"),
]
UEN         = "UEN: 201200696W"
TRAINER     = "Dr. Alfred Ang"
DAYS        = 3

# cover badge (top-right of the title slide)
BADGE_TOP   = "PYTHON"
BADGE_SUB   = "VIBE CODING"

# trainer profile card bullets (label, text)
TRAINER_BULLETS = [
    ("Role", "Principal Trainer, Tertiary Infotech Academy Pte. Ltd."),
    ("Expertise", "Python application development, AI-assisted (vibe) coding, data analytics and deployment."),
    ("Delivers", "WSQ courses on Python, AI-assisted development, data engineering & software delivery."),
    ("Founder", "Founder and lead instructor at Tertiary Infotech / Tertiary Courses."),
]

ICE_BREAKER = [
    "Your name and organisation / role.",
    "Your experience with Python and with AI coding assistants (if any).",
    "What you want to build and deploy after this course.",
]

# closing slides
NEXT_STEPS_TITLE = "Where to Go Next"
NEXT_STEPS = [
    "Rebuild CardGuard from scratch on your own machine, using your AI assistant for every step.",
    "Add a new fraud rule and a matching pytest test, then redeploy the container.",
    "Swap SQLite for PostgreSQL — the repository layer is the only module that should change.",
    "Publish your image to a registry and deploy it to a cloud host.",
    "Practise the four-part prompt pattern on your own work: goal, constraints, inputs, expected output.",
]
THANK_YOU_LINE = "You can now build, test and deploy a real Python application with AI assistance."
THANK_YOU_KICKER = "KEEP BUILDING"

# ------------------------------------------------------------------ toolchain
# Every lab standardises on uv for environment + dependency management so runs
# are fast, reproducible and identical on every learner machine.
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

# ------------------------------------------------------------------ topics
# num, code, title, subtitle, weighting, concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Vibe Coding Foundations",
         subtitle="uv Projects · AI Coding Assistants · Prompting Patterns · AI-Assisted Refactoring",
         weighting="15–20%",
         concepts=[
            "Vibe coding is directing an AI assistant to write code you specify, review and own — you remain accountable for correctness.",
            "uv manages the interpreter, virtual environment and locked dependencies: uv init, uv add, uv run.",
            "Effective prompts state the goal, the constraints, the inputs and the expected output — vague prompts produce plausible but wrong code.",
            "Always read and run AI-generated code before trusting it; refactoring conversationally is faster than rewriting by hand.",
         ]),
    dict(num=2, code="02",
         title="Object-Oriented Programming in Python",
         subtitle="Classes · Encapsulation · Inheritance · Composition · Dunder Methods",
         weighting="20–25%",
         concepts=[
            "A class bundles data (attributes) with the behaviour that operates on it (methods); an object is one instance of it.",
            "Encapsulation hides internal state behind methods and properties so callers depend on behaviour, not layout.",
            "Inheritance models 'is-a' and shares behaviour; composition models 'has-a' and is usually the more flexible default.",
            "Dunder methods (__init__, __repr__, __eq__) integrate your classes with Python's built-in operators and printing.",
         ]),
    dict(num=3, code="03",
         title="Data Analytics with pandas",
         subtitle="DataFrames · Cleaning · Transformation · GroupBy · Aggregation · Reporting",
         weighting="20–25%",
         concepts=[
            "A DataFrame is a labelled 2-D table; a Series is one column. Most analytics is selecting, filtering and reshaping these.",
            "Real data is dirty: missing values, wrong dtypes and duplicates must be handled explicitly before analysis.",
            "split-apply-combine (groupby then aggregate) answers most business questions about a dataset.",
            "An analytics pipeline should be a set of small, testable functions — not one long script.",
         ]),
    dict(num=4, code="04",
         title="Data Modelling with Pydantic and FastAPI",
         subtitle="Typed Models · Validation · Endpoints · Request/Response Schemas · Auto Docs",
         weighting="20–25%",
         concepts=[
            "Pydantic models declare the shape of data with Python type hints and validate it at runtime, failing fast on bad input.",
            "FastAPI turns typed Python functions into HTTP endpoints, deriving validation and OpenAPI docs from the annotations.",
            "Separate request models from response models so the API contract is explicit and safe to change.",
            "The analytics layer stays plain Python; FastAPI is a thin transport layer over it.",
         ]),
    dict(num=5, code="05",
         title="Packaging and Deployment",
         subtitle="uv Lockfiles · Configuration · Containers · Deploying a Service",
         weighting="15–20%",
         concepts=[
            "uv.lock pins exact versions so the application installs identically in development and production.",
            "Configuration belongs in environment variables, never hard-coded — secrets must never be committed.",
            "A container image bundles the interpreter, dependencies and application code into one deployable artifact.",
            "A deployment is not done until the running service has been verified with a real request against a health endpoint.",
         ]),
]

# ------------------------------------------------------------------ 3-day schedule (8 training hours/day)
# Each day: list of (start, end, minutes, kind, text). kind: 'admin','topic','activity','break','lunch','assess','recap'
# Day totals must be 480 training minutes (lunch excluded from the 8h).
DAY_THEMES = {
    1: "Vibe Coding Foundations & Object-Oriented Python",
    2: "Data Analytics with pandas, Pydantic & FastAPI",
    3: "FastAPI, Packaging, Deployment & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 50 minutes, open book.",
    practical="Case Study (CS) — a CardGuard scenario with practical tasks drawn from the labs, 80 minutes, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
