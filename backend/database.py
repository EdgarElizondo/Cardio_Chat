import pymongo

class database:
    def __init__(self,name) -> None:
        self.name = name
        
        self.MONGODB_HOST = '127.0.0.1'
        self.MONGODB_PORT = '27017'
        self.MONGODB_TIMEOUT = 1000
        self.URI_CONNECTION = "mongodb://" + self.MONGODB_HOST + ":" + self.MONGODB_PORT + "/"
    
    def _connect(self):
        try:
            client = pymongo.MongoClient(self.URI_CONNECTION, serverSelectionTimeoutMS=self.MONGODB_TIMEOUT)
            client.server_info()
            print('OK -- Connected to MongoDB at server %s' % self.MONGODB_HOST)
            db = client[self.name]
            return db
        except pymongo.errors.ServerSelectionTimeoutError as error:
            print('Error with MongoDB connection: %s' % error)
            return -1
        except pymongo.errors.ConnectionFailure as error:
            print('Could not connect to MongoDB: %s' % error)
            return -1
        
    def add_user_to_db(self,user_data):
        
        user = {"userid":user_data["userid"],
                    "Gender":user_data["Gender"],
                    "Age":user_data["Age"],
                    "BMI":user_data["BMI"],
                    "Race":user_data["Race"],
                    "Smoke":user_data["Smoke"],
                    "Drink":user_data["Drink"],
                    "Exercise":user_data["Exercise"],
                    "Sleep_Time":user_data["Sleep_Time"],
                    "Physical_Health":user_data["Physical_Health"],
                    "Mental_Health":user_data["Mental_Health"],
                    "Difficult_Walking":user_data["Difficult_Walking"],
                    "General_Health":user_data["General_Health"],
                    "Stroke":user_data["Stroke"],
                    "Asthma":user_data["Asthma"],
                    "Diabetis":user_data["Diabetis"],
                    "Kidney_Disease":user_data["Kidney_Disease"],
                    "Skin_Cancer":user_data["Skin_Cancer"]}

        # Insert Data
        collection = self._connect()['new_data']
        collection.insert_one(user)