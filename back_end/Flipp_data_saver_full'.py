import sys
import subprocess

library_list = ["pymongo[srv]", "requests", "pandas", "uuid"]


for i in library_list:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])    


from pymongo.mongo_client import MongoClient
import requests
import pandas as pd
import uuid
from datetime import datetime
import pymongo
from pymongo import TEXT
from pymongo.mongo_client import MongoClient
import datetime

def Connect_MongoDB_Cluster():
    uri = "mongodb+srv://skdave21:Password123@flipppredictorprojectcl.aiq0ag2.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        

def fetch_data():
    stores = ["Freshco","Walmart","2001","Ample","Costco","Food Basics","NoFrill","Shoppers","Real Canadian","Staples","Bestbuy"]
    # url = f"https://backflipp.wishabi.com/flipp/items/search?&q={query}&locale=en-ca&q={query}&postal_code=M5S+3H1&radius=50&locale=en-ca"
    
    value = pd.DataFrame()
   
    
    for store in stores:
        url = f"https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code=N2E1J1&q={store}"
        # make a request with start and per_page parameters to paginate through the results
        # request_url = f"{url}&start={start}&per_page={per_page}"
        response = requests.get(url)
        data = response.json()
        
        # extract the total number of items and the items themselves from the response
        # total_items = data["total"]
        # items = data["items"]
        
        # print out the name and price of each item
        # for item in items:
        #     print(item["flyer_item"]["name"])
        #     print(item["flyer_item"]["price"])
        
        value1 = pd.DataFrame(data['items'])
        value = value.append(value1)
        value['saved_date'] = datetime.datetime.today()
    return value
        
def clean_flipp_data(value):
    value = value.drop(columns=['score','id','bottom','indexed','item_type','post_price_text',
                                        'right','top','left','pre_price_text','clipping_image_url'])
    value.dropna(axis = 1, how="all")
    value.drop_duplicates(inplace = True)    
    value.rename(columns={"_L1":"category","_L2":"sub_category"}, inplace=True)
    value['id'] = value['merchant_name']+"_"+value['flyer_id'].astype(str)+"_"+value['flyer_item_id'].astype(str)
    value = value.reset_index()
    
    value['name'] = value['name'].str.lower()
    return value
    

def provide_data_on_deal():
    raw_data = fetch_data()
    deals = clean_flipp_data(raw_data)
    insert_value = deals.to_dict('index')
    return insert_value

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
    
today = datetime.date.today()
weekday = today.weekday()

print(weekday)
# if (weekday == 4):

client = Connect_MongoDB_Cluster()
flipp_data_db = create_table(client)

collection = create_collection(flipp_data_db)


data = provide_data_on_deal()
# breakpoint()
insert_data(flipp_data_db,collection,data)

print("Running task on ",today)
print("Finished inserting data")
    