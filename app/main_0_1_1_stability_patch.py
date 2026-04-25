import re
from pathlib import Path
import streamlit as st

# =========================
# Astra Lex — Version 0.1.1
# =========================

APP_TITLE = "Astra Lex — Space Law AI"
APP_CAPTION = "Prototype for structured consultation of international space law"

PRESENTATION_TEXT = """
Launched on April 12, 2026, Astra Lex is a prototype for structured consultation of international space law.

This first version allows users to query the 1967 Outer Space Treaty, identify the most relevant article based on a given question, provide a concise synthesis, and explain the reasoning behind this selection.

Astra Lex provides structured legal information, not legal advice.

This launch marks the first step toward a more comprehensive system for the analysis of space law.
"""

BASE_PATH = Path(__file__).resolve().parent.parent
TEXT_FILE = BASE_PATH / "texts" / "outer_space_treaty.txt"

ROMAN_MAP = {
    "1": "I", "2": "II", "3": "III", "4": "IV", "5": "V",
    "6": "VI", "7": "VII", "8": "VIII", "9": "IX",
    "10": "X", "11": "XI", "12": "XII", "13": "XIII",
    "14": "XIV", "15": "XV", "16": "XVI", "17": "XVII"
}

ORDINAL_MAP = {
    "first": "I", "second": "II", "third": "III", "fourth": "IV",
    "fifth": "V", "sixth": "VI", "seventh": "VII", "eighth": "VIII",
    "ninth": "IX", "tenth": "X", "eleventh": "XI", "twelfth": "XII",
    "thirteenth": "XIII", "fourteenth": "XIV", "fifteenth": "XV",
    "sixteenth": "XVI", "seventeenth": "XVII"
}

def split_articles(text):
    articles = {}
    current_article = None
    current_lines = []

    for line in text.splitlines():
        stripped = line.strip()
        upper = stripped.upper()

        if upper.startswith("ARTICLE "):
            if current_article:
                articles[current_article] = "\n".join(current_lines).strip()
            current_article = upper
            current_lines = []
        elif current_article:
            current_lines.append(stripped)

    if current_article:
        articles[current_article] = "\n".join(current_lines).strip()

    return articles

def extract_article_reference(question, articles):
    q = question.lower()

    if "last article" in q or "final article" in q:
        if articles:
            return sorted(articles.keys())[-1]

    match = re.search(r"\barticle\s+([ivxlcdm]+)\b", q)
    if match:
        return "ARTICLE " + match.group(1).upper()

    match = re.search(r"\barticle\s+(\d+)\b", q)
    if match:
        num = match.group(1)
        if num in ROMAN_MAP:
            return "ARTICLE " + ROMAN_MAP[num]

    ordinal_words = "|".join(ORDINAL_MAP.keys())

    match = re.search(rf"\barticle\s+({ordinal_words})\b", q)
    if match:
        return "ARTICLE " + ORDINAL_MAP[match.group(1)]

    match = re.search(rf"\b({ordinal_words})\s+article\b", q)
    if match:
        return "ARTICLE " + ORDINAL_MAP[match.group(1)]

    match = re.search(r"\b(\d+)(st|nd|rd|th)\s+article\b", q)
    if match:
        num = match.group(1)
        if num in ROMAN_MAP:
            return "ARTICLE " + ROMAN_MAP[num]

    return None

def score_article(question, article_text, article_name):
    q = question.lower()
    words = q.split()
    text = article_text.lower()

    score = 0

    for word in words:
        if word in text:
            score += 2

    if "appropriation" in q and article_name == "ARTICLE II":
        score += 10
    if "responsibility" in q and article_name == "ARTICLE VI":
        score += 10
    if "liability" in q and article_name == "ARTICLE VII":
        score += 10
    if "astronaut" in q and article_name == "ARTICLE V":
        score += 10
    if "nuclear" in q and article_name == "ARTICLE IV":
        score += 10

    return score

def build_short_answer(article_name):
    answers = {
        "ARTICLE I": "Outer space is free for exploration and use by all States.",
        "ARTICLE II": "Outer space is not subject to national appropriation.",
        "ARTICLE III": "Activities must comply with international law.",
        "ARTICLE IV": "Weapons of mass destruction are prohibited in orbit.",
        "ARTICLE V": "Astronauts must be assisted and returned safely.",
        "ARTICLE VI": "States are responsible for national space activities.",
        "ARTICLE VII": "States are liable for damage caused by space objects.",
        "ARTICLE VIII": "States retain jurisdiction over registered objects.",
        "ARTICLE IX": "States must avoid harmful interference and consult.",
        "ARTICLE X": "States may observe space object flights.",
        "ARTICLE XI": "States must share information about space activities.",
        "ARTICLE XII": "Facilities must be open on a reciprocal basis.",
        "ARTICLE XIII": "The Treaty applies to international organizations.",
        "ARTICLE XIV": "Defines ratification and entry into force.",
        "ARTICLE XV": "Allows amendments.",
        "ARTICLE XVI": "Allows withdrawal.",
        "ARTICLE XVII": "Defines authentic languages."
    }

    return answers.get(article_name, "See full article.")

def load_articles():
    if not TEXT_FILE.exists():
        return None

    treaty_text = TEXT_FILE.read_text(encoding="utf-8")
    return split_articles(treaty_text)

# =========================
# UI
# =========================

st.title(APP_TITLE)
st.caption(APP_CAPTION)

# 🔥 IMPORTANT : affiché UNE SEULE FOIS
st.markdown(PRESENTATION_TEXT)

st.write("---")

st.subheader("Ask one question about space law:")
question = st.text_input("")

st.caption("Please ask one legal question at a time.")

articles = load_articles()

if question:
    st.subheader("Your question")
    st.write(question)

    if articles is None:
        st.error("Error: legal text file not found.")
    else:
        direct = extract_article_reference(question, articles)

        if direct and direct in articles:
            article_name = direct
            article_text = articles[article_name]
        else:
            best_score = -1
            article_name = None
            article_text = None

            for name, text in articles.items():
                score = score_article(question, text, name)
                if score > best_score:
                    best_score = score
                    article_name = name
                    article_text = text

        if article_name:
            st.subheader("Short answer")
            st.write(build_short_answer(article_name))

            st.subheader("Most relevant legal article")
            st.write(article_name)
            st.text(article_text)

            st.subheader("Disclaimer")
            st.write("Astra Lex provides legal information, not legal advice.")
