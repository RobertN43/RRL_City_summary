import requests

# 1. Unos grada
city_name = input("Unesite ime grada: ").strip()

if not city_name:
    print("Greška: Niste unijeli ime grada!")
else:
    # Wikipedija Action API (puno stabilniji za specijalne znakove i dijakritiku)
    wiki_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,  # Uzmi samo uvodni sažetak
        "explaintext": True,  # Čisti tekst bez HTML oznaka
        "titles": city_name,
        "redirects": 1,  # Automatski preusmjeri (npr. ako netko napiše munich)
    }

    headers = {
        "User-Agent": "MojQAStudentProjekt/1.0 (kontakt_student@mojdomena.hr)"
    }

    response = requests.get(wiki_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        # Wikipedia API vraća stranice unutar rječnika s ID-em stranice
        page_id = list(pages.keys())[0]

        # Ako je ID "-1", stranica ne postoji
        if page_id != "-1":
            page = pages[page_id]
            title = page.get("title")
            extract = page.get("extract")

            if extract:
                print(f"\n--- SAŽETAK ZA: {title} ---")
                print(extract)
            else:
                print(
                    f"\nGreška: Pronađena je stranica '{title}', ali nema sažetka."
                )
        else:
            print(f"\nGreška: Grad '{city_name}' nije pronađen na Wikipediji.")
    else:
        print(
            f"\nDošlo je do greške pri dohvatu s Wikipedije (Kod: {response.status_code})."
        )