## 🪴 Digital Garden

Cтатичный сайт-сборник заметок по Backend разработке.
Собирается с помощью [Quartz](https://quartz.jzhao.xyz/) из заметок в [Obsidian](https://obsidian.md/).

### Локальные доработки
* Добавление даты изменения заметки только для новых или измененных заметок.
* Использование `Makefile` для запуска команд подготовки заметок, сборки и развертывания проекта.

Для использования указанных доработок необходимо использовать [Poetry](https://python-poetry.org/):
1. Склонируйте проект:
```bash
git clone git@github.com:chrnmaxim/knowledge.git
```
2. Установите значение параметра `virtualenvs.in-project` как `true` для того, чтобы виртуальное окружение `.venv` могло быть создано в директории проекта:
```bash
poetry config virtualenvs.in-project true
```
3. В корневой директории проекта выполните команду:
```bash
poetry install
```

### About Quartz
> “[One] who works with the door open gets all kinds of interruptions, but [they] also occasionally gets clues as to what the world is and what might be important.” — Richard Hamming

Quartz is a set of tools that helps you publish your [digital garden](https://jzhao.xyz/posts/networked-thought) and notes as a website for free.
Quartz v4 features a from-the-ground rewrite focusing on end-user extensibility and ease-of-use.

🔗 Read the documentation and get started: https://quartz.jzhao.xyz/
