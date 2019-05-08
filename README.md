# pyPrintHelper
### Tool für den Raspi zum Drucken von PDFs

Der kleine Helper verbindet sich zu einem MQTT Broker und empfängt von diesem Druckaufträge.
Diese werden via `lp` Kommando an den Drucker geschickt. Die Datei wird anschließend gelöscht.

Verwendung:
`main.py -u <user> -c <password> -h <host> -p <port> -t <topic>`

Der Druck erfolgt mit dem im Raspi konfiguriertem Standard-Drucker.

