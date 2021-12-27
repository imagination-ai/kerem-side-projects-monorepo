import os

import streamlit as st
import pandas as pd
from common.clients.style_predictor_client import StylePredictorClient

STYLE_PREDICTOR_HOST = os.getenv("STYLE_PREDICTOR_HOST", "127.0.0.1")
STYLE_PREDICTOR_PORT = int(os.getenv("STYLE_PREDICTOR_HOST", 8080))

client = StylePredictorClient(host=STYLE_PREDICTOR_HOST, port=STYLE_PREDICTOR_PORT)
client.predict(text="ahmet", model_name="mock")


st.write("Here's our first attempt at using data to create a table:")
st.write(
    pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
)
