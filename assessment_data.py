"""
ASSESSMENT CONTENT for TGS-2019504591 — Build and Deploy Python Applications
with Vibe Coding.

Structure is held IDENTICAL to the reference papers on Google Drive
(WA (SAQ) v15 and CS Assessment v16); only the subject matter is re-authored
from the retired OOP/HPB-BMI syllabus onto the current CardGuard course:

    WA (SAQ)   7 questions, one knowledge code each          K1 .. K7
    Case Study 5 questions, ability codes distributed EXACTLY
               as the reference paper:
                   Q1 = A1, A3, A4, A10
                   Q2 = A2
                   Q3 = A5, A6, A8, A9
                   Q4 = A2
                   Q5 = A7

Every A1..A10 and K1..K7 is therefore covered, and each CS question cites the
labs it is drawn from. All questions are open-ended — no multiple choice.
"""

# ── WRITTEN ASSESSMENT (SAQ) — KNOWLEDGE K1..K7 ─────────────────────────────
# (code, context, question, [model-answer points])
WRITTEN = [
 ("K1",
  "You are working as a Python developer using an AI coding assistant to build a "
  "transaction-screening tool. A colleague argues that because the assistant writes the "
  "code, reviewing its output is optional.",
  "Explain what vibe coding is, and state who is accountable for AI-generated code and why "
  "reviewing every generated line still matters.  (K1)",
  ["Vibe coding is directing an AI coding assistant to write code that YOU specify, review "
   "and own — the assistant accelerates production, it does not take responsibility for the "
   "result.",
   "Accountability stays with the developer. The assistant has no knowledge of the business "
   "rules, the data or the consequences of being wrong; it predicts plausible code, which is "
   "not the same as correct code.",
   "AI-generated code fails in characteristic ways: invented (hallucinated) APIs, silently "
   "wrong business thresholds, missing edge-case and error handling, and outdated idioms "
   "drawn from older library versions.",
   "A concrete course example: assistants frequently emit pandas 1.x chained-assignment "
   "idioms, which no longer mutate in place under pandas 3.0 Copy-on-Write — the code runs "
   "but silently does nothing.",
   "The discipline taught in class: read the generated code, run it, test the boundaries, and "
   "only then keep it. Never paste code you have not read into a system that makes decisions.",
   "(Slides: Topic 1 — Vibe Coding Foundations. Labs 02, 03.)"]),

 ("K2",
  "Your team must be able to reproduce a colleague's environment exactly, on a different "
  "machine, months later.",
  "Explain how uv makes a Python project reproducible, and describe the role of "
  "pyproject.toml and uv.lock.  (K2)",
  ["uv manages the interpreter, the virtual environment and the dependencies as one unit, so "
   "every learner and every server runs an identical environment.",
   "pyproject.toml is the project MANIFEST — it declares what the project depends on, in the "
   "loose form the developer asked for (e.g. pandas).",
   "uv.lock is the LOCKFILE — it records the exact resolved version of every direct and "
   "transitive dependency, so a later install cannot silently pick up a different version.",
   "uv init creates the project; uv add resolves, installs and records a dependency in one "
   "step; uv run executes inside the project environment with no manual venv activation.",
   "uv python pin fixes the interpreter version so the code is not run on a different Python "
   "than it was developed against.",
   "Reproducibility is proven, not assumed: delete .venv, run uv sync to rebuild it from the "
   "lockfile, and confirm the program produces identical output (Lab 01).",
   "(Slides: Topic 1 — uv Projects. Lab 01.)"]),

 ("K3",
  "You ask an assistant 'write a function to score a transaction' and receive code that runs "
  "but does not do what the business needs.",
  "Explain the four-part prompting pattern taught in this course, and why a vague prompt "
  "produces plausible but wrong code.  (K3)",
  ["An effective prompt states four things: the GOAL (what the code must achieve), the "
   "CONSTRAINTS (rules, thresholds, limits), the INPUTS (names, types, ranges) and the "
   "EXPECTED OUTPUT (shape, type, rounding, error behaviour).",
   "A vague prompt forces the assistant to invent the unstated parts. It will silently choose "
   "its own thresholds, its own return shape and its own error handling — all plausible, none "
   "verified against the business rules.",
   "Worked contrast from the lab: 'write a function to score a transaction' leaves the score "
   "range, the risk thresholds, the overseas rule and the negative-amount behaviour "
   "undefined.",
   "The specified version names the signature score_transaction(amount, is_overseas, hour) -> "
   "dict, fixes the points per rule, caps the score at 100, and requires ValueError on a "
   "negative amount or an out-of-range hour — so the output can actually be checked.",
   "The test of a good prompt: could a second developer verify the result without asking you "
   "what you meant? If not, the prompt was underspecified.",
   "(Slides: Topic 1 — Prompting Patterns. Lab 02.)"]),

 ("K4",
  "You are designing the classes for the screening tool. A colleague proposes making every "
  "rule a subclass of a base rule, and another proposes giving the engine a list of rules.",
  "Explain the difference between inheritance and composition, and state when each is the "
  "appropriate choice.  (K4)",
  ["Inheritance models an IS-A relationship: a HighValueRule IS-A Rule, so it inherits the "
   "shared interface and overrides the behaviour that differs.",
   "Composition models a HAS-A relationship: a ScreeningEngine HAS-A list of Rule objects and "
   "delegates to them; it is not itself a rule.",
   "Inheritance is right when the subtypes genuinely share a contract and are substitutable — "
   "the engine can call rule.evaluate(txn) on any rule without knowing which subclass it is "
   "(polymorphism).",
   "Composition is the more flexible default: rules can be added, removed or reordered at "
   "runtime without touching the engine, and the engine is not coupled to a class hierarchy.",
   "In the course application both appear together and that is deliberate: a Rule base class "
   "with subclasses (inheritance, Lab 07) composed into an engine that holds them in a list "
   "(composition, Lab 08).",
   "The failure mode to avoid: deep inheritance chains built to share incidental code rather "
   "than a real IS-A contract — prefer composition when in doubt.",
   "(Slides: Topic 2 — Inheritance · Composition. Labs 07, 08.)"]),

 ("K5",
  "Your screening code reads a CSV of transactions that arrives from an external provider and "
  "is frequently malformed.",
  "Explain the split-apply-combine pattern in pandas, and describe how you would handle rows "
  "that fail validation.  (K5)",
  ["Split-apply-combine is the pattern behind groupby: SPLIT the rows into groups by a key, "
   "APPLY an aggregation to each group, and COMBINE the results back into one table.",
   "In the course application it answers the business question directly — group the "
   "transactions per cardholder, then aggregate to a mean and standard deviation to build "
   "each cardholder's spending baseline (Lab 11).",
   "Real data is dirty: missing values, wrong dtypes and duplicates must be handled "
   "explicitly BEFORE analysis, or the aggregates are quietly wrong.",
   "Validate rather than crash: convert types explicitly, coerce or drop unparseable values, "
   "and count what was rejected so the rejection rate itself is visible.",
   "Raise or log, never swallow: a bare except that hides a malformed row turns a data problem "
   "into a silent wrong answer. Catch the specific exception, record the offending row, and "
   "continue deliberately (Lab 10).",
   "Under pandas 3.0 Copy-on-Write, chained assignment no longer mutates in place — assign "
   "results back explicitly rather than relying on the older idiom.",
   "(Slides: Topic 3 — Data Analytics with pandas. Labs 09, 10, 11.)"]),

 ("K6",
  "The screening engine is to be exposed as a web API consumed by another team.",
  "Explain what Pydantic contributes to a FastAPI application, and why validating at the "
  "boundary matters.  (K6)",
  ["Pydantic validates data at RUNTIME from the type hints — the annotation stops being "
   "documentation and becomes an enforced contract.",
   "A BaseModel declares the shape of the request and the response: field names, types, "
   "required versus optional, and constraints such as a non-negative amount.",
   "FastAPI uses those models to parse and validate every incoming request, reject bad input "
   "with a clear 422 before any business logic runs, serialise the response, and generate the "
   "OpenAPI documentation automatically.",
   "Validating at the boundary means the core screening code can assume its inputs are "
   "already well-formed — hand-written isinstance checks scattered through the logic "
   "disappear (Lab 13).",
   "It also makes failures debuggable by the CALLER: the error names the offending field and "
   "why it was rejected, instead of surfacing as a TypeError deep in the engine.",
   "(Slides: Topic 4 — Pydantic · FastAPI. Labs 13, 14.)"]),

 ("K7",
  "The application must run identically on a colleague's laptop and on a production server.",
  "Explain how containerising the application achieves this, and describe how configuration "
  "and secrets should be handled.  (K7)",
  ["A container image bundles the interpreter, the locked dependencies and the application "
   "code into ONE artifact, so the runtime environment travels with the code rather than "
   "being rebuilt by hand on each machine.",
   "The lockfile is what makes the image reproducible — copy uv.lock into the image and "
   "install from it, so a rebuild months later resolves the same versions (Lab 19).",
   "Configuration must be EXTERNAL to the image: the same image is promoted from development "
   "to production unchanged, and only the environment differs. Read settings from environment "
   "variables (Lab 18).",
   "Secrets are never committed and never baked into the image. Keep a .env for local "
   "development, add it to .gitignore, and commit a .env.example documenting the required "
   "keys without their values.",
   "A multi-stage build keeps the final image small — build dependencies stay in the builder "
   "stage and do not ship to production. A .dockerignore excludes everything the image does "
   "not need.",
   "Compose runs the multi-tier stack together — the API and the UI as separate services on a "
   "shared network, started with one command (Lab 20).",
   "(Slides: Topic 5 — Packaging and Deployment. Labs 18, 19, 20.)"]),
]

# ── CASE STUDY — ABILITY A1..A10 ────────────────────────────────────────────
SCENARIO_INTRO = (
 "CardGuard Pte Ltd is a Singapore payments company that screens card transactions for "
 "fraud on behalf of small retail banks. Its current screening tool is a single "
 "2,000-line Python script written by a departed contractor: it has no tests, no "
 "validation, hard-coded thresholds, and a database password committed in the source. "
 "The analysts who use it cannot change a rule without asking a developer, and a recent "
 "release silently stopped flagging overseas transactions for three days before anyone "
 "noticed.")

SCENARIO_POINTS = [
 "The data: each transaction record carries a transaction id, a masked card number, a "
 "cardholder id, the merchant name, the merchant country, the amount in SGD, and a "
 "timestamp. The feed arrives as CSV from an external provider and is frequently "
 "malformed — missing amounts, amounts as text, and duplicated rows.",
 "The business rules the analysts want enforced: an amount above S$500 is high value; a "
 "merchant outside Singapore is an overseas risk; more than three transactions on the "
 "same card within ten minutes is a velocity burst; and a transaction more than three "
 "standard deviations above that cardholder's own average is anomalous.",
 "Each rule contributes points to a risk score from 0 to 100, and the analyst must be "
 "able to see WHICH rules fired and why — a bare score is not actionable.",
 "The consumers: a separate team needs to call the screening engine over HTTP from their "
 "settlement system, and the fraud analysts need a dashboard they can use themselves "
 "without running Python.",
 "The constraints: every screening decision must be retained for audit; the tool must run "
 "identically on a developer laptop and on the production server; and the database "
 "credentials must never appear in the repository again.",
 "You will build this with an AI coding assistant, exactly as you did in the labs — "
 "specifying, reviewing and testing every piece of generated code rather than accepting "
 "it unread.",
]

SCENARIO_TAIL = (
 "Answer all five questions below using the techniques and tools you applied in the "
 "hands-on labs. Write real, runnable Python — the code you produce is the evidence being "
 "assessed. Where a question asks you to explain a choice, explain it in your own words.")

# CS questions mirror the reference paper's mapping EXACTLY:
#   Q1 = A1, A3, A4, A10 · Q2 = A2 · Q3 = A5, A6, A8, A9 · Q4 = A2 · Q5 = A7
# (label, criterion, prompt, box_caption, lab_reference, [model-answer points])
CS_ITEMS = [
 ("Question 1", "A1, A3, A4, A10",
  "CardGuard's transaction feed arrives as a CSV that is frequently malformed. Set up a "
  "reproducible project for the screening tool and write the code that loads the feed into "
  "pandas, cleans it, and reports what was rejected. Your answer must show: the uv commands "
  "that create the project and add the dependencies; a load_transactions(path) function that "
  "reads the CSV, coerces the amount and timestamp columns to the correct dtypes, drops "
  "duplicate transaction ids, and returns the clean DataFrame together with a count of the "
  "rows it rejected; and the handling that stops one malformed row from crashing the run.",
  "Write your Python code and the uv commands in the box below",
  "Lab 01 Reproducible Project with uv · Lab 09 Load and Explore Transactions with pandas · "
  "Lab 10 Handle Errors with Exceptions",
  ["Project setup (A1): uv init cardguard, cd cardguard, uv python pin 3.12, then "
   "uv add pandas — uv writes pyproject.toml and uv.lock so the environment is reproducible. "
   "Run everything with uv run python ... (no venv activation).",
   "Loading (A3): pd.read_csv(path) then explicit type coercion — "
   "pd.to_numeric(df['amount'], errors='coerce') and "
   "pd.to_datetime(df['timestamp'], errors='coerce'). errors='coerce' turns unparseable "
   "values into NaN/NaT rather than raising, so the bad rows can be counted instead of "
   "killing the run.",
   "Cleaning (A3, A4): record the starting row count; drop rows where amount or timestamp is "
   "null; df.drop_duplicates(subset='transaction_id'); the rejected count is the difference "
   "between the starting and finishing row counts.",
   "A correct shape for the function:\n"
   "def load_transactions(path: str) -> tuple[pd.DataFrame, int]:\n"
   "    df = pd.read_csv(path)\n"
   "    before = len(df)\n"
   "    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')\n"
   "    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')\n"
   "    df = df.dropna(subset=['amount', 'timestamp'])\n"
   "    df = df.drop_duplicates(subset='transaction_id')\n"
   "    return df, before - len(df)",
   "Error handling (A4, A10): wrap the read in try/except catching the SPECIFIC exceptions — "
   "FileNotFoundError for a missing feed, pd.errors.EmptyDataError / ParserError for a "
   "corrupt file — and re-raise or log with the offending path. A bare except that swallows "
   "everything turns a data problem into a silent wrong answer.",
   "Reporting (A10): print or log the rejected count every run. A rejection rate that "
   "suddenly jumps is the earliest signal that the upstream feed changed — this is exactly "
   "the failure that went unnoticed for three days in the scenario.",
   "Reproducibility check (A1): rm -rf .venv then uv sync rebuilds the environment from "
   "uv.lock and the script produces identical output.",
   "Vibe-coding discipline (A10): the candidate should note that generated pandas code must "
   "be checked against pandas 3.0 — chained assignment no longer mutates in place under "
   "Copy-on-Write, and assistants frequently emit the older 1.x idiom."]),

 ("Question 2", "A2",
  "The analysts need to see WHICH rules fired on a transaction, not just a score. Model the "
  "transaction itself as a class. Create a Transaction class that takes the transaction id, "
  "masked card number, cardholder id, merchant name, merchant country, amount and timestamp, "
  "and that exposes: a readable __repr__ for the analyst log, an is_overseas property that is "
  "True when the merchant country is not 'SG', and validation that rejects a negative amount.",
  "Write your Python code in the box below",
  "Lab 05 Model a Domain with Classes and Dunder Methods · Lab 06 Encapsulate State with "
  "Properties and Validation",
  ["A correct class bundles the data with the behaviour that acts on it:\n"
   "class Transaction:\n"
   "    def __init__(self, txn_id, card, cardholder_id, merchant,\n"
   "                 country, amount, timestamp):\n"
   "        if amount < 0:\n"
   "            raise ValueError('amount must not be negative')\n"
   "        self.txn_id = txn_id\n"
   "        self.card = card\n"
   "        self.cardholder_id = cardholder_id\n"
   "        self.merchant = merchant\n"
   "        self.country = country\n"
   "        self._amount = amount\n"
   "        self.timestamp = timestamp",
   "__init__ is the constructor and takes self as its first parameter — omitting self is the "
   "classic error and raises a TypeError on instantiation.",
   "Validation belongs IN the constructor so an invalid Transaction can never exist. Raising "
   "ValueError fails fast and loudly rather than letting a negative amount reach the scoring "
   "engine.",
   "The is_overseas property:\n"
   "    @property\n"
   "    def is_overseas(self) -> bool:\n"
   "        return self.country != 'SG'\n"
   "A property exposes derived state read-only — callers cannot assign to it, which is "
   "exactly right for a value computed from another field.",
   "The dunder for the analyst log:\n"
   "    def __repr__(self) -> str:\n"
   "        return (f'Transaction({self.txn_id}, {self.merchant}, '\n"
   "                f'SGD {self._amount:.2f}, {self.country})')\n"
   "__repr__ integrates the class with Python's own printing so a list of transactions is "
   "readable without a custom formatter.",
   "Credit also for guarding amount behind a property with a setter that re-validates, and "
   "for __eq__ comparing on transaction id so duplicates can be detected with ==."]),

 ("Question 3", "A5, A6, A8, A9",
  "Implement the screening rules as a class hierarchy and compose them into an engine. Your "
  "answer must show: an abstract Rule base class defining the contract every rule must "
  "implement; at least two concrete rules — a high-value rule (over S$500) and an overseas "
  "rule; and a ScreeningEngine that holds a list of rules, evaluates a transaction against "
  "all of them, and returns the total score capped at 100 together with the reasons that "
  "fired. Explain why the engine uses composition rather than inheriting from Rule.",
  "Write your Python code and your explanation in the box below",
  "Lab 07 Build a Rule Hierarchy with Inheritance and Polymorphism · Lab 08 Compose Rules "
  "into an Engine",
  ["The abstract base defines the contract (A5):\n"
   "from abc import ABC, abstractmethod\n\n"
   "class Rule(ABC):\n"
   "    points: int = 0\n"
   "    reason: str = ''\n\n"
   "    @abstractmethod\n"
   "    def applies(self, txn) -> bool:\n"
   "        ...\n"
   "@abstractmethod forces every subclass to implement applies() — the contract is enforced "
   "at instantiation, not merely documented.",
   "Concrete rules override the behaviour that differs (A5, A6):\n"
   "class HighValueRule(Rule):\n"
   "    points, reason = 40, 'high value'\n"
   "    def __init__(self, threshold: float = 500.0):\n"
   "        self.threshold = threshold\n"
   "    def applies(self, txn) -> bool:\n"
   "        return txn.amount > self.threshold\n\n"
   "class OverseasRule(Rule):\n"
   "    points, reason = 30, 'overseas merchant'\n"
   "    def applies(self, txn) -> bool:\n"
   "        return txn.is_overseas",
   "The threshold is a constructor argument, not a hard-coded literal — this is what lets the "
   "analysts tune a rule without a developer, which the scenario explicitly asks for.",
   "The engine composes the rules (A8):\n"
   "class ScreeningEngine:\n"
   "    def __init__(self, rules: list[Rule]):\n"
   "        self.rules = rules\n\n"
   "    def screen(self, txn) -> dict:\n"
   "        score, reasons = 0, []\n"
   "        for rule in self.rules:\n"
   "            if rule.applies(txn):\n"
   "                score += rule.points\n"
   "                reasons.append(rule.reason)\n"
   "        return {'score': min(score, 100), 'reasons': reasons}",
   "Polymorphism is the point (A6): the loop calls rule.applies(txn) without knowing or "
   "caring which subclass it holds. Adding a new rule requires NO change to the engine.",
   "Why composition, not inheritance (A9): a ScreeningEngine HAS-A list of rules; it IS-NOT-A "
   "rule. Inheriting from Rule would be a false IS-A, would give the engine an applies() "
   "method that means nothing, and would couple it to the hierarchy. Composition also lets "
   "rules be added, removed or reordered at runtime.",
   "Returning the reasons alongside the score (A8) is what makes the output actionable for "
   "the analyst — the scenario states a bare score is not enough.",
   "Credit for capping with min(score, 100) as specified, and for noting the rule list is the "
   "single place a new rule is registered."]),

 ("Question 4", "A2",
  "The screening engine must be callable over HTTP by the settlement team, and every request "
  "must be validated before it reaches the engine. Write the Pydantic models and the FastAPI "
  "endpoint: a TransactionIn model describing an incoming transaction with the correct types "
  "and a non-negative amount, a ScreenResult model for the response carrying the score and "
  "the reasons, and a POST /screen endpoint that validates the request, runs the engine and "
  "returns the result.",
  "Write your Python code in the box below",
  "Lab 13 Replace Hand-Written Validation with Pydantic Models · Lab 14 Expose the Screening "
  "Engine as a FastAPI Endpoint",
  ["The request model declares the contract:\n"
   "from pydantic import BaseModel, Field\n"
   "from datetime import datetime\n\n"
   "class TransactionIn(BaseModel):\n"
   "    transaction_id: str\n"
   "    card: str\n"
   "    cardholder_id: str\n"
   "    merchant: str\n"
   "    country: str\n"
   "    amount: float = Field(ge=0)\n"
   "    timestamp: datetime",
   "Field(ge=0) enforces the non-negative amount at the boundary. Pydantic validates at "
   "runtime FROM the type hints — the annotation becomes an enforced contract rather than "
   "documentation.",
   "The response model:\n"
   "class ScreenResult(BaseModel):\n"
   "    transaction_id: str\n"
   "    score: int\n"
   "    reasons: list[str]",
   "The endpoint:\n"
   "from fastapi import FastAPI\n\n"
   "app = FastAPI()\n"
   "engine = ScreeningEngine([HighValueRule(), OverseasRule()])\n\n"
   "@app.post('/screen', response_model=ScreenResult)\n"
   "def screen(txn: TransactionIn) -> ScreenResult:\n"
   "    result = engine.screen(txn)\n"
   "    return ScreenResult(transaction_id=txn.transaction_id, **result)",
   "Declaring txn: TransactionIn is what wires the validation in — FastAPI parses the JSON "
   "body, validates it against the model, and returns a 422 with the offending field named "
   "BEFORE any business logic runs.",
   "response_model=ScreenResult validates and serialises the response and documents it in the "
   "auto-generated OpenAPI page at /docs.",
   "Validating at the boundary means the engine can assume well-formed input — the "
   "hand-written isinstance checks the old script needed disappear.",
   "Run it with uv run uvicorn main:app --reload and demonstrate the 422 by posting a "
   "negative amount."]),

 ("Question 5", "A7",
  "CardGuard's credentials were previously committed to the repository, and the tool must run "
  "identically on a laptop and in production. Show how you would externalise the "
  "configuration, keep the secrets out of source control, and containerise the API. Your "
  "answer must include the settings code, the files you would and would not commit, and a "
  "Dockerfile that installs from the lockfile.",
  "Write your code, your file list and your Dockerfile in the box below",
  "Lab 18 Externalise Configuration and Protect Secrets · Lab 19 Lock Dependencies and "
  "Containerise the API · Lab 20 Deploy the Full Stack with Docker Compose",
  ["Settings read from the environment, never hard-coded:\n"
   "from pydantic_settings import BaseSettings, SettingsConfigDict\n\n"
   "class Settings(BaseSettings):\n"
   "    database_url: str\n"
   "    high_value_threshold: float = 500.0\n"
   "    model_config = SettingsConfigDict(\n"
   "        env_file='.env', env_prefix='CARDGUARD_')\n\n"
   "settings = Settings()",
   "What is committed and what is NOT — this is the heart of the question:\n"
   "  COMMIT: .env.example (the required keys with placeholder values), .gitignore, "
   "Dockerfile, .dockerignore, pyproject.toml, uv.lock\n"
   "  NEVER COMMIT: .env (the real secrets), any credential in source, the .venv directory",
   ".gitignore must contain .env BEFORE the first commit — adding it afterwards does not "
   "remove the secret from git history. A credential that has been pushed must be rotated, "
   "not merely deleted.",
   "A correct multi-stage Dockerfile installing from the lockfile:\n"
   "FROM python:3.12-slim AS builder\n"
   "COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv\n"
   "WORKDIR /app\n"
   "COPY pyproject.toml uv.lock ./\n"
   "RUN uv sync --frozen --no-dev\n\n"
   "FROM python:3.12-slim\n"
   "WORKDIR /app\n"
   "COPY --from=builder /app/.venv /app/.venv\n"
   "COPY . .\n"
   "ENV PATH=\"/app/.venv/bin:$PATH\"\n"
   "CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",
   "uv sync --frozen installs the EXACT versions in uv.lock and fails if the lockfile is out "
   "of date — this is what makes the image reproducible months later.",
   "The multi-stage build keeps build tooling out of the final image; .dockerignore excludes "
   ".venv, .env, .git and __pycache__ so secrets and bulk never enter the build context.",
   "Secrets reach the running container at RUNTIME — docker run --env-file, or compose "
   "env_file / a secrets mount — never via COPY and never via an ENV line in the Dockerfile, "
   "which would bake them into a shipped layer.",
   "The same image is promoted from development to production unchanged; only the environment "
   "differs. That is what guarantees the laptop and the server behave identically.",
   "Credit for compose running the API and Streamlit UI as two services on a shared network "
   "(Lab 20)."]),
]
