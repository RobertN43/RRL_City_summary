import os
import requests
from dotenv import load_dotenv

# 1. Učitavanje API ključa iz .env datoteke
load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

# 2. Unos grada
city_input = input("Unesite ime grada: ").strip()

# Provjera praznog unosa
if not city_input:
    print("Greška: Niste unijeli ime grada!")
else:
    headers = {
        "User-Agent": "MojQAStudentProjekt/1.0 (kontakt_student@mojdomena.hr)"
    }

    try:
        # --- A) DOHVAĆANJE WIKIPEDIJA SAŽETKA ---
        wiki_url = "https://en.wikipedia.org/w/api.php"
        wiki_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": city_input,
            "redirects": 1,
        }

        wiki_response = requests.get(
            wiki_url, headers=headers, params=wiki_params, timeout=10
        )
        summary_text = None
        official_title = city_input

        if wiki_response.status_code == 200:
            wiki_data = wiki_response.json()
            pages = wiki_data.get("query", {}).get("pages", {})
            page_id = list(pages.keys())[0]

            if page_id != "-1":
                page = pages[page_id]
                official_title = page.get("title", city_input)
                summary_text = page.get("extract")

        # --- B) DOHVAĆANJE VREMENSKE PROGNOZE ---
        weather_url = "http://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "q": city_input,
            "APPID": weather_api_key,
            "units": "metric",  # Celzijusi
        }

        weather_response = requests.get(
            weather_url, params=weather_params, timeout=10
        )
        temp = None

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            temp = weather_data["main"]["temp"]
            if isinstance(temp, float) and temp.is_integer():
                temp = int(temp)

        # --- C) OBRADA REZULTATA I GENERIRANJE DATOTEKE ---
        if (
            not summary_text
            or wiki_response.status_code != 200
            or weather_response.status_code == 404
        ):
            print(f"Greška: Grad '{city_input}' nije pronađen.")

        elif weather_response.status_code == 401:
            print("Greška 401: API ključ nije ispravan ili još nije aktiviran.")

        elif summary_text and temp is not None:
            temp_sentence = f"Current temperature in {official_title} is {temp} degrees Celsius."
            full_content = f"{summary_text}\n\n{temp_sentence}"

            file_name = f"{official_title}.txt"

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(full_content)
            print(
                f"Uspjeh! Stvorena je datoteka '{file_name}' sa sažetkom i temperaturom."
            )

    except requests.exceptions.ConnectionError:
        print(
            "Greška: Nemate internetsku vezu ili je poslužitelj nedostupan."
        )
    except requests.exceptions.Timeout:
        print("Greška: Zahtjev je potrajao predugo (Timeout).")
    except Exception as e:
        print(f"Došlo je do neočekivane greške: {e}")