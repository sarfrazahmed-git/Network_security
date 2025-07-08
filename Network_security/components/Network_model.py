class Network_model:
    def __init__(self, model, preprocessor=None):
        self.model = model
        self.preprocessor = preprocessor
    def predict(self, X):
        if self.preprocessor:
            X = self.preprocessor.transform(X)
        return self.model.predict(X)