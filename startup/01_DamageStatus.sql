CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE DamageStatus PURGE;

create table DamageStatus (
	id INT,
	status VARCHAR2(50)
);
insert into DamageStatus (id, status) values (1, 'working');
insert into DamageStatus (id, status) values (2, 'repaired');
insert into DamageStatus (id, status) values (3, 'waiting');

COMMIT;
EXIT;