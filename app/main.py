from fastapi import FastAPI, HTTPException, Request
import dateparser
import spacy
from timexy import Timexy

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

nlp = spacy.load("en_core_web_sm")


config = {
    "kb_id_type": "timex3",  # possible values: 'timex3'(default), 'timestamp'
    "label": "timexy",       # default: 'timexy'
    "overwrite": False       # default: False
}
nlp.add_pipe("timexy", config=config, before="ner")

def send_message(message, channel):
    print(message)
    try:
        # Call the chat.postMessage method using the WebClient
        if message:

            result = client.chat_postEphemeral(
                channel=channel, 
                text=message, 
                user="U1RNT514Y"
            )
            logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

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
    if "event" in body and "bot_id" in body["event"] and body["event"]["bot_id"]:
        return  {"message": "ok"}
    if "event" in body and "channel" in body["event"]:
            channel = body["event"]["channel"]
            if "text" in body["event"]:
                text = body["event"]["text"]

                doc = nlp(text)
                for e in doc.ents:
                    parsed = dateparser.parse(e.text)
                    ist, cst, est = convert_date(parsed)
                    message = "Conversion: "+e.text+"\nIST: " + str(ist) + "\nCST: " + str(cst) + "\nEST: " + str(est)
                    send_message(message, channel)
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return {"message": "ok"}