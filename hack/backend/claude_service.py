import os
import json
from openai import OpenAI
from models import LogLine, CrashReport

# Configuration for DeepSeek
MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

_client = None

def _get_client():
    """Initializes and returns a clean OpenAI client configured for DeepSeek."""
    global _client
    if _client is None:
        # Step 1: Ensure no system-level proxies interfere with the API call
        for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
            os.environ.pop(var, None)
            
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # Step 2: Correct initialization for modern OpenAI SDK
        # Removed httpx.Client(proxies=None) to fix the 'unexpected keyword' bug
        _client = OpenAI(
            api_key=api_key,
            base_url=DEEPSEEK_BASE_URL
        )
    return _client

def _clean_json(text: str) -> str:
    """Extracts the JSON object from potential markdown code blocks in AI response."""
    text = text.replace("```json", "").replace("```", "").strip()
    start = text.find('{')
    end = text.rfind('}') + 1
    return text[start:end] if (start != -1 and end > start) else text

def generate_crash_report(lines: list[LogLine], session_id: str) -> CrashReport:
    """Analyzes log snippets and returns a structured AI crash report."""
    # Use the most recent logs to provide context for the failure
    snippet = "\n".join([f"[{l.timestamp}] {l.level}: {l.message}" for l in lines[-60:]])
    
    prompt = (
        "Analyze these system logs. Identify the root cause, affected services, and a fix. "
        "Return ONLY a JSON object with these fields: "
        "first_anomalous_event, probable_root_cause, affected_services (list), "
        "timeline (list of {'time', 'event', 'severity'}), recommended_fix, "
        "anomaly_category, confidence (HIGH/MEDIUM/LOW).\n\n"
        f"LOGS:\n{snippet}"
    )
    
    try:
        # Request completion from DeepSeek
        response = _get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional Site Reliability Engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2  # Low temperature for more consistent JSON output
        )
        
        raw_content = response.choices[0].message.content
        data = json.loads(_clean_json(raw_content))
        
        return CrashReport(session_id=session_id, **data)
        
    except Exception as e:
        # Graceful fallback if the API fails or returns malformed JSON
        return CrashReport(
            session_id=session_id,
            first_anomalous_event="Analysis Interrupted",
            probable_root_cause=f"AI Engine Error: {str(e)}",
            affected_services=[],
            timeline=[],
            recommended_fix="Verify DEEPSEEK_API_KEY and network connectivity.",
            anomaly_category="DIAGNOSTIC_ERROR",
            confidence="LOW"
        )