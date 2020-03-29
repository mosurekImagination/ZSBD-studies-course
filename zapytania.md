# Zapytania 

## Niska złożoność 4
1. x Pokaż wszystkie niewypożyczone samochody
1. x Pokaż zapełnione stacje ( maksymalna liczba samochodów w stacji )
1. x Pokaż wyłączone / włączone stacje

## Średnia złożoność 5 
1. x Samochody ktore mialy wykonane X ostatnich przegladow przez ta sama firme
1. x Samochody naprawione przez konkretne firmy
1. x Pogrupowane samochody, liczba uszkodzen i kosztow ich naprawy.
1. x Top X miast w ktorych wypozyczane sa samochody 
1. x % samochodow wypozyczanych i oddawanych w tym samym miescie 
1. x Pogrupowane miasta, liczba dostępnych, niedostępnych samochodów, liczba dostępnych, niedostępnych stacji
1. x Pogrupowane firmy, liczba i suma faktur za inspekcje i naprawy

## Wysoka złożoność 4
1. x Uzytkownicy ktorzy wypozyczyli samochod w okreslonym przedziale czasowym w okreslonym miescie.
1. x Wybierz uzytkownikow ktorzy spowodowali uszkodzenia powyzej kwoty X w Y kolejnych wypozyczen.
1. x Uzytkownicy ktorzy w zadanym okresie czasu mieli kontakt z konkretnym pracownikiem (coronavirus)
1. x Uzytkownicy ktorzy spowodowali wiecej szkod niz przychodu

# Operacje na bazie

## Niska złożoność 4
1. x Dodaj samochód stacji
1. x Zaktualizuj stan licznika samochodu
1. x Zaktualizuj godziny otwarcia stacji, ktora znajduje sie w miescie X

## Średnia złożoność  4
1. x Usuń stację
    * Przenies pracownika do innej stacji
    * Przenieś wszystkie samochody do innej stacji
    * Usuń stację
1. x Dodaj nowy przeglad samochodu
    * nowa faktura
    * (nowa firma)
    * (nowa lokalizacja)
    * zmiana statusu samochodu na dostepny
1. x Dodaj znizke do trwajacych wypozyczen rozpoczetych w danym miescie w okreslonym czasie
1. Wylacz stacje ktore generuja wiecej strat niz zyskow

## Wysoka złożoność 5
1. x Dodanie oceny do wypozyczenia wyzwala obliczenie nowej oceny dla samochodu, ktorego dotyczy wypozyczenie.
1. x Dla uzytkownikow posiadajacych wiecej niz 10 wypozyczen dodaj znizke dla nieoplaconych transakcji (Payment) w wysokosci -1% za kazde wypozyczenie powyzej 10, ale maksymalnie 30
1. x Wystawienie faktury za naprawe
    * zmiana statusu wszystkich uszkodzen
    * naprawa samochodu (available)
    * dodanie kosztow naprawy do oplaty za wypozyczenie
1. x Wylacz stacje ktore maja mniej niz X wypozyczen, o ile w panstwie w ktorym wystepuje stacja nie ma mnie niz Y stacji
1. x Wylacz stacje ktore generuja straty wyzsze niz srednia strat ze stacji w tym samym panstwie


