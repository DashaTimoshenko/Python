Посилання на heroku http://db-lab-3.herokuapp.com/warehouse_crud

Лабораторна робота №3
Інструкція по розгортанню:

Завантажити всі файли з репозиторію, перейти у створену директорію, ініціалізувати git-репозиторій Увійти в Heroku-акаунт (через heroku login). Додати зміни, закомітити та задеплоїти (git add .; git commit -am "some message"; git push heroku master)

Організація CRUD-операцій:

    CREATE –  створення нового складу, контейнеру, продукту та записів про зберігання цього продукту.

    READ – перегляд вмісту таблиць.

    UPDATE –оновлення інформації про кількість товару в певному контейнері(таблиця Storage)

    DELETE –  видалення складу, контейнеру, продукту та записів про зберігання цього продукту

Слої:

    •	database layer -- БД Postresql.

    •	persistence layer -- файл models.py

    •	business layer -- файли app.py, query.py.

    •	presentation layer -- html-файли.
