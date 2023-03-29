# Gitea-downloader

[![Actions Status](https://github.com/sergkim13/gitea_downloader/actions/workflows/project_ci.yml/badge.svg)](https://github.com/sergkim13/gitea_downloader/actions/workflows/project_ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/b07c26e3c7a206397066/maintainability)](https://codeclimate.com/github/sergkim13/gitea_downloader/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b07c26e3c7a206397066/test_coverage)](https://codeclimate.com/github/sergkim13/gitea_downloader/test_coverage)

## **Test assignment for Radium.**

### **Description**:
This script downloads in async mode files from given gitea repository, save it to temporary directory and count hash of each file.


### **Requirements**:
1. MacOS / Linux
2. [Poetry](https://python-poetry.org/)
3. `Make` utile

### **Install**:
1. Clone repository: https://github.com/sergkim13/gitea_downloader.git
2. Type: `make instal`

### **Usage**:
1. Type: `make start`

### **Tests**:
1. Type: `make test`
2. Type: `make test-cov` to see test coverage.

### **Linter**:
1. Type `make lint` to run WPS linter. Configuration source: https://gitea.radium.group/radium/project-configuration

### **Demo**:
[![asciicast](https://asciinema.org/a/nm5DRnkEim3bFATJfM34ATvPd.svg)](https://asciinema.org/a/nm5DRnkEim3bFATJfM34ATvPd)

### **Task description**
<details>
    <summary>Click to show</summary>
    
- Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку.
- После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
- Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
- Обязательно 100% покрытие тестами
- При выполнении в ChatGPT - обязательна переработка
</detail>