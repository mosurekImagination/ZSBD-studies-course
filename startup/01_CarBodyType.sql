CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE CarBodyType PURGE;

create table CarBodyType (
	id NUMBER GENERATED ALWAYS AS IDENTITY,
	type VARCHAR2(50)
);
insert into CarBodyType  (type) values ('Coupe');
insert into CarBodyType  (type) values ('Hetchback');
insert into CarBodyType  (type) values ('Combi');
insert into CarBodyType  (type) values ('Normal');
insert into CarBodyType  (type) values ('Van');

COMMIT;
EXIT;
