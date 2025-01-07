from fastapi import FastAPI
import uvicorn

import auth
from database import engine
import models

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


@app.get("/tasks")
async def user_tasks():
    pass


@app.post("/tasks")
async def register_task():
    pass


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
