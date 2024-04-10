DHBW Projekt für verteilte Systeme
Schreiben und Lesen einer RQLite Datenbank mit integriertem Interface
Messungen von Latenzzeiten

Start des Servers von folder 'client\app' aus mit: 
uvicorn main:app --reload

Starte die Clients mit python main.py

Gegebenenfalls ist es nötig Umgebungsvariablen anzulegen

Um den Test zu starten im Ordner stresstest:
locust -f locust_main.py

Wie das System zu verteilen ist:
- Einwählen
- Files kopieren: 
    scp -P 12221 -r controller pi@jukebox.dynalias.org:studienprojekte/smartcity/client
- Jetzt sind sie nur auf einem Server. Von diesem aus auf andere verteilen: 

- Starten:
    - uvicorn main:app --host 0.0.0.0 --port 8030 (anderen Port benutzen)
