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