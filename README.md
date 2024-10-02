# Server-inventory
[Link til issue](https://github.com/orgs/Randers-Kommune-Digitalisering/projects/16/views/1?pane=issue&itemId=70099167)

# Formål med projektet
Dette projekt har til formål at visualiserer følgende data
* Diskplads
* Installerede programmer
* Installerede Certifikater
* Services
* System Info(Last Boot Up Time)
* Share Access Info(Shares)
* Auto Run Info
* Installed Updates
* Local Users
* UserProfileList


## Connect til MSSQL Databasen
Følgende ENV variables indsættes. Disse findes inde på Bitwarden
* DB_HOST
* DB_USER
* DB_PASS
* DB_NAME

For at connecte til databasen lokalt kan man anvende forskellige database værktøjer(```Azure Data Studio & DBrever```). 

Hvis man vil forbinde til Databasen med Azure Data Studio køres følgende commando i CMD:
``` runas /netonly /user:laksen04\svc-server-inventory "<path to Azure Data Studio>```

## Køresel af main.py
* Start applikationen: ```streamlit run main.py```