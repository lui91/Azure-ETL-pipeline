from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump
import re
from sklearn.model_selection import GridSearchCV
import os
import numpy as np
import pandas as pd


class ml_model:
    def __init__(self, postgre_data: pd.DataFrame) -> None:
        self.data = postgre_data
        self.pre_process = self.tokenize
        self.model = self.build_model
        self.X, self.Y = self.create_X_Y_format()
        self.model_file_path = os.getenv('ML_OUT_PATH')

    def create_X_Y_format(self):
        X = self.data["message"]
        Y = self.data[self.data.columns[1:]]
        return X, Y

    def tokenize(self, text) -> list:
        """ Pre process a text line"""
        lower_case = text.lower()
        words = re.sub(r'[^a-zA-Z0-9]', " ", lower_case)
        words = words.split()
        return words

    def build_model(self) -> GridSearchCV:
        """ Build process pipeline and perform grid 
            search for hyperparameter tuning """
        pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer=self.tokenize)),
            ('tfidf', TfidfTransformer()),
            ('predictor', MultiOutputClassifier(RandomForestClassifier()))
        ])
        grid_params = {
            "predictor__estimator__criterion": ["gini", "entropy"],
            "predictor__estimator__max_features": ["sqrt", "log2"]
        }
        cv = GridSearchCV(pipeline, grid_params)
        return cv

    def evaluate_model(self, model, X_test, Y_test) -> None:
        """ Calculate precision, recall and F1 score """
        weighted_recall = []
        weighted_precision = []
        weighted_f1 = []

        Y_pred = model.predict(X_test)
        for i, key in enumerate(Y_test):
            report = classification_report(
                Y_pred[:, i], Y_test.iloc[:, i], output_dict=True)
            weighted_precision.append(report['weighted avg']['precision'])
            weighted_recall.append(report['weighted avg']['recall'])
            weighted_f1.append(report['weighted avg']['f1-score'])
        print(f"Precision: {np.mean(np.asarray(weighted_precision))}")
        print(f"Recall: {np.mean(np.asarray(weighted_recall))}")
        print(f"F1 score: {np.mean(np.asarray(weighted_f1))}")

    def save_model(self, model, model_filepath: str):
        """ Save the best configuration of the model found with grid search """
        if os.path.exists(model_filepath):
            os.remove(model_filepath)
        estimator = model.best_estimator_
        dump(estimator, model_filepath)

    def train_model(self):
        X_train, X_test, Y_train, Y_test = train_test_split(
            self.X, self.Y, test_size=0.2)

        print('Building model...')
        model = self.build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        self.evaluate_model(model, X_test, Y_test)

        print('Saving model...\n    MODEL: {}'.format(self.model_filepath))
        self.save_model(model, self.model_filepath)

        print('Trained model saved!')
