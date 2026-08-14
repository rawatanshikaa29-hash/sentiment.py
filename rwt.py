"""
Sentiment analysis engine using VADER (Valence Aware Dictionary and sEntiment Reasoner).
Falls back to keyword-based analysis if VADER is unavailable.
"""

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _analyzer = SentimentIntensityAnalyzer()
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
# Keyword banks for fallback + mood enrichment
MOOD_KEYWORDS = {
    "crisis":   ["suicide", "kill myself", "end it all", "want to die", "self harm", "hurt myself", "no reason to live"],
    "anxious":  ["anxious", "anxiety", "panic", "nervous", "worried", "stress", "stressed", "overwhelmed", "fear", "scared", "dread", "tense", "uneasy"],
    "sad":      ["sad", "depressed", "depression", "hopeless", "crying", "cry", "lonely", "alone", "empty", "numb", "lost", "grief", "heartbroken", "miserable", "worthless"],
    "angry":    ["angry", "anger", "furious", "rage", "hate", "frustrated", "frustration", "annoyed", "irritated", "mad"],
    "tired":    ["tired", "exhausted", "drained", "fatigued", "sleepy", "no energy", "burnt out", "burnout", "weak"],
    "happy":    ["happy", "great", "amazing", "wonderful", "excited", "joy", "joyful", "good", "fantastic", "awesome", "grateful", "thankful", "blessed", "content"],
    "calm":     ["calm", "peaceful", "relaxed", "fine", "okay", "ok", "alright", "neutral", "steady"],
}

def _keyword_mood(text: str) -> str:
    lower = text.lower()
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return mood
    return "neutral"

def analyze_sentiment(text: str) -> tuple[str, float]:
    """
    Returns (mood_label, compound_score).
    mood_label: one of crisis | anxious | sad | angry | tired | happy | calm | neutral
    compound_score: float in [-1.0, 1.0]
    """
    # Always check for crisis keywords first — safety priority
    lower = text.lower()
    if any(kw in lower for kw in MOOD_KEYWORDS["crisis"]):
        return ("crisis", -1.0)

    if VADER_AVAILABLE:
        scores = _analyzer.polarity_scores(text)
        compound = scores["compound"]

        # Enrich VADER result with keyword context
        keyword_mood = _keyword_mood(text)
        if keyword_mood not in ("neutral", "calm"):
            return (keyword_mood, compound)

        # Map compound score to mood label
        if compound >= 0.5:
            mood = "happy"
        elif compound >= 0.1:
            mood = "calm"
        elif compound >= -0.1:
            mood = "neutral"
        elif compound >= -0.35:
            mood = "sad"
        elif compound >= -0.6:
            mood = "anxious"
        else:
            mood = "sad"

        return (mood, compound)

    else:
        # Pure keyword fallback
        mood = _keyword_mood(text)
        score_map = {
            "happy": 0.7, "calm": 0.2, "neutral": 0.0,
            "tired": -0.2, "anxious": -0.5, "sad": -0.6,
            "angry": -0.55, "crisis": -1.0,
        }
        return (mood, score_map.get(mood, 0.0))

