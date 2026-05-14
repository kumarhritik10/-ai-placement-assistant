# AI Placement Writing Assistant

> An AI-powered NLP tool that helps college students write better resumes, polish interview answers, and upgrade vocabulary for campus placements.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

### Resume Corrector
- **Probabilistic spell correction** using the Norvig algorithm (edit-distance + unigram language model)
- **Placement-domain vocabulary** — domain terms like `CTC`, `LPA`, `CGPA`, `TensorFlow`, `ReactJS` are never mis-corrected
- **Word-level diff view** — hover over any highlighted word to see what was changed
- **ATS keyword scoring** — see which role-specific keywords are matched vs missing
- **Composite Resume Score** (Spell + ATS + Professionalism)
- Download corrected text

### Interview Answer Polish
- **Filler word detector** — highlights weak words like *basically, literally, kind of, I think*
- **Professionalism score** — 0–100 penalty-based metric
- Spell-corrected, polished answer output
- STAR method tips panel

### Vocabulary Upgrade
- **Weak-to-strong word mapper** — detects words like *used, made, helped, worked on* and suggests power alternatives
- **Power verb bank** — curated action verbs (*Architected, Spearheaded, Optimized*...)
- **ATS keyword reference** per target role

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Spell Correction | Norvig Algorithm (custom, `auto_correct.py`) |
| Grammar Pass | TextBlob |
| Domain Vocab | Custom `placement_vocab.py` |
| Corpus | Peter Norvig's `big.txt` (auto-downloaded) |

---

## Project Structure

```
ai-placement-assistant/
├── app.py                  # Main Streamlit application
├── auto_correct.py         # Norvig spell-corrector with placement vocab
├── placement_vocab.py      # Domain vocabulary, ATS keywords, filler words
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Dark theme configuration
└── README.md
```

---

## Run Locally

```bash
git clone https://github.com/yourusername/ai-placement-assistant.git
cd ai-placement-assistant

pip install -r requirements.txt
python -m textblob.download_corpora

streamlit run app.py
```

The corpus (`big.txt`) downloads automatically on first run (~6 MB).

---

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select `app.py` as the main file
5. Click **Deploy**

No additional configuration needed — `requirements.txt` and `.streamlit/config.toml` are auto-detected.

---

## How the Spell Corrector Works

The core algorithm is based on **Peter Norvig's probabilistic spell-corrector**:

1. **Language Model** — builds a frequency table from a large English corpus (`big.txt`)
2. **Edit Distance** — generates all words within 1 or 2 character edits (delete, transpose, replace, insert)
3. **Candidate Selection** — picks the candidate with the highest corpus probability
4. **Domain Injection** — placement-specific words are assigned very high frequency weights so they are never corrected away

```python
P(word) = freq(word) / total_words      # unigram probability
correction(word) = argmax P(candidate)   # most probable candidate
```

---

## How ATS Scoring Works

ATS (Applicant Tracking System) scoring checks how many role-specific keywords appear in the text:

```
ATS Score = matched_keywords / total_role_keywords * 100
```

Keywords are curated for 6 roles: SDE, Data Analyst, ML Engineer, Full Stack, DevOps, Business Analyst.

---

## Resume Score Formula

```
Resume Score = Spell Score * 0.35 + ATS Score * 0.35 + Professionalism Score * 0.30
```

---

## License

MIT License — free to use, modify, and distribute.
