from Network_security.entity.config_entity import DataTrainerConfig
from Network_security.logger.logger import logging
from Network_security.Myexception.Myexception import CustomException
from Network_security.entity.artifact_entity import DataTransformationArtifact,DataTrainerArtifact
from Network_security.util.main_util.utils import save_object,load_object,load_numpy_array_data
from Network_security.util.ml_util.utils import evaluate_model
from Network_security.entity.artifact_entity import classificationMetricArtifact
import sys
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
from Network_security.components.Network_model import Network_model
import mlflow
class ModelTrainer:
    def __init__(self, data_trainer_config: DataTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.data_trainer_config = data_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(f"Error in ModelTrainer init: {e}", sys)
        
    
    def grid_search(self,models,params,X_train,y_train):
        try:
            best_model_params = {}
            for model_name, model in models.items():
                logging.info(f"Training model: {model_name}")
                random_search = RandomizedSearchCV(model, params[model_name], cv=3, scoring="f1_macro")
                random_search.fit(X_train, y_train)
                best_model = random_search.best_estimator_
                best_model_params[model_name] = {"model": best_model, "params": random_search.best_params_, "score": random_search.best_score_}
                logging.info(f"Best parameters for {model_name}: {random_search.best_params_}")
                logging.info(f"Best score for {model_name}: {random_search.best_score_}")
            return best_model_params
        except Exception as e:
            raise CustomException(f"Error in grid_search: {e}", sys)
    def load_train_data(self):
        logging.info("Loading transformed data")
        train_data = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
        X_train = train_data[:, :-1]
        y_train = train_data[:, -1]
        return X_train, y_train
    
    def load_test_data(self):
        logging.info("Loading transformed test data")
        test_data = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
        X_test = test_data[:, :-1]
        y_test = test_data[:, -1]
        return X_test, y_test
    
    def train_models(self):
        try:
            X_train, y_train = self.load_train_data()

            models = {
                "RandomForest": RandomForestClassifier(),
                "GradientBoosting": GradientBoostingClassifier(),
                "XGBoost": XGBClassifier(),
                "LogisticRegression": LogisticRegression(),
                "DecisionTree": DecisionTreeClassifier()
            }
            params = {
                "RandomForest": {
                    "n_estimators": [100, 200],
                    "max_depth": [None, 10, 20],
                    "min_samples_split": [2, 5]
                },
                "GradientBoosting": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5]
                },
                "XGBoost": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5]
                },
                "LogisticRegression": {
                    "C": [0.1, 1.0, 10.0],
                    "solver": ['liblinear', 'saga']
                },
                "DecisionTree": {
                    "max_depth": [None, 10, 20],
                    "min_samples_split": [2, 5]
                }
            }
            logging.info("Starting model training with hyperparameter tuning")
            best_model_params = self.grid_search(models, params, X_train, y_train)
            logging.info("Model training completed with hyperparameter tuning")
            print("Best model parameters:", best_model_params)
            best_model_name = max(best_model_params, key=lambda x: best_model_params[x]["score"])
            best_model = best_model_params[best_model_name]["model"]
            return best_model_params[best_model_name]
        except Exception as e:
            raise CustomException(f"Error in train_models: {e}", sys)
    def track_mlflow(self, model, train_metric:classificationMetricArtifact):
        with mlflow.start_run():
            f1_score = train_metric.f1_score
            accuracy = train_metric.accuracy
            precision = train_metric.precision
            recall = train_metric.recall

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.sklearn.log_model(model, "model")

    def initiate_model_trainer(self):
        try:
            X_train, y_train = self.load_train_data()
            X_test, y_test = self.load_test_data()
            best_model_params = self.train_models()
            best_model = best_model_params["model"]
            best_model_name = best_model.__class__.__name__
            logging.info(f"Best model: {best_model_name} with parameters: {best_model_params['params']}")
            train_pred = best_model.predict(X_train)
            test_pred = best_model.predict(X_test)
            train_metric = evaluate_model(y_train, train_pred)
            self.track_mlflow(best_model,train_metric)
            test_metric = evaluate_model(y_test, test_pred)
            logging.info(f"Train metrics: {train_metric}")
            logging.info(f"Test metrics: {test_metric}")
            model_trainer_artifact = DataTrainerArtifact(
                trained_model_file_path=self.data_trainer_config.trained_model_file_path,
                train_metric_artifact=train_metric,
                test_metric_artifact=test_metric,
            )
            Net_model = Network_model(model=best_model, preprocessor=load_object(self.data_transformation_artifact.data_transformation_object_file_path))
            train_metric_new = evaluate_model(y_train, Net_model.predict(X_train))
            test_metric_new = evaluate_model(y_test, Net_model.predict(X_test))
            logging.info(f"New Train metrics: {train_metric_new}")
            logging.info(f"New Test metrics: {test_metric_new}")
            save_object(file_path=model_trainer_artifact.trained_model_file_path, obj=Net_model)
            logging.info(f"Model saved at: {model_trainer_artifact.trained_model_file_path}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(f"Error in initiate_model_trainer: {e}", sys)