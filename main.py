import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from server.utils.tools import CustomException
from server.routes import main_services
app = FastAPI(
    title="fastapi training",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_services.main_route)

@app.get('/')
def ping():
    return {'msg': 'acknowledged'}


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.error_detail, "response": exc.response},
    )
#
if __name__=="__main__":
    uvicorn.run("main:app",port=5000,workers=1)