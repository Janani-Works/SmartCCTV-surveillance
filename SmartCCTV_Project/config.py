import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

def _get(name, default=None, required=False):
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f'Missing required env var: {name}')
    return val

@dataclass
class Settings:
    twilio_sid: str = _get('TWILIO_ACCOUNT_SID', required=True)
    twilio_token: str = _get('TWILIO_AUTH_TOKEN', required=True)
    from_number: str = _get('TWILIO_FROM_NUMBER', required=True)
    to_number: str = _get('ALERT_TO_NUMBER', required=True)
    cooldown_s: int = int(_get('ALERT_COOLDOWN_SECONDS', 120))
    conf_thresh: float = float(_get('CONF_THRESH', 0.35))
    iou_thresh: float = float(_get('IOU_THRESH', 0.5))

SETTINGS = Settings()
