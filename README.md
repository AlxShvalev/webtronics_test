# Webtronics social

## Описание
Тестовое задание на позицию Python-developer в компанию Webtronics

Проект представляет собой простой REST API сервис для социальной сети

Сервис позволяет:
- Зарегистрироваться новому пользователю
- Зарегистрированный пользователь может аутентифицироваться
с использованием username и password
- Зарегистрированный пользователь может создавать, редактировать, удалять свои Посты
- Зарегистрированный пользователь может ставить лайки постам других пользователей (но не своим)
---
## Технологии
![Python](https://img.shields.io/badge/python_3.11-3670A0?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-005571?style=for-the-badge)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
---
## Установка
Клонировать репозиторий
```bash
git clone https://github.com/AlxShvalev/webtronics_test.git
cd webtronics_test
```
Отредактировать файл `.env.example`, задав необходимые переменные окружения.
Переименовать файл в `.env`
---
## Запуск
В директории с проектом выполнить
```bash
docker build .
```
