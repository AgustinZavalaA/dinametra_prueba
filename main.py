import threading
from fastapi import FastAPI
import uvicorn
import time

import auth
from database import LocalSession, engine
from models import Task
import models
import tasks

app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router)
# models.Base.metadata.drop_all(engine) # only uncomment this if you dont care about the data in the db or if encounter a db issue
models.Base.metadata.create_all(bind=engine)


def delete_complete_tasks() -> None:
    while True:
        db = LocalSession()
        try:
            # print("DELETING COMPLETED TASKS")

            db.query(Task).filter(Task.completed).delete()
            db.commit()
        finally:
            db.close()

        # time.sleep(30) # used for debugging
        time.sleep(10 * 60)  # 10 minutes * 60 seconds


delete_tasks_thread = threading.Thread(target=delete_complete_tasks, daemon=True)
delete_tasks_thread.start()


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
