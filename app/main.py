# from fastapi import Depends, FastAPI,Request,Cookie, HTTPException, status
# from contextlib import contextmanager,asynccontextmanager
# from app.database import get_db, SessionLocal
# from fastapi.middleware.cors import CORSMiddleware
# from app.auth.router import router_auth
# from dotenv import load_dotenv

# @asynccontextmanager
# async def lifespan_context(app: FastAPI):
#     yield


# app = FastAPI(lifespan=lifespan_context)

# get_db_manager = contextmanager(get_db)

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):    

#         response = await call_next(request)
#         return response

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # app.include_router(router)
# app.include_router(router_auth)
# load_dotenv()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}