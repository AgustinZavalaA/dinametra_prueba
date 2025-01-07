from fastapi import FastAPI
import uvicorn

import auth
from database import engine
import models
import tasks

app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router)
# models.Base.metadata.drop_all(engine) # only uncomment this if you dont care about the data in the db or if encounter a db issue
models.Base.metadata.create_all(bind=engine)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
