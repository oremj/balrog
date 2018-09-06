INSERT INTO permissions VALUES('admin','bill',NULL,1);
INSERT INTO permissions VALUES('permission','bob',NULL,1);
INSERT INTO permissions VALUES('release','bob','{"products": ["fake", "a", "b"], "actions": ["create", "modify"]}',1);
INSERT INTO permissions VALUES('release','julie','{"products": ["a"], "actions": ["modify"]}',1);
INSERT INTO permissions VALUES('rule','julie','{"products": ["fake"], "actions": ["create"]}',1);
INSERT INTO permissions VALUES('release_read_only','bob','{"products": ["a", "b"], "actions": ["set"]}',1);
INSERT INTO permissions VALUES('rule','bob','{"products": ["a", "b"], "actions": ["modify"]}',1);
INSERT INTO permissions VALUES('release','ashanti','{"products": ["a"], "actions": ["modify"]}',1);
INSERT INTO permissions VALUES('scheduled_change','mary','{"actions": ["enact"]}',1);
INSERT INTO permissions VALUES('release_locale','ashanti','{"products": ["a"], "actions": ["modify"]}',1);
INSERT INTO permissions VALUES('admin','billy','{"products": ["a"]}',1);
INSERT INTO releases VALUES('a','a',1,'{"name": "a", "hashFunction": "sha512", "schema_version": 1}',0);
INSERT INTO releases VALUES('ab','a',1,'{"name": "ab", "hashFunction": "sha512", "schema_version": 1}',0);
INSERT INTO releases VALUES('b','b',1,'{"name": "b", "hashFunction": "sha512", "schema_version": 1}',0);
INSERT INTO releases VALUES('c','c',1,'{"name": "c", "hashFunction": "sha512", "schema_version": 1}',0);
INSERT INTO releases VALUES('d','d',1,'{"platforms": {"p": {"locales": {"d": {"complete": {"hashValue": "abc", "filesize": 1234, "from": "*"}}}}}, "name": "d", "hashFunction": "sha512", "schema_version": 1}',0);
INSERT INTO releases_history VALUES(1,'bill','ab',NULL,NULL,NULL,5,0);
INSERT INTO releases_history VALUES(2,'bill','ab','a',1,'{"name": "ab", "hashFunction": "sha512", "schema_version": 1}',6,0);
INSERT INTO releases_history VALUES(3,'bill','d',NULL,NULL,NULL,9,0);
INSERT INTO releases_history VALUES(4,'bill','d','d',1,'{"platforms": {"p": {"locales": {"d": {"complete": {"hashValue": "abc", "filesize": 1234, "from": "*"}}}}}, "name": "d", "hashFunction": "sha512", "schema_version": 1}',10,0);
INSERT INTO releases_history VALUES(5,'bill','b',NULL,NULL,NULL,15,0);
INSERT INTO releases_history VALUES(6,'bill','b','b',1,'{"name": "b", "hashFunction": "sha512", "schema_version": 1}',16,0);
INSERT INTO permissions_req_signoffs_history VALUES(1,'bill','doop','releng',NULL,NULL,10);
INSERT INTO permissions_req_signoffs_history VALUES(2,'bill','doop','releng',2,1,11);
INSERT INTO permissions_req_signoffs_history VALUES(3,'bill','doop','releng',1,2,25);
INSERT INTO product_req_signoffs_history VALUES(1,'bill','fake','k','relman',NULL,NULL,10);
INSERT INTO product_req_signoffs_history VALUES(2,'bill','fake','k','relman',2,1,11);
INSERT INTO product_req_signoffs_history VALUES(3,'bill','fake','k','relman',1,2,25);
INSERT INTO permissions_req_signoffs VALUES('fake','releng',1,1);
INSERT INTO permissions_req_signoffs VALUES('bar','releng',1,1);
INSERT INTO permissions_req_signoffs VALUES('blah','releng',1,1);
INSERT INTO permissions_req_signoffs VALUES('doop','releng',1,2);
INSERT INTO permissions_req_signoffs VALUES('superfake','relman',1,1);
INSERT INTO product_req_signoffs VALUES('fake','a','releng',1,1);
INSERT INTO product_req_signoffs VALUES('fake','e','releng',1,1);
INSERT INTO product_req_signoffs VALUES('fake','j','releng',1,1);
INSERT INTO product_req_signoffs VALUES('fake','k','relman',1,2);
INSERT INTO user_roles VALUES('bill','releng',1);
INSERT INTO user_roles VALUES('bill','qa',1);
INSERT INTO user_roles VALUES('bob','relman',1);
INSERT INTO user_roles VALUES('julie','releng',1);
INSERT INTO user_roles VALUES('mary','relman',1);
INSERT INTO rules VALUES(1,100,'c',100,'minor','a','3.5','a','d',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(2,100,'b',100,'minor','a','3.3','a','d',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,'frodo',NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(3,100,'a',100,'minor','a','3.5','a','a',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(4,80,'a',100,'minor','fake',NULL,'a','d',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(5,80,'c',0,'minor','a','3.3','a','d',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(6,40,'a',50,'minor','fake',NULL,'e',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(7,30,'a',85,'minor','fake',NULL,'c',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO rules VALUES(8,25,'a',100,'minor','fake2',NULL,'c',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,1,NULL);
INSERT INTO rules VALUES(9,25,'a',100,'minor','fake3',NULL,'c',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,1);
INSERT INTO permissions_scheduled_changes_history VALUES(1,'bill',20,1,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(2,'bill',21,1,'bill','insert',0,1,'rule','janet','{"products": ["foo"]}',NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(3,'bill',40,2,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(4,'bill',41,2,'bill','update',0,1,'release_locale','ashanti',NULL,1);
INSERT INTO permissions_scheduled_changes_history VALUES(5,'bill',60,3,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(6,'bill',61,3,'bill','insert',0,1,'permission','bob',NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(7,'bill',100,3,'bill','insert',1,2,'permission','bob',NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(8,'bill',200,4,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(9,'bill',201,4,'bill','delete',0,1,'scheduled_change','mary',NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(10,'bill',204,5,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(11,'bill',205,5,'bill','insert',0,1,'rule','joe','{"products": ["fake"]}',NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(12,'bill',404,6,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO permissions_scheduled_changes_history VALUES(13,'bill',405,6,'bill','update',0,1,'release','bob','{"products": ["a", "b"]}',1);
INSERT INTO permissions_scheduled_changes_signoffs_history VALUES(1,'bill',30,1,'bill',NULL);
INSERT INTO permissions_scheduled_changes_signoffs_history VALUES(2,'bill',31,1,'bill','releng');
INSERT INTO permissions_scheduled_changes_signoffs VALUES(1,'bill','releng');
INSERT INTO permissions_scheduled_changes_signoffs VALUES(2,'bill','releng');
INSERT INTO permissions_scheduled_changes_signoffs VALUES(2,'mary','relman');
INSERT INTO permissions_scheduled_changes_signoffs VALUES(4,'bill','releng');
INSERT INTO permissions_scheduled_changes_signoffs VALUES(4,'mary','relman');
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(1,'bill',20,1,NULL,NULL);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(2,'bill',21,1,10000000,1);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(3,'bill',40,2,NULL,NULL);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(4,'bill',41,2,20000000,1);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(5,'bill',60,3,NULL,NULL);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(6,'bill',61,3,30000000,1);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(7,'bill',100,3,30000000,2);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(8,'bill',200,4,NULL,NULL);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(9,'bill',201,4,76000000,1);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(10,'bill',204,5,NULL,NULL);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(11,'bill',205,5,98000000,1);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(12,'bill',404,6,NULL,NULL);
INSERT INTO permissions_scheduled_changes_conditions_history VALUES(13,'bill',405,6,38000000,1);
INSERT INTO permissions_scheduled_changes VALUES(1,'bill',0,'insert',1,'rule','janet','{"products": ["foo"]}',NULL);
INSERT INTO permissions_scheduled_changes VALUES(2,'bill',0,'update',1,'release_locale','ashanti',NULL,1);
INSERT INTO permissions_scheduled_changes VALUES(3,'bill',1,'insert',2,'permission','bob',NULL,NULL);
INSERT INTO permissions_scheduled_changes VALUES(4,'bill',0,'delete',1,'scheduled_change','mary',NULL,1);
INSERT INTO permissions_scheduled_changes VALUES(5,'bill',0,'insert',1,'rule','joe','{"products": ["fake"]}',NULL);
INSERT INTO permissions_scheduled_changes VALUES(6,'bill',0,'update',1,'release','bob','{"products": ["a", "b"]}',1);
INSERT INTO permissions_scheduled_changes_conditions VALUES(1,10000000,1);
INSERT INTO permissions_scheduled_changes_conditions VALUES(2,20000000,1);
INSERT INTO permissions_scheduled_changes_conditions VALUES(3,30000000,2);
INSERT INTO permissions_scheduled_changes_conditions VALUES(4,76000000,1);
INSERT INTO permissions_scheduled_changes_conditions VALUES(5,98000000,1);
INSERT INTO permissions_scheduled_changes_conditions VALUES(6,38000000,1);
