# Aktywne reguly:
1.  Weryfikacja warunku wypożyczenia lub zwrócenia samochodu ze/do każdej aktywnej stacji minimum 10 razy w miesiącu:
	- **Opis:** Reguła służy sprawdzaniu czy stacje są aktywnie używane i wyłączanie nieużywanych
	- **Zdarzenia inicjujace:** Nowy miesiąc
	- **Warunki uruchomienia:** Tylko dla aktywnych stacji
	- **Dzialanie:** Sprawdzamy czy suma wypożyczeń i zwrotów dla stacji wynosi co najmniej 10, jeśli nie - zmieniamy status stacji na
	- **Szacunek zlozonosci:** Zliczenie wierszy złączenia tabel CarStation i RentalHistory, modyfikacja części wierszy z tabeli CarStation
