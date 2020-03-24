CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE PaymentType PURGE;

create table PaymentType (
	id NUMBER GENERATED ALWAYS AS IDENTITY,
	type VARCHAR2(50)
);
insert into PaymentType  (type) values ('credit_card');
insert into PaymentType  (type) values ('cash');

COMMIT;
EXIT;
