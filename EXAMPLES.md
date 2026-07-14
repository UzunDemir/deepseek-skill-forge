# Примеры использования DeepSeek Subagents

## Пример 1: Починка бага с backend-developer скиллом

**Запрос пользователя:**

> `POST /api/v2/payments/retry` падает с 500 в проде. Почини.

**Что происходит под капотом:**

1. DeepSeek TUI видит "backend баг" — триггерится `backend-developer` скилл
2. Я загружаю SKILL.md, следую working mode:

```
Working mode:
1. Map entry point, domain logic boundary, persistence side effects
2. Implement smallest coherent change
3. Validate under normal and failure paths
```

3. Я нахожу endpoint → трассирую до retry handler → вижу: нет проверки статуса платежа перед retry
4. Патчу, валидирую, возвращаю структурированный ответ

**Ответ (по return contract скилла):**

```
Files changed:
  billing/api/v2/payments.py (+8/-3)
  billing/domain/payment_retry.py (+15/-2)

Behavior change:
  Added state validation — retry only for 'pending' or 'failed' payments
  Now returns 409 Conflict for 'processing' instead of 500

Validation performed:
  Success: payment in 'failed' → retry accepted
  Failure: payment in 'processing' → 409
  Rollback: existing happy path unchanged

Residual risk:
  Idempotency key not validated — second retry creates duplicate
```

---

## Пример 2: PR review с параллельными sub-agent'ами

**Запрос пользователя:**

> Проверь мой PR перед мержем. Ветка `fix/payment-timeout`.

**Что происходит:**

1. DeepSeek TUI загружает `orchestration-presets/pr-review-chain.yaml`
2. Я спавню три sub-agent'а параллельно:

```
  agent_spawn(reviewer, scope="diff")
  agent_spawn(docs-researcher, question="API docs match?")
  agent_spawn(search-specialist, query="similar patterns")
```

3. Жду все три → синтезирую

**Ответ пользователю:**

```
## PR Review: fix/payment-timeout

### Findings (by severity)

🔴 Critical:
- security-auditor: missing auth check on /api/v2/admin/payments

🟡 High:
- reviewer: timeout not configurable — hardcoded 5s
- docs-researcher: OpenAPI spec outdated — missing retry error codes

🟢 Info:
- search-specialist: 3 similar retry handlers in billing-service

### Recommendation
Add auth middleware + make timeout configurable + update spec.
```

---

## Пример 3: Исследование новой кодовой базы

**Запрос пользователя:**

> Я новенький в проекте. Как устроены платежи?

**Что происходит:**

1. Триггерится orchestration-preset `repo-exploration.yaml`
2. Спавню search-specialist + code-mapper + docs-researcher параллельно
3. Loaded knowledge-synthesizer скилл для объединения

**Ответ:**

```
## Payment System Overview

### Entry Points
  billing/api/v2/ — 3 HTTP endpoints (create, retry, refund)

### Domain Layer
  billing/domain/ → state machine:
    initiated → pending → processing → completed
                                     ↘ failed → pending

### Infrastructure
  billing/infrastructure/ — Stripe client, idempotency store

### Owned By
  @payments-team, #billing-service Slack channel
```

---

## Пример 4: Установка и использование

```bash
# Установка одного скилла
cp -r skills/01-core-development/backend-developer ~/.deepseek/skills/

# Или целой категории
cp -r skills/04-quality-security ~/.deepseek/skills/

# Перезагрузка DeepSeek TUI
# Скиллы загружаются автоматически при старте
```

**Теперь при запросе "Почини баг в /api/v2/orders" — DeepSeek TUI автоматом загрузит backend-developer.**

---

## Пример 5: Вызов скилла явно

```
skill reviewer
```

Загружает инструкции reviewer в текущий контекст. После этого я делаю review всех изменений по возвратному контракту: scope → findings → recommendations → residual risk.

---

## Пример 6: Создание нового скилла из .toml

```bash
# Конвертация
python scripts/codex2deepseek.py \
  awesome-codex-subagents/categories/06-developer-experience/cli-developer.toml

# Результат:
#   skills/06-developer-experience/cli-developer/SKILL.md
#   skills/06-developer-experience/cli-developer/contract.yaml
#   skills/06-developer-experience/cli-developer/benchmark.yaml
```

---

## Пример 7: Полный workflow баг-фикса

```
1. user:  "POST /orders падает"
2. Apply backend-developer → трассирую, нахожу deadlock в транзакции
3. Пишу фикс
4. spawn security-auditor → проверяет, что фикс не открывает новые уязвимости
5. Синтезирую ответ с residual risk
```
