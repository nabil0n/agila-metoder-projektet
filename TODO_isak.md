1. Undersök och utvärdera docker-compose.yaml
    - Den rullar, men på rätt sätt?
    - Behöver vi lägga till något?

2. Undersök och utvärdera Dockerfile
    - Versioner?
    - Poetry?
    - requirements.txt?



---

Saker jag gjort / tänkt på:

**Tisdag kväll den 20 aug**
- I docker-compose.yaml på rad 53 av-kommenterade jag "build: .", detta löste äntligen problemet jag haft med att compose inte ville ta med min pyproject.toml och därmed inte heller skapa en requirements.txt.
- Jag måste dock läsa på mer om Poetry då jag inte riktigt förstår varför allt verkar köras i python=3.12.5, men vissa commands ger error *Current Python version (3.12.5) is not allowed by the project (~3.10).* Initiellt googlande på detta pekar på att vissa dependencies bygger på python3.10 (typ pytest).
- inuti airflow i terminalen blir jag ibland utlåst när jag försöker se poetrys olika resurser: *sh: 4: poetry: Permission denied*. Jag har inte hittat varför, och det känns rätt slumpmässigt.
- Jag la till *RUN poetry self update* i Dockerfile, vilket visade sig vara entrén till ett kaninhål av versionsproblematik. Ska man fortsätta lappa tills det håller? Delvis hjärtat av problemet verkar vara att python och airflow enligt uppgift ska vara i senaste version. Detta skapar sedan sprickor som leder till sprickor som leder till sprickor.

**Onsdag 21 aug**
- Börjar dagen med att testa sätta 'dependency'="latest" ("*" verklar inte fungera så letar efter senaste på pypi) på allt som har fått många nya uppdateringar över det som stod i original i en kopia av pyproject.toml, som jag för tillfället döper om. (Ändrar inte heller openai och langchain då jag haft mycket problem med förändringen av syntax från olika versioner med just dem.)
- Jag trial&error-ar tills jag får docker compose build att rulla utan error.
- Hittar att python=3.12 inte installerar setuptools automatiskt... Lägger till i Dockerfile.
- Efter MYCKET pill med att få 3.12 att fungera utan framgång (läser mig fram till att det har något att göra med Airflows installation av numpy, men inget om hur man ändrar det i uruppförandet av dockern) så testar jag att sätta python=3.11, och då rullar allt som det ska. **FRÅGA RAPHAEL VAD SOM MENAS MED "SENASTE VERSIONEN"!**
- Allt rullar. MEN. Jag har inga permissions inne i airflow genom terminalen som handlar om Poetry. Kanske inte behövs? Men känns sisådär. Bör nog lämna det nu iaf då man suttit med nån timma.
- Allt som allt så tror jag jag gjort tillräckligt för vårt möte imorgonbitti, där jag onekligen kommer själv, eller få hjälp på vägen, inse fler brister i mitt tillvägagångssätt.

**Torsdag 22aug tillsammans**
- Beslut fattades att poetry är bajs. Nu gör vi vår egen requirements.txt och kör på pip!
- Det rullar både i build ich airflow, men i airflow är det fortfarande svårt att se vilka dependancies som installerats. "pip list" listar en annan uppsättning paket än de som vi installerat med requirements.txt
- LYCKA! Att avkommentera rad 52 i docker-compose.yaml (image:...) gjorde att vår pip installerade paketen på rätt ställe i pip list inne i vår airflow env.

**Torsdag 22aug kväll**
- Jag branchar av för att testa hur @dags skulle kunna komma att bli implementerade.
- Mappen newsfeed med all kod kopieras tillfälligt in i dags-mappen för att smidigare kunna hänvisa till koden.
- Först testas bara att jag kan få upp i webinterfacet min test-dag. Det går bra.
- download_blogs_from_rss verkar också hyffsat enkelt rulla som importerade script i en @task.
- Lite strul dock med extract_articles; filer skapas, men inget landar i sista steget i .json-filen.
- Jag löste ovanstående med att justera pydantic syntax i datatypes.py med hjälp av googling. dump_args var en funktion som försvunnit.