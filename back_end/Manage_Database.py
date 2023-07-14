import pymongo
from pymongo import TEXT
import connect_mongo as cm
from pymongo.mongo_client import MongoClient
import Flipp_data as fd
# def check_if_table_exists():
    
    
    
def create_table(client):
    flipp_data_db = client['flipp_database']
    return flipp_data_db
    
def create_collection(mongoDatabase):
    try:
        mongoDatabase.create_collection("flipp_data")
    except:
        print("Collection already exists")
        
    collection = mongoDatabase["flipp_data"]
    
    # collection.create_index("UUID", unique = True)
    return collection
    
    
def insert_data(flipp_data_db,db_collection,data):
    # try:
        for i in data:    
            value = data[i]
            db_collection.update_one({
                                        "id" : value['id']
                                        },
                                     {
                                         "$set": value,
                                         },
                                     upsert= True)
    # except:
    #     print("ERROR")
    
    
# def __main__():
client = cm.Connect_MongoDB_Cluster()
flipp_data_db = create_table(client)

collection = create_collection(flipp_data_db)


data = fd.provide_data_on_deal()
# breakpoint()
insert_data(flipp_data_db,collection,data)

# saved_data = collection.find({"merchant_name":"FreshCo", "name":"Maggi Masala Noodles 70 g"})
saved_data = collection.find({})

saved_data_list = list(saved_data)

import pandas as pd
saved_data_df = pd.DataFrame(saved_data_list)
# for data in saved_data_list:
#     print(data)






# print(flipp_data_db.list_database_names())



