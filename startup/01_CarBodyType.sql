CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE CarBodyType PURGE;

create table CarBodyType (
	id INT,
	type VARCHAR2(50)
);
insert into CarBodyType (id, type) values (1, 'Coupe');
insert into CarBodyType (id, type) values (2, 'Hetchback');
insert into CarBodyType (id, type) values (3, 'Combi');
insert into CarBodyType (id, type) values (4, 'Normal');
insert into CarBodyType (id, type) values (5, 'Van');

COMMIT;
EXIT;