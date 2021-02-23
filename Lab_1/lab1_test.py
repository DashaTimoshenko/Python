import psycopg2
import time
import csv
from iter_file import IteratorFile

conn = psycopg2.connect(
    host="localhost",
    database="",
    user="",
    password="")

def time_test(func):
    """функція для вимірювання часу роботи завантаження даних у БД"""
    def f(a):
        t1 = time.time()
        func(a)
        t2 = time.time()
        print(str(t2 - t1) + ": " + func.__name__)

    return f


def create_table():
    command = (
        """
        DROP TABLE IF EXISTS test_tb;

        CREATE TABLE test_tb
        (
           OUTID               TEXT,
           Birth               integer,
           SEXTYPENAME         TEXT,
           REGNAME             TEXT,
           AREANAME            TEXT,
           TERNAME             TEXT,
           REGTYPENAME         TEXT,
           TerTypeName         TEXT,
           ClassProfileNAME    TEXT,
           ClassLangName       TEXT,
           EONAME              TEXT,
           EOTYPENAME          TEXT,
           EORegName           TEXT,
           EOAreaName          TEXT,
           EOTerName           TEXT,
           EOParent            TEXT,
           UkrTest             TEXT,
           UkrTestStatus       TEXT,
           UkrBall100          numeric(10,2),
           UkrBall12           integer,
           UkrBall             integer,
           UkrAdaptScale       integer,
           UkrPTName           TEXT,
           UkrPTRegName        TEXT,
           UkrPTAreaName       TEXT,
           UkrPTTerName        TEXT,
           histTest            TEXT,
           HistLang            TEXT,
           histTestStatus      TEXT,
           histBall100         numeric(10,2),
           histBall12          integer,
           histBall            integer,
           histPTName          TEXT,
           histPTRegName       TEXT,
           histPTAreaName      TEXT,
           histPTTerName       TEXT,
           mathTest            TEXT,
           mathLang            TEXT,
           mathTestStatus      TEXT,
           mathBall100         numeric(10,2),
           mathBall12          integer,
           mathBall            integer,
           mathPTName          TEXT,
           mathPTRegName       TEXT,
           mathPTAreaName      TEXT,
           mathPTTerName       TEXT,
           physTest            TEXT,
           physLang            TEXT,
           physTestStatus      TEXT,
           physBall100         numeric(10,2),
           physBall12          integer,
           physBall            integer,
           physPTName          TEXT,
           physPTRegName       TEXT,
           physPTAreaName      TEXT,
           physPTTerName       TEXT,
           chemTest            TEXT,
           chemLang            TEXT,
           chemTestStatus      TEXT,
           chemBall100         numeric(10,2),
           chemBall12          integer,
           chemBall            integer,
           chemPTName          TEXT,
           chemPTRegName       TEXT,
           chemPTAreaName      TEXT,
           chemPTTerName       TEXT,
           bioTest             TEXT,
           bioLang             TEXT,
           bioTestStatus       TEXT,
           bioBall100          numeric(10,2),
           bioBall12           integer,
           bioBall             integer,
           bioPTName           TEXT,
           bioPTRegName        TEXT,
           bioPTAreaName       TEXT,
           bioPTTerName        TEXT,
           geoTest             TEXT,
           geoLang             TEXT,
           geoTestStatus       TEXT,
           geoBall100          numeric(10,2),
           geoBall12           integer,
           geoBall             integer,
           geoPTName           TEXT,
           geoPTRegName        TEXT,
           geoPTAreaName       TEXT,
           geoPTTerName        TEXT,
           engTest             TEXT,
           engTestStatus       TEXT,
           engBall100          numeric(10,2),
           engBall12           integer,
           engDPALevel         TEXT,
           engBall             integer,
           engPTName           TEXT,
           engPTRegName        TEXT,
           engPTAreaName       TEXT,
           engPTTerName        TEXT,
           fraTest             TEXT,
           fraTestStatus       TEXT,
           fraBall100          numeric(10,2),
           fraBall12           integer,
           fraDPALevel         TEXT,
           fraBall             integer,
           fraPTName           TEXT,
           fraPTRegName        TEXT,
           fraPTAreaName       TEXT,
           fraPTTerName        TEXT,
           deuTest             TEXT,
           deuTestStatus       TEXT,
           deuBall100          numeric(10,2),
           deuBall12           integer,
           deuDPALevel         TEXT,
           deuBall             integer,
           deuPTName           TEXT,
           deuPTRegName        TEXT,
           deuPTAreaName       TEXT,
           deuPTTerName        TEXT,
           spaTest             TEXT,
           spaTestStatus       TEXT,
           spaBall100          numeric(10,2),
           spaBall12           integer,
           spaDPALevel         TEXT,
           spaBall             integer,
           spaPTName           TEXT,
           spaPTRegName        TEXT,
           spaPTAreaName       TEXT,
           spaPTTerName        TEXT,
           zno_year            integer
        )""")
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()


def Case(row, zno_year):
    """Формує рядки для файлового об'єкта"""
    for i in [18, 29, 39, 49, 59, 69, 79, 88, 98, 108, 118]:
        row[i] = row[i].replace(',', '.')
    str = ';'.join(row)
    return str + ';' + zno_year


@time_test
def import_data(file_name):
    """Функція, що зчитує дані з файлу та записує їх до таблиці"""
    cur = conn.cursor()

    with open(file_name) as f:
        spamreader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_ALL)
        zno_year = file_name[5:9]
        next(spamreader, None)
        fd = IteratorFile(Case(x, zno_year) for x in spamreader) # створення файлового об'єкта

        cur.copy_from(fd, 'test_tb', sep=';', null='null')
        conn.commit()
    cur.close()


def export_request():
    """Функція, що виконує запит та записує результати цього запиту у файл result.csv"""
    # Запит: порівняти найкращий бал з Історії України в кожному регіоні у 2020 та 2019 роках серед тих кому було зараховано тест
    cur = conn.cursor()
    sql = """COPY (select test_tb.histPTRegName, 
           max(case when test_tb.zno_year = 2019 then test_tb.histBall100 end) as zno_2019,
           max(case when test_tb.zno_year = 2020 then test_tb.histBall100 end) as zno_2020
           from test_tb 
           where test_tb.histTestStatus = 'Зараховано'
           group by test_tb.histPTRegName) TO STDOUT WITH CSV HEADER DELIMITER ';'"""
    with open("result.csv", "w") as file: # Файл з результатами виконання запиту
        cur.copy_expert(sql, file)
        cur.close()

create_table()
import_data('Odata2019File.csv')
import_data('Odata2020File.csv')
export_request()

conn.close()

    # 0	    OUTID               TEXT,
    # 1	    Birth               integer,
    # 2	    SEXTYPENAME         TEXT,
    # 3	    REGNAME             TEXT,
    # 4	    AREANAME            TEXT,
    # 5	    TERNAME             TEXT,
    # 6	    REGTYPENAME         TEXT,
    # 7	    TerTypeName         TEXT,
    # 8	    ClassProfileNAME    TEXT,
    # 9	    ClassLangName       TEXT,
    # 10	EONAME              TEXT,
    # 11	EOTYPENAME          TEXT,
    # 12	EORegName           TEXT,
    # 13	EOAreaName          TEXT,
    # 14	EOTerName           TEXT,
    # 15	EOParent            TEXT,
    # 16	UkrTest             TEXT,
    # 17	UkrTestStatus       TEXT,
    # 18	UkrBall100          numeric(10,2),
    # 19	UkrBall12           integer,
    # 20	UkrBall             integer,
    # 21	UkrAdaptScale       integer,
    # 22	UkrPTName           TEXT,
    # 23	UkrPTRegName        TEXT,
    # 24	UkrPTAreaName       TEXT,
    # 25	UkrPTTerName        TEXT,
    # 26	histTest            TEXT,
    # 27	HistLang            TEXT,
    # 28	histTestStatus      TEXT,
    # 29	histBall100         numeric(10,2),
    # 30	histBall12          integer,
    # 31	histBall            integer,
    # 32	histPTName          TEXT,
    # 33	histPTRegName       TEXT,
    # 34	histPTAreaName      TEXT,
    # 35	histPTTerName       TEXT,
    # 36	mathTest            TEXT,
    # 37	mathLang            TEXT,
    # 38	mathTestStatus      TEXT,
    # 39	mathBall100          numeric(10,2),
    # 40	mathBall12           integer,
    # 41	mathBall            integer,
    # 42	mathPTName          TEXT,
    # 43	mathPTRegName       TEXT,
    # 44	mathPTAreaName      TEXT,
    # 45	mathPTTerName       TEXT,
    # 46	physTest            TEXT,
    # 47	physLang            TEXT,
    # 48	physTestStatus      TEXT,
    # 49	physBall100          numeric(10,2),
    # 50	physBall12           integer,
    # 51	physBall            integer,
    # 52	physPTName          TEXT,
    # 53	physPTRegName       TEXT,
    # 54	physPTAreaName      TEXT,
    # 55	physPTTerName       TEXT,
    # 56	chemTest            TEXT,
    # 57	chemLang            TEXT,
    # 58	chemTestStatus      TEXT,
    # 59	chemBall100          numeric(10,2),
    # 60	chemBall12           integer,
    # 61	chemBall            integer,
    # 62	chemPTName          TEXT,
    # 63	chemPTRegName       TEXT,
    # 64	chemPTAreaName      TEXT,
    # 65	chemPTTerName       TEXT,
    # 66	bioTest             TEXT,
    # 67	bioLang             TEXT,
    # 68	bioTestStatus       TEXT,
    # 69	bioBall100          numeric(10,2),
    # 70	bioBall12           integer,
    # 71	bioBall             integer,
    # 72	bioPTName           TEXT,
    # 73	bioPTRegName        TEXT,
    # 74	bioPTAreaName       TEXT,
    # 75	bioPTTerName        TEXT,
    # 76	geoTest             TEXT,
    # 77	geoLang             TEXT,
    # 78	geoTestStatus       TEXT,
    # 79	geoBall100          numeric(10,2),
    # 80	geoBall12           integer,
    # 81	geoBall             integer,
    # 82	geoPTName           TEXT,
    # 83	geoPTRegName        TEXT,
    # 84	geoPTAreaName       TEXT,
    # 85	geoPTTerName        TEXT,
    # 86	engTest             TEXT,
    # 87	engTestStatus       TEXT,
    # 88	engBall100          numeric(10,2),
    # 89	engBall12           integer,
    # 90	engDPALevel         TEXT,
    # 91	engBall             integer,
    # 92	engPTName           TEXT,
    # 93	engPTRegName        TEXT,
    # 94	engPTAreaName       TEXT,
    # 95	engPTTerName        TEXT,
    # 96	fraTest             TEXT,
    # 97	fraTestStatus       TEXT,
    # 98	fraBall100          numeric(10,2),
    # 99	fraBall12           integer,
    # 100	fraDPALevel         TEXT,
    # 101	fraBall             integer,
    # 102	fraPTName           TEXT,
    # 103	fraPTRegName        TEXT,
    # 104	fraPTAreaName       TEXT,
    # 105	fraPTTerName        TEXT,
    # 106	deuTest             TEXT,
    # 107	deuTestStatus       TEXT,
    # 108	deuBall100          numeric(10,2),
    # 109	deuBall12           integer,
    # 110	deuDPALevel         TEXT,
    # 111	deuBall             integer,
    # 112	deuPTName           TEXT,
    # 113	deuPTRegName        TEXT,
    # 114	deuPTAreaName       TEXT,
    # 115	deuPTTerName        TEXT,
    # 116	spaTest             TEXT,
    # 117	spaTestStatus       TEXT,
    # 118	spaBall100          numeric(10,2),
    # 119	spaBall12           integer,
    # 120	spaDPALevel         TEXT,
    # 121	spaBall             integer,
    # 122	spaPTName           TEXT,
    # 123	spaPTRegName        TEXT,
    # 124	spaPTAreaName       TEXT,
    # 125	spaPTTerName        TEXT,
    # 126	zno_year            integer
