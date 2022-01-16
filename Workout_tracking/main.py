import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()   # access the env file in the directory

nutrition_id = os.environ["NUTRITION_ID"] # or os.environ.get('NUTRITION_ID)
nutrition_token = os.environ["NUTRITION_TOKEN"]

NUTRITION_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_URL = "https://api.sheety.co/c70d559d6f429abcb12d5da44cdad0cc/copyOfMyWorkouts/workouts"
bearer_headers = {
    "Authorization": os.getenv("Authorization")
}

exercise = str(input("What did you do today? "))
nutrition_parameters = {
    "query": exercise,
    "gender": "male",
    "weight_kg": "87",
    "height_cm": "183",
    "age": "23"
}

nutrition_header = {
    "x-app-id": nutrition_id,
    "x-app-key": nutrition_token,
}

today = datetime.now()
format_time = today.strftime("%X")  # format time to 00:00:00
format_date = today.strftime("%x")  # format date to dd/mm/yy
# print(format_time)

workout = requests.post(url=NUTRITION_URL, json=nutrition_parameters, headers=nutrition_header)
result = workout.json()
print(result)
# print(duration, burnt_calories, result, workout_name, sep="\n")

for each in result['exercises']:
    spreadsheet_input = {'workout': {
        "date": format_date,
        "time": format_time,
        "exercise": each['name'].title(),
        "duration": each['duration_min'],
        "calories": each['nf_calories'],
    }}
    spreadsheet = requests.post(url=SHEETY_URL, json=spreadsheet_input, headers=bearer_headers)
    spreadsheet.raise_for_status()
    print(spreadsheet.json())
