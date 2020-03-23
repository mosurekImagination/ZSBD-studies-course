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
 
## Wymagania:  
* Docker
* docker-compose
 
## Instrukcja użytkowania:  
* **Pierwsze uruchomienie:**  
  ```docker-compose up``` (Obraz zajmuje ponad 6 GB, więc pobieranie może trochę potrwać. Dodatkowo pierwsze uruchomienie zajmuje około 30 minut)
* **Połączenie z klientem lini komend z drugiego okna terminala:**  
  ```docker exec -ti <id_dockera> sqlplus usr/pwd@pdb```
* **Uruchomienie SQL z pliku**  
  ```docker exec -t <id_dockera> /bin/sh -c 'sqlplus usr/pwd@pdb < /opt/oracle/scripts/manual/transaction1.sql'  ```
* **Wykonywanie operacji na danych:**  
  Wprowadzanie poleceń SQL
* **Wyłączanie:**  
  CTRL + C lub docker-compose stop
* **Uruchamianie kolejny raz:**  
  ```docker-compose start```
* **Restart:**  
  ```docker-compose restart```
* **Usunięcie kontenerów i sieci Dockera:**  
  ```docker-compose down``` (Potem konieczne będze czekanie na "pierwsze" uruchomienie)
  
## Rozwijanie projektu:  
Dodawanie lub modyfikacja skrytptów z folderów setup (wykonywane raz przy pierwszym uruchomieniu) i startup (wykonywane przy każdym uruchomieniu, przy pierwszym też - po setup) i tym sposobem automatyzacja tworzenia, odświeżania danych i przebiegu testów, z przesyłaniem wyników na maszynę hosta, pod jednym poleceniem - docker-compose start

Skrypty umieszczane w folderach setup i startup powinny mieć liczbę na początku nazwy, ponieważ są uruchamiane alfabetycznie.
