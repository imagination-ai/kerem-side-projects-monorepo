from fastapi import APIRouter
from pydantic import BaseModel


from style.predict.servable.serve import get_servable

router = APIRouter()


class PredictionRequest(BaseModel):
    text: str
    model_name: str


@router.get("/")
async def index():
    return {"success": True, "message": "Predictions Router is working!"}


@router.post("/predict")
async def predict(request: PredictionRequest):
    servable = get_servable(request.model_name)
    prediction = servable.run_inference(request.text)
    return {"success": True, "prediction": prediction}


@router.post("/predicts")
async def predicts(request: PredictionRequest):
    servable = get_servable(request.model_name)
    predictions = servable.run_inference_multiclass(request.text)
    return {"success": True, "predictions": predictions}
