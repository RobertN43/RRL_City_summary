import os
import requests

# 1. Unos grada
city_name = input("Unesite ime grada: ").strip()

# 2. Wikipedia API URL
wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city_name}"

# 3. Postavljamo User-Agent zaglavlje (Wikipedia ovo obavezno traži)
headers = {"User-Agent": "MyQATestApp/1.0 (contact@example.com)"}

# 4. Šaljemo zahtjev s dodanim zaglavljem
response = requests.get(wiki_url, headers=headers)

# 5. Provjeravamo status
if response.status_code == 200:
    data = response.json()
    summary = data.get("extract")

    print("\n--- SAŽETAK S WIKIPEDIJE ---")
    print(summary)

elif response.status_code == 404:
    print(f"\nGreška: Grad '{city_name}' nije pronađen na Wikipediji.")
else:
    print(
        f"\nDošlo je do greške pri dohvatu s Wikipedije (Status kod: {response.status_code})."
    )