import psycopg2
import os
from airflow.decorators import task


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


@task(task_id="postgre_insert_provider")
def call_stored_procedure():
    ''' Insert record to dimprovider'''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dimprovider (description) VALUES ('figure eight provided data');")
    conn.commit()
    cursor.close()
    conn.close()


@task(task_id="postgre_stored_procedure")
def call_stored_procedure():
    ''' Insert record to dimtweet'''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dimtweet (batch) VALUES (0);")
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
    # SQL string to create table DimTweet"
    return '''
    USING DISASTER_data;
    CREATE TABLE IF NOT EXISTS DimTweet (
    tweet_key SERIAL,
    batch int NOT NULL,
    PRIMARY KEY(tweet_key)
    );
    '''


def get_date_dim():
    # SQL string to create table DimDate"
    return '''
    CREATE TABLE IF NOT EXISTS DimDate (
    date_key SERIAL,
    month int NOT NULL,
    day int NOT NULL,
    year int NOT NULL,
    quarter int NOT NULL,
    hour int NOT NULL,
    complete TIMESTAMP NOT NULL,
    PRIMARY KEY(date_key)
    );
    '''


def get_provider_dim():
    # SQL string to create table DimProvider"
    return '''
    CREATE TABLE IF NOT EXISTS DimProvider (
    provider_key SERIAL,
    description VARCHAR(30),
    PRIMARY KEY(provider_key)
    );
    '''


def get_tweets_fact():
    # SQL string to create table FactTweet"
    return '''
    CREATE TABLE IF NOT EXISTS FactTweet (
    id SERIAL,
    date_key int,
    tweet_key int,
    provider_key int,
	alt_id int NOT NULL,
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
    direct_report int,
    PRIMARY KEY (id),
    FOREIGN KEY (date_key) REFERENCES DimDate(date_key),
    FOREIGN KEY (tweet_key) REFERENCES DimTweet(tweet_key),
    FOREIGN KEY (provider_key) REFERENCES DimProvider(provider_key));
    '''


def get_insert_date():
    # SQL string to create stored procedure insert_date"
    return '''
    CREATE OR REPLACE PROCEDURE insert_date()
    language plpgsql    
    as $$
    DECLARE 
    todayRegistered INT DEFAULT 0;
    today_Date TIMESTAMP := CURRENT_TIMESTAMP;
    BEGIN
        SELECT CASE WHEN COUNT(complete) <> 0 THEN 1 ELSE 0 END
        INTO todayRegistered
        FROM (SELECT complete FROM DimDate WHERE DATE(complete) = DATE(today_Date) and EXTRACT(HOUR FROM complete) = EXTRACT(HOUR FROM today_Date)) as date_table;
        IF todayRegistered = 0 THEN
        INSERT INTO DIMDATE (month, day, year, quarter, hour, complete)
                VALUES (EXTRACT(MONTH FROM CURRENT_TIMESTAMP),
                        EXTRACT(DAY FROM CURRENT_TIMESTAMP),
                        EXTRACT(YEAR FROM CURRENT_TIMESTAMP),
                        EXTRACT(QUARTER FROM CURRENT_TIMESTAMP),
                        EXTRACT(HOUR FROM CURRENT_TIMESTAMP),
                        CURRENT_TIMESTAMP);
        raise notice 'Today date added';
        END IF;
        commit;
    end;$$;
    '''
