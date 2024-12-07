import json
from typing import AsyncGenerator
from urllib.request import urlretrieve
from fastapi import HTTPException, UploadFile
from openai import NOT_GIVEN, AsyncOpenAI
from dotenv import load_dotenv
import os
from socketio import AsyncServer
from sqlalchemy.orm import Session
from jose import jwt
from app.uploadfile.service import UploadFileService
from .models import *
from .crud import *
from ..common.responses_msg import *
from jose import JWTError

load_dotenv()
upload = UploadFileService()
open_api_key =os.getenv('OPENAI_KEY','')
assistant_id = os.getenv('ASSISTANT_ID','')
class ChatbotService:
    async def set_up_handle(self, db:Session,sio:AsyncServer,sid:str):
        try:
            token = sio.get_environ(sid)["HTTP_AUTHORIZATION"]
            user_info = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])     
        except JWTError as e:
            print(f"JWTError: {e}")
            # Xử lý lỗi hoặc trả về thông báo lỗi
            return
        except Exception as e:
            print(f"Error: {e}")
            return
        
#     async def chat_handler(self, data, db:Session, sio:AsyncServer, sid:str):
#         token = sio.get_environ(sid)["HTTP_AUTHORIZATION"]
#         user_info = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])        
#         thread_id = data.get("thread_id")
#         message:str = data.get("message") or ''
#         name = message[:50] if len(message) > 50 else message
#         body:CreateUserThread = CreateUserThread(name = name)

#         if not thread_id:
#             thread = await self.create_thread(db,assistant_id,open_api_key,token,body)
#             thread_id = thread.thread_id

#             await sio.emit('thread', thread_id,to=sid)
        
#         async for result in self.run_thread_stream(db,thread_id, message):
#             await sio.emit('message', result,to=sid)

#     async def run_thread_stream(self,db: Session, thread_id:str, message:str) -> AsyncGenerator[str, None]:               
#         # Danh sách để lưu trữ toàn bộ câu trả lời
#         response_data = []
            
#         await AsyncOpenAI(api_key=open_api_key).beta.threads.messages.create(thread_id=thread_id,role="user", content=[{"type": "text", "text": message}])                
        
#         stream = await AsyncOpenAI(api_key=open_api_key).beta.threads.runs.create(
#             assistant_id=assistant_id,
#             thread_id=thread_id,            
#             stream=True)
        
#         async for chunk in stream:                   
#             if chunk.event == "thread.run.created":                     
#                 start = {
#                     "type":"START",
#                     "value":""
#                 }
#                 yield f"data: {json.dumps(start)}\n\n"
#                 pass
#             if chunk.event == "thread.message.delta":                
#                 annotations = chunk.data.delta.content[0].text.annotations
#                 data = {
#                     "type":"text",
#                     "value":chunk.data.delta.content[0].text.value
#                 }                
#                 if annotations is None or len(annotations) == 0:
#                     response_data.append(chunk.data.delta.content[0].text.value)
#                     yield f"data: {json.dumps(data)}\n\n"
#         end = {
#             "type":"EOS",
#             "value":""
#         }
#         yield f"data: {json.dumps(end)}\n\n"
