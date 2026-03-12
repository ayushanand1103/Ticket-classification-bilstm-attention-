## Importing various librariesn 
##Pymongo for data base operation
##Numpy for mathematical operations
##bson for dealing with bson files (mongo db stores data in bson format (similar to json))
##Tesorflow for loading model and preprocessing
##Pickle is for loading the tokenzier 
## os for operating system operations(reqired by tensorflow)
import pymongo 
import numpy as np 
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import WriteError, PyMongoError
from bson.errors import InvalidId
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
from tensorflow.keras.models import load_model

#Loading model
Model = load_model(
    r"C:/Projects/Ticketing system/bilstm_attention_ticket_classifier.keras",
    safe_mode=False
)



#Loading tokenizer
TOKENIZER_PATH = r"C:/Projects/Ticketing system/tokenizer.pkl"


with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

word_index = tokenizer.word_index


class model:
    # Preprocessing text for model
    @staticmethod
    def preprocessing(ticket):
        ticket = str(ticket)
        seq = tokenizer.texts_to_sequences([ticket])  
        padded_sequence = pad_sequences(
            seq,
            maxlen=500,
            padding="post",
            truncating="post"
        )
        return padded_sequence
    
    @staticmethod
    def prediction(padded_sequence):
        probablity = Model.predict(padded_sequence)
        return probablity
    
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
Ticketing = client.Ticketing
db = client.Ticketing

# Validator
user_info_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Name", "Email", "Phone number", "Ticket"],
        "properties": {
            "Name": {"bsonType": "string"},
            "Email": {"bsonType": "string"},
            "Phone number": {"bsonType": "string"},
            "Ticket": {"bsonType": "string"}
        }
    }
}

db.command({
    "collMod": "User_info",
    "validator": user_info_validator,
    "validationLevel": "strict",
    "validationAction": "error"
})

# Ensuring all ids are same with User_info collection

class Collection_allotment : 
    @staticmethod
    def IT_Tech(a):
        IT_tech = Ticketing.IT_Tech
        IT_tech.insert_one(a)
    
    @staticmethod
    def Customer_service(a):
        Customer_service = Ticketing.Customer_service
        Customer_service.insert_one(a) 
    
    @staticmethod
    def Billing_finance(a):
        Billing_Finance = Ticketing.Billing_finance
        Billing_Finance.insert_one(a)
        
# Collection update

class collection_update:
    @staticmethod
    def IT_tech(_id,update):
        IT_tech = Ticketing.IT_Tech
        IT_tech.update_one({"_id":_id},update)

    def Customer_service(_id,update):
        Customer_service = Ticketing.Customer_service
        Customer_service.update_one({"_id":_id},update)

    def Billing_finance(_id,update):
        Billing_finance = Ticketing.Billing_finance
        Billing_finance.update_one({"_id":_id},update)


# CRUD operations being performed
class User:
    @staticmethod
    def insert(Name, Email, Phone_num, Ticket,Status="Not solved"):
        try:
            ## Choosing the main collection to which all the queries and user info is added 
            collection = Ticketing.User_info
            ## Calling model class function to preprocess the input to be feeded in model 
            ## and predicting the result
            padded_sequence = model.preprocessing(Ticket)
            probablity = model.prediction(padded_sequence)
            prob_1 = probablity[0] ## Result was 2 D array so we are accesing the first element of it 
            prob_1 = np.array(prob_1) ## Transforming the array into numpy array
            ## Doing Allotment tasks
            if np.max(prob_1) == prob_1[0]:
                department = "IT / Technical Support"
                User_info = {
                "Name": Name,
                "Email": Email,
                "Phone number": Phone_num,
                "Ticket": Ticket,
                "Status":Status,
                "Department":department
            }
                id = collection.insert_one(User_info).inserted_id
                id_ticket = {
                    "_id" : id,
                    "Ticket":Ticket,
                    "Status":Status
                }
                
                ##Calling the collection allotment class and calling IT_Tech function (which inserts into IT_Tech collection)
                Collection_allotment.IT_Tech(id_ticket)

            elif np.max(prob_1) == prob_1[1]:
                department = "Customer Service"
                User_info = {
                "Name": Name,
                "Email": Email,
                "Phone number": Phone_num,
                "Ticket": Ticket,
                "Status":Status,
                "Department":department
            }
                id = collection.insert_one(User_info).inserted_id
                id_ticket = {
                    "_id" : id,
                    "Ticket":Ticket,
                    "Status":Status
                }

                ##Calling the collection allotment class and calling Customer_service funtion (which inserts into Customer_service collection)
                Collection_allotment.Customer_service(id_ticket)

            elif np.max(prob_1) == prob_1[2]:
                department = "Billing / Finance"
                User_info = {
                "Name": Name,
                "Email": Email,
                "Phone number": Phone_num,
                "Ticket": Ticket,
                "Status":Status,
                "Department":department
            }
                
                id = collection.insert_one(User_info).inserted_id
                id_ticket = {
                    "_id":id,
                    "Ticket":Ticket,
                    "Status":Status
                }

                ##Calling the collection allotment class and calling Billing_finance function (which inserts into Billing_finance collection)
                Collection_allotment.Billing_finance(id_ticket)
            
            
            return f"Ticket raised successfully "

        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e:
            return f"Data base error"
        
    @staticmethod
    def read_name(id):
        try:
            ## Reading name from User_info which is our main collection which stores all the queries
            collection = Ticketing.User_info
            _id = ObjectId(id)
            query = collection.find_one({"_id":_id})
            if query is None:
                return "No ticket found"
            else :    
                Name = query["Name"]
                return Name
            
        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"
        
    @staticmethod
    def read_email(id):
        try:
            ## Reads email from User_info collection which is our main collection which stores all queries
            collection = Ticketing.User_info
            _id = ObjectId(id)
            query = collection.find_one({"_id":_id})
            if query is None:
                return "No ticket found"
            else :    
                Email = query["Email"]
                return Email
            
        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"
        
    @staticmethod
    def read_phonenumber(id):
        try:
            ## Reads phone_number from User_info collection which is our main collection and stores our all queries
            collection = Ticketing.User_info
            _id = ObjectId(id)
            query = collection.find_one({"_id": _id})
            if query is None:
                return None
            return query["Phone number"]

        except InvalidId:
            return None

        except PyMongoError:
            return None
        

        
    @staticmethod
    def read_ticket(id):
        try:
            ##Reads ticket from User_info collection and not departmental collections
            collection = Ticketing.User_info
            _id = ObjectId(id)
            query = collection.find_one({"_id":_id})
            if query is None:
                return "No ticket found"
            else :    
                ticket = query["Ticket"]
                return f"This is your ticket : {ticket}"
            
        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"

    @staticmethod    
    def read_status(id):
        try:
            ## Reads status from User_info collection which is our main collection
            collection = Ticketing.User_info
            _id = ObjectId(id)
            status = collection.find_one({"_id":_id})
            if status is None :
                return "No query found"
            else :
                status_ = status["Status"]
                return f"The status of ticket raised is : {status_}"
        
        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"
        
    @staticmethod
    def read_department(id):
        try:
            ## Reads department from User_info collection which is our main collection
            collection = Ticketing.User_info
            _id = ObjectId(id)
            department = collection.find_one({"_id":_id})
            if department is None :
                return "No query found"
            else :
                department_ = department["Department"]
                return f"The status of ticket raised is : {department}"
        
        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"
        
    @staticmethod
    def update_value_Ticket(_id,updated_value):
        try :
            _id = ObjectId(_id)
            collection = Ticketing.User_info
            ## Making sure id is deleted from all other department collection
            IT_tech = Ticketing.IT_Tech
            IT_tech.delete_one({"_id": _id})
            Customer_service = Ticketing.Customer_service
            Customer_service.delete_one({"_id": _id})
            Billing_finance = Ticketing.Billing_finance
            Billing_finance.delete_one({"_id": _id})
            ## Deletion Complete

            ## Checking which department the Updated ticket belong 
            padded_sequence = model.preprocessing(updated_value)
            probablity = model.prediction(padded_sequence)
            prob_1 = probablity[0]  ## Used [0] becuase the out was 2 dimensional array
            prob_1 = np.array(prob_1) ## transforming into numpy array
            ## Performing classification
            if np.max(prob_1) == prob_1[0]:
                ## Prob_1[0] stores probablity for IT_Tech department
                department = "IT / Technical Support"
                update = {
                "$set":{
                    "Ticket" : updated_value,
                    "Department":department
                }
            }
                insert = {
                    "_id": _id,
                    "Ticket":updated_value,
                    "Status":User.read_status(_id),

                }
                collection.update_one({"_id":_id},update)
                Collection_allotment.IT_Tech(insert)

            elif np.max(prob_1) == prob_1[1]:
                ## Prob_1[1] stores probablity for Customer service
                department = "Customer Service"
                update = {
                "$set":{
                    "Ticket" : updated_value,
                    "Department":department
                }
            }
                insert = {
                    "_id":_id,
                    "Ticket":updated_value,
                    "Status":User.read_status(_id),
                }
                collection.update_one({"_id":_id},update)
                Collection_allotment.Customer_service(insert)

            elif np.max(prob_1) == prob_1[2]:
                ## ## Prob_1[2] stores probablity for Billing and finance
                department = "Billing / Finance"
            
                update = {
                "$set":{
                    "Ticket" : updated_value,
                    "Department":department
                    }
                }   
                insert = {
                    "_id":_id,
                    "Ticket":updated_value,
                    "Status":User.read_status(_id),
                }
                collection.update_one({"_id":_id},update)
                Collection_allotment.Billing_finance(insert)
            return f"Ticket updated successfully"

        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"

    @staticmethod
    def update_value_Name(id,updated_value):
        try :
            ## Updating Name value in User_info collection which is our main collection
            _id = ObjectId(id)
            collection = Ticketing.User_info
            update = {
                "$set":{
                    "Name" : updated_value
                }
            }
            collection.update_one({"_id":_id},update)
            return "Name updated successfully"

        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"

    @staticmethod
    def update_value_Email(id,updated_value):
        try :
            ## Updating Email value in User_info collection which is our main collection
            _id = ObjectId(id)
            collection = Ticketing.User_info
            update = {
                "$set":{
                    "Email" : updated_value
                }
            }
            collection.update_one({"_id":_id},update)
            return "Email updated successfully"
        
        except WriteError as e:
            return f"Validation error"
        
        except PyMongoError as e :
            return f"Data base error"
        
        except InvalidId as e :
            return f"Invalid Ticket ID"

    @staticmethod
    def update_value_Phone_num(id, updated_value):
        try:
            ## Updating Phone_number value in User_info collection which is our main collection
            _id = ObjectId(id)
            result = Ticketing.User_info.update_one(
                {"_id": _id},
                {"$set": {"Phone number": updated_value}}
            )
            if result.matched_count == 0:
                return "No ticket found"
            return "Phone number updated successfully"

        except WriteError:
            return "Validation error"

        except InvalidId:
            return "Invalid Ticket ID"

        except PyMongoError:
            return "Database error"
        
    @staticmethod
    def update_value_Department(id,updated_value):
        try:
            ## Updating Department value in User_info collection which is our main collection
            _id = ObjectId(id)
            result = Ticketing.User_info.update_one(
                {"_id": _id},
                {"$set": {"Department": updated_value}}
            )
            if result.matched_count == 0:
                return "No ticket found"
            return "Department updated successfully"

        except WriteError:
            return "Validation error"

        except InvalidId:
            return "Invalid Ticket ID"

        except PyMongoError:
            return "Database error"
        
    @staticmethod
    def delete_ticket(id):
        try:
            ## Deleting ticket from every collection
            _id = ObjectId(id)
            ##Deleting Ticket from User_info collection

            result = Ticketing.User_info.delete_one({"_id": _id})
            if result.deleted_count == 0:
                return "No ticket found"
            
            ## Deleting ticket from other department collection
            Ticketing.IT_Tech.delete_one({"_id": _id})
            Ticketing.Customer_service.delete_one({"_id": _id})
            Ticketing.Billing_finance.delete_one({"_id": _id})

            return "Ticket deleted successfully"

        except InvalidId:
            return "Invalid Ticket ID"

        except PyMongoError:
            return "Database error"

User.insert("Ayush","ayushanand.1103@gmail.com","9717765187","I attempted to complete a payment for my subscription on [date], but the transaction failed while the amount was still deducted from my bank account. The payment status shows unsuccessful on the portal, however, the amount has been debited.Kindly verify the transaction and confirm whether the payment was successful or initiate a refund at the earliest.")
