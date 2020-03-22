--Transakcja 2
CONNECT usr/pwd@//localhost:1521/pdb;

--1. Pokaż zapełnione stacje ( maksymalna liczba samochodów w stacji )
SELECT COUNT(ID) FROM CARSTATION WHERE CAR_LIMIT = 10;

--2. Zaktualizuj stan licznika samochodu
UPDATE CAR SET MILEAGE = 3000 WHERE ID = 3;

--3. Zaktualizuj godziny otwarcia stacji, ktora znajduje sie w miescie X
UPDATE CARSTATION
SET OPEN_HOUR = 7,
    CLOSE_HOUR = 15
WHERE ID = (SELECT CARSTATION.ID
            FROM CARSTATION
                     JOIN LOCATION L on CARSTATION.LOCATION_ID = L.ID
            WHERE L.CITY = 'Dongping');

--4. Pogrupowane samochody, liczba uszkodzen i kosztow ich naprawy.
SELECT CAR.MODEL, COUNT(DMG.ID) USZKODZENIA, SUM(INV.SUMMARY_COST)
FROM DAMAGE DMG
         JOIN CAR ON DMG.CAR_ID = CAR.ID
         JOIN INVOICE INV on DMG.INVOICE_ID = INV.ID
GROUP BY CAR.MODEL;


--5. Dodaj nowy przeglad samochodu
--------nowa faktura
--------(nowa firma)
--------zmiana statusu samochodu na dostepny
INSERT INTO COMPANY (id, location_id, name)
VALUES (999999, 100, 'New company');
INSERT INTO INVOICE (STATUS_ID, COMPANY_ID, SUMMARY_COST, EXPOSURE_DATE, PAYMENT_DATE, EXPIRE_DATE)
VALUES (1,
        (SELECT ID FROM COMPANY WHERE ROWNUM = (SELECT MAX(ROWNUM) FROM COMPANY)),
        100,
        TO_DATE('2017/12/05', 'yyyy/mm/dd'),
        TO_DATE('2018/12/05', 'yyyy/mm/dd'),
        TO_DATE('2019/12/05', 'yyyy/mm/dd'));


--6. Dla uzytkownikow posiadajacych wiecej niz 2 wypozyczen dodaj znizke dla nieoplaconych transakcji (Payment) w wysokosci 5%
UPDATE PAYMENT
SET DISCOUNT = 5, COST = COST * 0.95
WHERE ID in (
    WITH USER_RENTALS AS (SELECT *
                          FROM (SELECT U.ID USR_ID, COUNT(H.ID) RENTALS
                                FROM RENTALHISTORY H
                                         JOIN SYSTEMUSER U ON H.USER_ID = U.ID
                                GROUP BY U.ID)
                          WHERE RENTALS > 2),
         MATCH_RENTALS_PAYMENTS AS (SELECT PAYMENT_ID, RENTALS
                                    FROM RENTALHISTORY H
                                             JOIN USER_RENTALS UR ON H.USER_ID = UR.USR_ID),
         WAITING_PAYMENTS AS (SELECT P.ID, RENTALS
                              FROM PAYMENT P
                                       RIGHT JOIN MATCH_RENTALS_PAYMENTS MRP ON P.ID = MRP.PAYMENT_ID
                                       JOIN PAYMENTSTATUS PS ON P.STATUS_ID = PS.ID
                              WHERE PS.STATUS = 'waiting'
         )
    SELECT ID
    FROM WAITING_PAYMENTS
);



--7. Wybierz uzytkownikow ktorzy spowodowali uszkodzenia powyzej kwoty X w Y kolejnych wypozyczen.


--8. Wylacz stacje ktore maja mniej niz X wypozyczen, o ile w panstwie w ktorym wystepuje stacja nie ma mnie niz Y stacji
UPDATE CARSTATION
SET AVAILABLE = 'false'
WHERE ID in (
    WITH GROUPED_RENTALS AS (
        SELECT START_STATION_ID, COUNT(ID) RENTALS
        FROM RENTALHISTORY RH
        GROUP BY START_STATION_ID),

         COUNTRY_CARSTATIONS AS (
             SELECT L.COUNTRY, COUNT(CS.ID) STATIONS
             FROM CARSTATION CS
                      JOIN LOCATION L on CS.LOCATION_ID = L.ID
             GROUP BY L.COUNTRY
         )

    SELECT GR.START_STATION_ID
    FROM GROUPED_RENTALS GR
             JOIN CARSTATION CS ON GR.START_STATION_ID = CS.ID
             JOIN LOCATION L ON CS.LOCATION_ID = L.ID
             JOIN COUNTRY_CARSTATIONS CC ON CC.COUNTRY = L.COUNTRY
    WHERE RENTALS < 2
      AND STATIONS > 10
);