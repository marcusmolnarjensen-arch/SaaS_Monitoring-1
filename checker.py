
import os
import requests
import psycopg
import time
from dotenv import load_dotenv

load_dotenv("password.env")

connection = psycopg.connect(
    host=os.environ.get("POSTGRES_HOST"),
    port=os.environ.get("POSTGRES_PORT"),
    dbname=os.environ.get("POSTGRES_DB"),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD")
)

print("Connexion à PostgreSQL réussie !")

websites_name = [
    "youtube.com",
    "yahoo.com",
    "google.com",
    "bing.com",
    "siteinexistant.com"
]

while True:
    for website_name in websites_name:
        try:
            response = requests.get("https://" + website_name, timeout=10)

            status_code = response.status_code
            response_time = response.elapsed.total_seconds() * 1000

            is_online = True
            is_healthy = status_code == 200

            print(website_name)
            print(status_code)
            print(round(response_time, 2))
            print("Online:", is_online)
            print("Healthy:", is_healthy)

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO monitoring_results
                (website_url, status_code, is_online, response_time_ms, is_healthy)
                VALUES (%s, %s, %s, %s, %s)
                """,
                ("https://" + website_name, status_code, is_online, round(response_time), is_healthy)
            )

            connection.commit()
            cursor.close()

            print("Résultat enregistré dans PostgreSQL !")
            print("----------------")

        except requests.exceptions.RequestException:
            print(website_name)
            print("Online: False")
            print("Healthy: False")

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO monitoring_results
                (website_url, status_code, is_online, response_time_ms, is_healthy)
                VALUES (%s, %s, %s, %s, %s)
                """,
                ("https://" + website_name, None, False, None, False)
            )

            connection.commit()
            cursor.close()

            print("Échec enregistré dans PostgreSQL !")
            print("----------------")

    print("Prochaine vérification dans 60 secondes...")
    time.sleep(60)
