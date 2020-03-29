# Środowisko obejmuje Oracle Database 19.3 Enterprise Edition zainstalowaną wraz z zależnościami na Oracle Linux

## Zawartość:  
* plik **docker-compose.yml** - Konfiguracja kontenera Dockera  
* folder **setup** - Skrypty .sh i .sql uruchamiane po instalacji bazy danych  
   * plik **01_user.sql** - Skrypt tworzący i konfigurujący użytkownika dla bazy danych  
* folder **startup** - Skrypty .sh i .sql uruchamiane przy każdym uruchomieniu bazy danych  
   * pliki **01_*.sql** - Pliki usuwające i tworzący od nowa tabele i wiersze
   * plik **02_shellExample.sh** - Przykładowy plik stanowiący wzór do przyszłej implementacji skryptów w Bashu
* folder **manual** - Skrypty .sh i .sql uruchamiane manualnie, np. z poziomu skryptu uruchamianego przy starcie bazy danych  
* folder **oradata** - Folder tworzony przy starcie kontenera, nie dodawany do repozytorium (jest w .gitignore). Zawiera pliki bazy danych z kontenera
* folder **dump** - zawiera plik schema_dump.dmp z danymi do bazy

Skrypty umieszczane w folderach **setup** i **startup** powinny mieć liczbę na początku nazwy,
 ponieważ są uruchamiane alfabetycznie.

## Wymagania:  

* Linux (rekomendowany Vagrant z obrazem [jhipster-devbox](https://github.com/jhipster/jhipster-devbox))
* Docker
* docker-compose
* Python3 & pip3
* [Oracle Instant Client Basic](https://www.oracle.com/database/technologies/instant-client.html)
 
## Instrukcja użytkowania dockera:  
* **Pierwsze uruchomienie:**  
  ```docker-compose up``` (Obraz zajmuje ponad 6 GB, więc pobieranie może trochę potrwać. Dodatkowo pierwsze uruchomienie zajmuje około 30 minut)
* **Połączenie z klientem lini komend z drugiego okna terminala:**  
  ```docker exec -ti <id_dockera> sqlplus usr/pwd@pdb```
* **Uruchomienie SQL z pliku**  
  ```docker exec -t <id_dockera> /bin/sh -c 'sqlplus usr/pwd@pdb < /opt/oracle/scripts/manual/transaction1.sql'  ```
* **Uruchomienie SQL**  
  ```docker exec -t <id_dockera> /bin/sh -c 'echo "SELECT * FROM CAR;" | sqlplus usr/pwd@pdb'  ```
* **Wyłączanie:**  
  CTRL + C lub docker-compose stop
* **Uruchamianie kolejny raz:**  
  ```docker-compose start```
* **Restart:**  
  ```docker-compose restart```
* **Usunięcie kontenerów i sieci Dockera:**  
  ```docker-compose down``` (Potem konieczne będzie czekanie na "pierwsze" uruchomienie)
  
## Data Pump

Data Pump to narzędzie rekomendowane przez Oracle do importownaia/eksportowania 
danych. 

W związku z tym, że wprowadzenie wszystkich danych do bazy za pomocą ```INSERT``` trwało ponad godzinę,
zostały one wyeksporotwane do pliku ```schema_dump.dmp```, który powinien znajdować się w folderze ```/dump```.

Dzięki Data Pump, import danych trwa około 7 sekund.


### Dump file

Zanim cokolwiek uruchomisz musisz pobrac ten plik do lokalizacji ```dump/schema_dump.dmp```

Dlaczego jest na ufile.io? Bo na githubie limit rozmiaru pliku to 100mb

```
https://ufile.io/attyn0lt
```

## Instrukcja użytkowania skryptu Python

### Funkcje skryptu

* bezpośrednie połączenie z bazą danych
* sprawdzenie poprawności wprowadzenia danych (na podstawie ilości wierszy)
* reinicjalizacja bazy danych (usunięcie i powtórny import danych)
* uruchomienie dowolnego polecenia SQL (funkcja ```execute_sql```)
* uruchomienie pliku SQL (funkcja ```execute_sql_file```)
* uruchomienie pliku JSON o strukturze (funkcja ```execute_transaction```:
```json
[
  {
    "name": "Firmy, które wykonały najwięcej zleceń w danym mieście, liczba i suma zleceń",
    "query": "WITH SQ1 AS(SELECT LOCATION.CITY, COMPANY.NAME, COUNT(INVOICE.ID) AS INVOICECOUNT, SUM(INVOICE.SUMMARY_COST) INVOICESUM FROM LOCATION JOIN COMPANY ON LOCATION.ID = COMPANY.LOCATION_ID JOIN INVOICE ON COMPANY.ID = INVOICE.COMPANY_ID GROUP BY LOCATION.CITY, COMPANY.NAME) SELECT SQ1.CITY, NAME, INVOICECOUNT, INVOICESUM FROM SQ1 JOIN (SELECT CITY, MAX(INVOICECOUNT) MAXINVOICECOUNT FROM SQ1 GROUP BY CITY) SQ2 ON SQ1.CITY = SQ2.CITY WHERE INVOICECOUNT = MAXINVOICECOUNT ORDER BY SQ1.CITY"
  },
  {
    "name": "Dodaj samochód stacji",
    "query": "UPDATE CAR SET CAR_STATION_ID=1 WHERE ID=1"
  }
]
```

* przeprowadzenie benchmarku polegającego na wielokrotnym uruchomieniu (domyślnie 20) zestawów danych z ```/manual```
    * minimalny, średni i maksymalny czas wykonania per zapytanie
    * minimalny, średni i maksymalny czas wykonania per zestaw
    
    
### Jak to wszystko uruchomić?

#### Przygotowanie środowiska
1. Zainstaluj python3 i pip3
1. Zainstaluj ```cx_Oracle``` - ```pip3 install cx_Oracle```
1. Zainstaluj [Oracle Instant Client Basic](https://www.oracle.com/database/technologies/instant-client.html)
1. Ustaw zmienną środowiskową ```LD_LIBRARY_PATH``` na folder instalacji Oracle Instant Client Basic - np. ```LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6```
1. Uruchom docker z bazą - ```docker-compose up``` z głownego folderu projektu

#### Uruchomienie benchmarków
1. Upewnij się, że docker z bazą działa: ```docker ps```
1. Jeżeli nie działa to ```docker-compose start```, jak go usunąłeś to ```docker-compose up```
1. Poczekaj, aż baza się uruchomi, najlepiej spróbuj połączyć się do niej
    ```
    docker exec -ti <id_dockera> sqlplus usr/pwd@pdb
    ```
1. Jeżeli udało się połączyć przejdź do folderu ```scripts``` i uruchom skrypt ```python3 one_click_script.py```
1. Benchmark powinien zostać uruchomiony