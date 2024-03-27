# Lagerstyringssystem

## Lagerkoncept

Jeg har skabt en fiktiv boghandel, og de varer, som går ind på og ud fra lageret, er altså bøger. Bøgerne findes i tre forskellige medier: trykte bøger, lydbøger og e-bøger. Jeg valgte dette koncept for at give mig selv mulighed for at opsætte nogle rammer for mit lagerstyringssystem og dermed skabe en fleksible og dynamisk omend lukket kodestruktur.  
For enkelthedens skyld har jeg valgt at arbejde med et `stock` attribut for alle tre medier. Det er nok ikke helt realistisk, at alle lyd- og e-bøger indkøbes på begrænsede licenser og derfor har et `stock` attribut, men det har jeg altså valgt at se bort fra.

## Kodestruktur

Koden er opdelt i to primære filer: `classes.py` og `main.py`. De to filer har hver sine funktioner og hver sit "ansvar".

### `classes.py`

Her findes de Python-klasser, som lagerstyringssystemet er bygget op omkring. Se nærmere beskrivelse af de forskellige klasser nedenfor under **Lagersystemets opbygning**.

### `main.py`

Her findes en terminalmenu og funktioner, som kan bruges til at tilgå lagerstyringssystemet. Se nærmere beskrivelse nedenfor under **Interaktion med lagersystemet**.

## Lagersystemets opbygning

Lageret er bygget op omkring Python-klasser, som varetager hver deres opgaver og funktioner.

### `Book`

Dette er en `parent class` med tre `child classes`: `PrintedBook`, `Audiobook` og `EBook`. Der skabes ingen nye bog-objekter direkte fra selve `Book`-klassen. Alle nye bøger sorteres efter medie, når de tilføjes til lageret, og bog-objekterne skabes derefter ud fra den relevante `child` klasse.

### `PrintedBook`, `Audiobook` og `EBook`

Dette er de tre `child classes` til `Book`, som beskrevet ovenfor.

### `Factory`

Her behandles indkommen data om nye bøger, som skal tilføjes til lageret. Klassen har ansvar for at skabe det korrekte objekt baseret på den nye bogs medie, dvs. vælge mellem de tre `child classes`. Desuden har den ansvar for at sende information om nye bøger videre til lagerkataloget.

### `Catalogue`:

Her kan bøger tilføjes hhv. slettes fra lageret. Klassen har ansvar for alle søgefunktioner. Bøger kan søges frem fra kataloget vha. bogens id, forfatter, titel, kategori (fiction/non-fiction) og medie (printed/audio/e-book). Desuden rummer klassen en metode, som genererer sortede lister over alle bøger på lageret. Listen kan sorteres efter forfatter, titel, kategori, medie og lagerbeholdning (i opad- eller nedadgående orden).

## Interaktion med lagersystemet

Lagersystemet kan som beskrevet tilgås og afprøves via menuen i filen `main.py`. Kernen i menuen er funktionen `main`, som styrer selve hovedmenuen. Herfra kan brugeren vælge fire forskellige undermenuer: 'Add a new book', 'Search for a book', 'Delete a book' og 'Get reports on the bookstore's stock'. Hver undermenu styres af sin egen funktion, og når en undermenu forlades og afsluttes, bliver brugeren sendt tilbage til hovedmenuen. Nedenfor følger en mere detaljeret beskrivelse af de forskellige undermenuer.

### Menuen 'Add a new book'

Denne menu rummer to forskellige funktioner:

1. Bøger kan tilføjes til systemet fra en lokal fil, `books_data.csv`. Formålet med denne funktion er at give brugeren mulighed for initialt at tilføje noget data, så systemets øvrige funktioner kan afprøves.
2. Brugeren kan tilføje ny data til systemet. Den vil blive bedt om at indtaste alle nødvendige oplysninger, som så bliver sendt af sted til den relevante metode i lagerstyringssystemet, hvor bogen 'skabes' i systemet.

### Menuen 'Search for a book'

I denne menu kan brugeren søge i lagerkataloget ved at vælge en `query_type` og indtaste en `query_value`. Disse data sendes videre til den relevante metode i lagerstyringssystemet, som returnerer et søgeresultat.

### Menuen 'Delete a book'

Her kan en bog slettes fra kataloget/lageret. En bog, som anmodes slettet, identificeres via sit ID.

### Menuen 'Get reports on the bookstore's stock'

Her kan brugeren få genereret en inventarliste over alle bøger på lageret, sorteret efter brugerens ønske. Brugeren indtaster den ønskede sortering, som sendes af sted til den relevante metode i lagersystemet. Herfra returneres en sorteret inventarliste.

## Fremtidige forbedringer og udvidelser af funktionaliteten

Jeg ser mange muligheder for at forbedre og udvide funktionaliteten i mit program. Her følger nogle af dem:

### Flere og bedre rapporter

Lige nu kan der kun genereres sorterede lister over hele lagerbeholdningen. Derfor bør der udvikles flere typer af rapporter, fx opsummering af antal varer pr. kategori, medie eller målgruppe, antal unikke ID'er, varer med lagerbeholdning under en vis på forhånd defineret grænse, osv. Visse af disse rapporter bør kunne genereres vha. søgefunktionerne i `Catalogue`-klassen, eksempelvis ved at søge efter alle bøger i kategorien `fiction` og derefter tælle antallet af bøger i denne kategori.

### Transaktionssystem

Der bør skabes en transaktions-klasse, som varetager køb og salg af bøger. Her kan der skabes funktionalitet, som kigger på køb/salg over tid, indtjening (sammenligning af købs- og salgspris), osv. Dette transaktionssystem skal have adgang til at opdatere `Book`-klassens `stock`-attribut ved køb/salg. Desuden kan der skabes en rabatteringsfunktionalitet, som beregner en ny rabatteret pris vha. den oprindelige salgspris og eksempelvis en rabat i procent.

### Forbindelser mellem søgefunktioner og `Book`-klassens metoder

Der findes en række metoder i `Book`-klassen, som ikke er forbundet med resten af lagerstyringssystemet. De kan naturligvis i teorien tilgås og anvendes på et konkret bog-objekt, men de er ikke på nogen hensigtsmæssig måde knyttet sammen med eksempelvis søgefunktionerne. En udvidelse og forbedring af funktionaliteten kunne derfor være at skabe mulighed for at kalde disse metoder på de søgeresultater, som genereres i `Catalogue`-klassens søgemetoder.

### Test

Systemet kan forbedres gennem både unittests og end-to-end tests. Jeg har dog ingen erfaring med automatiserede tests, så det er et punkt på en fremtidig to-do-liste, som kræver en hel del forudgående læring fra min side.

## Ugens helt store ahaoplevelse

Før jeg startede på Specialisterne Academy, har jeg kun arbejdet med frontendudvikling. Jeg har været vant til at arbejde med fx integration af REST API'er i mine applikationer, men ikke med at bygge dem. Derigennem har jeg fået masser erfaring med fejlhåndtering af brugerinput, og den vanlige arbejdsgang har været at tjekke og validere brugerinput, før koden sender forespørgsler om data af sted til en API. Et konkret og virkeligt eksempel: Du får ikke lov til at trykke på den her knap, før du har indtastet den data, jeg skal bruge for at kunne sende dig videre i mit system.  
Til gengæld har jeg ingen som helst erfaring med at bygge fejlhåndtering ind i min kode, uden at have en brugerflade og nogle brugerinput at validere. Derfor var min umiddelbare tilgang til ugens opgave at bygge fejlhåndtering af brugerinput ind i mine menuer i terminalen. På den måde vidste jeg med sikkerhed, at de data – fx om nye bøger, køb og salg eller søgninger i kataloget – som blev sendt af sted til de relevante metoder i klasserne, var valide.  
Ahaoplevelsen bestod nu i, at jeg indså, at det ikke hjælper noget som helst at validere data indtastet i terminalen, eftersom mit lagerstyringssystem i et virkeligt scenarie aldrig ville blive tilgået via terminalen. Det ville snarere blive koblet til en brugerflade, som jeg fra min backendposition hverken har noget forhåndskendskab til eller nogen mulighed for at kontrollere. Derfor skal al fejlhåndtering i min kode naturligvis flyttes ind i klasserne/metoderne. Nu, når jeg har fattet det, er det jo indlysende, at det er sådan, jeg skal tænke og skrive min kode. Men eftersom jeg er vant til at tænke stik modsat og altid at have en bruger i tankerne, var det virkelig en form for åbenbaring at forstå, hvordan man arbejder med fejlhåndtering i backendudvikling. Om jeg er nået helt i mål i denne uge, ved jeg ikke. Men jeg har i hvert fald gjort mit bedste, og nu ved jeg, hvordan jeg i fremtiden skal tænke og arbejde.