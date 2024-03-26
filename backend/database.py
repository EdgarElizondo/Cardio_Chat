import pymongo

class database:
    def __init__(self,name,cloud=True) -> None:
        self.name = name
        self.cloud = cloud
        if self.cloud:
            self.URI_CONNECTION = "mongodb+srv://EdgarElizondo:@corbot.3jul9je.mongodb.net/?retryWrites=true&w=majority&appName=CorBot"
            # self.URI_CONNECTION = "mongodb+srv://liamedina98:Lia2145.@corbot.j8mkkdi.mongodb.net/?retryWrites=true&w=majority&appName=CorBot"
            # self.URI_CONNECTION = "mongodb+srv://EdgarElizondo:@corbot.3jul9je.mongodb.net/?retryWrites=true&w=majority&appName=CorBot"
        else:
            self.MONGODB_HOST = '127.0.0.1'
            self.MONGODB_PORT = '27017'
            self.MONGODB_TIMEOUT = 1000
            self.URI_CONNECTION = "mongodb://" + self.MONGODB_HOST + ":" + self.MONGODB_PORT + "/"

    def _connect(self):
        
        # Create a new client and connect to the server
        client = pymongo.MongoClient(self.uri)
        
        # Send a ping to confirm a successful connection
        try:
            client.server_info()
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            db = client[self.name]
            return db
        
        except Exception as e:
            print(e)

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