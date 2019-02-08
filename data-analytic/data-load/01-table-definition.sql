drop schema petfinder_adoption_prediction cascade;
create schema petfinder_adoption_prediction;

drop table if exists petfinder_adoption_prediction.breed_labels;
create table petfinder_adoption_prediction.breed_labels
(
	breedid integer,
	pet_type integer,
	breedname text
)
distributed randomly;

drop table if exists petfinder_adoption_prediction.color_labels;
create table petfinder_adoption_prediction.color_labels
(
	colorid integer,
	colorname text
)
distributed randomly;

drop table if exists petfinder_adoption_prediction.state_labels;
create table petfinder_adoption_prediction.state_labels
(
	stateid integer,
	statename text
)
distributed randomly;

drop table if exists petfinder_adoption_prediction.test;
create table petfinder_adoption_prediction.test
(
	pet_type integer,
	pet_name text,
	age integer,
	breed1 integer,
	breed2 integer,
	gender integer,
	color1 integer,
	color2 integer,
	color3 integer,
	maturitysize integer,
	furlength integer,
	vaccinated integer,
	dewormed integer,
	sterilized integer,
	health integer,
	quantity integer,
	fee integer,
	state integer,
	rescuerid text,
	videoamt integer,
	description text,
	petid text,
	photoamt numeric
)
distributed randomly;

drop table if exists petfinder_adoption_prediction.train;
create table petfinder_adoption_prediction.train
(
	pet_type integer,
	pet_name text,
	age integer,
	breed1 integer,
	breed2 integer,
	gender integer,
	color1 integer,
	color2 integer,
	color3 integer,
	maturitysize integer,
	furlength integer,
	vaccinated integer,
	dewormed integer,
	sterilized integer,
	health integer,
	quantity integer,
	fee integer,
	state integer,
	rescuerid text,
	videoamt integer,
	description text,
	petid text,
	photoamt numeric,
	adoptionspeed integer
)
distributed randomly;