# Zapytania 

## Transakcja 1
1. Pokaż wszystkie niewypożyczone samochody
1. Dodaj samochód stacji
1. Pogrupowane miasta, liczba dostępnych, niedostępnych samochodów, liczba dostępnych, niedostępnych stacji
1. Samochody naprawione przez konkretne firmy
1. Usuń stację
    * Przenies pracownika do innej stacji
    * Przenieś wszystkie samochody do innej stacji
    * Usuń stację
1. Dodanie oceny do wypozyczenia wyzwala obliczenie nowej oceny dla samochodu, ktorego dotyczy wypozyczenie.
1. Uzytkownicy ktorzy wypozyczyli samochod w okreslonym przedziale czasowym w okreslonym miescie.
1. Uzytkownicy ktorzy spowodowali wiecej szkod niz przychodu


## Transakcja 2
1. Pokaż zapełnione stacje ( maksymalna liczba samochodów w stacji )
1. Zaktualizuj stan licznika samochodu
1. Zaktualizuj godziny otwarcia stacji, ktora znajduje sie w miescie X
1. Pogrupowane samochody, liczba uszkodzen i kosztow ich naprawy.
1. Dodaj nowy przeglad samochodu
    * nowa faktura
    * (nowa firma)
    * (nowa lokalizacja)
    * zmiana statusu samochodu na dostepny
1. Dla uzytkownikow posiadajacych wiecej niz 10 wypozyczen dodaj znizke dla nieoplaconych transakcji (Payment) w wysokosci -1% za kazde wypozyczenie powyzej 10, ale maksymalnie 30
1. Wybierz uzytkownikow ktorzy spowodowali uszkodzenia powyzej kwoty X w Y kolejnych wypozyczen.
1. Wylacz stacje ktore maja mniej niz X wypozyczen, o ile w panstwie w ktorym wystepuje stacja nie ma mnie niz Y stacji

## Transakcja 3

1. Pokaż wyłączone / włączone stacje
1. Pogrupowane firmy, liczba i suma faktur za inspekcje i naprawy
1. Samochody ktore mialy wykonane X ostatnich przegladow przez ta sama firme
1. Top X miast w ktorych wypozyczane sa samochody 
1. % samochodow wypozyczanych i oddawanych w tym samym miescie 
1. Dodaj znizke do trwajacych wypozyczen rozpoczetych w danym miescie w okreslonym czasie
1. Wystawienie faktury za naprawe
    * zmiana statusu wszystkich uszkodzen
    * naprawa samochodu (available)
    * dodanie kosztow naprawy do oplaty za wypozyczenie
1. Uzytkownicy ktorzy w zadanym okresie czasu mieli kontakt z konkretnym pracownikiem (coronavirus)
1. Wylacz stacje ktore generuja straty wyzsze niz srednia strat ze stacji w tym samym panstwie
