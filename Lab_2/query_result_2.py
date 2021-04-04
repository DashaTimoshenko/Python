import psycopg2
from config import Config

conn = psycopg2.connect(
    host=Config.host,
    database=Config.database,
    user=Config.user,
    password=Config.password)

cur = conn.cursor()
sql = """COPY (select test_tb.histPTRegName, 
       max(case when test_tb.zno_year = 2019 then test_tb.histBall100 end) as zno_2019,
       max(case when test_tb.zno_year = 2020 then test_tb.histBall100 end) as zno_2020
       from test_tb 
       where test_tb.histTestStatus = 'Зараховано'
       group by test_tb.histPTRegName) TO STDOUT WITH CSV HEADER DELIMITER ';'"""
with open("query_res_2.csv", "w") as file:  # Файл з результатами виконання запиту
    cur.copy_expert(sql, file)
    cur.close()
conn.close()