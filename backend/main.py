from typing import Optional
from routers import base_router
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse


def create_app():
    
    app = FastAPI()
    app.include_router(base_router.router)
    
    return app

app = create_app()

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)