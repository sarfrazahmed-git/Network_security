from dataclasses import dataclass
@dataclass
class ArtifactEntity:
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    drift_report_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    data_transformation_object_file_path: str


@dataclass
class classificationMetricArtifact:
    accuracy: float
    precision: float
    recall: float
    f1_score: float
@dataclass

class DataTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: classificationMetricArtifact
    test_metric_artifact: classificationMetricArtifact
