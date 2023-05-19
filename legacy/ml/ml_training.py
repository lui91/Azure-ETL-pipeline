from airflow.decorators import task
from includes.azure.postgre_handling import get_connection
from includes.ml.model_structure import ml_model
import pandas as pd


@task(task_id="train_ml_model")
def ml_pipeline():
    dataset = get_dataset()
    model = ml_model(dataset)
    model.train_model()


def get_dataset() -> pd.DataFrame:
    ''' Fetch dataset to train model locally '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message, related,request,offer,aid_related,medical_help,medical_products,\
                   search_and_rescue,security,military,child_alone,water,food,shelter,clothing,money,\
                   missing_people,refugees,death,other_aid,infrastructure_related,transport,buildings,\
                   electricity,tools,hospitals,shops,aid_centers,other_infrastructure,weather_related,\
                   floods,storm,fire,earthquake,cold,other_weather FROM tweets_fact;")
    rows = cursor.fetchall()
    cols = ["message", "related", "request", "offer", "aid_related", "medical_help", "medical_products", "search_and_rescue", "security", "military", "child_alone", "water", "food", "shelter", "clothing", "money", "missing_people", "refugees",
            "death", "other_aid", "infrastructure_related", "transport", "buildings", "electricity", "tools", "hospitals", "shops", "aid_centers", "other_infrastructure", "weather_related", "floods", "storm", "fire", "earthquake", "cold", "other_weather"]
    df = pd.DataFrame(rows, columns=cols)
    return df
