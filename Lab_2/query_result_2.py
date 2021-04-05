import psycopg2
from config import Config

conn = psycopg2.connect(
    host=Config.host,
    database=Config.database,
    user=Config.user,
    password=Config.password)

cur = conn.cursor()
sql = """COPY (select eo_view.region_name, 
       max(case when passing_exam.zno_year = 2019 then passing_exam.Ball100 end) as zno_2019,
       max(case when passing_exam.zno_year = 2020 then passing_exam.Ball100 end) as zno_2020
       from passing_exam
	   join eo_view on (passing_exam.institution_id = eo_view.institution_id)
	   join subjects on (passing_exam.subject_id = subjects.subject_id)
       where passing_exam.test_status = 'Зараховано' and
	   subjects.subject_name = 'Історія України'
	   group by eo_view.region_name) TO STDOUT WITH CSV HEADER DELIMITER ';'"""
with open("query_res_2.csv", "w") as file:  # Файл з результатами виконання запиту
    cur.copy_expert(sql, file)
    cur.close()
conn.close()
