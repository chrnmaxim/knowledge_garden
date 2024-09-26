---
title: Poetry
draft: false
tags:
---
### Установка и конфигурация Poetry

1. Установить [pipx](https://pipx.pypa.io/stable/installation/):

```bash
python -m pip install --user pipx
```

2. Добавить pipx в`PATH`:

```bash
python -m pipx ensurepath
```

> [!Note]
> Вам нужно будет открыть новый терминал, чтобы изменения PATH вступили в силу.

3. Установить [poetry](https://python-poetry.org/docs/#installation):

```bash
pipx install poetry
```

4. Установить значение параметра `virtualenvs.in-project` как `true` для того, чтобы виртуальное окружение `.venv` могло быть создано в директории проекта:

```bash
poetry config virtualenvs.in-project true
```

5.  Инициализируйте проект:

```bash
poetry init
```

6. Добавьте необходимые зависимости:
```bash
poetry add <dependency>
```

### Полезные ссылки
* [Документация Poetry](https://python-poetry.org/)
* [Миграция зависимостей проекта с `pip` в `poetry`](https://gist.github.com/chrnmaxim/4f0cc4dcf41b2b69cf68f0bc2b4abbff)
----
📂 [[Python]]

Последнее изменение: 26.09.2024 09:14