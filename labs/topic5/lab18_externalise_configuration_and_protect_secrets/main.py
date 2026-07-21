# main.py (replace decide())
from config import settings

def decide(score: float) -> str:
    if score >= settings.decline_threshold: return "decline"
    if score >= settings.review_threshold:  return "review"
    return "approve"

