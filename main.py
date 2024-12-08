from datetime import datetime
import requests
import os

API_ID = os.environ["API_ID"]
API_KEY = os.environ["API_KEY"]

exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY
}

user_input = input("What form of exercise have you done today and for how long?\n")

exercise_params = {
    "query": user_input,
    "gender": "male",
    "weight_kg": 87,
    "height_cm": 186,
    "age": 20,
}

response = requests.post(exercise_url,headers=headers, json=exercise_params)


training_data = response.json()


calories_for_exercise = [exercise["nf_calories"] for exercise in training_data["exercises"]]

duration_for_exercise = [exercise["duration_min"] for exercise in training_data["exercises"]]

chosen_exercise = [exercise["user_input"] for exercise in training_data["exercises"]]

exercise_id = [exercise["tag_id"] for exercise in training_data["exercises"]]

date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%H:%M:%S")

sheety_url = "https://api.sheety.co/8b2f495b8b8535a5cf54936bcc5a44df/myTraining/workouts"

sheety_params = {
    "workout": {
        "date": date,
        "time": time,
        "exercise": chosen_exercise[0].title(),
        "duration": duration_for_exercise[0],
        "calories": calories_for_exercise[0],

    }
}

secret_key = os.environ["secret_key"]

sheet_headers= {
    "Authorization": f"Bearer {secret_key}"
}


response = requests.post(sheety_url, json=sheety_params, headers=sheet_headers)

print(response.text)




