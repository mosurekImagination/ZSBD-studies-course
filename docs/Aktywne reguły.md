# Aktywne reguly:
1.  Weryfikacja warunku wypożyczenia lub zwrócenia samochodu ze/do każdej aktywnej stacji minimum 10 razy w miesiącu:
	- **Opis:** Reguła służy sprawdzaniu czy stacje są aktywnie używane i wyłączanie nieużywanych
	- **Zdarzenia inicjujace:** Nowy miesiąc
	- **Warunki uruchomienia:** Tylko dla aktywnych stacji
	- **Dzialanie:** Sprawdzamy czy suma wypożyczeń i zwrotów dla stacji wynosi co najmniej 10, jeśli nie - zmieniamy status stacji na niedostępny
	- **Szacunek zlozonosci:** Zliczenie wierszy złączenia tabel CarStation i RentalHistory, modyfikacja części wierszy z tabeli CarStation
2.  Zablokowanie możliwości wypożyczenia samochodu ze stacji poza godzinami otwarcia:
	- **Opis:** Reguła służy zablokowaniu wypożyczenia samochodu poza godzinami otwarcia stacji
	- **Zdarzenia inicjujace:** Dodanie nowego wiersza RentalHistory i ustawienie atrybutu avaliable tabeli Car na 'false'
	- **Warunki uruchomienia:** Czas wypożyczenia nie mieści się w godzinach otwarcia stacji
	- **Dzialanie:** Usuwamy dodany wiersz RentalHistory i ustawiamy pole avaliable spowrotem na 'true'
	- **Szacunek zlozonosci:** Porównanie atrybutów wiersza ze złączenia trzech tabel i modyfikacja jednago z atrybutów
