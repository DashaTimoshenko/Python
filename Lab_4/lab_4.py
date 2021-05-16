import pandas as pd
from config import Config
from pymongo import MongoClient
import json
import time
import csv

client = MongoClient(
    "mongodb://" + Config.host + ":" + Config.port + "/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = client[Config.database]
coll = db[Config.collection]

int_list = Config.int_columns_list
float_list = Config.float_columns_list
check_coll = db['check_collection']


# if collection.estimated_document_count() == 0:
#     # db.createCollection('posts', {capped: False})
#     db.proselyte.insert_one({"name": "proselyte"})
#     collection.insert_one({'file_name': 'Odata2019File.csv', 'rows_count': 353813, 'end_file': True})
#     print(True)

# coll.delete_many({'OUTID': {'$ne': "Nan" } })

# -----------------------------import_data-----------------------------
# ---------------------------------------------------------------------
def import_data(file_name, ins_rows_count):
    zno_year = file_name[5:9]
    my_list = []
    new_ins_rows_count = ins_rows_count
    i = 1
    with open(file_name, "r", encoding="cp1251") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';', quoting=csv.QUOTE_ALL)
        # len_row = len(csv_reader[0].keys())
        for j in range(ins_rows_count):
            next(csv_reader)
        for row in csv_reader:
            for x, y in row.items():
                if y == 'null':
                    row[x] = None
                elif x in int_list:
                    row[x] = int(row[x])
                elif x in float_list:
                    row[x] = float(row[x].replace(',', '.'))
            document = row
            document['zno_year'] = int(zno_year)
            my_list.append(document)
            if i == 1000:
                try:
                    coll.insert_many(my_list, ordered=False)
                    new_ins_rows_count += i
                    check_coll.update({'file_name': file_name},
                                      {'file_name': file_name, 'rows_count': new_ins_rows_count, 'end_file': False})
                    i = 1
                    my_list = []
                except:
                    pass

                continue
                # break
            else:
                i += 1

        if len(my_list) != 0:
            try:
                coll.insert_many(my_list, ordered=False)
                new_ins_rows_count += len(my_list)
                check_coll.update({'file_name': file_name},
                                  {'file_name': file_name, 'rows_count': new_ins_rows_count, 'end_file': True})
            except:
                pass

        # print(new_ins_rows_count)


# -----------------------------------------------------------------------
# len_file_list = len(Config.file_list)
# t1 = time.time()
# for ind in range(len_file_list):
#
#     if check_coll.count_documents({'file_name': Config.file_list[ind]}) == 0:
#         check_coll.insert_one({'file_name': Config.file_list[ind], 'rows_count': 0, 'end_file': False})
#
#     inserted_rows_count = check_coll.find_one({'file_name': Config.file_list[ind]})
#     import_data(Config.file_list[ind], inserted_rows_count['rows_count'])
# t2 = time.time()
# print('Data was loaded in ' + str(t2 - t1) + ' seconds\n')
# with open("loading_time.txt", "w") as file_t:
#     file_t.write('Data was loaded in ' + str(t2 - t1) + ' seconds\n')




query_res = coll.aggregate(
    [
    {"$match": {"histTestStatus":"Зараховано"}},


        {"$group": {
            "_id": {
                "zno_year": "$zno_year",
                "histPTRegName": "$histPTRegName"},
            "hist_max_Ball100": {"$max": "$histBall100"}
        }},

        {"$sort": {"_id": 1}}
    ])





with open('query_result.csv', 'w', encoding="utf-8") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['histPTRegName', 'year', 'ball_100'])

    for document in query_res:
        zno_year = document["_id"]["zno_year"]
        histPTRegName = document["_id"]["histPTRegName"]
        max_Ball = document["hist_max_Ball100"]
        csv_writer.writerow([histPTRegName, zno_year, max_Ball])
