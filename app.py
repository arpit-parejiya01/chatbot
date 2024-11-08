from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

available_time_slots = [
    "8:00 AM to 9:00 AM",
    "9:00 AM to 10:00 AM",
    "1:00 PM to 2:00 PM",
    "4:00 PM to 5:00 PM",
    "5:00 PM to 6:00 PM"
]

data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # Initial message
    if user_message == "start":
        response = {
            "message": "Hi there! 👋 Welcome to 'TalyGrooming', I am here to assist you.",
            "options": ["How can I help you today? Are you interested in booking an appointment for your pet grooming?"],
            "buttons": ["Yes, I am interested", "No, I am not interested"]
        }
    elif user_message == "Yes, I am interested":
        response = {
            "message": "Great! Please select a date for your booking:",
            "date_picker": True
        }
    elif user_message == "No, I am not interested":
        response = {"message": "Thank you for visiting TalyGrooming."}
    elif "selected date" in user_message:
        response = {
            "message": f"You have selected {user_message.split(':')[-1].strip()} for your appointment. Please choose a time slot:",
            "time_slots": available_time_slots
        }
        data['Date'] = user_message.split(':')[-1].strip()
    elif user_message in available_time_slots:
        response = {
            "message": f"You have selected {user_message}. Next, which service would you like to choose?",
            "radio_options": ["Full Service Haircut", "Full Service Bath", "Skunk off Treatment"]
        }
        data['Time Slot'] = user_message
    elif user_message in ["Full Service Haircut", "Full Service Bath", "Skunk off Treatment"]:
        data['Service'] = user_message
        response = {"message": "Great! Please provide your pet's name:", "input_field": "pet_name"}
    elif "pet_name:" in user_message:
        data['pet_name'] = user_message.split(':')[-1].strip()
        response = {"message": "Thank you! What is your pet's breed?", "input_field": "pet_breed"}
    elif "pet_breed:" in user_message:
        response = {
            "message": "What is the size of your dog?",
            "radio_options": ["1 to 10 lbs", "11 to 30 lbs", "31 to 60 lbs", "61 to 80 lbs", "81+ lbs"]
        }
        data['pet_breed'] = user_message.split(':')[-1].strip()
    elif user_message in ["1 to 10 lbs", "11 to 30 lbs", "31 to 60 lbs", "61 to 80 lbs", "81+ lbs"]:
        data['size_of_dog'] = user_message
        print(data)
        response = {
            "message": f"Thank you for providing all the information. Here are your booking details:\n"
                       f"Service: {user_message}\nPet Name: {data['pet_name']}\nBreed: {data['pet_breed']}\nSize: {data['size_of_dog']}\n Time Slot: {data['Time Slot']}\nDate of Appontment: {data['Date']}"
        }

    
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
