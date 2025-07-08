from Network_security.entity.artifact_entity import classificationMetricArtifact
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
def evaluate_model(y_true, y_pred):
    class_metric = classificationMetricArtifact(
        accuracy=accuracy_score(y_true, y_pred),
        precision=precision_score(y_true, y_pred, average='weighted', zero_division=0),
        recall=recall_score(y_true, y_pred, average='weighted', zero_division=0),
        f1_score=f1_score(y_true, y_pred, average="macro", zero_division=0)
    )
    return class_metric