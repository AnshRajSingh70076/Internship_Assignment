# tools.py

from langchain.tools import tool
import warnings
warnings.filterwarnings("ignore")
# ---------------------------
# Outcome Data (STRICT)
# ---------------------------
CALL_OUTCOMES = {
    "CALL_001": "Resolved",
    "CALL_002": "Resolved",
    "CALL_003": "Unresolved",
    "CALL_004": "Resolved",
    "CALL_005": "Resolved",
    "CALL_006": "Resolved",
    "CALL_007": "Unresolved",
    "CALL_008": "Escalated",
    "CALL_009": "Resolved",
    "CALL_010": "Unresolved",
    "CALL_011": "Escalated",
    "CALL_012": "Resolved",
    "CALL_013": "Unresolved",
    "CALL_014": "Resolved",
    "CALL_015": "Resolved",
    "CALL_016": "Escalated",
    "CALL_017": "Unresolved",
    "CALL_018": "Resolved",
    "CALL_019": "Escalated",
    "CALL_020": "Unresolved",
}

# ---------------------------
# Sentiment Data
# ---------------------------
CALL_SENTIMENTS = {
    "CALL_001": "Negative – delayed delivery",
    "CALL_002": "Negative – damaged product",
    "CALL_003": "Neutral – informational query",
    "CALL_004": "Negative – billing issue",
    "CALL_005": "Negative – wrong product delivered",
    "CALL_006": "Neutral – cancellation request",
    "CALL_007": "Neutral – warranty query",
    "CALL_008": "Negative – missed delivery commitment",
    "CALL_009": "Neutral – account issue resolved",
    "CALL_010": "Neutral – serviceability query",
    "CALL_011": "Negative – fraud/tampering issue",
    "CALL_012": "Neutral – exchange request",
    "CALL_013": "Negative – cashback issue",
    "CALL_014": "Neutral – system cancellation",
    "CALL_015": "Neutral – policy query",
    "CALL_016": "Negative – repeated unresolved complaint",
    "CALL_017": "Neutral – coupon policy query",
    "CALL_018": "Neutral – invoice request",
    "CALL_019": "Negative – misleading product info",
    "CALL_020": "Negative – refund delay",
}

# ---------------------------
# TOOLS
# ---------------------------

@tool
def get_call_outcome(call_id: str) -> str:
    """Return outcome of a call (Resolved / Unresolved / Escalated)"""
    return CALL_OUTCOMES.get(call_id, "Unknown Call ID")


@tool
def get_sentiment_summary(call_id: str) -> str:
    """Return sentiment of a call"""
    return CALL_SENTIMENTS.get(call_id, "Unknown Call ID")