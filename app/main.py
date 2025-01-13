from fastapi import Depends, FastAPI,Request,Cookie, HTTPException, status
from contextlib import contextmanager,asynccontextmanager
from app.database import get_db, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.users.router import router_users
from app.auth.router import router_auth
from app.menu.router import router_menus
from app.uploadfile.router import router_uploadfile
from app.orders.router import router_order
from app.chatbot.router import router_chat_bot
from app.tables.router import router_tables
from app.auth.utils import gettoken, checktoken
from app.common.responses_msg import *
from fastapi.responses import JSONResponse
from .common.api_const import paths
import socketio
from app.chatbot.service import ChatbotService
import asyncio

@asynccontextmanager
async def lifespan_context(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan_context)

get_db_manager = contextmanager(get_db)

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
                        content=create_error_response("INVALID_MISSING_TOKEN", STT_CODE.get("INVALID_MISSING_TOKEN", "Unknown error code"))
                    )
        request.state.info_user = check['data']
        response = await call_next(request)
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://datn-mquickb-fe-v2.vercel.app", "http://localhost:3000", "https://mquickb.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_menus)
app.include_router(router_order)
app.include_router(router_tables)
app.include_router(router_uploadfile)
app.include_router(router_chat_bot)
load_dotenv()
chat = ChatbotService()

sio  = socketio.AsyncServer(async_mode='asgi',cors_allowed_origins=[])
socket_app = socketio.ASGIApp(sio)

app.mount("/", socket_app)

@sio.on('connect')
async def connect(sid, environ):    
    with get_db_manager() as db:             
        await chat.set_up_handle(db,sio,sid) 
    await sio.emit('connect_ok', "Message from server to "+sid,to=sid)

@sio.on('disconnect')
async def disconnect(sid):
    pass

@sio.on('message')
async def message(sid, data):      
    with get_db_manager() as db:             
        await chat.chat_handler(data,db,sio,sid)

# @sio.on("message")
# async def message(sid, data):
#     try:
#         print(f"Start sending numbers from 1 to 50 to: {sid}")
#         for number in range(1, 51):  # Phát từng số từ 1 đến 50
#             await sio.emit("message", {"number": number}, to=sid)
#             await asyncio.sleep(1)  # Đợi 1 giây trước khi gửi số tiếp theo
#     except Exception as e:
#         print(f"Error in 'message' event: {e}")