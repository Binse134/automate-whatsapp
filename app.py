
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://binsealter:Binsealter@binsewhatsapp.cyoqz.mongodb.net/")
db = cluster["binsetest"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)



@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        res.message("Hello, thanks for contacting *Alter*. \n Choose an option:"
                         " \n \n *Type*\n\n 1️⃣ To *Contact us* \n 2️⃣ To *order* snacks \n ")
        users.insert_one({"number": number, "status":"main", "messages": []})
    elif user["status"] == "main":
        try:
            option =int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 1:
            res.message("Phone: 73490448923 \n E-mail:something@gmail.com")
        elif option == 2:
            res.message("You have entered ordering mode")
            users.update_one({"number": number}, {"$set": {"status": "ordering"}}) 
            res.message(" Select one:\n 1️⃣ Red Velvet \n 2️⃣ Dark Forest")
        elif option == 3:
            res.message("We work everyday from 9 AM to 9 PM")
        elif option == 4:
             res.message("Our address is Mangalore")
        else:
            res.message("Enter a Valid Response")

    elif user["status"] == "ordering":
        try:
            option =int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status":"main"}})
            res.message("\n Choose an option:"
                         " \n \n *Type*\n\n 1️⃣ To *Contact us* \n 2️⃣ To *order* snacks \n 0️⃣ to go back ")

        elif 1 <= option <= 9:
            cakes = ["Red velvet", "Dark Forest"]
            selected = cakes[option - 1] #in list counting starts from 0 so if the user types 1 list needs to select the 0th value or index value 0 so option(1) - 1 = 0.
            users.update_one({"number": number}, {"$set":{"status":"address"}})
            users.update_one({"number": number}, {"$set":{"item":selected}})
            res.message("Excellent choice😉")
            res.message("Please enter your address to continue")
        else:
            res.message("Please enter a valid response")
    elif user["status"] == "address":
        selected = user["item"]
        res.message("thanks")
        res.message(f" your order for {selected} has been received.")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one({"number": number}, {"$set":{"status": "ordered"}})
    # elif user["status"] == "ordered":
    #     res.message("Hello, thanks for contacting again. \n Choose an option:"
    #                      " \n \n *Type*\n\n 1️⃣ To *Contact us* \n 2️⃣ To *order* snacks \n")
    #     users.update_one({"number": number}, {"$set":{"status": "main"}})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
