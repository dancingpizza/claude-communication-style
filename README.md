# Claude Communication Style

Скилл для ответов на русском. В разговоре помогает отвечать коротко, в сложных вопросах объяснять причины, а при правке текста сохранять разницу между «сможем сделать» и «сделаем».

Скилл не зависит от рабочего проекта. После установки ему не нужны сеть, Python и отдельные скиллы.

## Установка

Через `npx skills` (нужен Node.js 22.20 или новее). Для OpenCode во всех проектах:

```sh
npx skills add dancingpizza/claude-communication-style -a opencode -g
```

Чтобы установить только в текущий проект, запустите команду из его корня без `-g`. Для другого агента замените `opencode` или уберите `-a opencode`, чтобы выбрать агента при установке.

Начните новую сессию. Если агент не выбрал скилл сам, попросите применить `claude-communication-style`.

## Обновление

Для глобальной установки через `npx skills`:

```sh
npx skills update claude-communication-style -g
```

Для установки в проекте выполните `npx skills update claude-communication-style -p` из корня проекта. Обновляется только этот скилл.

## Установка вручную

```sh
git clone https://github.com/dancingpizza/claude-communication-style.git
```

Скопируйте папку `skills/claude-communication-style/` в каталог скиллов своего агента. Для OpenCode это, например, `~/.config/opencode/skills/`. Для обновления скачайте свежую версию и замените установленную копию.

## Материалы

- [Правила для агента](skills/claude-communication-style/SKILL.md)
- [Примеры на русском](skills/claude-communication-style/references/examples.md)
- [Источники и лицензии сторонних материалов](dev/sources.md)

Установщик берёт рабочий пакет из `skills/claude-communication-style/`. Наборы для проверки ответов лежат в [`evals/`](evals/), материалы для сопровождения сторонних компонентов в [`dev/vendor/`](dev/vendor/), а проверка комплекта в [`scripts/`](scripts/).

Из корня репозитория запустите `python3 scripts/check_bundle.py`, чтобы проверить состав пакета, ссылки и контрольные суммы. Python нужен для этой проверки и двух необязательных скриптов Humanizer.
