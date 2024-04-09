DHBW Projekt für verteilte Systeme
Schreiben und Lesen einer RQLite Datenbank mit integriertem Interface
Messungen von Latenzzeiten

Start des Servers von folder 'client\app' aus mit: 
uvicorn main:app --reload

Starte die Clients mit python main.py

Gegebenenfalls ist es nötig Umgebungsvariablen anzulegen

Um den Test zu starten im Ordner stresstest:
locust -f locust_main.py