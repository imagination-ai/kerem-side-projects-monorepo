from abc import ABC, abstractmethod

import dill


class BaseServable(ABC):
    SCHEMA_SLUG = "schema.json"
    MODEL_TYPE: str
    MODEL_VARIANT: str

    def __init__(self, model):
        self.model = model

    @abstractmethod
    def export(self, path):
        raise NotImplementedError

    @abstractmethod
    def run_inference(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, path):
        raise NotImplementedError


class SklearnBasedClassifierServable(BaseServable):
    MODEL_VARIANT = "sklearn-classification"

    def export(self, path):
        with open(path, "wb") as f:
            dill.dump(self.model, f)

    def run_inference(self, texts):
        prediction = self.model.predict([texts])
        print(prediction)
        return prediction[0]

    def run_inference_multiclass(self, texts):
        prob = self.model.predict_proba([texts]).tolist()[0]
        labels = self.model.classes_
        output = sorted(zip(labels, prob), reverse=True, key=lambda e: e[1])
        return output

    @classmethod
    def load(cls, path):
        return cls(model=dill.load(open(path, "rb")))


class MockServable(BaseServable):
    def run_inference(self, texts):
        return {"Bon jovi": 0.15, "Kerem": 0.55, "Osman": 0.30}

    @classmethod
    def load(cls, path):
        return cls(model=None)

    def export(self, path):
        pass
