import streamlit as st
import re

# ==================================================
# SENTIMENT & MOOD DATA
# ==================================================

MOODS = {
    "Happy": {
        "emoji": "😊",
        "keywords": [
            "happy", "great", "good", "amazing", "wonderful",
            "joy", "joyful", "awesome", "fantastic", "glad",
            "grateful", "thankful", "blessed", "love"
        ],
        "suggestion": "Keep enjoying this moment! Celebrate your small wins and share your happiness with someone. ✨",
        "try": "🎉 Celebrate a small win • ❤️ Share your happiness • 📸 Capture the moment"
    },

    "Excited": {
        "emoji": "🤩",
        "keywords": [
            "excited", "exciting", "thrilled", "eager",
            "can't wait", "looking forward", "yay"
        ],
        "suggestion": "Your excitement is great energy! Use it to take one positive step toward your goal. 🚀",
        "try": "🎯 Set a goal • 🚀 Take action • 📝 Plan your next step"
    },

    "Sad": {
        "emoji": "😔",
        "keywords": [
            "sad", "cry", "crying", "lonely", "alone",
            "heartbroken", "grief", "miserable", "empty",
            "lost", "upset"
        ],
        "suggestion": "It's okay to have difficult days. Give yourself some time and talk to someone you trust. 💙",
        "try": "🎵 Listen to music • 🚶 Take a short walk • 💬 Talk to someone"
    },

    "Depressed": {
        "emoji": "💙",
        "keywords": [
            "depressed", "depression", "hopeless",
            "worthless", "numb", "no hope"
        ],
        "suggestion": "You don't have to handle everything alone. Be gentle with yourself and consider reaching out to someone you trust or a mental-health professional. 💙",
        "try": "💬 Talk to someone • 🌿 Take one small step • 🧘 Give yourself time"
    },

    "Anxious": {
        "emoji": "😰",
        "keywords": [
            "anxious", "anxiety", "panic", "nervous",
            "worried", "stress", "stressed", "overwhelmed",
            "scared", "fear", "uneasy"
        ],
        "suggestion": "Take a slow breath and focus on one thing at a time. You don't need to solve everything right now. 🌿",
        "try": "🌬️ Deep breathing • 📝 Write your thoughts • 📵 Take a screen break"
    },

    "Angry": {
        "emoji": "😡",
        "keywords": [
            "angry", "anger", "furious", "rage", "hate",
            "frustrated", "frustration", "annoyed",
            "irritated", "mad"
        ],
        "suggestion": "Pause before reacting. Take a few breaths and step away for a moment before responding. 🧘",
        "try": "🚶 Step away • 💧 Drink water • ⏳ Wait before responding"
    },

    "Tired": {
        "emoji": "😴",
        "keywords": [
            "tired", "exhausted", "drained", "sleepy",
            "fatigued", "weak", "burnout", "burnt out",
            "no energy"
        ],
        "suggestion": "Your body may need a break. Rest, hydrate, and give yourself permission to slow down. 🌙",
        "try": "😴 Rest • 💧 Hydrate • 🌙 Get proper sleep"
    },

    "Calm": {
        "emoji": "😌",
        "keywords": [
            "calm", "peaceful", "relaxed", "fine",
            "okay", "ok", "alright", "steady"
        ],
        "suggestion": "You seem to be in a balanced state. Keep doing what helps you feel peaceful. 🌿",
        "try": "🧘 Meditate • 🎵 Enjoy calm music • 🌿 Spend time peacefully"
    },

    "Motivated": {
        "emoji": "💪",
        "keywords": [
            "motivated", "focused", "determined",
            "confident", "productive", "strong",
            "ready", "goal", "achieve"
        ],
        "suggestion": "You've got momentum! Keep going, even if progress feels small. Consistency beats perfection. 🔥",
        "try": "🎯 Set a goal • ⏱️ Start a task • ✅ Track your progress"
    },

    "Successful": {
        "emoji": "🏆",
        "keywords": [
            "success", "successful", "selected", "won",
            "achieved", "achievement", "promoted",
            "passed", "victory", "accomplished"
        ],
        "suggestion": "Congratulations! 🎉 You earned this moment. Celebrate your achievement and use it as motivation for your next goal.",
        "try": "🏆 Celebrate • 📝 Reflect • 🚀 Set your next goal"
    },

    "Lonely": {
        "emoji": "🥺",
        "keywords": [
            "lonely", "alone", "isolated",
            "no one", "nobody"
        ],
        "suggestion": "Feeling lonely can be difficult. Consider connecting with a friend, family member, or someone you trust. ❤️",
        "try": "💬 Message a friend • 👨‍👩‍👧 Spend time with family • ❤️ Connect with someone"
    }
}


# ==================================================
# ANALYSIS FUNCTION
# ==================================================

def analyze_text(text):

    text_lower = text.lower()

    # ----------------------------------------------
    # Mood detection
    # ----------------------------------------------

    mood = "Neutral"

    for mood_name, data in MOODS.items():

        for word in data["keywords"]:

            if word in text_lower:
                mood = mood_name
                break

        if mood != "Neutral":
            break

    # ----------------------------------------------
    # Positive / Negative words
    # ----------------------------------------------

    positive_words = [
        "happy", "good", "great", "amazing", "awesome",
        "love", "wonderful", "excellent", "success",
        "successful", "excited", "best", "grateful",
        "thankful", "achieved", "won"
    ]

    negative_words = [
        "sad", "bad", "hate", "angry", "upset",
        "depressed", "anxious", "stress", "worried",
        "lonely", "tired", "terrible", "hopeless",
        "worthless", "frustrated"
    ]

    positive_count = sum(
        text_lower.count(word)
        for word in positive_words
    )

    negative_count = sum(
        text_lower.count(word)
        for word in negative_words
    )

    # ----------------------------------------------
    # Sentiment
    # ----------------------------------------------

    if positive_count > negative_count:
        sentiment = "Positive"

    elif negative_count > positive_count:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    # ----------------------------------------------
    # Score
    # ----------------------------------------------

    total = positive_count + negative_count

    if total == 0:
        score = 0.0

    else:
        score = (positive_count - negative_count) / total

    # ----------------------------------------------
    # Intensity
    # ----------------------------------------------

    score_abs = abs(score)

    if score_abs >= 0.70:
        intensity = "High"

    elif score_abs >= 0.30:
        intensity = "Medium"

    else:
        intensity = "Low"

    # ----------------------------------------------
    # Tone
    # ----------------------------------------------

    if mood in ["Happy", "Excited", "Motivated", "Successful"]:
        tone = "Positive & Energetic"

    elif mood in ["Sad", "Depressed", "Lonely"]:
        tone = "Emotional"

    elif mood in ["Angry"]:
        tone = "Aggressive"

    elif mood in ["Anxious"]:
        tone = "Worried"

    elif mood in ["Tired"]:
        tone = "Low Energy"

    elif mood in ["Calm"]:
        tone = "Peaceful"

    else:
        tone = "Neutral"

    # ----------------------------------------------
    # Statistics
    # ----------------------------------------------

    words = text.split()

    word_count = len(words)

    character_count = len(text)

    sentences = len(
        re.findall(r"[.!?]+", text)
    )

    if sentences == 0:
        sentences = 1

    return (
        mood,
        sentiment,
        score,
        intensity,
        tone,
        word_count,
        character_count,
        sentences,
        positive_count,
        negative_count
    )


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Sentiment Analyzer",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("🧠 AI Sentiment & Mood Analyzer")

st.write(
    "Analyze emotions, sentiment, tone and intensity "
    "from any text using Python."
)

st.divider()


# ==================================================
# EXAMPLE TEXT
# ==================================================

st.subheader("✨ Try an Example")

col1, col2, col3 = st.columns(3)

if "text" not in st.session_state:
    st.session_state.text = ""


with col1:
    if st.button("😊 Happy Example"):
        st.session_state.text = (
            "I am extremely happy today! "
            "Everything is going amazingly well."
        )

with col2:
    if st.button("😔 Sad Example"):
        st.session_state.text = (
            "I feel lonely and sad today. "
            "Nothing seems to be going right."
        )

with col3:
    if st.button("🏆 Success Example"):
        st.session_state.text = (
            "I finally got selected for my dream job! "
            "I am so excited and proud."
        )


# ==================================================
# TEXT INPUT
# ==================================================

st.subheader("📝 Enter Your Text")

text = st.text_area(
    "Write something below:",
    value=st.session_state.text,
    placeholder="Example: I worked really hard and finally achieved my goal!",
    height=160
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

if st.button(
    "🔍 Analyze Text",
    use_container_width=True
):

    if text.strip() == "":
        st.warning("Please enter some text first.")

    else:

        results = analyze_text(text)

        (
            mood,
            sentiment,
            score,
            intensity,
            tone,
            word_count,
            character_count,
            sentences,
            positive_count,
            negative_count
        ) = results

        st.divider()

        # ==========================================
        # MAIN RESULTS
        # ==========================================

        st.subheader("📊 Analysis Results")

        col1, col2, col3, col4, col5 = st.columns(5)

        mood_emoji = MOODS.get(
            mood,
            {"emoji": "😐"}
        )["emoji"]

        with col1:
            st.metric(
                "🎭 Mood",
                f"{mood_emoji} {mood}"
            )

        with col2:
            st.metric(
                "💭 Sentiment",
                sentiment
            )

        with col3:
            st.metric(
                "📊 Score",
                f"{score:+.2f}"
            )

        with col4:
            st.metric(
                "🔥 Intensity",
                intensity
            )

        with col5:
            st.metric(
                "🗣️ Tone",
                tone
            )

        # ==========================================
        # SENTIMENT METER
        # ==========================================

        st.subheader("📈 Sentiment Intensity")

        st.progress(
            int((score + 1) * 50)
        )

        st.caption(
            "Negative ← Sentiment → Positive"
        )

        # ==========================================
        # TEXT STATISTICS
        # ==========================================

        st.subheader("📝 Text Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Words",
                word_count
            )

        with col2:
            st.metric(
                "Characters",
                character_count
            )

        with col3:
            st.metric(
                "Sentences",
                sentences
            )

        with col4:
            st.metric(
                "Positive Words",
                positive_count
            )

        # ==========================================
        # PERSONALIZED SUGGESTION
        # ==========================================

        st.subheader("💡 Personalized Suggestion")

        if mood in MOODS:

            data = MOODS[mood]

            st.info(
                f"{data['emoji']} **{data['suggestion']}**"
            )

            st.write("### 🌱 You can try:")

            st.write(data["try"])

        else:

            st.info(
                "😐 Your text appears neutral. "
                "Keep going at your own pace."
            )

        # ==========================================
        # SENTIMENT BREAKDOWN
        # ==========================================

        st.subheader("📊 Sentiment Breakdown")

        total_words = positive_count + negative_count

        if total_words == 0:

            positive_percent = 0
            negative_percent = 0
            neutral_percent = 100

        else:

            positive_percent = (
                positive_count / total_words * 100
            )

            negative_percent = (
                negative_count / total_words * 100
            )

            neutral_percent = max(
                0,
                100 - positive_percent - negative_percent
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🟢 Positive",
                f"{positive_percent:.0f}%"
            )

        with col2:
            st.metric(
                "🔴 Negative",
                f"{negative_percent:.0f}%"
            )

        with col3:
            st.metric(
                "⚪ Neutral",
                f"{neutral_percent:.0f}%"
            )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Built with Python 🐍 + Streamlit • "
    "Sentiment & Mood Analysis Project"
)
