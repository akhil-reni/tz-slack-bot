from fastapi import FastAPI, HTTPException, Request
import dateparser

app = FastAPI()
origins = ["*"]

import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import iso8601
import dateutil.parser
from pytz import timezone
from dateparser import search
from datetime import datetime, timedelta
# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_TOKEN"))
logger = logging.getLogger(__name__)
# ID of the channel you want to send the message to


def convert_date(date_str):
    fmt = '%H:%M:%S'
    ist =  timezone('Asia/Kolkata')
    cst =  timezone('US/Central')
    est = timezone('US/Eastern')
    date_str = date_str - timedelta(hours=1)

    ist_time = date_str.astimezone(ist).strftime(fmt)
    cst_time = date_str.astimezone(cst).strftime(fmt)
    est_time = date_str.astimezone(est).strftime(fmt)
    return ist_time, cst_time, est_time


@app.post("/api/webhook/")
async def get_webhook_response(request: Request):
    message = False
    body = await request.json()
    if "event" in body and "channel" in body["event"]:
            channel = body["event"]["channel"]
            if "text" in body["event"]:
                text = body["event"]["text"]
                searched_dates = dateparser.search.search_dates(text)
                if searched_dates and len(searched_dates):
                    text = searched_dates[0][0]
                    
                    parsed = dateparser.parse(text)
                    if parsed:
                        ist, cst, est = convert_date(parsed)
                        message = "IST: " + str(ist) + "\nCST: " + str(cst) + "\nEST: " + str(est)
                        print(message)


    if "event" in body and "bot_id" in body["event"] and body["event"]["bot_id"]:
        message = False
    try:
        # Call the chat.postMessage method using the WebClient
        if message:

            result = client.chat_postMessage(
                channel=channel, 
                text=message
            )
            logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

    print(body)
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return {"message": "ok"}