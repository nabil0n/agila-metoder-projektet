Detta repo innehåller en påhittad legacy produkt som ni i detta projekt skall uppdatera, dockerisera och sätta upp en ordentlig data pipeline till. De flesta av dessa första tasks kommer leda till nya tasks. Tidsuppskatta även de nya och synka prioritet med PO. 

Se till att utvecklingsmiljön använder ny/senaste docker, airflow och python. Notera att existerande kod inte går att köra i en docker-container med nuvarande versioner av airflow och alltså måste portas. En ytterligare notis är att äldre versioner använde kommandot `docker-compose`. Det har nu blivit `docker compose`. 


## STORY
```
Användaren vill kunna starta systemet via 'docker compose up'.
``` 
### Tasks
    · Undersök existerande airflow (`docker-compose.yml`) konfiguration och porta nödvändiga delar till senaste airflow `docker-compose.yaml`.
    · Skapa en ny airflow dockerfil som inkluderar nödvändig kod
    · Ändra data-lake hanteringen till S3 kompatibelt
    · Undersök databashanteringen i data warehouse koden


## STORY
    Vid ett givet tidsintervall skall de senaste bloggarna sammanfattas i en discord kanal
### Tasks
    · Undersök hur discordbotten fungerar
    · Undersök hur bloggarna hanteras (postas samma många ggr etc)
    · Skriv en eller flera airflow DAGs som:
        · Hämtar bloggar (Extract)
        · Sammanfattar bloggar (Transform)
        · Gör sammanfattningar tillgängliga (Load)
        · Skickar uppdateringar till discord