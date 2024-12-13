from fastapi import FastAPI
from app.routers import task, user


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

@app.get("/")
async def welcome():
    return  {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)