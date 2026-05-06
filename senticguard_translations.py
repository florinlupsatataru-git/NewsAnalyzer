# senticguard_translations.py

TRANSLATIONS = {
    "RO": {
        "sidebar_title": "SenticGuard Web v3.1",
        "lang_select": "Alege Limba / Select Language",
        "main_title": "SenticGuard AI",
        "sub_title": "Integritate Media și Analiză Deep",
        "system_desc": "SenticGuard este un sistem inteligent conceput pentru a identifica tiparele de manipulare emoțională, senzaționalism și dezinformare din fluxurile de știri din România, utilizând tehnologia NLP.",
        "tab_link": "Link Articol",
        "tab_manual": "Text Manual",
        "url_label": "URL Articol:",
        "manual_label": "Titlu / Paragraf:",
        "analyze_btn": "Analizează",
        "reset_btn": "Reset",
        "success_load": "Articol detectat: ",
        "error_load": "Eroare de acces: ",
        "warn_no_input": "Te rugăm să introduci date în câmpul selectat.",
        "confidence": "ÎNCREDERE MODEL:",
        "deep_title": "Deep Analysis: Titlu vs. Conținut",
        "deep_analysis": "Analiză Conținut",
        "mismatch": "Atenție: Discrepanță detectată între tonul titlului și cel al conținutului.",
        "match": "Tonul titlului corespunde cu cel al conținutului.",
        "categories": {
            "OBIECTIV": "Informație neutră, bazată pe fapte verificabile.",
            "ALARMIST": "Titlu care induce panică sau teamă exagerată.",
            "SENZATIONAL": "Creat special pentru a atrage atenția prin exagerări.",
            "CONFLICTUAL": "Subliniază dispute sau tensiuni sociale.",
            "INFORMATIV": "Conținut util, ghiduri sau explicații.",
            "OPINIE": "Punct de vedere subiectiv sau analiză."
        }, 
        "labels_map": {
            "OBIECTIV": "obiectiv",
            "ALARMIST": "alarmist",
            "SENZATIONAL": "senzațional",
            "CONFLICTUAL": "conflictual",
            "INFORMATIV": "informativ",
            "OPINIE": "de opinie"
        },
        "phrases": {
            "match_high": [
                "Articolul păstrează un ton {label_v} de la început până la final fără să prezinte variații de stil.",
                "Întreaga știre este construită într-un stil {label_v} care se regăsește în toate secțiunile textului.",
                "Mesajul este prezentat pe un ton marcat clar ca fiind unul {label_v}.",
                "Titlul și conținutul se încadrează ambele în categoria {label_v}.",
                "Analiza confirmă un mod de redactare constant {label_v} pe tot parcursul acestui material.",
                "Un material unitar unde atât titlul cât și corpul știrii sunt {label_v}.",
                "Conținutul este unul {label_v} iar această trăsătură este vizibilă în întreg textul.",
                "Textul nu prezintă schimbări de abordare și rămâne în stilul {label_v} până la final.",
                "Evaluarea indică o structură clară care este specifică unui material de tip {label_v}.",
                "Titlul reprezintă corect substanța articolului deoarece ambele sunt tipic {label_v}."
            ],
            "match_low": [
                "Articolul pare să adopte o direcție {label_v} deși tonul general este unul destul de reținut pe tot parcursul textului.",
                "Analiza sugerează un stil predominant {label_v} însă nuanțele nu sunt suficient de pronunțate pentru un verdict cert.",
                "Materialul înclină spre zona {label_v} chiar dacă abordarea autorului rămâne una destul de neutră în anumite fragmente.",
                "Se observă o ușoară tentă {label_v} care pare să definească întreaga structură a acestui conținut.",
                "Textul pare a fi unul de tip {label_v} dar intensitatea mesajului este mai mică decât în cazul unor materiale similare.",
                "Există indicii care trimit spre un stil {label_v} fără ca acesta să fie unul extrem de evident la prima lectură.",
                "Abordarea pare să fie una {label_v} însă limbajul folosit este destul de nuanțat în majoritatea paragrafelor.",
                "Dacă evaluăm tonul general, acesta tinde spre zona {label_v} deși păstrează un caracter destul de echilibrat.",
                "Există o nuanță {label_v} care s-ar putea regăsi în modul în care sunt prezentate informațiile.",
                "Articolul pare să se încadreze în zona {label_v} chiar dacă nu prezintă trăsături foarte clare."
            ],
            "mismatch_high": [
                "Deși titlul pare mai degrabă {label_s}, conținutul este în mod evident unul {label_v}.",
                "Sub un titlu care sugerează stilul {label_s} articolul dezvoltă de fapt o perspectivă {label_v}.",
                "Chiar dacă titlul este formulat ca fiind {label_s} textul indică un caracter {label_v}.",
                "Titlul înclină spre zona {label_s} însă corpul știrii rămâne unul predominant {label_v}.",
                "Dincolo de eticheta {label_s} a titlului fondul acestui articol este în esență unul {label_v}.",
                "Deși prima impresie creată de titlu este de tip {label_s} conținutul se dovedește a fi {label_v}.",
                "Observăm o nuanță de {label_s} la nivel de titlu dar mesajul principal rămâne cel {label_v}.",
                "Articolul folosește un titlu de tip {label_s} dar textul propriu-zis este scris într-o manieră {label_v}.",
                "În ciuda modului {label_s} în care este prezentat titlul analiza indică un material clar {label_v}.",
                "Titlul pare să facă parte din categoria {label_s} dar substanța articolului este una de tip {label_v}."
            ],
            "mismatch_low": [
                "Deși titlul ar putea sugera o notă de {label_s} textul pare să încline mai degrabă spre un stil {label_v}.",
                "Există o ușoară ambivalență între titlul {label_s} și restul articolului care pare să fie totuși unul {label_v}.",
                "Chiar dacă prima impresie indică stilul {label_s} conținutul pare să dezvolte o perspectivă ceva mai apropiată de {label_v}.",
                "Titlul pare formulat pentru a indica un ton {label_s} însă analiza textului sugerează mai degrabă un caracter {label_v}.",
                "Se simte un contrast fin între titlul {label_s} și corpul știrii care tinde să rămână în zona {label_v}.",
                "Analiza indică o anumită discrepanță deoarece titlul pare {label_s} însă restul materialului înclină ușor spre zona {label_v}.",
                "Există posibilitatea ca titlul să fi fost ales pentru un efect de tip {label_s} chiar dacă substanța articolului tinde spre un ton {label_v}.",
                "Sistemul detectează o nuanță de {label_s} în prezentare, dar parcurgerea textului sugerează mai degrabă un caracter {label_v}.",
                "Deși forma de expunere din titlu pare a fi {label_s} mesajul de fond pare să se apropie ceva mai mult de categoria {label_v}.",
                "Articolul balansează între un titlu de tip {label_s} și un conținut care pare să aibă totuși o tentă predominant {label_v}."
            ]
        }
    },
    "EN": {
        "sidebar_title": "SenticGuard Web v3.1",
        "lang_select": "Select Language",
        "main_title": "SenticGuard AI",
        "sub_title": "Media Integrity & Deep Analysis",
        "system_desc": "SenticGuard is an intelligent system designed to identify patterns of emotional manipulation, sensationalism, and disinformation in Romanian news feeds using NLP technology.",
        "tab_link": "Article Link",
        "tab_manual": "Manual Text",
        "url_label": "Article URL:",
        "manual_label": "Title / Paragraph:",
        "analyze_btn": "Analyze",
        "reset_btn": "Reset",
        "success_load": "Article detected: ",
        "error_load": "Access error: ",
        "warn_no_input": "Please provide input for the selected mode.",
        "confidence": "MODEL CONFIDENCE:",
        "deep_title": "Deep Analysis: Title vs. Content",
        "deep_analysis": "Content Analysis",
        "mismatch": "Attention: Discrepancy detected between title and content tone.",
        "match": "Title tone matches the content tone.",
        "categories": {
            "OBIECTIV": "Neutral info, based on verifiable facts.",
            "ALARMIST": "Headlines designed to induce panic or fear.",
            "SENZATIONAL": "Content crafted to attract attention through exaggerations.",
            "CONFLICTUAL": "Highlights disputes or social tensions.",
            "INFORMATIV": "Useful content, guides or explanations.",
            "OPINIE": "Subjective viewpoint or personal analysis."
        },
        "labels_map": {
            "OBIECTIV": "objective",
            "ALARMIST": "alarmist",
            "SENZATIONAL": "sensational",
            "CONFLICTUAL": "conflictual",
            "INFORMATIV": "informative",
            "OPINIE": "opinion"
        },
        "phrases": {
            "match_high": [
                "The article maintains a {label_v} tone from beginning to end without presenting any style variations.",
                "The entire news story is built in a {label_v} style that is found in all sections of the text.",
                "The message is presented in a tone clearly marked as being one {label_v}.",
                "The title and content both fall into the {label_v} category.",
                "The analysis confirms a constant {label_v} writing style throughout this material.",
                "A unitary material where both the title and the body of the news story are {label_v}.",
                "The content is one {label_v} and this feature is visible throughout the text.",
                "The text does not present any changes in approach and remains in the {label_v} style until the end.",
                "The evaluation indicates a clear structure that is specific to a material of type {label_v}.",
                "The title correctly represents the substance of the article because both are typically {label_v}."
            ],
            "match_low": [
                "The article seems to adopt a {label_v} direction although the general tone is quite restrained throughout the text.",
                "The analysis suggests a predominant {label_v} style but the nuances are not pronounced enough for a definite verdict.",
                "The material leans towards the {label_v} area even though the author's approach remains quite neutral in certain fragments.",
                "A slight {label_v} tinge is observed that seems to define the entire structure of this content.",
                "The text seems to be of the {label_v} type but the intensity of the message is lower than in the case of similar materials.",
                "There are indications that point towards a {label_v} style without it being extremely obvious at first reading.",
                "The approach seems to be a {label_v} one but the language used is quite nuanced in most paragraphs.",
                "If we evaluate the general tone, it tends towards the {label_v} area although it retains a fairly neutral character balanced.",
                "There is a {label_v} nuance that could be found in the way the information is presented.",
                "The article seems to fall into the {label_v} area even though it does not present very clear features."
            ],
            "mismatch_high": [
                "Although the title seems more {label_s}, the content is clearly {label_v}.",
                "Under a title that suggests {label_s} style, the article actually develops a {label_v} perspective.",
                "Even though the title is phrased as {label_s} the text indicates a {label_v} character.",
                "The title leans towards {label_s} but the body of the news remains predominantly {label_v}.",
                "Beyond the {label_s} label of the title, the substance of this article is essentially {label_v}.",
                "Although the first impression created by the title is of {label_s} type, the content turns out to be {label_v}.",
                "We notice a shade of {label_s} at the title level but the main message remains {label_v}.",
                "The article uses a {label_s} title but the actual text is written in a {label_v} manner.",
                "Despite the {label_s} way the title is presented indicates a clear {label_v} material.",
                "The title seems to be in the {label_s} category but the substance of the article is {label_v}."
            ],
            "mismatch_low": [
                "Although the title might suggest a note of {label_s} the text seems to lean more towards a {label_v} style.",
                "There is a slight ambivalence between the title {label_s} and the rest of the article which nevertheless seems to be a {label_v} one.",
                "Even though the first impression indicates a {label_s} style the content seems to develop a perspective somewhat closer to {label_v}.",
                "The title seems formulated to indicate a {label_s} tone but the analysis of the text suggests rather a {label_v} character.",
                "There is a subtle contrast between the title {label_s} and the body of the news which tends to remain in the {label_v} area.",
                "The analysis indicates a certain discrepancy because the title seems {label_s} but the rest of the material leans slightly towards the {label_v} area.",
                "There is a possibility that the title was chosen for a {label_s} effect even though the substance of the article tends towards a {label_v}.",
                "The system detects a shade of {label_s} in the presentation, but the text scan suggests a more {label_v} character.",
                "Although the form of exposition in the title seems to be {label_s} the underlying message seems to be somewhat closer to the {label_v} category.",
                "The article balances between a {label_s} title and a content that still seems to have a predominantly {label_v} tone."
            ]
        }
    }
}
