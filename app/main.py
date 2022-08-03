from fastapi import FastAPI, HTTPException, Request

app = FastAPI()
origins = ["*"]


@app.post("/api/webhook/")
async def get_webhook_response(request: Request):
    body = await request.json()
    return {"challenge": body["challenge"]}