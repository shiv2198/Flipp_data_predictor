from pymongo.mongo_client import MongoClient
    
    
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
        

# Connect_MongoDB_Cluster()    