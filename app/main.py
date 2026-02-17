from fastapi import FastAPI 

app = FastAPI()

@app.get("/health")
def fnc():
    return {
        "status": "ok",
        "service": "inventory"
    }

