CONNECT usr/pwd@//localhost:1521/pdb;

DROP TABLE DocumentType PURGE;

create table DocumentType (
	id INT,
	type VARCHAR(50)
);
insert into DocumentType (id, type) values (1, 'id_card');
insert into DocumentType (id, type) values (2, 'passport');
insert into DocumentType (id, type) values (3, 'driving_license');

COMMIT;
EXIT;