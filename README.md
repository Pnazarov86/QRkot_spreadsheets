# Cервис QRKot.

### Описание
Проект QRKot — Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

### Технологии
 - Python 3.9
 - FastApi 0.78
 - Alembic 1.7
 - SQLAlchemy 1.4
____
### Запуск проекта на Linux:
Клонируйте репозиторий.
Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
### Запуск проекта
Выполните команду
```
uvicorn app.main:app --reload 
```
Проект доступен по ссылке
```
http://127.0.0.1:8000/
```
Документация к проекту
```
http://127.0.0.1:8000/docs#/
```

____
### Автор  
Пётр Назаров  
https://github.com/Pnazarov86
