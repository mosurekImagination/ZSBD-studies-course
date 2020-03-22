CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE PaymentStatus PURGE;

create table PaymentStatus (
	id INT,
	status VARCHAR2(50)
);
insert into PaymentStatus (id, status) values (1, 'paid');
insert into PaymentStatus (id, status) values (2, 'waiting');
insert into PaymentStatus (id, status) values (3, 'cancelled');

COMMIT;
EXIT;