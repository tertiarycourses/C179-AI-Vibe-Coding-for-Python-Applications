# Labs — Build and Deploy Python Applications with Vibe Coding

20 hands-on labs building **CardGuard**, a card-transaction fraud screening system.

Every lab uses `uv`. Run the combined notebook [CardGuard-All-Labs.ipynb](CardGuard-All-Labs.ipynb) or work through the per-lab folders below.

| Lab | Topic | Title | Objective |
|---|---|---|---|
| 1 | Vibe Coding Foundations | [Set Up a Reproducible Python Project with uv](topic1/lab01_set_up_a_reproducible_python_project_with_uv/README.md) | Create and run a Python project using uv |
| 2 | Vibe Coding Foundations | [Write Effective Prompts for an AI Coding Assistant](topic1/lab02_write_effective_prompts_for_an_ai_coding_assista/README.md) | Apply prompting patterns that produce correct, reviewable code |
| 3 | Vibe Coding Foundations | [Review and Correct AI-Generated Code](topic1/lab03_review_and_correct_ai_generated_code/README.md) | Identify and fix defects in code produced by an AI assistant |
| 4 | Vibe Coding Foundations | [Refactor Working Code Conversationally](topic1/lab04_refactor_working_code_conversationally/README.md) | Use an AI assistant to restructure code without changing its behaviour |
| 5 | Object-Oriented Programming in Python | [Model a Domain with Classes and Dunder Methods](topic2/lab05_model_a_domain_with_classes_and_dunder_methods/README.md) | Define classes that bundle data with behaviour |
| 6 | Object-Oriented Programming in Python | [Encapsulate State with Properties and Validation](topic2/lab06_encapsulate_state_with_properties_and_validation/README.md) | Protect object state behind a controlled interface |
| 7 | Object-Oriented Programming in Python | [Build a Rule Hierarchy with Inheritance and Polymorphism](topic2/lab07_build_a_rule_hierarchy_with_inheritance_and_poly/README.md) | Share behaviour through a base class and override it per rule |
| 8 | Object-Oriented Programming in Python | [Compose Rules into an Engine](topic2/lab08_compose_rules_into_an_engine/README.md) | Use composition to assemble behaviour from independent parts |
| 9 | Data Analytics with pandas | [Load and Explore Transactions with pandas](topic3/lab09_load_and_explore_transactions_with_pandas/README.md) | Read SQL into a DataFrame and profile it |
| 10 | Data Analytics with pandas | [Handle Errors with Exceptions](topic3/lab10_handle_errors_with_exceptions/README.md) | Use try/except/else/finally and raise meaningful custom exceptions |
| 11 | Data Analytics with pandas | [Build Per-Cardholder Baselines with GroupBy](topic3/lab11_build_per_cardholder_baselines_with_groupby/README.md) | Compute per-group statistics with split-apply-combine |
| 12 | Data Analytics with pandas | [Detect Velocity Bursts with Rolling Time Windows](topic3/lab12_detect_velocity_bursts_with_rolling_time_windows/README.md) | Analyse ordered time-series data per group |
| 13 | Data Modelling with Pydantic and FastAPI | [Replace Hand-Written Validation with Pydantic Models](topic4/lab13_replace_hand_written_validation_with_pydantic_mo/README.md) | Declare data shape with type hints and validate at runtime |
| 14 | Data Modelling with Pydantic and FastAPI | [Expose the Screening Engine as a FastAPI Endpoint](topic4/lab14_expose_the_screening_engine_as_a_fastapi_endpoin/README.md) | Turn typed Python functions into HTTP endpoints |
| 15 | Data Modelling with Pydantic and FastAPI | [Persist Screening Decisions to SQLite](topic4/lab15_persist_screening_decisions_to_sqlite/README.md) | Write application state to a database from the API layer |
| 16 | Data Modelling with Pydantic and FastAPI | [Test the API with pytest and httpx](topic4/lab16_test_the_api_with_pytest_and_httpx/README.md) | Write automated tests for a FastAPI application |
| 17 | Packaging and Deployment | [Build a Fraud Analyst Dashboard with Streamlit](topic5/lab17_build_a_fraud_analyst_dashboard_with_streamlit/README.md) | Create a data application UI that consumes the API |
| 18 | Packaging and Deployment | [Externalise Configuration and Protect Secrets](topic5/lab18_externalise_configuration_and_protect_secrets/README.md) | Move settings out of code into the environment |
| 19 | Packaging and Deployment | [Lock Dependencies and Containerise the API](topic5/lab19_lock_dependencies_and_containerise_the_api/README.md) | Package the application into a reproducible image |
| 20 | Packaging and Deployment | [Deploy the Full Stack with Docker Compose](topic5/lab20_deploy_the_full_stack_with_docker_compose/README.md) | Run and verify a multi-service application |

## Setup

```bash
uv add pandas pydantic fastapi 'uvicorn[standard]' streamlit httpx pytest
uv run python mockdata.py
```
