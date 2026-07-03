# presales-planner

Telegram bot that **auto-schedules a team's tasks across people and days** —
respecting each person's capacity, task dependencies and deadlines — with a
FastAPI web admin for hard edits. One process, one Postgres writer, single-tenant.

<p>
  <img alt="Python" src="https://img.shields.io/badge/python-3.12-blue">
  <img alt="aiogram" src="https://img.shields.io/badge/aiogram-3.x-2CA5E0">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green">
</p>

Give it a project and it assigns every task to the right person on the right day,
flags overloads and unreachable deadlines, and explains its plan in plain language.
Tasks can be captured by **text or voice**; the resulting plan is editable from the
bot or the web admin. Intent parsing runs through Claude; scheduling is a
deterministic greedy solver over a critical-path graph.

## Architecture

Four layers, dependencies point inward:

```
bot/ (aiogram)   web/ (FastAPI + htmx)
        \             /
          app/ (use-cases)
             |
     domain/ (solver, calendar)   ← pure, no IO
             |
     infra/ (db, llm, stt, calendar, scheduler)
```

External integrations sit behind ports (`SolverPort`, `IntentParserPort`,
`WorkingCalendar`, `RepoPort`, `STTPort`), so adapters are swappable and the
domain stays pure and testable.

## Stack

Python 3.12 · aiogram 3 · FastAPI · SQLAlchemy 2 (async) · PostgreSQL 16 ·
Redis 7 · NetworkX (greedy solver) · Claude Haiku (intent parsing) ·
faster-whisper (speech-to-text) · APScheduler · matplotlib · uv.

## Quick start

```bash
# 1. Infra
docker compose up -d            # postgres + redis

# 2. Dependencies
uv sync

# 3. Config
cp .env.example .env            # fill BOT_TOKEN, ANTHROPIC_API_KEY, TEAM_CHAT_ID, ...

# 4. DB + demo seed
uv run alembic upgrade head
uv run python -m seed.load

# 5. Run (bot + web admin on :8000 + scheduler)
uv run python -m planner.main
```

The `seed/` data (team, roles/skills, task templates) is **fictional demo data** —
edit `seed/team.yaml`, `seed/capability.yaml` and `seed/tasks_*.yaml` for your own team.

## Configuration

Everything is via `.env` (see [`.env.example`](.env.example)). Key variables:

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | yes | Async Postgres DSN (`postgresql+asyncpg://…`) |
| `REDIS_URL` | yes | Redis connection string |
| `BOT_TOKEN` | yes | Telegram bot token from @BotFather |
| `ANTHROPIC_API_KEY` | yes | Claude API key (intent parsing) |
| `TEAM_CHAT_ID` | yes | Telegram chat id for notifications |
| `JWT_SECRET` | prod | Admin session signing secret; app refuses to start with `DEBUG=false` if unset |
| `NOTION_TOKEN` / `NOTION_DATABASE_ID` | no | Optional Telegram → Notion task mirror |
| `TIMEZONE` | no | Scheduling timezone (default `Europe/Moscow`) |
| `DEBUG` | no | Must be `false` in production (enables the loopback `/dev-login` shortcut) |

## Make targets

`make dev` · `make test` · `make cov` · `make seed` · `make migrate` ·
`make lint` · `make acceptance`

## Tests

```bash
uv run pytest tests --cov=src/planner --cov-report=term-missing
```

Three levels: **unit** (domain solver, calendar, intent, use-cases — no IO),
**integration** (db + calendar/LLM via vcrpy on a real Postgres), and
**e2e** (bot flows + web admin).

## Status

Sprints 1–6 implemented: schema + seed, greedy solver, intent parsing + bot
baseline, use-cases + PNG (Gantt/heatmap) render, FastAPI admin, observability
and an error boundary. Deferred to v2: OR-Tools/PyJobShop solver, multi-tenant,
production deploy hardening.

## Docs

- [`docs/SPEC.md`](docs/SPEC.md) — design & specification
- [`docs/architecture.md`](docs/architecture.md) — layering and ports
- [`docs/acceptance.md`](docs/acceptance.md) — acceptance scenarios
- [`plans/`](plans) — incremental hardening plans

## License

[MIT](LICENSE) © 2026 Gleb Sergeevich Loktionov.

Reuse (including by AI models) is asked to keep attribution — see [NOTICE](NOTICE).
