import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from service.startup.StandardScaler import initialize_standard_scaler
from service.startup.Thresholds import initialize_thresholds
from service.startup.Models import initialize_models
from service.startup.Explainers import initialize_explainers
from service.startup.RefNodes import initialize_ref_nodes
from service.startup.PredProba import initialize_pred_proba_dfs
from service.router import HealthRouter, BaselineModelsRouter, ProspectiveRouter, RetrospectoveRouter, ProspectiveRefRouter
from fastapi import APIRouter

os.environ["OPENBLAS_NUM_THREADS"] = '8'

app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
# app.add_middleware(HTTPSRedirectMiddleware)
router = APIRouter(redirect_slashes=False)
app.include_router(HealthRouter.router)
app.include_router(BaselineModelsRouter.router)
app.include_router(ProspectiveRouter.router)
app.include_router(RetrospectoveRouter.router)
app.include_router(ProspectiveRefRouter.router)

@app.on_event("startup")
async def startup_event():
    print("Startup")
    initialize_pred_proba_dfs(app)
    print("Loaded prediction probabilities to estimate thresholds")
    initialize_ref_nodes(app)
    print("Loaded reference nodes")
    initialize_standard_scaler(app)
    print("Loaded standard scaler")
    initialize_thresholds(app)
    print("Loaded thresholds")
    initialize_models(app)
    print("Loaded models")
    initialize_explainers(app)
    print("Loaded explainers")
    print("Finished")



app.include_router(router)
