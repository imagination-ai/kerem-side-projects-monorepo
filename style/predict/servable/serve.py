from style.constants import MODEL_EXPORT_PATH
from style.predict.servable.base import (
    MockServable,
    SklearnBasedClassifierServable,
)

SERVABLE_REGISTRY = {}


def get_servable(model_name):
    servable = SERVABLE_REGISTRY.get(model_name)
    if servable is None:
        if model_name == "mock":
            servable = MockServable.load(path=None)
        else:
            servable = SklearnBasedClassifierServable.load(
                path=MODEL_EXPORT_PATH / model_name
            )
        SERVABLE_REGISTRY[model_name] = servable
    return servable
