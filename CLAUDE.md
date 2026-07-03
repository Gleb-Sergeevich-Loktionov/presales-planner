# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**presales-planner** — a Telegram bot that auto-schedules a team's tasks across
people and days (capacity, dependencies, deadlines) with a FastAPI web admin.
Single-tenant, one process, one Postgres writer. Intent parsing via Claude;
scheduling via a deterministic greedy solver over a critical-path graph.

## Commands

```bash
docker compose up -d                      # postgres + redis
uv sync                                    # dependencies
uv run alembic upgrade head                # migrations
uv run python -m seed.load                 # demo seed
uv run python -m planner.main              # run bot + web admin (:8000) + scheduler

uv run pytest tests                        # all tests
uv run pytest tests/unit/domain -k solver  # a single test / subset
make lint                                  # ruff + mypy (strict)
make acceptance                            # acceptance scenarios
```

Python 3.12, package lives in `src/planner`, managed with `uv` (see `uv.lock`).

## Architecture (dependencies point inward)

- **`bot/`** (aiogram) and **`web/`** (FastAPI) — delivery adapters.
- **`app/`** — use-cases (add_project, confirm_plan, what_if, set_vacation, …).
- **`domain/`** — pure logic, **no IO**: greedy solver, critical path, working
  calendar, capability model, intent types.
- **`infra/`** — adapters: DB (SQLAlchemy async + Alembic), LLM (Claude), STT
  (faster-whisper), calendar, scheduler (APScheduler), Notion sink.

Every external integration sits behind a Port (`SolverPort`, `IntentParserPort`,
`WorkingCalendar`, `RepoPort`, `STTPort`). The domain never imports infra.

## Conventions & invariants

- Keep `domain/` pure and IO-free — it's the primary unit-test target.
- New integration = new adapter behind an existing Port; don't leak infra into `app`/`domain`.
- Plans are versioned; edits supersede prior versions rather than mutating them.
- `DEBUG=false` in production (it gates the loopback `/dev-login` shortcut); the
  app refuses to start with `DEBUG=false` while `JWT_SECRET` is unset.
- `seed/` is **fictional demo data** — no real personal data belongs in the repo.
