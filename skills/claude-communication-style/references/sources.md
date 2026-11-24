# Происхождение, лицензии и правки

Копии собраны 24 ноября 2026 года. Ссылки ниже нужны только для проверки
происхождения. Для работы скилла сеть не нужна.

## Вложенные скиллы

| Копия | Источник | Коммит | Лицензия |
| --- | --- | --- | --- |
| Не включён | [poulvinay/clear-explain](https://github.com/poulvinay/clear-explain) | `53467f390d9c8af53713968dfffb1c39103b5a28` | В репозитории не указана |
| [vendor/humanizer/](../vendor/humanizer/) | [codxt/humanizer](https://github.com/codxt/humanizer) | `f4b448cb91e9f20ff4e0feab172c672851b63eee` | MIT, [LICENSE](../vendor/humanizer/LICENSE), [THIRD_PARTY_NOTICES.md](../vendor/humanizer/THIRD_PARTY_NOTICES.md) |
| [vendor/plain-language/](../vendor/plain-language/) | [arjunprabhulal/agent-skills, skills/docs/plain-language](https://github.com/arjunprabhulal/agent-skills/tree/main/skills/docs/plain-language) | `42dd24080fce6d731d00e2a1134f398c3da4171b` | MIT, [LICENSE](../vendor/plain-language/LICENSE) из корня репозитория |
| [vendor/talk-skill/](../vendor/talk-skill/) | [DeadAlmighty/talk-skill](https://github.com/DeadAlmighty/talk-skill) | `e48e4773422875f51868cf53a5172c38642fddc2` | MIT, [LICENSE](../vendor/talk-skill/LICENSE) |
| [vendor/response-style/](../vendor/response-style/) | [gabrielmongefranco/repo-template, skills/response-style](https://github.com/gabrielmongefranco/repo-template/tree/main/skills/response-style) | `59dd405563f0ea975f34c2964debbc6b0215d251` | Текст скилла под GFDL 1.3 или новее ([FDL-1.3.txt](../vendor/response-style/FDL-1.3.txt)), код репозитория под GPL-3.0 ([LICENSE](../vendor/response-style/LICENSE), [NOTICE](../vendor/response-style/NOTICE)) |

У Clear Explain не указана лицензия, поэтому оригинал не распространяется с этим
скиллом. Правила объяснения и примеры по-русски есть в локальных материалах.

## Что скопировано

В пакете сохранены рабочие инструкции Talk Skill, Plain Language и Humanizer,
справочники Humanizer и два скрипта для проверки текста. Краткие правила
Response Style собраны в [решениях](decisions.md). Полный исходный текст,
заметки, тесты и служебные файлы сторонних проектов хранятся в исходном
репозитории этого скилла, в `dev/vendor/` и `evals/`.

Вложенные инструкции называются `SKILL.upstream.md`, чтобы загрузчики находили
один скилл. Лицензии и уведомления лежат рядом с соответствующими материалами.
Контрольные суммы пакета хранятся в исходном репозитории в `scripts/vendor.sha256`.

## Ориентиры по тону

- [Claude Opus 5.5 system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-opus-5-5),
  версия от 9 ноября 2026 года, разделы `tone_and_formatting` и `lists_and_bullets`.
- [Claude Sonnet 5.5 system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-5-5),
  те же разделы.

Из них взяты тёплый тон без негативных предположений о собеседнике, минимум оформления,
проза в разговоре и объяснениях, пункты списка в одно-два предложения, не больше одного
вопроса за ответ, правка только того, что просили поменять, и запрет на мат, если
собеседник сам не ругается. Разница между версиями такая: Opus строже к спискам в
объяснениях, Sonnet допускает их для многосоставного содержания. Компромисс описан в
[decisions.md](decisions.md), раздел 3.

## Правила оформления скиллов

- [Agent Skills specification](https://agentskills.io/specification): поля `name`,
  `description`, `license`, `compatibility`, `metadata`, совпадение имени с каталогом,
  лимит в 500 строк для `SKILL.md`, ссылки на один уровень вглубь.
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
  описание в третьем лице с условиями применения, оглавление в длинных справочниках,
  проверка на реальных запросах и на всех целевых моделях. В этом же документе сказано,
  что Claude API и claude.ai не принимают слово `claude` в поле `name`. Имя
  `claude-communication-style` выбрано по заданию и подходит для файловых загрузчиков
  (Claude Code, OpenCode, Codex). Для загрузки через API или claude.ai скилл придётся
  переименовать, например в `natural-russian-style`, вместе с каталогом.
