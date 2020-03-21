from flask import Flask, request
import config
from operations import sftp_operation, send_email, send_slack_message, pass_gen
from validation import parse_message, FTPIncorrectSyntax


# Listening to API requests from the slack bot
app = Flask(__name__)
bot_id = config.BOT_ID
password = pass_gen()


@app.route("/slack/events", methods=["GET", "POST"])
def listen():
    slack_event = request.get_json()
    message = slack_event["event"]["text"]
    user = slack_event["event"]["user"]
    try:
        val_out = parse_message(message)
        company = val_out[1]
        email = val_out[2]
        if not (not (bot_id in message) or bot_id in user):
            sftp_operation(company, password)
            send_email(email, company, password)
            send_slack_message(config.SUCCESS)
    except FTPIncorrectSyntax as e:
        send_slack_message(e.message)
    return "OK"


app.run(host='0.0.0.0', debug=True, port=3005)

