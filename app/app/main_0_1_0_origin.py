import streamlit as st
from pathlib import Path
import re

st.title("Astra Lex — Space Law AI")
st.caption("Prototype for structured consultation of international space law")

st.markdown("""
Launched on April 12, 2026, Astra Lex is a prototype for structured consultation of international space law.

This first version allows users to query the 1967 Outer Space Treaty, identify the most relevant article based on a given question, provide a concise synthesis, and explain the reasoning behind this selection.

Astra Lex provides structured legal information, not legal advice.

This launch marks the first step toward a more comprehensive system for the analysis of space law.
""")
st.markdown("""
Launched on April 12, 2026, Astra Lex is a prototype for structured consultation of international space law.

This first version allows users to query the 1967 Outer Space Treaty, identify the most relevant article based on a given question, provide a concise synthesis, and explain the reasoning behind this selection.

Astra Lex provides structured legal information, not legal advice.

This launch marks the first step toward a more comprehensive system for the analysis of space law.
""")

base_path = Path(__file__).resolve().parent.parent
text_file = base_path / "texts" / "outer_space_treaty.txt"


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
    "17": "XVII"
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
    "seventeenth": "XVII"
}


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

    match = re.search(r"\barticle\s+(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth)\b", q)
    if match:
        return "ARTICLE " + ORDINAL_MAP[match.group(1)]

    match = re.search(r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth)\s+article\b", q)
    if match:
        return "ARTICLE " + ORDINAL_MAP[match.group(1)]

    match = re.search(r"\b(\d+)(st|nd|rd|th)\s+article\b", q)
    if match:
        num = match.group(1)
        if num in ROMAN_MAP:
            return "ARTICLE " + ROMAN_MAP[num]

    return None


def normalize_question(question):
    q = question.lower()

    replacements = {
        "own": "appropriation sovereignty",
        "ownership": "appropriation sovereignty",
        "appropriate": "appropriation sovereignty",
        "country": "state",
        "countries": "states",
        "state": "state sovereignty",
        "responsible": "responsibility",
        "responsibility": "responsibility",
        "liable": "liability damage",
        "liability": "liability damage",
        "damage": "liable liability",
        "damages": "liable liability",
        "caused": "damage liability",
        "space object": "object launched",
        "space objects": "object launched",
        "harmful interference": "harmful interference consultations",
        "interference": "harmful interference consultations",
        "consultation": "consultations harmful interference",
        "consultations": "consultations harmful interference",
        "free exploration": "free exploration use",
        "exploration": "exploration use freedom",
        "use": "use freedom",
        "moon": "moon celestial bodies",
        "celestial body": "celestial bodies moon",
        "celestial bodies": "celestial bodies moon",
        "astronaut": "astronauts envoys assistance return",
        "astronauts": "astronauts envoys assistance return",
        "envoy": "envoys mankind astronauts",
        "rescue": "astronauts assistance return",
        "return": "astronauts return rescue",
        "assistance": "astronauts assistance rescue",
        "private company": "non-governmental entities authorization supervision",
        "private companies": "non-governmental entities authorization supervision",
        "private entity": "non-governmental entities authorization supervision",
        "non-governmental": "non-governmental entities authorization supervision",
        "authorization": "authorization supervision non-governmental",
        "supervision": "authorization supervision non-governmental",
        "registered": "registry jurisdiction control",
        "registry": "registry jurisdiction control",
        "register": "registry jurisdiction control",
        "control": "jurisdiction control registry",
        "jurisdiction": "jurisdiction control registry",
        "peaceful": "peaceful purposes weapons nuclear",
        "nuclear": "nuclear weapons mass destruction",
        "weapons": "weapons mass destruction peaceful",
        "military": "military peaceful weapons",
        "orbit": "orbit nuclear weapons object",
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
        "chinese": "english russian french spanish chinese authentic texts"
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
    if "consultation" in q and article_name == "ARTICLE IX":
        score += 10
    if "observe" in q and article_name == "ARTICLE X":
        score += 10
    if "secretary-general" in q and article_name == "ARTICLE XI":
        score += 10
    if "stations" in q and article_name == "ARTICLE XII":
        score += 10
    if "international intergovernmental organizations" in q and article_name == "ARTICLE XIII":
        score += 10
    if "entry into force" in q and article_name == "ARTICLE XIV":
        score += 10
    if "amendments" in q and article_name == "ARTICLE XV":
        score += 10
    if "withdrawal" in q and article_name == "ARTICLE XVI":
        score += 10
    if "authentic texts" in q and article_name == "ARTICLE XVII":
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


def build_reason(article_name, direct_reference=False):
    if direct_reference:
        return f"Astra Lex selected {article_name} because your question directly refers to that article."
    return f"Astra Lex selected {article_name} as the most relevant legal provision."


question = st.text_input("Ask one question about space law:")
st.caption("Please ask one legal question at a time.")

if text_file.exists():
    treaty_text = text_file.read_text(encoding="utf-8")
    articles = split_articles(treaty_text)
else:
    treaty_text = ""
    articles = {}

if question:
    st.subheader("Your question")
    st.write(question)

    if not text_file.exists():
        st.subheader("Result")
        st.write("Error: the legal text file was not found.")
    elif not articles:
        st.subheader("Result")
        st.write("Error: the legal text was loaded, but no articles were detected.")
    else:
        direct = extract_article_reference(question, articles)

        if direct and direct in articles:
            article_name = direct
            article_text = articles[article_name]
            direct_reference = True
        else:
            best_score = -1
            best_article = None

            for name, text in articles.items():
                s = score_article(question, text, name)
                if s > best_score:
                    best_score = s
                    best_article = (name, text)

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
