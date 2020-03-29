# Aktywne reguly:
1.  Weryfikacja warunku wypożyczenia lub zwrócenia samochodu ze/do każdej aktywnej stacji minimum 10 razy w miesiącu:
	- **Opis:** Reguła służy sprawdzaniu czy stacje są aktywnie używane i wyłączanie nieużywanych
	- **Zdarzenia inicjujace:** Nowy miesiąc
	- **Warunki uruchomienia:** Tylko dla aktywnych stacji
	- **Dzialanie:** Sprawdzamy czy suma wypożyczeń i zwrotów dla stacji wynosi co najmniej 10, jeśli nie - zmieniamy status stacji na niedostępny
	- **Szacunek zlozonosci:** Zliczenie wierszy złączenia tabel CarStation i RentalHistory, modyfikacja części wierszy z tabeli CarStation
	- **Mechanizmy:** Asercje, triggery
1.  Zablokowanie możliwości wypożyczenia samochodu ze stacji poza godzinami otwarcia:
	- **Opis:** Reguła służy zablokowaniu wypożyczenia samochodu poza godzinami otwarcia stacji
	- **Zdarzenia inicjujace:** Dodanie nowego wiersza RentalHistory i ustawienie atrybutu avaliable tabeli Car na 'false'
	- **Warunki uruchomienia:** Czas wypożyczenia nie mieści się w godzinach otwarcia stacji
	- **Dzialanie:** Usuwamy dodany wiersz RentalHistory i ustawiamy pole avaliable spowrotem na 'true'
	- **Szacunek zlozonosci:** Porównanie atrybutów wiersza ze złączenia trzech tabel i modyfikacja jednego z atrybutów
	- **Mechanizmy:** Asercje, triggery
1.  Sprawdzenie warunku wypożyczenia samochodu przez użytkowników w okresie ostatnich 2 lat.
	- **Opis:** Reguła służy sprawdzeniu czy użytkownik wypożyczał samochód w okresie ostatnich dwóch lat
	- **Zdarzenia inicjujace:** W każdą sobotę o 2:00
	- **Warunki uruchomienia:** Uruchomienie bezwzględne
	- **Dzialanie:** Grupujemy wiersze tabeli RentalHistory, których end_date miesci sie w okresie dwóch lat od teraz ze względu na user_id. Wybieramy tylko te user_id, dla których liczba wypożyczeń jest równa 0.
	- **Szacunek zlozonosci:** Grupowanie jednej tabeli, ze względu na jeden atrybut ze sprawdzeniem warunku + Select z wyniku ze sprawdzeniem warunku
	- **Mechanizmy:** Asercje, triggery
