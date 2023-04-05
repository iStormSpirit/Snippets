## О проекте
Проект Snippets - суть проекта заключается в том, что бы пользователи могли делиться частью своего кода с другими пользователями, а так же комментировать (с возможность прикреплять картинки) чужие сообщения.

## Развертывание проекта

1. Создать venv: python3 -m venv snippets_venv
2. Активировать: source snippets_venv/bin/activate
3. Установить зависимости: pip install -r requirements.txt
4. Применить миграции: python manage.py migrate
5. Запустить проект: python manage.py runserver

run django-extensions console: 
`python manage.py shell_plus --ipython`
