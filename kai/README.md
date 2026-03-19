# Kai Bridge — координация между инстансами Claude Code

## Как работает
- `tasks/pending.md` — новое задание (пишет master)
- `tasks/running.md` — выполняется (agent переименовывает)
- `tasks/result.md` — результат (agent пишет)
- `tasks/history/` — архив выполненных

## Агенты
- **master**: ThinkCentre2 (дом) — ставит задания
- **kumtor**: V-DATAMINE-01 (работа) — выполняет
