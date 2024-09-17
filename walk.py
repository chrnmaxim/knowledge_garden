"""
Рекурсивно сканирует директорию с контентом, и составляет оглавление
в файле index.md.
"""

import datetime
import os

CONTENT_PATH = "./content"

class Note:
    def __init__(self, title: str, updated_at: datetime.datetime) -> None:
        self.title = title
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"{self.title}, {self.updated_at}"


def get_file_times(path: str) -> tuple[datetime.datetime, datetime.datetime]:
    """
    Возвращает tuple из времени создания и времени изменения файла.
    - `path`: полный путь до файла.
    """

    # file creation timestamp in float
    c_time = os.path.getctime(path)
    # convert creation timestamp into DateTime object
    dt_c = datetime.datetime.fromtimestamp(c_time)

    # file modification timestamp of a file
    m_time = os.path.getmtime(path)
    # convert timestamp into DateTime object
    dt_m = datetime.datetime.fromtimestamp(m_time)

    return dt_c, dt_m


exclude_folders = [
    "attachments",
    "content",
]

toc_dirs = ""
toc_full = ""
notes: list[Note] = []

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(CONTENT_PATH):
    path = root.split(os.sep)
    folder = os.path.basename(root)

    if folder in exclude_folders:
        continue

    file_tabs = len(path) - 2
    folder_tabs = file_tabs - 1

    line = folder_tabs * "\t" + f"- 📂 [[{folder}]]<br>\n"
    toc_dirs += line
    toc_full += line

    for file in files:
        if file.endswith("md"):
            title = file[:-3]
            toc_full += file_tabs * "\t" + f"- 📄 [[{title}]]<br>\n"

            # # Добавим ссылку на директорию в конце каждой заметки
            # full_path = os.path.join(root, file)
            # dt_c, dt_m = get_file_times(full_path)
            # notes.append(Note(title=title, updated_at=dt_m))
            # with open(file=full_path, mode="a", encoding="utf-8") as note:
            #     note.write(f"\n\n----\n📂 [[{folder}]] | Последнее изменение: {dt_m.strftime(format="%d.%m.%Y %H:%M")}")

# Получить список 10 последних обновленных заметок
notes.sort(key=lambda x: x.updated_at, reverse=True)
last_updated_notes = ""
for note in notes[:10]:
    last_updated_notes += f"- [[{note.title}]]\n"

index_md = f"""
---
title: Главная
---
Сборник [моих](https://github.com/chrnmaxim) заметок по Backend разработке.

Заметки, в основном, предназначены для личного пользования и обмена информацией c коллегами.

Идея создания собственного [цифрового сада](https://jzhao.xyz/posts/networked-thought)
вдохновлена [Hazadus](https://github.com/hazadus).

----

### Недавно обновлённые заметки

{last_updated_notes}

----

## Краткое оглавление
{toc_dirs}

## Полное оглавление
{toc_full}
"""

print(index_md)
with open(file=f"{CONTENT_PATH}/index.md", mode="w", encoding="utf-8") as file:
    file.write(index_md)