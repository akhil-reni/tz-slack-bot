from fastapi import FastAPI, HTTPException, Request
import datetimeparser

app = FastAPI()
origins = ["*"]

import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_TOKEN"))
logger = logging.getLogger(__name__)
# ID of the channel you want to send the message to

@app.post("/api/webhook/")
async def get_webhook_response(request: Request):
    body = await request.json()
    if "event" in body and "channel" in body["event"]:
            channel = body["event"]["channel"]
    try:
        # Call the chat.postMessage method using the WebClient
        if channel:
            result = client.chat_postMessage(
                channel=channel_id, 
                text="Hello world"
            )
            logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

    print(body)
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return {"message": "ok"}