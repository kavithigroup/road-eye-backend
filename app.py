from fastapi import FastAPI
from fastapi.middleware import cors

import api

app = FastAPI()

app.add_middleware(cors.CORSMiddleware, allow_origins=["http://localhost"], allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"])
app.include_router(api.router)
