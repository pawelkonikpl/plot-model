import csv

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


with open('ogloszenia.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Utwórz obiekt writer
    csv_writer = csv.writer(csvfile)

    # Zapisz nagłówki
    csv_writer.writerow(['Lokalizacja i data', 'Cena', 'Wielkość działki', 'Cena za metr', 'Url'])
    for page in range(1, 8):
        url = f"https://www.olx.pl/nieruchomosci/dzialki/zawoja/?min_id=889531105&page={page}&reason=observed_search&search%5Bdist%5D=30&search%5Border%5D=relevance%3Adesc#889015226"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Znajdź wszystkie ogłoszenia na stronie
            listings = soup.find_all('div', {'data-cy': 'l-card'})
            # Otwórz plik CSV do zapisu

            for listing in listings:
                # Pobierz lokalizację i datę
                base_url = listing.find('a').get('href')
                location_date = listing.find('p', {'data-testid': 'location-date'}).text.strip().split('-')[0]

                # Pobierz cenę
                price = listing.find('p', {'data-testid': 'ad-price'}).text.strip().split('zł')[0]

                # Pobierz wielkość działki
                size_with_prize = listing.find('div', {'color': 'text-global-secondary'}).text.strip()
                size = size_with_prize.split('-')[0].split('m')[0].strip()
                price_per_meter = size_with_prize.split('-')[1].split('zł')[0].strip()

                csv_writer.writerow([location_date, price, size, price_per_meter, base_url])

                # Wyświetl dane
                print("Lokalizacja i data:", location_date)
                print("Cena:", price)
                print("Wielkość działki:", size)
                print("Za metr działki:", price_per_meter)
            print("\n")

        else:
            print("Błąd podczas pobierania strony. Kod statusu:", response.status_code)