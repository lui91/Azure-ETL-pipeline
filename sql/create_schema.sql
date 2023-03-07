CREATE DATABASE disaster_data;
CREATE TABLE tweet_Dim (
tweet_key SERIAL ,
PRIMARY KEY(tweet_key)
);
CREATE TABLE date_dim (
date_key SERIAL,
day_date DATE NOT NULL,
PRIMARY KEY(date_key)
);
CREATE TABLE provider_dim (
provider_key SERIAL,
Description VARCHAR(30),
PRIMARY KEY(provider_key)
);
CREATE TABLE Tweets_Fact (
    tweet_key int,
    date_key int,
    provider_key int,
	id SERIAL,
	message VARCHAR(280),
	original VARCHAR(280),
	genre VARCHAR(20),
	related int,
	request int,
	offer int,
	aid_related int,
	medical_help int,
	medical_products int,
	search_and_rescue int,
	security int,
	military int,
	child_alone int,
	water int,
	food int,
	shelter int,
	clothing int,
	money int,
	missing_people int,
	refugees int,
	death int,
	other_aid int,
	infrastructure_related int,
	transport int,
	buildings int,
	electricity int,
	tools int,
	hospitals int,
	shops int,
	aid_centers int,
	other_infrastructure int,
	weather_related int,
	floods int,
	storm int,
	fire int,
	earthquake int,
	cold int,
	other_weather int,
    PRIMARY KEY (id),
    FOREIGN KEY (Tweet_key) REFERENCES tweet_dim(Tweet_key),
    FOREIGN KEY (Date_key) REFERENCES date_dim(Date_key),
    FOREIGN KEY (Provider_key) REFERENCES provider_dim(Provider_key)
);
delimiter //
CREATE OR REPLACE PROCEDURE insert_date()
language plpgsql    
as $$
BEGIN
	DECLARE todayRegistered INT DEFAULT 0;
	DECLARE today_Date DATE;
	set today_Date = curdate();
	SELECT IF(COUNT(*) <> 0, 1, 0)
	INTO todayRegistered
	FROM (SELECT Day_date FROM Date_dim WHERE Day_date = today_Date) as date_table;
	IF todayRegistered = 0 THEN
	INSERT INTO Date_Dim (Day_date) values(today_Date);
	END IF;
    commit;
end;$$;