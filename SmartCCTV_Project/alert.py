
from twilio.rest import Client
import time
from config import SETTINGS

_client = Client(SETTINGS.twilio_sid, SETTINGS.twilio_token)
_last_sent_ts = 0.0

def _cooldown_ok():
    global _last_sent_ts
    return (time.time() - _last_sent_ts) >= SETTINGS.cooldown_s

def _mark_sent():
    global _last_sent_ts
    _last_sent_ts = time.time()

def send_sms(message):
    if not _cooldown_ok():
        return
    _client.messages.create(body=message, from_=SETTINGS.from_number, to=SETTINGS.to_number)
    _mark_sent()

def make_call(message="Alert! Suspicious activity detected."):
    if not _cooldown_ok():
        return
    _client.calls.create(from_=SETTINGS.from_number, to=SETTINGS.to_number, twiml=f'<Response><Say>{message}</Say></Response>')
    _mark_sent()

