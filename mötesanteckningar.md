## Möte 20 aug

### Saker vi gjort

* Isak klonat repo, gett alla access
* Gått igenom koden
* Uppdaterat `docker-compose.yaml`, går att köra.

### Saker vi kommit fram till:

* Vi lär oss Poetry.
* Vi har möten 9- på tisdagar och torsdagar, med möjlighet att ansluta övriga vardagar.
* Gå in på pytorch, lär dig grunderna.
* Hett tips: Kolla in airflowgrejen Isak tipsade om
* Vi ska skriva en eller flera DAGs enligt Tasks. Dessa DAGs behöver bara importera .py-filerna för sin funktionalitet.
* Vi döper våra branches efter våra tasks.

### Ansvarsområden / tasks

* Isak: Porta `docker-compose.yml`, `Dockerfile`
* Kevin: Gör kompatibel med Amazon S3
* Mikael: Skriva tester med pytest t.ex. och kolla så att .py-filerna funkar
* Max: Undersök hur discordbotten fungerar
* Joakim: Undersök databashanteringen

## Möte 22 aug

### Saker vi gjort

* Isak har mergat in det vi gjorde idag i main, så att rätt image används i airflow och alla dependencies installeras
* Mikael gjort klart testcases.

### Ansvarsområden / tasks

* Alla sysslar nu med någon form av DAG-implementering. Alla testar sig fram lite till nästa gång, då vi mergar det bästa av våra lärdomar.

## Möte 27 aug
* Isak fått DAGS att funka. 
* Kevin undersöker A3
* Max har fått Discrod bott med tidräkning att fungera.
* Mikael undersökte också DAGs och fick daggen att starta.
* Joakim har undersökt databashanteringen lite

### Möte med Raphael
* Hur göra för att inte köra över varandra om man ska jobba på typ samma sak? Antingen 1) Bryta ner i mindre tasks 2) Parprogrammera 3) Sitta och vänta.
Agila metoder ska åtgärda så att man utnyttjar tiden, får planera om. 
"Sprint-abort" i nödfall om det inte går.
* På Ericsson firas man med tårta om man gör mer än man hade som task
* Vid mergekonflikt bör man pausa och gå o prata med den andra personen som jobbat på samma sak, istället för att trycka på commit.

### Idéer för att fortsätta förfina: 
* Gör Unique_id till samma i både sammanfattning och bloggartikel, om strängen finns i original xml som man laddar ner. Om inte, se till att inte ladda ner samma igen på annat sätt. Eller?: Max
* Gör även en icke-teknisk sammanfattning: Isak
* Lägg in ytterligare en blogg eller tre att sammanfatta från: Isak 
* Få DAGs att hitta newsfeed från src/newsfeed: Mikael
* Få databasen att fungera. Den ska även fungera inifrån DAG: Kevin

## Möte 3 sep

### Genomgång av aktivitet sedan sist
* Isak har fått jmlr att fungera, men bara för description
* Även fått den att göra non technical summary (återtstår - lagra i databasen som non technical summary)
* Kevin: Research - Både data lake och data warehouse finns i bucket. Boto3 är Amazons serviceklient.
  - Localstack är separat, som bara bygger upp en utvecklingsmiljö. Går inte att ha understreck, måste vara bindestreck.

### Gjort tillsammans
* Merga in Kevins databashantering i main.

## Uppgifter till nästa gång
- Isak: Undersöka precommit hooks, inklusive formattering.
- Joakim: Fixa så att datan lagras i data lake istället för lokala .json-filer.
- Mikael fortsätter
- Skriva dokumentation? 