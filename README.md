DHBW Projekt für verteilte Systeme
Lesen einer Mongo-Datenbank mit integriertem Interface


Zunächst muss der HauptClient (Ordner client) auf den ersten Server kopiert werden. 
Hier in den Ordner app wechseln und mit dem Befehl:  
uvicorn main:app --host 0.0.0.0 --port 9023  
den Server starten. 
Der Client ist nun im Browser unter: http://10.8.0.1:9023/ zu finden. 

Nun werden controller1/2/3 auf den jeweiligen ersten zweiten und dritten Server kopiert. 
Diese werden einzeln mit: 
python main.py 
gestartet. 

Wird nun im Client der Get Latest Entry Button gedrückt wird eine Anfrage verteilt und das Ergebnis angezeigt. 

Tests lassen sich mit dem Kopieren des stresstest Ordners auf den ersten Server, mit dem Befehl: 
locust -P 9025 -f locust_main.py 
unter der URL 
http://10.8.0.1:9025/ 
starten. 


########################################################
Entwickler Hinweise
Start des Servers von folder 'client\app' aus mit: 
uvicorn main:app --reload

Starte die Clients mit python main.py

Gegebenenfalls ist es nötig Umgebungsvariablen anzulegen

Um den Test zu starten im Ordner stresstest:
locust -f locust_main.py

Wie das System zu verteilen ist:
- Routerzugriff:
    ssh pi@jukebox.dynalias.org -p 12221
    Vs24!DhWb20!

    Auf Server mit:
    ssh pi@192.168.180.65 (66/6)7
    login42
- Einwählen
- Files kopieren: 
    scp -P 12221 -r controller pi@jukebox.dynalias.org:studienprojekte/smartcity/client
- Auf anderen Server kopieren mit:
    scp -r controller2 pi@192.168.180.66:studienprojekte/smartcity/client
- Jetzt sind sie nur auf einem Server. Von diesem aus auf andere verteilen: 

- Starten:
    - uvicorn main:app --host 0.0.0.0 --port 9023 (anderen Port benutzen)
        Server ist im Browser unter: http://10.8.0.1:9023/ zu finden
    - Andere controller starten mit:
        python main.py
    - Test startem mit:
        locust -P 9025 -f locust_main.py
        unter: http://10.8.0.1:9025/

