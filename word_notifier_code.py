import os
import json
import time
from datetime import date
import requests
from dotenv import load_dotenv
from plyer import notification


load_dotenv()
WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")
print("WORDNIK_API_KEY",WORDNIK_API_KEY)

def get_word_of_the_day(current_date):
    """
    Fetching word of the day from the Wordnik API
    """
    response_data = {"word": "Sorry, No new word today", "definition": "No definition available"}
    if WORDNIK_API_KEY:
        url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?date={current_date}" \
              f"&api_key={WORDNIK_API_KEY}"
        response = requests.get(url)
        api_response = json.loads(response.text)
        if response.status_code == 200:
            response_data["word"] = api_response["word"]
            for definition in api_response["definitions"]:
                response_data["definition"] = definition["text"]
                break
    else:
        # use a mock word if there is no Wordnik API key
        response_data["word"] = "mesmerizing"
        response_data["definition"] = "capturing one's attention as if by magic"
    return response_data

def notify(response_data):
    """
    Desktop notification 
    """
    while True:
        notification.notify(
            title = response_data["word"],
            app_name = "Word Notifier",
            app_icon = "C:\Python\Python39\word_notifier\word\icon.ico",
            message = response_data["definition"],
            ticker = "Word of the day",
            timeout = 12
            )
        time.sleep(60*60)

if __name__ == "__main__":
    current_date = date.today()
    data = get_word_of_the_day(current_date)
    notify(data)



