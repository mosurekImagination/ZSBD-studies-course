# Log Converter
Narzędzie do szybkiego transformowania pliku loga do tabelki w markdownie

# Wymagania 
* Java 8+

# Użycie
* W konsoli wpisać komendę:
> `java -jar LogConverter.jar <sciezka/do/log.log> <sciezka/do/zapisu>`

* Przykład 
> `java -jar LogConverter.jar ./stats.log ./results`

> ***NOTE:***: Parametry sa opcjonalne, lub mozliwe jest podanie wartosci default dla kazdego aby wybrac domyslne sciezki <br> 
> Domyślne ścieżki to:
> * Log : stats.log
> * Wyniki : results 
>
> ***NOTE:*** Ścieżki są względne do pliku `jar`