from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from torch.nn.functional import normalize
from joblib import load
from service.impl.Prediction import Prediction
from service.impl.GraphPrediction import GraphPrediction
from service.meta.OutPrediction import OutPrediction
from service.meta.CBC import CBC
from service.meta.GraphCBC import GraphCBC



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_event():
    print()
    app.state.model = load('rf.joblib')

def user_function(kwargs):
    return normalize(kwargs["updated_features"] - kwargs["mean_neighbors"], p=2.0, dim=1)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/get_pred/")
async def get_pred(cbc_items: list[CBC])->OutPrediction:
    prediction = Prediction(cbc_items, app.state.model)
    return prediction.get_output()

@app.post("/get_graph_pred/")
async def get_graph_pred(graph_cbc_items: list[GraphCBC])->OutPrediction:
    prediction = GraphPrediction(graph_cbc_items, app.state.model)
    return prediction.get_output()