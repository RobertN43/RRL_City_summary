import os
import requests
from dotenv import load_dotenv

# 1. Učitavanje API ključa iz .env datoteke
load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

# 2. Unos grada
city_input = input("Unesite ime grada: ").strip()

if not city_input:
    print("Greška: Niste unijeli ime grada!")
else:
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
    headers = {
        "User-Agent": "MojQAStudentProjekt/1.0 (kontakt_student@mojdomena.hr)"
    }

    wiki_response = requests.get(wiki_url, headers=headers, params=wiki_params)

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
        else:
            print(f"Greška: Grad '{city_input}' nije pronađen na Wikipediji.")
    else:
        print(
            f"Greška pri dohvatu Wikipedije (Kod: {wiki_response.status_code})."
        )

    # Ako nismo dobili sažetak s Wikipedije, nemamo što dalje pisati u datoteku
    if summary_text:
        # --- B) DOHVAĆANJE VREMENSKE PROGNOZE ---
        weather_url = "http://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "q": city_input,
            "APPID": weather_api_key,
            "units": "metric",  # Celzijusi
        }

        weather_response = requests.get(weather_url, params=weather_params)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            temp = weather_data["main"]["temp"]

            # Formatiranje temperature u slučajevima poput 23.0 -> 23
            if isinstance(temp, float) and temp.is_integer():
                temp = int(temp)

            # Rečenica o temperaturi prema PDF specifikaciji
            temp_sentence = f"Current temperature in {official_title} is {temp} degrees Celsius."

            # Sastavljanje kompletnog sadržaja za datoteku
            full_content = f"{summary_text}\n\n{temp_sentence}"

            # --- C) SPREMANJE U DATOTEKU <city name>.txt ---
            file_name = f"{official_title}.txt"

            try:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(full_content)
                print(
                    f"\nUspeh! Rezultat je uspješno spremljen u datoteku: {file_name}"
                )
            except Exception as e:
                print(f"Greška pri zapisivanju u datoteku: {e}")

        elif weather_response.status_code == 404:
            print(
                f"Greška: Grad '{city_input}' nije pronađen na OpenWeatherMapu."
            )
        elif weather_response.status_code == 401:
            print(
                "Greška 401: API ključ još nije aktivan ili je neispravan."
            )
        else:
            print(
                f"Greška pri dohvatu prognoze (Kod: {weather_response.status_code})."
            )