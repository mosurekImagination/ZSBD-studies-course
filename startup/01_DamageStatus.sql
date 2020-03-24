CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE DamageStatus PURGE;

create table DamageStatus (
	id NUMBER GENERATED ALWAYS AS IDENTITY,
	status VARCHAR2(50)
);
insert into DamageStatus  (status) values ('working');
insert into DamageStatus  (status) values ('repaired');
insert into DamageStatus  (status) values ('waiting');
COMMIT;
EXIT;
