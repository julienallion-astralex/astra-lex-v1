import re
from pathlib import Path
import streamlit as st


# =========================
# Astra Lex — Version 0.1.2
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
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V",
    "6": "VI",
    "7": "VII",
    "8": "VIII",
    "9": "IX",
    "10": "X",
    "11": "XI",
    "12": "XII",
    "13": "XIII",
    "14": "XIV",
    "15": "XV",
    "16": "XVI",
    "17": "XVII",
}

ORDINAL_MAP = {
    "first": "I",
    "second": "II",
    "third": "III",
    "fourth": "IV",
    "fifth": "V",
    "sixth": "VI",
    "seventh": "VII",
    "eighth": "VIII",
    "ninth": "IX",
    "tenth": "X",
    "eleventh": "XI",
    "twelfth": "XII",
    "thirteenth": "XIII",
    "fourteenth": "XIV",
    "fifteenth": "XV",
    "sixteenth": "XVI",
    "seventeenth": "XVII",
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
            return sorted_articles(articles)[-1]

    match = re.search(r"\barticle\s+([ivxlcdm]+)\b", q)
    if match:
        return "ARTICLE " + match.group(1).upper()

    match = re.search(r"\barticle\s+(\d+)\b", q)
    if match:
        number = match.group(1)
        if number in ROMAN_MAP:
            return "ARTICLE " + ROMAN_MAP[number]

    ordinal_words = "|".join(ORDINAL_MAP.keys())

    match = re.search(rf"\barticle\s+({ordinal_words})\b", q)
    if match:
        return "ARTICLE " + ORDINAL_MAP[match.group(1)]

    match = re.search(rf"\b({ordinal_words})\s+article\b", q)
    if match:
        return "ARTICLE " + ORDINAL_MAP[match.group(1)]

    match = re.search(r"\b(\d+)(st|nd|rd|th)\s+article\b", q)
    if match:
        number = match.group(1)
        if number in ROMAN_MAP:
            return "ARTICLE " + ROMAN_MAP[number]

    return None


def roman_to_number(article_name):
    roman_values = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
        "VIII": 8,
        "IX": 9,
        "X": 10,
        "XI": 11,
        "XII": 12,
        "XIII": 13,
        "XIV": 14,
        "XV": 15,
        "XVI": 16,
        "XVII": 17,
    }

    roman = article_name.replace("ARTICLE", "").strip()
    return roman_values.get(roman, 999)


def sorted_articles(articles):
    return sorted(articles.keys(), key=roman_to_number)


def normalize_question(question):
    q = question.lower()

    replacements = {
        "own": "appropriation sovereignty claim",
        "ownership": "appropriation sovereignty claim",
        "owned": "appropriation sovereignty claim",
        "appropriate": "appropriation sovereignty claim",
        "appropriation": "appropriation sovereignty claim",
        "sovereignty": "appropriation sovereignty claim",
        "claim": "appropriation sovereignty claim",
        "country": "state",
        "countries": "states",
        "moon": "moon celestial bodies",
        "celestial body": "celestial bodies moon",
        "celestial bodies": "celestial bodies moon",
        "free exploration": "free exploration use",
        "exploration": "exploration use freedom",
        "responsible": "responsibility",
        "responsibility": "responsibility",
        "private company": "non-governmental entities authorization supervision",
        "private companies": "non-governmental entities authorization supervision",
        "private entity": "non-governmental entities authorization supervision",
        "non-governmental": "non-governmental entities authorization supervision",
        "authorization": "authorization supervision non-governmental",
        "supervision": "authorization supervision non-governmental",
        "liable": "liability damage",
        "liability": "liability damage",
        "damage": "liability damage",
        "damages": "liability damage",
        "caused": "damage liability",
        "astronaut": "astronauts envoys assistance return",
        "astronauts": "astronauts envoys assistance return",
        "envoy": "envoys astronauts",
        "rescue": "astronauts assistance return",
        "return": "astronauts assistance return",
        "assistance": "astronauts assistance return",
        "nuclear": "nuclear weapons mass destruction",
        "weapon": "nuclear weapons mass destruction",
        "weapons": "nuclear weapons mass destruction",
        "orbit": "orbit nuclear weapons",
        "military": "military peaceful weapons",
        "peaceful": "peaceful purposes weapons",
        "registered": "registry jurisdiction control",
        "registry": "registry jurisdiction control",
        "register": "registry jurisdiction control",
        "control": "jurisdiction control registry",
        "jurisdiction": "jurisdiction control registry",
        "consultation": "consultations harmful interference",
        "consultations": "consultations harmful interference",
        "interference": "harmful interference consultations",
        "harmful interference": "harmful interference consultations",
        "contamination": "harmful contamination due regard",
        "international law": "charter united nations international law",
        "united nations": "charter united nations international law",
        "observe": "observe observation flight",
        "observation": "observe observation flight",
        "flight": "observe observation flight",
        "inform": "inform secretary-general public scientific community",
        "information": "inform secretary-general public scientific community",
        "secretary-general": "inform secretary-general public scientific community",
        "public": "inform public scientific community",
        "scientific community": "scientific community inform",
        "stations": "stations installations equipment reciprocity visit",
        "installations": "stations installations equipment reciprocity visit",
        "equipment": "stations installations equipment reciprocity visit",
        "visit": "reciprocity visit consultations safety",
        "reciprocity": "reciprocity visit stations",
        "international organization": "international intergovernmental organizations responsibility",
        "international organizations": "international intergovernmental organizations responsibility",
        "entry into force": "entry into force ratification accession depositary",
        "ratification": "ratification accession depositary entry into force",
        "accession": "ratification accession depositary entry into force",
        "depositary": "depositary governments ratification accession",
        "amendment": "amendments acceptance majority",
        "amendments": "amendments acceptance majority",
        "withdraw": "withdrawal notification",
        "withdrawal": "withdrawal notification",
        "languages": "english russian french spanish chinese authentic texts",
        "authentic": "english russian french spanish chinese authentic texts",
        "english": "english russian french spanish chinese authentic texts",
        "russian": "english russian french spanish chinese authentic texts",
        "french": "english russian french spanish chinese authentic texts",
        "spanish": "english russian french spanish chinese authentic texts",
        "chinese": "english russian french spanish chinese authentic texts",
    }

    for old, new in replacements.items():
        q = q.replace(old, new)

    return q


def score_article(question, article_text, article_name):
    q = normalize_question(question)
    words = q.split()
    text = article_text.lower()

    score = 0

    for word in words:
        if word in text:
            score += 2

    # Strong legal routing rules
    if any(term in q for term in ["appropriation", "sovereignty", "claim"]):
        if article_name == "ARTICLE II":
            score += 50

    if "free" in q and "exploration" in q:
        if article_name == "ARTICLE I":
            score += 40

    if "international law" in q or "charter" in q:
        if article_name == "ARTICLE III":
            score += 35

    if any(term in q for term in ["nuclear", "weapons", "military", "peaceful"]):
        if article_name == "ARTICLE IV":
            score += 40

    if "astronauts" in q or "envoys" in q:
        if article_name == "ARTICLE V":
            score += 40

    if "responsibility" in q:
        if article_name == "ARTICLE VI":
            score += 40

    if "non-governmental" in q or "authorization" in q or "supervision" in q:
        if article_name == "ARTICLE VI":
            score += 40

    if "liability" in q or "damage" in q:
        if article_name == "ARTICLE VII":
            score += 40

    if any(term in q for term in ["registry", "jurisdiction", "control"]):
        if article_name == "ARTICLE VIII":
            score += 40

    if any(term in q for term in ["consultations", "interference", "harmful", "contamination"]):
        if article_name == "ARTICLE IX":
            score += 40

    if "observe" in q or "observation" in q or "flight" in q:
        if article_name == "ARTICLE X":
            score += 35

    if "secretary-general" in q or "scientific community" in q or "inform" in q:
        if article_name == "ARTICLE XI":
            score += 35

    if any(term in q for term in ["stations", "installations", "equipment", "visit", "reciprocity"]):
        if article_name == "ARTICLE XII":
            score += 35

    if "international intergovernmental organizations" in q:
        if article_name == "ARTICLE XIII":
            score += 35

    if any(term in q for term in ["ratification", "accession", "depositary", "entry into force"]):
        if article_name == "ARTICLE XIV":
            score += 35

    if "amendments" in q or "amendment" in q:
        if article_name == "ARTICLE XV":
            score += 35

    if "withdrawal" in q or "withdraw" in q:
        if article_name == "ARTICLE XVI":
            score += 35

    if "authentic" in q or "languages" in q:
        if article_name == "ARTICLE XVII":
            score += 35

    return score


def build_short_answer(article_name):
    answers = {
        "ARTICLE I": "Outer space is free for exploration and use by all States.",
        "ARTICLE II": "Outer space, including the Moon and other celestial bodies, is not subject to national appropriation.",
        "ARTICLE III": "Activities in outer space must be carried on in accordance with international law.",
        "ARTICLE IV": "Weapons of mass destruction are prohibited in orbit, and celestial bodies must be used for peaceful purposes.",
        "ARTICLE V": "Astronauts are regarded as envoys of mankind and must be assisted and returned safely.",
        "ARTICLE VI": "States bear international responsibility for national space activities, including activities by non-governmental entities.",
        "ARTICLE VII": "Launching States may be internationally liable for damage caused by their space objects.",
        "ARTICLE VIII": "A State on whose registry a space object is carried retains jurisdiction and control over that object and its personnel.",
        "ARTICLE IX": "States must act with due regard, avoid harmful contamination, and consult before causing potentially harmful interference.",
        "ARTICLE X": "States must consider requests to observe the flight of space objects on a basis of equality.",
        "ARTICLE XI": "States conducting space activities agree to inform the Secretary-General, the public, and the international scientific community.",
        "ARTICLE XII": "Stations, installations, equipment, and space vehicles on celestial bodies must be open on a basis of reciprocity.",
        "ARTICLE XIII": "The Treaty applies to activities carried out by States individually, jointly, or through international intergovernmental organizations.",
        "ARTICLE XIV": "This article defines signature, ratification, accession, depositary governments, and entry into force.",
        "ARTICLE XV": "States Parties may propose amendments to the Treaty.",
        "ARTICLE XVI": "A State Party may withdraw from the Treaty by written notification after one year.",
        "ARTICLE XVII": "The Treaty texts in English, Russian, French, Spanish, and Chinese are equally authentic.",
    }

    return answers.get(article_name, "See full article.")


def build_reason(article_name, direct_reference=False):
    if direct_reference:
        return f"Astra Lex selected {article_name} because your question directly refers to that article."

    reasons = {
        "ARTICLE I": "Astra Lex selected this article because your question relates to freedom of exploration and use of outer space.",
        "ARTICLE II": "Astra Lex selected this article because your question relates to ownership, appropriation, sovereignty, or claims over the Moon or other celestial bodies.",
        "ARTICLE III": "Astra Lex selected this article because your question relates to international law and the general legal framework governing space activities.",
        "ARTICLE IV": "Astra Lex selected this article because your question relates to peaceful uses of space or prohibited weapons in orbit or on celestial bodies.",
        "ARTICLE V": "Astra Lex selected this article because your question relates to astronauts, their assistance, rescue, return, or emergency situations.",
        "ARTICLE VI": "Astra Lex selected this article because your question relates to responsibility for national space activities or non-governmental entities.",
        "ARTICLE VII": "Astra Lex selected this article because your question relates to damage, liability, or harm caused by a space object.",
        "ARTICLE VIII": "Astra Lex selected this article because your question relates to registry, jurisdiction, control, or authority over space objects.",
        "ARTICLE IX": "Astra Lex selected this article because your question relates to due regard, harmful interference, contamination, or international consultations.",
        "ARTICLE X": "Astra Lex selected this article because your question relates to observation of space object flights.",
        "ARTICLE XI": "Astra Lex selected this article because your question relates to information-sharing about space activities.",
        "ARTICLE XII": "Astra Lex selected this article because your question relates to access to stations, installations, equipment, or space vehicles on celestial bodies.",
        "ARTICLE XIII": "Astra Lex selected this article because your question relates to international organizations and joint space activities.",
        "ARTICLE XIV": "Astra Lex selected this article because your question relates to signature, ratification, accession, depositary governments, or entry into force.",
        "ARTICLE XV": "Astra Lex selected this article because your question relates to amendments to the Treaty.",
        "ARTICLE XVI": "Astra Lex selected this article because your question relates to withdrawal from the Treaty.",
        "ARTICLE XVII": "Astra Lex selected this article because your question relates to authentic languages or the final formal provisions of the Treaty.",
    }

    return reasons.get(article_name, f"Astra Lex selected {article_name} as the most relevant legal provision.")


def load_articles():
    if not TEXT_FILE.exists():
        return None

    treaty_text = TEXT_FILE.read_text(encoding="utf-8")
    return split_articles(treaty_text)


def display_homepage():
    st.title(APP_TITLE)
    st.caption(APP_CAPTION)
    st.markdown(PRESENTATION_TEXT)
    st.write("---")


def display_answer(question, articles):
    st.subheader("Your question")
    st.write(question)

    if articles is None:
        st.error("Error: the legal text file was not found.")
        return

    if not articles:
        st.error("Error: the legal text was loaded, but no articles were detected.")
        return

    direct = extract_article_reference(question, articles)

    if direct and direct in articles:
        article_name = direct
        article_text = articles[article_name]
        direct_reference = True
    else:
        best_score = -1
        best_article = None

        for name, text in articles.items():
            score = score_article(question, text, name)
            if score > best_score:
                best_score = score
                best_article = (name, text)

        if best_article is None:
            st.warning("No relevant article found.")
            return

        article_name, article_text = best_article
        direct_reference = False

    st.subheader("Short answer")
    st.write(build_short_answer(article_name))

    st.subheader("Most relevant legal article")
    st.write(article_name)
    st.text(article_text)

    st.subheader("Why Astra Lex selected this article")
    st.write(build_reason(article_name, direct_reference))

    st.subheader("Disclaimer")
    st.write("Astra Lex provides legal information, not legal advice.")


# =========================
# Streamlit App
# =========================

display_homepage()

st.subheader("Ask one question about space law:")
question = st.text_input("")

st.caption("Please ask one legal question at a time.")

articles = load_articles()

if question:
    display_answer(question, articles)
