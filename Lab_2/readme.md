1.	Завантажити всі файли з репозиторію, перейти у створену директорію.
2.	Додати в папку цього репозиторія csv-файли з даними по ЗНО за 2019 та 2020 роки (https://zno.testportal.com.ua/opendata).
3.	Запустити файл lab_1.py. За потреби, змінити в файлі config.py значення змінних host, database, user, password
4.	Запустити flyway для міграції таблиці. За потреби, змінити в файлі  flyway.conf
    ˗	flyway.url=jdbc:postgresql://localhost:5432/postgres
    ˗	flyway.user = postgres
    ˗	flyway.password = postgres
5.	Запустити програму query_lab2.py. Вона виконує аналогічний до лабораторної 1 запит, але працює з базою даних у третій нормальній формі . Результат запиту буде записаний у файл query_res_2.csv.
