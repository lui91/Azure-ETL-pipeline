import psycopg2
import os
from airflow.decorators import task
import pandas as pd


def get_connection():
    host = os.getenv('TF_VAR_POSTGRE_HOST')
    dbname = os.getenv('TF_VAR_POSTGRE_DB')
    user = os.getenv('TF_VAR_POSTGRE_LOGIN')
    password = os.getenv('TF_VAR_POSTGRE_PASSWORD')
    sslmode = 'require'

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(
        host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    return conn


@task(task_id="postgre_call_stored_procedure")
def call_stored_procedure():
    ''' Call stored procedure to add current date to date dim'''
    conn = get_connection()
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute("CALL insert_date();")
    conn.commit()
    cursor.close()
    conn.close()


@task(task_id="postgre_create_schema")
def create_postgre_schema():
    ''' Run sql file to generate the DB schema.'''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(get_tweet_dim())
    cursor.execute(get_date_dim())
    cursor.execute(get_provider_dim())
    cursor.execute(get_tweets_fact())
    cursor.execute(get_insert_date())
    conn.commit()
    cursor.close()
    conn.close()


def get_tweet_dim():
    # return "CREATE TABLE tweet_dim (tweet_key SERIAL , PRIMARY KEY(tweet_key));"
    return '''
    CREATE TABLE tweet_Dim (
    tweet_key SERIAL ,
    PRIMARY KEY(tweet_key)
    );
    '''


def get_date_dim():
    # return "CREATE TABLE date_dim (date_key SERIAL, day_date DATE NOT NULL, PRIMARY KEY(date_key));"
    return '''
    CREATE TABLE date_dim (
    date_key SERIAL,
    day_date DATE NOT NULL,
    PRIMARY KEY(date_key)
    );
    '''


def get_provider_dim():
    # return "CREATE TABLE provider_dim (provider_key SERIAL, Description VARCHAR(30), PRIMARY KEY(provider_key));"
    return '''
    CREATE TABLE provider_dim (
    provider_key SERIAL,
    Description VARCHAR(30),
    PRIMARY KEY(provider_key)
    );
    '''


def get_tweets_fact():
    return '''
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
    FOREIGN KEY (Provider_key) REFERENCES provider_dim(Provider_key));
    '''


def get_insert_date():
    return '''
    CREATE OR REPLACE PROCEDURE insert_date()
    language plpgsql    
    as $$
    DECLARE 
    todayRegistered INT DEFAULT 0;
    today_Date DATE := CURRENT_DATE;
    BEGIN
        SELECT CASE WHEN COUNT(day_Date) <> 0 THEN 1 ELSE 0 END
        INTO todayRegistered
        FROM (SELECT Day_date FROM Date_dim WHERE Day_date = today_Date) as date_table;
        IF todayRegistered = 0 THEN
        INSERT INTO Date_Dim (Day_date) values(today_Date);
        raise notice 'Today date added';
        END IF;
        commit;
    end;$$;
    '''
