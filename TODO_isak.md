## Isaks dagbok

**Tisdag själv den 20 aug**
- I docker-compose.yaml på rad 53 av-kommenterade jag "build: .", detta löste äntligen problemet jag haft med att compose inte ville ta med min pyproject.toml och därmed inte heller skapa en requirements.txt.
- Jag måste dock läsa på mer om Poetry då jag inte riktigt förstår varför allt verkar köras i python=3.12.5, men vissa commands ger error *Current Python version (3.12.5) is not allowed by the project (~3.10).* Initiellt googlande på detta pekar på att vissa dependencies bygger på python3.10 (typ pytest).
- inuti airflow i terminalen blir jag ibland utlåst när jag försöker se poetrys olika resurser: *sh: 4: poetry: Permission denied*. Jag har inte hittat varför, och det känns rätt slumpmässigt.
- Jag la till *RUN poetry self update* i Dockerfile, vilket visade sig vara entrén till ett kaninhål av versionsproblematik. Ska man fortsätta lappa tills det håller? Delvis hjärtat av problemet verkar vara att python och airflow enligt uppgift ska vara i senaste version. Detta skapar sedan sprickor som leder till sprickor som leder till sprickor.

**Onsdag 21 aug själv**
- Börjar dagen med att testa sätta 'dependency'="latest" ("*" verklar inte fungera så letar efter senaste på pypi) på allt som har fått många nya uppdateringar över det som stod i original i en kopia av pyproject.toml, som jag för tillfället döper om. (Ändrar inte heller openai och langchain då jag haft mycket problem med förändringen av syntax från olika versioner med just dem.)
- Jag trial&error-ar tills jag får docker compose build att rulla utan error.
- Hittar att python=3.12 inte installerar setuptools automatiskt... Lägger till i Dockerfile.
- Efter MYCKET pill med att få 3.12 att fungera utan framgång (läser mig fram till att det har något att göra med Airflows installation av numpy, men inget om hur man ändrar det i uruppförandet av dockern) så testar jag att sätta python=3.11, och då rullar allt som det ska. **FRÅGA RAPHAEL VAD SOM MENAS MED "SENASTE VERSIONEN"!**
- Allt rullar. MEN. Jag har inga permissions inne i airflow genom terminalen som handlar om Poetry. Kanske inte behövs? Men känns sisådär. Bör nog lämna det nu iaf då man suttit med nån timma.
- Allt som allt så tror jag jag gjort tillräckligt för vårt möte imorgonbitti, där jag onekligen kommer själv, eller få hjälp på vägen, inse fler brister i mitt tillvägagångssätt.

**Torsdag 22aug tillsammans**
- Beslut fattades att poetry är bajs i detta projekt. Nu gör vi vår egen requirements.txt och kör på pip!
- Det rullar både i build ich airflow, men i airflow är det fortfarande svårt att se vilka dependancies som installerats. "pip list" listar en annan uppsättning paket än de som vi installerat med requirements.txt
- LYCKA! Att avkommentera rad 52 i docker-compose.yaml (image:...) gjorde att vår pip installerade paketen på rätt ställe i pip list inne i vår airflow env.

**Torsdag 22aug själv**
- Jag branchar av för att testa hur @dags skulle kunna komma att bli implementerade.
- Mappen newsfeed med all kod kopieras tillfälligt in i dags-mappen för att smidigare kunna hänvisa till koden.
- Först testas bara att jag kan få upp i webinterfacet min test-dag. Det går bra.
- download_blogs_from_rss verkar också hyffsat enkelt rulla som importerade script i en @task.
- Lite strul dock med extract_articles; filer skapas, men inget landar i sista steget i .json-filen.
- Jag löste ovanstående med att justera pydantic syntax i datatypes.py med hjälp av googling. dump_args var en funktion som försvunnit.

**Fredag 23aug själv**
- Jag är sugen på att testa langchain och openai summarize.py. Jag börjar därför med att testa om systemet godkänner att jag använder orginalversionerna från projektet; langchain=0.0.221 och openai=0.27.8.
- Det blev helt kaiko. Jag väljer istället att använda de senaste versionerna i utbyte mot den antagliga oundvikliga huvudvärken senare.
- Något som saknas är langchain-community. Detta läggs till i requirements.txt.
- Mer pydantic problematik! I v2 av pydantic finns ej längre parse_file_as(). Hittade denna fantastiska sida https://docs.pydantic.dev/latest/migration/#removed-in-pydantic-v2, men som inte hjälper mig just nu. Istället hittar jag en annan lösning på github.
- Bra med .env-filer såklart. Men irriterande att inte kunna hitta en bra guide på syntax då inga exempel ligger uppe.
- Nyckeln läses till sist korrekt, och summeringen fungerar väl. Kommenterade bort article = article[1:] och insåg direkt varför den fanns där.... Detta tar ett tag.
- Insåg även att i min @dag behöver jag inte retunera något från @task funktionerna. Utan det räcker gott att endast köra main() från varje fil.
- Summarize.py fungerar nu i min test @dag.

**Lördag 24aug själv**
- Har inget annat för mig så fortsätter kolla lite.
- Lämnar allt gällande s3 osv så länge, då det verkade som Kevin kommit långt med det redan.
- Jag undersöker lite hur web-hooks fungerar, och om jag kan göra en disc bot i min egna disc.
- Spännande. Hittils har jag gått tillväga att bara kalla på funktioner i min @dag, men send_to_disc.py fungerar direkt utan någon RaisedError. Jag får börja någon annanstans.
- Bra läsning för detta: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
- OOf. Det gick mer tid än vad jag vill erkänna till att hitta vad som faktiskt var problemet. Men efter många tillagda logger.debug() hittade jag tillslut det übersimpla felet att funktionen load_summaries letar efter dem i fel mapp!! Hmm, undra om det kanske är någon lärare som försökt lägga lite fälleben här hehe.
- Dock ska väl så snart vi implementerar s3 det ändå ändras till något annat värde.
- Jag behövde även fippla lite med att få dotenv() att läsa webhook url korrekt.
- Löste ovanstående med att importera os.environ.
- Nästa problem. openai är lite långsam. Hur ser vi till att summeringarna hinner komma från openai innan de skickas till discord?
- Mycket intressant diskussion i ämnet: https://stackoverflow.com/questions/55002234/apache-airflow-delay-a-task-for-some-period-of-time
- Dock var inte länken ändå vad jag var ute efter. Airflows egna dokumentation vissade hur man enkelt kunde anävnda >> för att påvisa ordning. Och den verkar vänta på openai på korrekt sätt nu!