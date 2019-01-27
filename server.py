import re

from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import Message, MessagingResponse

from config import PRIVATE_NUMBER, TWILIO_NUMBER

def encode_message(msg, number):
	return "{}: {}".format(number, msg)

def decode_message(msg):
	pattern = re.compile('^\+\d*')
	number = pattern.match(msg).group()
	body = msg[len(number) + 2:]
	return body, number

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
	from_number = request.form['From']
	msg_body = request.form['Body']

	if from_number == PRIVATE_NUMBER:
		msg, to_number = decode_message(msg_body)
		return send_message(msg, to_number)
	else:
		msg = encode_message(msg_body, from_number)
		return send_message(msg, PRIVATE_NUMBER)

def send_message(msg, number):
	response = MessagingResponse()
	response.message(msg, to=number, from_=TWILIO_NUMBER)
	return str(response)

if __name__ == '__main__':
	app.run()