<div align="center">
    <h1>
        <b>API Avito Shop</b>
    </h1>
    <h3>
        Сервис покупки мерча сотрудниками Авито
    </h3>
    <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/alex6712/sos-course-work?logo=GitHub">
    <img alt="Tests Passed" src="https://github.com/alex6712/sos-course-work/actions/workflows/backend-tests.yml/badge.svg">
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</div>

Курсовая работа по предмету Сервис-ориентированные системы студента Ванюкова Алексея Игоревича, ИРИТ, НГТУ, 21-ИС.

## Запуск решения

Корневая папка сервиса ``backend/avito_shop``.

### Установка зависимостей

В корневой папке находятся файлы ``poetry.lock`` и ``pyproject.toml``, которые используются **Poetry** для менеджмента 
зависимостей, необходимых для работы сервиса.

Чтобы их установить используйте следующую команду:

```powershell
cd backend/avito_shop
poetry install
```

Также в той папке находятся файл ``requirements.txt``,
поэтому также присутствует возможность установки зависимостей с помощью **pip**:

```powershell
pip install -r requirements.txt
```

### Запуск скрипта

Сервер запускается с помощью скрипта ``start.py`` в корневой папке проекта.

Чтобы запустить скрипт, используйте команду

```powershell
py start.py
```

находясь в корневой папке проекта.

Если зависимости были установлены с помощью poetry, и виртуальное окружение не было
активировано, то используйте следующий алгоритм:

1. Откройте **PowerShell** в корневой папке проекта с правами администратора.
2. Исполните команды
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   Invoke-Expression (poetry env activate)
   ```

Таким образом вы активируете виртуальное окружение проекта со всеми необходимыми зависимостями.

## Задача

С полным текстом задачи можно ознакомиться [здесь](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/Backend/Backend-trainee-assignment-winter-2025/Backend-trainee-assignment-winter-2025.md).

Необходимо было реализовать API, позволяющий выполнять следующие действия:
- перевод монет между сотрудниками;
- покупка сотрудником мерча за монеты;
- просмотр истории покупок;
- просмотр личного счёта с выводом текущей суммы и истории переводов.

В задачу также входила реализация авторизации с использованием JWT.

## Стек

Я использовал фреймворк **FastAPI** для создания API, а также фреймворк **SQLAlchemy**
для связи с базой данных.

База данных использует диалект **PostgreSQL** (версия *SQL 17*), для её менеджмента использовался **pgAdmin 4**.

## Лицензия

[MIT License](https://github.com/alex6712/gi-characters-analyzer/blob/master/LICENSE.md)

## Автор

Ванюков Алексей Игоревич, ИРИТ, НГТУ, группа 21-ИС.

* Telegram: [Eclipse6712](https://t.me/ecuripusu)
* ВКонтакте: [Ванюков Алексей](https://vk.com/zerolevelmath)
* Адрес электронной почты: alexeivanyukov@yandex.ru
