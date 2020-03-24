CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE DocumentType PURGE;

create table DocumentType (
	id NUMBER GENERATED ALWAYS AS IDENTITY,
	type VARCHAR2(50)
);
insert into DocumentType  (type) values ('id_card');
insert into DocumentType  (type) values ('passport');
insert into DocumentType  (type) values ('driving_license');

COMMIT;
EXIT;
