<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/DeepSeek-Subagents-4F46E5?style=for-the-badge&logo=deepseek&logoColor=white&labelColor=1E1B4B">
    <img alt="DeepSeek Subagents" src="https://img.shields.io/badge/DeepSeek-Subagents-4F46E5?style=for-the-badge&logo=deepseek&logoColor=white&labelColor=1E1B4B">
  </picture>
</div>

<div align="center">

### 172 специализированных AI-агента для DeepSeek TUI

[![Skills](https://img.shields.io/badge/skills-74-22C55E?style=flat-square)](skills/)
[![Spawn Templates](https://img.shields.io/badge/spawn_templates-98-3B82F6?style=flat-square)](spawn-templates/)
[![Categories](https://img.shields.io/badge/categories-13-A855F7?style=flat-square)](#-категории)
[![License](https://img.shields.io/badge/license-MIT-F59E0B?style=flat-square)](LICENSE)
[![Validation](https://img.shields.io/badge/validation-passing-22C55E?style=flat-square)](#-валидация)

</div>

---

**DeepSeek Subagents** — это библиотека готовых инструкций для DeepSeek TUI, конвертированная из [Awesome Codex Subagents](https://github.com/VoltAgent/awesome-codex-subagents) и расширенная **контрактами**, **бенчмарками** и **композиционными воркфлоу**.

Каждый агент — не Т9К промпт, а инженерная спецификация: рабочая модель, фокусы, quality checks, возвратный контракт и границы ответственности.

---

## 🔥 Как это работает

<div align="center">

```
┌─ Ты пишешь ─────────────────────────────────────────────┐
│  "Почини POST /api/v2/payments/retry — падает с 500"    │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─ DeepSeek TUI ──────────────────────────────────────────┐
│  Авто-триггер: запрос совпал с описанием backend-       │
│  developer — скилл загружен в контекст                  │
├─────────────────────────────────────────────────────────┤
│  1. Map entry point, domain logic, persistence           │
│  2. Implement smallest coherent change                   │
│  3. Validate success + failure paths                    │
│  4. Return: files, behavior change, residual risk       │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─ Ответ ─────────────────────────────────────────────────┐
│  Files:        billing/api/v2/payments.py (+8/-3)       │
│  Behavior:     добавил проверку статуса перед retry     │
│  Validation:   success (failed → retry),                │
│                failure (processing → 409)               │
│  Residual:     idempotency key не проверяется           │
└──────────────────────────────────────────────────────────┘
```

</div>

**Без скилла:** ответ "починил, тесты прошли".
**Со скиллом:** структурированный FAANG-ревью с residual risk.

---

## 📦 Установка

```bash
# Копируй скиллы в ~/.deepseek/skills/
cp -r skills/* ~/.deepseek/skills/

# DeepSeek TUI сам найдёт их при следующем запуске
```

Готово. Теперь каждый твой запрос автоматически получает нужную специализацию.

---

## 🗂️ Категории

<table>
<tr>
<th width="50">#</th>
<th width="250">Категория</th>
<th width="80">Агентов</th>
<th>Описание</th>
</tr>

<tr>
<td align="center">01</td>
<td><b>Core Development</b></td>
<td align="center">13</td>
<td>Backend, frontend, API, fullstack, mobile, WebSocket</td>
</tr>

<tr>
<td align="center">02</td>
<td><b>Language Specialists</b></td>
<td align="center">31</td>
<td>Python, Rust, Go, Java, TS, C++, и ещё 26 языков</td>
</tr>

<tr>
<td align="center">03</td>
<td><b>Infrastructure</b></td>
<td align="center">16</td>
<td>K8s, Terraform, Docker, CI/CD, SRE, networking</td>
</tr>

<tr>
<td align="center">04</td>
<td><b>Quality & Security</b></td>
<td align="center">19</td>
<td>Code review, security audit, pentest, QA, compliance</td>
</tr>

<tr>
<td align="center">05</td>
<td><b>Data & AI</b></td>
<td align="center">13</td>
<td>ETL, ML, LLM, NLP, MLOps, prompt engineering</td>
</tr>

<tr>
<td align="center">06</td>
<td><b>Developer Experience</b></td>
<td align="center">15</td>
<td>CLI, docs, DX, refactoring, build engineering</td>
</tr>

<tr>
<td align="center">07</td>
<td><b>Specialized Domains</b></td>
<td align="center">14</td>
<td>Fintech, blockchain, IoT, gaming, healthcare</td>
</tr>

<tr>
<td align="center">08</td>
<td><b>Business & Product</b></td>
<td align="center">16</td>
<td>PM, BA, marketing, legal, UX research</td>
</tr>

<tr>
<td align="center">09</td>
<td><b>Meta & Orchestration</b></td>
<td align="center">11</td>
<td>Multi-agent coordination, workflow automation</td>
</tr>

<tr>
<td align="center">10</td>
<td><b>Research & Analysis</b></td>
<td align="center">12</td>
<td>Search, competitive analysis, market research</td>
</tr>

<tr>
<td align="center">11</td>
<td><b>AI Governance & Safety</b></td>
<td align="center">4</td>
<td>Guardrails, model risk, responsible AI</td>
</tr>

<tr>
<td align="center">12</td>
<td><b>Platform Engineering & IDP</b></td>
<td align="center">4</td>
<td>Backstage, golden paths, IDP architecture</td>
</tr>

<tr>
<td align="center">13</td>
<td><b>LLMOps & Observability</b></td>
<td align="center">4</td>
<td>Evals, hallucination investigation, observability</td>
</tr>

</table>

---

## 🧠 Архитектура

Проект использует **два механизма** вместо одного — это ключевое улучшение против Codex-оригинала:

```
skills/                     # SKILL.md — инструкции для ГЛАВНОГО АГЕНТА
├── 01-core-development/    #   backend-developer, frontend-developer...
├── 02-language-specialists/#   python-pro, rust-engineer...
└── ...                     #   74 doer-агента

spawn-templates/            # JSON — шаблоны для agent_spawn (sub-agent)
├── 04-quality-security/    #   reviewer, security-auditor...
├── 10-research-analysis/   #   docs-researcher, search-specialist...
└── ...                     #   98 reviewer-агентов

orchestration-presets/      # YAML — готовые композиционные workflow
└── pr-review-chain.yaml    #   параллельный PR review
└── bug-investigation.yaml  #   трассировка + дебаг + фикс
└── feature-implementation.yaml
└── repo-exploration.yaml
```

### Почему это сильнее Codex?

| Фича | Codex | DeepSeek Subagents |
|---|---|---|
| Формат | `.toml` | `SKILL.md` + `contract.yaml` + `benchmark.yaml` |
| Doer-агенты | Sub-agent (чёрный ящик) | Skill (инструкции для главного агента) |
| Reviewer-агенты | Sub-agent | Spawn template (параллельный `agent_spawn`) |
| Композиция | Вручную в промпте | orchestration-presets + contract.yaml |
| Валидация | Отсутствует | `validate_skills.py` — CI-ready |
| Модель | Привязана к GPT | Единая модель DeepSeek |
| Авто-триггеринг | Нет (явный вызов) | Через frontmatter `description` |

---

## 🚀 Примеры

### PR review за 5 секунд

```text
# Просто попроси — скилл сам загрузится:
Проверь мой PR перед мержем.

# DeepSeek TUI загружает pr-review-chain.yaml:
# → reviewer     (параллельно)
# → docs-researcher
# → search-specialist
# → синтез с конфликт-резолюцией
```

### Баг-фикс со structured output

```text
POST /api/v2/payments/retry падает с 500 в проде.

→ Авто-триггер backend-developer
→ Ответ возвращается по контракту: files + behavior + validation + residual risk
```

### Исследование чужого кода

```text
Я новенький. Как устроены платежи?

→ repo-exploration.yaml
→ search-specialist + code-mapper + docs-researcher (параллельно)
→ knowledge-synthesizer → карта системы
```

Подробнее в [EXAMPLES.md](EXAMPLES.md).

---

## 🛠️ Разработчикам

### Конвертация нового агента из .toml

```bash
python scripts/codex2deepseek.py source.toml
# → skills/<category>/<name>/SKILL.md
# → skills/<category>/<name>/contract.yaml
# → skills/<category>/<name>/benchmark.yaml
```

### Валидация

```bash
python scripts/validate_skills.py
# → 172 проверены, 0 ошибок
```

---

## 📄 Лицензия

MIT. См. [LICENSE](LICENSE).

---

<div align="center">

**Сделано с ❤️ для DeepSeek TUI сообщества**

[Вопросы и предложения](https://github.com/your-repo/issues) — открывайте issue

</div>
