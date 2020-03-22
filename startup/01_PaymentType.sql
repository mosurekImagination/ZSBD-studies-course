CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE PaymentType PURGE;

create table PaymentType (
	id INT,
	type VARCHAR2(50)
);
insert into PaymentType (id, type) values (1, 'credit_card');
insert into PaymentType (id, type) values (2, 'cash');

COMMIT;
EXIT;