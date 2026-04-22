---
# AGENTS.md - Supermercados Scraper
opencode-init: false
skill-version: 1.8.0
domain-profile: Traditional App
compliance: None
verbosity-level: standard
expires-after: 90 days
inherits: none
operational-mode: refactor
decision-log-enabled: false
created-date: 2026-04-28
---

## Agent Profile [HIGH]
- **Role:** Python Developer (Scraper & GUI Tools)
- **Responsibilities:** Build and maintain web scraping modules, GUI interfaces (dearpygui), and CLI tools (typer). Ensure data extraction reliability and code quality.
- **Decision Authority:** Can approve changes to scraping logic, GUI layouts, and CLI arguments independently.

## Operational Modes [HIGH]
- **Current Mode:** Refactor
- **Mode-Specific Rules:**
  - *Standard:* Follow all guardrails, standard TDD/workflow rules
  - *Refactor:* Prioritize DRY, design patterns, test coverage; relax non-critical style rules
  - *Hotfix:* Bypass non-critical linting/style guardrails for speed; require "Recorded Technical Debt" entry post-fix
  - *Discovery:* Relax rigid guardrails for creativity; allow iterative prototyping without mandatory TDD
  - *Emergency:* Override all non-essential guardrails; require post-incident review and ADR entry

## Tech Stack & Tooling [HIGH]
- **Language/Runtime:** Python 3.x (Paradigm: Procedural)
- **Typing System:** Gradual Typing (type hints with typing module)
- **Package Manager:** pip (requirements.txt)
- **Frameworks:** Typer (CLI), DearPyGui (GUI), BeautifulSoup4 + lxml (Scraping)
- **Infrastructure:** Podman (local containers)
- **Version Control:** jj (jujutsu)
- **Shell:** fish
- **CI/CD:** None (personal project)

## Coding Standards [HIGH]
- **Style:** PEP 8 compliance
- **Typing:** Strict type hints required on all function signatures (use `typing` module: `Any`, `Dict`, `List`, `Optional`, `Annotated`)
- **Formatting:** No automated formatter specified; adhere to PEP 8 manually
- **Error Handling:** Use `except` with specific exception types; FORBID bare `except:`

## Testing Requirements [HIGH]
- **Coverage Minimum:** 80%
- **Test Types:** Unit tests (scraping logic, data parsing), Integration tests (CLI commands)
- **Framework:** pytest (inferred from test_app.py, test_gui.py)
- **TDD Mandatory:** Yes - Write tests BEFORE implementation code (Red-Green-Refactor)

## Security & Compliance Shield [CRITICAL]
### Security Baseline
- **Secrets Management:** No hardcoded credentials; use environment variables or `.env.example` for configuration
- **Input Validation:** Validate all user inputs via typer CLI arguments and GUI inputs
- **SCA/SAST:** Run `pip-audit` before each commit to check for vulnerable dependencies
- **Web Scraping Ethics:** Respect `robots.txt`; implement rate limiting; use `fake-useragent` responsibly

### OWASP Top 10 Considerations
- **Injection:** Sanitize all parsed HTML content before processing
- **Sensitive Data:** Ensure scraped data is handled locally; no unauthorized data transmission

## Workflow & Git [HIGH]
- **Version Control:** jj (jujutsu)
- **Commit Format:** Conventional Commits style (feat, fix, refactor, test, chore, docs)
- **Branch Strategy:** Linear history with `jj` (no branches - use changesets)
- **Code Review:** Not required (personal project)
- **Rebase Workflow:** Use `jj rebase` for history editing

## Development Methodology [HIGH]
- **Approach:** Test-Driven Development (TDD) - MANDATORY
- **TDD Workflow:** Red-Green-Refactor cycle
  1. Write a failing test (Red)
  2. Write minimal code to pass the test (Green)
  3. Refactor while keeping tests green
- **Pre-commit:** Run tests and `pip-audit` before each `jj commit`

## Guardrails [CRITICAL]
### Forbidden
- `eval()` and `exec()` under any circumstances
- `datetime.now()` (use dependency injection for time-dependent code)
- `random` without explicit seed (not applicable for this project's use case)
- Bare `except:` clauses (always specify exception type)
- `Any` type annotations (use specific types from `typing` module)
- Hardcoded credentials or API keys
- Unrestricted web requests without timeouts

### Mandatory
- Type hints on ALL function signatures (use `from typing import Annotated, Dict, List, Optional, Any`)
- Test-Driven Development (TDD): Write tests BEFORE implementation code
- Use `Path` from `pathlib` for file path operations (already implemented correctly)
- Input validation for all external data (scraped content, user inputs)
- Respectful scraping: implement delays between requests, check robots.txt
- Run `pip-audit` before committing dependency changes

## Review Triggers [LOW]
This file must be updated when:
- New major dependency added (e.g., switching scraping framework)
- Tech stack migration (e.g., moving from dearpygui to another GUI framework)
- Architecture changes (e.g., adding database storage)
- **Dead Man's Switch:** Review if file older than 90 days (Created: 2026-04-28)
