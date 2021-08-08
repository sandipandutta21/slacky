""" Slacky bot for slack """
import os
import re
from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler

app = Flask(__name__)

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
bolt_app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))


@bolt_app.message("poop")
def delete_message(payload: dict):
    """ This will filter from all the message and which has poop in it it will pass only those"""
    """ Admin access scope required, which is only available with the paid version of Slack """
    response = client.chat_delete(channel=payload["channel"],
                                  ts=payload["ts"])


@bolt_app.message(re.compile("(hi|hello|hey) slacky"))
def reply_in_thread(payload: dict):
    """ This will reply in thread instead of creating a new thread """
    response = client.chat_postMessage(channel=payload.get('channel'),
                                       thread_ts=payload.get('ts'),
                                       text=f"Hi <@{payload['user']}>")


@bolt_app.message("hello slacky")
def greetings(payload: dict, say: Say):
    """ This will check all the message and pass only those which has 'hello slacky' in it """
    user: str = payload.get("user")
    say(f"Hi <@{user}>")


@bolt_app.event("team_join")
def team_join(payload: dict, say: Say):
    """ This will greet the user who has joined the channel """
    text = f"Hi <@{payload['user']}>, Welcome to the channel"
    say(text=text, channel=payload['channel'])


@bolt_app.command("/help")
def help_command(say, ack):
    """ This is for slash coammnd /help """
    ack()
    text = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a slash command"
                }
            }
        ]
    }
    say(text=text)


handler = SlackRequestHandler(bolt_app)


@app.route("/slacky/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request and dispatch method of App """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    
    
