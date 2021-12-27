from fastapi import APIRouter, Form

from style.predict.servable.serve import get_servable

router = APIRouter()


@router.get("/")
async def index():
    return {"success": True, "message": "Predictions Router is working!"}


@router.post("/predict")
async def predict(text: str = Form(...), model_name: str = Form(...)):
    servable = get_servable(model_name)
    prediction = servable.run_inference(text)
    return {"success": True, "prediction": prediction}


@router.post("/predicts")
async def predicts(text: str = Form(...), model_name: str = Form(...)):
    servable = get_servable(model_name)
    predictions = servable.run_inference_multiclass(text)
    return {"success": True, "predictions": predictions}
