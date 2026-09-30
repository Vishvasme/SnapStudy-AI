import streamlit as st
import re

st.set_page_config(
    page_title="SnapStudy AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 SnapStudy AI")
st.subheader("Your lightweight AI-powered study assistant")

st.write(
    "Paste your study material below and generate a concise study guide."
)

text = st.text_area(
    "Study Material",
    height=250,
    placeholder="Paste your lecture notes, textbook content, or study material here..."
)

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def summarize(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    if len(sentences) <= 5:
        return sentences

    return sentences[:5]

def create_questions(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

    questions = []

    for sentence in sentences[:5]:
        words = sentence.split()

        if len(words) >= 5:
            keyword = words[min(3, len(words) - 1)].strip(".,!?")
            questions.append(
                f"What is the significance of {keyword} according to the study material?"
            )

    return questions

if st.button("✨ Generate Study Guide"):

    if not text.strip():
        st.warning("Please enter some study material first.")

    else:
        text = clean_text(text)

        st.success("Study guide generated!")

        st.markdown("## 📝 Summary")

        summary = summarize(text)

        for sentence in summary:
            st.write("• " + sentence)

        st.markdown("## ❓ Practice Questions")

        questions = create_questions(text)

        if questions:
            for i, question in enumerate(questions, 1):
                st.write(f"**{i}. {question}**")
        else:
            st.write("Add more detailed study material to generate questions.")

        st.markdown("## 🧠 Key Topics")

        words = text.split()

        # Simple frequency-based topic extraction
        stopwords = {
            "the", "and", "that", "this", "with", "from",
            "have", "which", "are", "was", "were", "for",
            "into", "their", "there", "about", "these",
            "they", "then", "than", "also", "been"
        }

        frequency = {}

        for word in words:
            word = re.sub(r"[^a-zA-Z]", "", word).lower()

            if len(word) > 5 and word not in stopwords:
                frequency[word] = frequency.get(word, 0) + 1

        topics = sorted(
            frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:8]

        for topic, count in topics:
            st.write(f"🔹 **{topic}**")

st.divider()

st.caption(
    "SnapStudy AI — A prototype for exploring AI-assisted learning "
    "and privacy-friendly study workflows."
)
