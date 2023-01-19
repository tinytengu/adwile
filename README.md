# adwile_test

Тестовое задание Adwile ([ТЗ](https://gist.github.com/eremeevdev/2fedea34c40a366d3eb92dbfdbb72500))

## Установка и запуск

> Процесс установки может быть абсолютно разный, хоть через Docker контейнеры, хоть вручную, я приведу самый простой пример Develop окружения.

0. Клонировать репозиторий

1. Инициализировать и активировать виртуальное окружение Python (pipenv, poetry, etc.)

```bash
python3 -m venv .venv
source ./.venv/scripts/activate
```

2. Установить зависимости проекта

```bash
pip install -r requirements.txt
```

3. Инициализировать БД

```bash
python manage.py makemigrations
python manage.py migrate
```

4. (Опционально) Создать аккаунт суперпользователя

```bash
python manage.py createsuperuser
```

5. Запустить Development сервер

```bash
python manage.py runserver
```

6. Готово, сервер запущен на [`http://localhost:8000/`](http://localhost:8000/)

## (Bonus) Действия при оплате/отклонении тизера

Произведение каких-либо операций при изменении статуса тизера (оплате или отклонении), можно реализовать либо оверрайдом методов модели, либо сигналами, я покажу на сигналах:

```python
from django.db.models.signals import post_save

from teasers.models import Teaser


def status_changed_callback(signal, sender, instance: Teaser, *args, **kwargs):
    if instance.status == Teaser.Status.PAID:
        print(f"The teaser '{instance}' was paid for")
    if instance.status == Teaser.Status.REJECTED:
        print(f"The teaser '{instance}' was rejected")


post_save.connect(status_changed_callback, sender=Teaser)
```
