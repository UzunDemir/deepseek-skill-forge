# Contributing to DeepSeek Subagents

Спасибо за интерес к проекту. Это коллекция SKILL.md для DeepSeek TUI, сконвертированная из Codex subagents и расширенная контрактами, бенчмарками и композицией.

## Как добавить новый скилл

### Если это doer-агент (пишет код)

```bash
# 1. Конвертируй из .toml (если есть источник)
python scripts/codex2deepseek.py awesome-codex-subagents/categories/NN-category/agent-name.toml --mode skill

# 2. Или создай вручную
mkdir -p skills/NN-category/agent-name/
```

Обязательные файлы:
- `SKILL.md` — фронтматер (name, description) + тело (working mode, focus, quality checks, return, do not)
- `contract.yaml` — produces / consumes / depends / parallel_compatible
- `benchmark.yaml` — минимум 1 тестовый промпт с expected и eval

### Если это reviewer-агент (читает код)

```bash
python scripts/codex2deepseek.py awesome-codex-subagents/categories/NN-category/agent-name.toml --mode spawn
```

Файл создаётся в `spawn-templates/NN-category/agent-name.json`

## Требования к качеству

### SKILL.md
- `description` должен быть конкретным и пригодным для авто-триггеринга
- Body должен содержать все 5 секций: Working mode, Focus on, Quality checks, Return, Do not
- Максимум 500 строк (progressive disclosure — длинные части в `references/`)

### contract.yaml
- `produces.type` — один из: change-set, finding[], report, analysis, plan
- `parallel_compatible` — список имён скиллов, с которыми можно параллелить
- `conflicts_with` — список имён скиллов, с которыми НЕЛЬЗЯ запускать одновременно

### benchmark.yaml
- Каждый тест: `id`, `prompt`, `expected.checks`, `eval.method`
- method: `llm-as-judge` или `grep`
- Минимум 1 тест на скилл

## Процесс PR

1. Добавил/изменил SKILL.md, contract.yaml, benchmark.yaml
2. Запусти `python scripts/validate_skills.py` — все проверки должны пройти
3. Для нового скилла — добавил запись в индекс категории `skills/NN-category/SKILL.md`
4. PR с описанием мотивации и примером использования

## Стиль

- Документация на русском (фронтматер — на английском для триггеринга)
- Инструкции — конкретные, task-shaped, без маркетинга
- Return contract — обязателен. Агент должен знать, что именно он возвращает
