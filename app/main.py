from fastapi import FastAPI,Request
from dotenv import load_dotenv
from app.database import get_db
from fastapi.middleware.cors import CORSMiddleware
import socketio
from contextlib import contextmanager,asynccontextmanager
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio


scheduler = BackgroundScheduler()
auth = AuthService()
graph_task_hour = 1
graph_task_minute = 15
graph_task_second = 0

token_task_hour = 23
token_task_minute = 2
token_task_second = 0

def run_token_synthetic_task():
    asyncio.run(auth.token_synthetic_task())


@asynccontextmanager
async def lifespan_context(app: FastAPI):    
    scheduler.add_job(daily_task, 'cron',hour=graph_task_hour, minute=graph_task_minute, second=graph_task_second)
    scheduler.add_job(run_token_synthetic_task, 'cron',hour=token_task_hour, minute=token_task_minute, second=token_task_second)
    scheduler.start(paused=False)
    yield
    scheduler.shutdown()    


app = FastAPI(lifespan=lifespan_context)

get_db_manager = contextmanager(get_db)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(exc.detail, ERR_CODE.get(exc.detail, "Unknown error code"))
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):    
    with get_db_manager() as db:
        token = gettoken(request)    
        check = await checktoken(token, db)
        if request.url.path in paths:
            pass
        else :
            if check['result'] == False:
                return JSONResponse(
                    status_code=403,
                    content={"detail": ERR_CODE.get("INVALID_MISSING_TOKEN", "INVALID_MISSING_TOKEN")},
                )

        request.state.info_user = check['data']
        response = await call_next(request)
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(router_auth)
load_dotenv()
