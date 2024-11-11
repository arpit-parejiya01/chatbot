from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
from flask_cors import CORS
CORS(app, origins=["*","192.168.2.77"])

available_time_slots = [
    "8:00 AM to 9:00 AM",
    "9:00 AM to 10:00 AM",
    "1:00 PM to 2:00 PM",
    "4:00 PM to 5:00 PM",
    "5:00 PM to 6:00 PM"
]

country = [
    "India",
    "America",
    "Canada",
    "England"
]

# Country to states mapping
states = {
    "India": ["Maharashtra", "Karnataka", "Delhi", "Uttar Pradesh"],
    "America": ["California", "Texas", "New York", "Florida"],
    "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta"],
    "England": ["England", "Scotland", "Wales", "Northern Ireland"]
}

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
            "message": "Hi there! 👋 Welcome to 'TalyGrooming', I am here to assist you with your bookings with TalyGrooming.",
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
        data['pet_breed'] = user_message.split(':')[-1].strip()
        response = {
            "message": "What is the size of your dog?",
            "radio_options": ["1 to 10 lbs", "11 to 30 lbs", "31 to 60 lbs", "61 to 80 lbs", "81+ lbs"]
        }
    elif user_message in ["1 to 10 lbs", "11 to 30 lbs", "31 to 60 lbs", "61 to 80 lbs", "81+ lbs"]:
        data['size_of_dog'] = user_message
        response = {
            "message": "Which of these best describes your pet's coat type?",
            "radio_options": ["Short Coat Breeds", "Wire Coat Breeds", "Soft Coat Breeds", "Double Coat Breeds"]
        }
    elif user_message in ["Short Coat Breeds", "Wire Coat Breeds", "Soft Coat Breeds", "Double Coat Breeds"]:
        data['coat_type'] = user_message
        response = {
            "message": "Does your dog need any of these extra services?",
            "radio_options": ["Dematting $1/min", "Ear Plucking ($10)", "Flea Preventative Shampoo ($10)", "Intensive Coat Hydration ($10)", "No"]
        }
    elif user_message in ["Dematting $1/min", "Ear Plucking ($10)", "Flea Preventative Shampoo ($10)", "Intensive Coat Hydration ($10)", "No"]:
        data['extra_service'] = user_message
        response = {
            "message": "Please select country for service",
            "country": country
        }
    elif user_message in country:
        data['country'] = user_message
        response = {
            "message": "Please select your State:",
            "states": states.get(user_message, [])
        }
    elif user_message in states.get(data.get('country', ''), []):
        data['state'] = user_message
        response = {
            "message": "Please provide your service address:",
            "input_field": "service_address"
        }
    elif "service_address:" in user_message:
        data['service_address'] = user_message.split(':')[-1].strip()
        response = {
            "message": f"Thank you! You've provided your service address: {data['service_address']}. Please provide your phone number:",
            "input_field": "phone_number"
        }
    elif "phone_number:" in user_message:
        phone_number = user_message.split(":")[-1].strip()
        if len(phone_number) == 10 and phone_number.isdigit():
            data['phone_number'] = phone_number
            response = {
                "message": f"Thank you! Your phone number is {data['phone_number']}. Here are your booking details:\n"
                           f"Date: {data['Date']}\n"
                           f"Time Slot: {data['Time Slot']}\n"
                           f"Service: {data['Service']}\n"
                           f"Pet Name: {data['pet_name']}\n"
                           f"Breed: {data['pet_breed']}\n"
                           f"Size: {data['size_of_dog']}\n"
                           f"Coat Type: {data['coat_type']}\n"
                           f"Extra Service: {data['extra_service']}\n"
                           f"Country: {data['country']}\n"
                           f"State: {data['state']}\n"
                           f"Service Address: {data['service_address']}\n"
                           f"Phone Number: {data['phone_number']}"
            }
        else:
            response = {"message": "Please enter the correct number. It should be 10 digits."}
    return jsonify(response)

@app.route("/embed.js")
def embed():
    return render_template("embed.js")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
