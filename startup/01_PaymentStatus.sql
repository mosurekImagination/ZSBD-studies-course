CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE PaymentStatus PURGE;

create table PaymentStatus (
	id NUMBER GENERATED ALWAYS AS IDENTITY,
	status VARCHAR2(50)
);
insert into PaymentStatus  (status) values ('paid');
insert into PaymentStatus  (status) values ('waiting');
insert into PaymentStatus  (status) values ('cancelled');

COMMIT;
EXIT;
