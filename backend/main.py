import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from service.startup.StandardScaler import initialize_standard_scaler
from service.startup.Thresholds import initialize_thresholds
from service.startup.Models import initialize_models
from service.startup.Explainers import initialize_explainers
from service.startup.RefNodes import initialize_ref_nodes
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
    initialize_ref_nodes(app)
    initialize_standard_scaler(app)
    initialize_thresholds(app)
    initialize_models(app)
    initialize_explainers(app)



app.include_router(router)
