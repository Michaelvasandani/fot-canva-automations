# AGENTS.md

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues (`Michaelvasandani/fot-canva-automations`) via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Project skills

- `make-event-card` (`.agents/skills/make-event-card/`): makes a new FoT Event Card in Canva from a Master Page. Claude Code reaches it through the `.claude/skills/make-event-card` symlink.
