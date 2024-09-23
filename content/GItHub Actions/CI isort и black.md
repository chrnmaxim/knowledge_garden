---
title: CI isort и black
draft: false
tags:
  - CI
---
### GitHub workflow для проверки форматирования isort и black

Данный workflow будет запускаться при каждом пуше в созданный Pull Request с base `develop`.

```GitHub
name: Push in PR into develop branch. Linter and Backend tests.

on:
  pull_request:
    branches:
      - develop
jobs:
  linter:
    name: Backend Linter and Isort check
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.11
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install black isort
  
      - name: Isort and Black check
        run: |
          cd backend/
          isort --check .
          black --check .
```
----
📂 [[GitHub Actions]]

Последнее изменение: 23.09.2024 15:16