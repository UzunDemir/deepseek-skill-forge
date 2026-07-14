---
name: deepseek-subagents
description: >
  Library of 172+ specialized DeepSeek TUI skills converted from Codex subagents.
  Use when the task matches one of the 13 categories: core development,
  language specialists, infrastructure, quality & security, data & AI,
  developer experience, specialized domains, business & product,
  meta & orchestration, research & analysis, AI governance & safety,
  platform engineering & IDP, or LLMOps & evals & observability.
  Each skill provides structured instructions with working mode, focus areas,
  quality checks, and a return contract.
---

# DeepSeek Subagents

Библиотека специализированных инструкций для DeepSeek TUI. Конвертировано из [Awesome Codex Subagents](https://github.com/VoltAgent/awesome-codex-subagents).

## Как использовать

DeepSeek TUI сам загружает подходящий скилл по описанию в фронтматере.
Для явной загрузки используй `skill <name>`.
Для спавна sub-agent'ов используй шаблоны из `spawn-templates/`.

## Структура

```
skills/                     # SKILL.md — загружаются в мой контекст
  01-core-development/      #   doer-агенты (пишут код)
  02-language-specialists/  #   языковые эксперты
  ...

spawn-templates/            # JSON-шаблоны для agent_spawn
  04-quality-security/      #   reviewer-агенты (читают код)
  ...

orchestration-presets/      # YAML-воркфлоу композиции
```

## Категории

| Категория | Агентов | Тип |
|---|---|---|
| 01 Core Development | 13 | doer |
| 02 Language Specialists | 31 | doer |
| 03 Infrastructure | 16 | doer |
| 04 Quality & Security | 19 | mixed |
| 05 Data & AI | 13 | doer |
| 06 Developer Experience | 15 | doer |
| 07 Specialized Domains | 14 | doer |
| 08 Business & Product | 16 | doer |
| 09 Meta & Orchestration | 11 | mixed |
| 10 Research & Analysis | 12 | reviewer |
| 11 AI Governance & Safety | 4 | reviewer |
| 12 Platform Engineering & IDP | 4 | doer |
| 13 LLMOps & Evals & Observability | 4 | reviewer |
