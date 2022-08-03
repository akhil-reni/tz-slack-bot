from fastapi import FastAPI, HTTPException, Request

app = FastAPI()
origins = ["*"]


@app.post("/api/webhook/")
async def get_webhook_response(request: Request):
    body = await request.json()
    print(body)
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return {"message": "ok"}