import os
import textwrap
import requests
from dotenv import load_dotenv

# Učitavanje API ključa iz .env datoteke
load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_city_summary(city):
    """Dohvaća kratki sažetak grada s Wikipedije."""

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city}"

    headers = {
        "User-Agent": "MojQAStudentProjekt/1.0 (kontakt_student@mojdomena.hr)"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 404:
        return None, None

    response.raise_for_status()

    data = response.json()

    return data["title"], data["extract"]


def get_temperature(city, api_key):
    """Dohvaća trenutnu temperaturu grada."""

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "APPID": api_key,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 404:
        return None

    if response.status_code == 401:
        raise ValueError("API ključ nije ispravan ili nije aktiviran.")

    response.raise_for_status()

    data = response.json()

    return data["main"]["temp"]


def save_to_file(city, summary, temperature):
    """Sprema podatke u tekstualnu datoteku."""

    filename = f"{city}.txt"

    # Prelomi tekst na 80 znakova po retku radi bolje čitljivosti
    formatted_summary = textwrap.fill(summary, width=80)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"{city}\n")
        file.write("=" * len(city))
        file.write("\n\n")
        file.write(formatted_summary)
        file.write("\n\n")
        file.write(
            f"Current temperature in {city} is {temperature} degrees Celsius."
        )

    return filename


def main():

    if not WEATHER_API_KEY:
        print("Greška: OPENWEATHER_API_KEY nije pronađen u .env datoteci.")
        return

    city = input("Unesite ime grada: ").strip()

    if not city:
        print("Greška: Niste unijeli ime grada.")
        return

    try:
        # Dohvati podatke s Wikipedije
        official_name, summary = get_city_summary(city)

        if summary is None:
            print(f"Greška: Grad '{city}' nije pronađen.")
            return

        # Koristi službeni naziv grada za dohvat temperature
        temperature = get_temperature(official_name, WEATHER_API_KEY)

        if temperature is None:
            print(f"Greška: Grad '{official_name}' nije pronađen.")
            return

        filename = save_to_file(
            official_name,
            summary,
            temperature,
        )

        print(f"Uspjeh! Stvorena je datoteka '{filename}'.")

    except ValueError as error:
        print(f"Greška: {error}")

    except requests.exceptions.ConnectionError:
        print("Greška: Nemate internetsku vezu ili je poslužitelj nedostupan.")

    except requests.exceptions.Timeout:
        print("Greška: Zahtjev je potrajao predugo (Timeout).")

    except requests.exceptions.RequestException as error:
        print(f"HTTP greška: {error}")

    except Exception as error:
        print(f"Došlo je do neočekivane greške: {error}")


if __name__ == "__main__":
    main()