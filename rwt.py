import streamlit as st

# -------------------------------------------------
# Sentiment Analysis - Keyword Based
# -------------------------------------------------

MOOD_KEYWORDS = {
    "crisis": [
        "suicide", "kill myself", "end it all",
        "want to die", "self harm", "hurt myself",
        "no reason to live"
    ],

    "anxious": [
        "anxious", "anxiety", "panic", "nervous",
        "worried", "stress", "stressed", "overwhelmed",
        "fear", "scared", "dread", "tense", "uneasy"
    ],

    "sad": [
        "sad", "depressed", "depression", "hopeless",
        "crying", "cry", "lonely", "alone", "empty",
        "numb", "lost", "grief", "heartbroken",
        "miserable", "worthless"
    ],

    "angry": [
        "angry", "anger", "furious", "rage",
        "hate", "frustrated", "frustration",
        "annoyed", "irritated", "mad"
    ],

    "tired": [
        "tired", "exhausted", "drained",
        "fatigued", "sleepy", "no energy",
        "burnt out", "burnout", "weak"
    ],

    "happy": [
        "happy", "great", "amazing", "wonderful",
        "excited", "joy", "joyful", "good",
        "fantastic", "awesome", "grateful",
        "thankful", "blessed", "content"
    ],

    "calm": [
        "calm", "peaceful", "relaxed",
        "fine", "okay", "ok", "alright",
        "neutral", "steady"
    ]
}


def analyze_sentiment(text):
    """Return mood and sentiment score."""

    text = text.lower()

    # Check crisis first
    for keyword in MOOD_KEYWORDS["crisis"]:
        if keyword in text:
            return "crisis", -1.0

    # Check other moods
    for mood, keywords in MOOD_KEYWORDS.items():

        if mood == "crisis":
            continue

        for keyword in keywords:
            if keyword in text:

                score_map = {
                    "happy": 0.8,
                    "calm": 0.3,
                    "neutral": 0.0,
                    "tired": -0.2,
                    "anxious": -0.5,
                    "sad": -0.6,
                    "angry": -0.7
                }

                return mood, score_map.get(mood, 0.0)

    return "neutral", 0.0


# -------------------------------------------------
# Streamlit App
# -------------------------------------------------

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="💭",
    layout="centered"
)

st.title("💭 Sentiment Analysis")
st.write("Enter a sentence and find out its mood.")

st.divider()

# Text input
text = st.text_area(
    "Enter your text:",
    placeholder="Example: I am feeling happy today!",
    height=150
)

# Analyze button
if st.button("🔍 Analyze Sentiment", use_container_width=True):

    if text.strip() == "":
        st.warning("Please enter some text first.")

    else:
        mood, score = analyze_sentiment(text)

        st.subheader("Result")

        # Display mood
        if mood == "happy":
            st.success("😊 Mood: Happy")

        elif mood == "calm":
            st.info("😌 Mood: Calm")

        elif mood == "sad":
            st.error("😔 Mood: Sad")

        elif mood == "angry":
            st.error("😡 Mood: Angry")

        elif mood == "anxious":
            st.warning("😟 Mood: Anxious")

        elif mood == "tired":
            st.warning("😴 Mood: Tired")

        elif mood == "crisis":
            st.error("⚠️ Mood: Crisis")

        else:
            st.info("😐 Mood: Neutral")

        # Score
        st.metric(
            "Sentiment Score",
            f"{score:.2f}"
        )

        # Progress bar
        st.write("Sentiment intensity")

        progress = (score + 1) / 2
        st.progress(progress)

        # Simple message
        if mood == "happy":
            st.write("✨ Your text has a positive tone.")

        elif mood == "sad":
            st.write("💙 Your text appears to have a negative/sad tone.")

        elif mood == "angry":
            st.write("🔥 Your text appears to express anger.")

        elif mood == "anxious":
            st.write("🌧️ Your text appears to express anxiety or worry.")

        elif mood == "tired":
            st.write("😴 Your text appears to express tiredness.")

        elif mood == "calm":
            st.write("🌿 Your text has a calm tone.")

        elif mood == "crisis":
            st.write(
                "If this reflects how you are actually feeling, "
                "please consider reaching out to someone you trust "
                "or a qualified professional for immediate support."
            )

        else:
            st.write("The text has a neutral tone.")

st.divider()

st.caption("Sentiment Analysis Project • Python + Streamlit")
