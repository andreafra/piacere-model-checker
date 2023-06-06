import logging
import os
import traceback
from importlib.resources import files

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

import mc_openapi.assets as ASSETS
from mc_openapi.doml_mc import (init_model, verify_csp_compatibility,
                                verify_model)
from mc_openapi.doml_mc.exceptions import *
from mc_openapi.doml_mc.intermediate_model.metamodel import DOMLVersion
from mc_openapi.doml_mc.mc import ModelChecker

assets = files(ASSETS)
static_path = assets / "static"
templates_path = assets / "templates"
app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

def handleDOMLX(doml_xmi: bytes, callback) -> dict:
    doml_version_str: str = None
    doml_version: DOMLVersion = None
    try:
        # First try to infer DOML version from ENV, then query params
        doml_version_str = os.environ.get("DOML_VERSION")
        
        if doml_version_str:
            doml_version = DOMLVersion.get(doml_version_str)
            logging.info(f"Forcing DOML {doml_version.value}")

        dmc = init_model(doml_xmi, doml_version)

        return callback(dmc)

    except (
        BadDOMLException,
        UnsupportedDOMLVersionException,
        MissingInfrastructureLayerException,
        NoActiveConcreteLayerException
    ) as e:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({
                "message": e.errors,
                "debug_message": traceback.format_exc()
            })
        )
    except (RuntimeError, Exception) as e:
        logging.error(traceback.format_exc())
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({
                "message": "An error has occurred. It could be an error within your DOML file. If it persist, try specifying DOML version manually.",
                "debug_message": traceback.format_exc()
            })
        )
        

@app.post("/modelcheck")
async def mc(request: Request):
    doml_xmi = await request.body()
    return handleDOMLX(doml_xmi, verify_model)
    
@app.post("/csp")
async def csp(request: Request):
    doml_xmi = await request.body()
    return handleDOMLX(doml_xmi, verify_csp_compatibility)

@app.post("/modelcheck_html")
async def mc_html(request: Request):
    doml_xmi = await request.body()
    res =  handleDOMLX(doml_xmi, verify_model)
    return templates.TemplateResponse("mc.html", {"request": request, **res})

@app.post("/csp_html")
async def csp_html(request: Request):
    doml_xmi = await request.body()
    res =  handleDOMLX(doml_xmi, verify_csp_compatibility)
    return templates.TemplateResponse("csp.html", {"request": request, **res})
