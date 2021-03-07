import psycopg2
from config import Config
import time
import csv
import io


class Lab1:
    def __init__(self):

        self.conn = None

        self.flag = 0

    def connection_db(self):
        self.conn = psycopg2.connect(
            host=Config.host,
            database=Config.database,
            user=Config.user,
            password=Config.password)

    def time_test(func):
        """функція для вимірювання часу роботи завантаження даних у БД"""

        def f(a, b):
            t1 = time.time()
            func(a, b)
            t2 = time.time()
            print(str(t2 - t1) + ": " + func.__name__)
            with open("loading_time.txt", "w") as file_t:
                file_t.write('Data was loaded in '+str(t2 - t1)+' seconds\n')

        return f

    def create_table(self):
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
        cur = self.conn.cursor()
        cur.execute(command)
        cur.close()

    def reconnect(self):
        connection_established = False
        while not connection_established:
            try:

                self.connection_db()

                connection_established = True
                print("Connection established !")

            except (Exception, psycopg2.DatabaseError):
                pass

    def Case(self, row, zno_year):
        """Формує рядки для файлового об'єкта"""
        for i in [18, 29, 39, 49, 59, 69, 79, 88, 98, 108, 118]:
            row[i] = row[i].replace(',', '.')
        str = Config.delimiter.join(row)
        return str + Config.delimiter + zno_year

    @time_test
    def import_data(self, file_list):
        """Функція, що зчитує дані з файлу та записує їх до таблиці"""
        for file_name in file_list:
            with open(file_name) as f:
                spamreader = csv.reader(f, delimiter=Config.delimiter, quoting=csv.QUOTE_ALL)
                zno_year = file_name[5:9]
                next(spamreader, None)
                out = io.StringIO()

                number_of_lines = 0
                rown = 0
                cur = self.conn.cursor()
                for x in spamreader:

                    out.write(self.Case(x, zno_year) + "\n")
                    rown += 1
                    if rown == Config.portion:
                        while rown != 0:
                            counter = 0
                            try:

                                out.seek(0)
                                if self.flag == 0 and number_of_lines > Config.portion * 2:
                                    self.conn.close()
                                    self.flag = 1
                                cur.copy_from(out, 'test_tb', sep=Config.delimiter, null='null')
                                self.conn.commit()

                                out.close()
                                out = io.StringIO()
                                rown = 0
                                number_of_lines += Config.portion


                            except (Exception, psycopg2.DatabaseError):

                                print("Base connection lost !")

                                counter += 1
                                if counter == 10:
                                    print('Failed to restore database connection')
                                    print('From the file {} were loaded {} lines'.format(file_name, number_of_lines))
                                    cur.close()
                                    out.close()
                                    return -1
                                self.reconnect()
                                cur = self.conn.cursor()
                cur.close()
                quantity = rown+number_of_lines
                if rown > 0:

                    while rown != 0:
                        counter = 0
                        try:
                            cur = self.conn.cursor()
                            out.seek(0)
                            cur.copy_from(out, 'test_tb', sep=Config.delimiter, null='null')
                            self.conn.commit()
                            cur.close()
                            rown = 0
                        except (Exception, psycopg2.DatabaseError):

                            print("Base connection lost !")

                            counter += 1
                            if counter == 10:
                                print('Failed to restore database connection')
                                print('From the file {} were loaded {} lines'.format(file_name, number_of_lines))
                                cur.close()
                                out.close()
                                return -1
                            self.reconnect()

                print('From the file {} were loaded all lines: {}'.format(file_name, quantity))
                out.close()

    def export_request(self):
        """Функція, що виконує запит та записує результати цього запиту у файл query_result.csv"""
        # Запит: порівняти найкращий бал з Історії України в кожному регіоні у 2020 та 2019 роках серед тих кому було зараховано тест
        cur = self.conn.cursor()
        sql = """COPY (select test_tb.histPTRegName, 
               max(case when test_tb.zno_year = 2019 then test_tb.histBall100 end) as zno_2019,
               max(case when test_tb.zno_year = 2020 then test_tb.histBall100 end) as zno_2020
               from test_tb 
               where test_tb.histTestStatus = 'Зараховано'
               group by test_tb.histPTRegName) TO STDOUT WITH CSV HEADER DELIMITER ';'"""
        with open("query_result.csv", "w") as file:  # Файл з результатами виконання запиту
            cur.copy_expert(sql, file)
            cur.close()


test = Lab1()
test.connection_db()
test.create_table()
if test.import_data(Config.file_list) != -1:
    test.export_request()

test.conn.close()
