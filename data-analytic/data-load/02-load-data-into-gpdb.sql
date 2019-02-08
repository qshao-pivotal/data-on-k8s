truncate petfinder_adoption_prediction.breed_labels;
drop external table if exists  petfinder_adoption_prediction.breed_labels_ext;
create external table petfinder_adoption_prediction.breed_labels_ext
(like petfinder_adoption_prediction.breed_labels)
LOCATION ('s3://data-warehousing-minio:9000/petfinder-adoption-prediction/breed_labels.csv region=us-east-1 config=/home/gpadmin/minio.conf')
FORMAT 'CSV' ( HEADER DELIMITER ',' );
insert into petfinder_adoption_prediction.breed_labels select * from petfinder_adoption_prediction.breed_labels_ext;

truncate petfinder_adoption_prediction.color_labels;
drop external table if exists  petfinder_adoption_prediction.color_labels_ext;
create external table petfinder_adoption_prediction.color_labels_ext
(like petfinder_adoption_prediction.color_labels)
LOCATION ('s3://data-warehousing-minio:9000/petfinder-adoption-prediction/color_labels.csv region=us-east-1 config=/home/gpadmin/minio.conf')
FORMAT 'CSV' ( HEADER DELIMITER ',' );
insert into petfinder_adoption_prediction.color_labels select * from petfinder_adoption_prediction.color_labels_ext;

truncate petfinder_adoption_prediction.state_labels;
drop external table if exists  petfinder_adoption_prediction.state_labels_ext;
create external table petfinder_adoption_prediction.state_labels_ext
(like petfinder_adoption_prediction.state_labels)
LOCATION ('s3://data-warehousing-minio:9000/petfinder-adoption-prediction/state_labels.csv region=us-east-1 config=/home/gpadmin/minio.conf')
FORMAT 'CSV' ( HEADER DELIMITER ',' );
insert into petfinder_adoption_prediction.state_labels select * from petfinder_adoption_prediction.state_labels_ext;

truncate petfinder_adoption_prediction.test;
drop external table if exists  petfinder_adoption_prediction.test_ext;
create external table petfinder_adoption_prediction.test_ext
(like petfinder_adoption_prediction.test)
LOCATION ('s3://data-warehousing-minio:9000/petfinder-adoption-prediction/test.csv region=us-east-1 config=/home/gpadmin/minio.conf')
FORMAT 'CSV' ( HEADER DELIMITER ',' QUOTE AS '"');
insert into petfinder_adoption_prediction.test select * from petfinder_adoption_prediction.test_ext;


truncate petfinder_adoption_prediction.train;
drop external table if exists  petfinder_adoption_prediction.train_ext;
create external table petfinder_adoption_prediction.train_ext
(like petfinder_adoption_prediction.train)
LOCATION ('s3://data-warehousing-minio:9000/petfinder-adoption-prediction/train.csv region=us-east-1 config=/home/gpadmin/minio.conf')
FORMAT 'CSV' ( HEADER DELIMITER ',' QUOTE AS '"');
insert into petfinder_adoption_prediction.train select * from petfinder_adoption_prediction.train_ext;