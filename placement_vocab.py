"""
placement_vocab.py
------------------
Curated vocabulary for the college placement domain.

Modules:
  PLACEMENT_WORDS  — domain terms boosted in spell-corrector (never mis-corrected)
  WEAK_TO_STRONG   — weak resume word → list of strong alternatives
  ATS_KEYWORDS     — role-specific keyword bank for ATS scoring
  FILLER_WORDS     — informal words to flag in interview answers
  POWER_VERBS      — strong action verbs for resume bullets
"""

# ── 1. Tech & Domain Jargon (These won't be spell-corrected) ─────────────────
PLACEMENT_WORDS = {
    # Programming & Frameworks
    "python", "java", "cpp", "cplusplus", "html", "css", "javascript", "typescript",
    "react", "reactjs", "nodejs", "nextjs", "vuejs", "angular", "php", "sql", "nosql",
    "tensorflow", "pytorch", "keras", "sklearn", "numpy", "pandas", "matplotlib", "seaborn",
    "fastapi", "flask", "django", "springboot", "opencv", "scikit-learn", "nltk", "transformers",
    
    # Infra & DB
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "kubernetes", "docker",
    "aws", "gcp", "azure", "terraform", "linux",
    
    # Placements & Academic
    "ctc", "lpa", "cgpa", "sgpa", "gpa", "ppo", "ppt", "btech", "mtech", "mba", "cttc", "bhuvneshwar", "bcrec",
    "infosys", "wipro", "tcs", "cognizant", "accenture", "deloitte", "capgemini",
    "certifications", "accomplishments", "coursework", "extracurricular", "coordinator", "karate",
    
    # NLP & ML Keywords
    "nlp", "llm", "bert", "gpt", "aiml", "preprocessing", "pipelines", "exploratory", "datasets",
    "grouping", "visualization", "recognition", "facial", "accuracy", "precision", "intelligent",
    "algorithmic", "spelling", "correction", "corrections", "detection", "identifying", "cleaning",
    "structures", "algorithms", "temporal", "series", "spatially", "artificial", "intelligence",
    
    # Strong Verbs (must never be corrected)
    "spearheaded", "orchestrated", "architected", "optimized", "streamlined",
    "automated", "mentored", "leveraged", "deployed", "refactored", "implemented",
    "implements", "structured", "filtering", "detecting", "classifying", "typing", "integrating",
    
    # General Acronyms
    "api", "restful", "graphql", "cicd", "devops", "mlops", "sde", "dsa", "oop", "mvc", "git"
}

# ── Weak word → strong resume alternatives ───────────────────────────────────
WEAK_TO_STRONG = {
    "used":           ["leveraged", "utilized", "implemented", "deployed"],
    "made":           ["developed", "architected", "engineered", "built"],
    "helped":         ["collaborated", "contributed", "facilitated", "assisted"],
    "worked on":      ["spearheaded", "led", "owned", "drove"],
    "did":            ["executed", "delivered", "accomplished", "performed"],
    "got":            ["achieved", "secured", "attained", "earned"],
    "showed":         ["demonstrated", "showcased", "illustrated", "presented"],
    "fixed":          ["resolved", "optimized", "debugged", "refactored"],
    "improved":       ["enhanced", "optimized", "accelerated", "elevated"],
    "created":        ["designed", "developed", "engineered", "built"],
    "increased":      ["scaled", "amplified", "boosted", "elevated"],
    "reduced":        ["optimized", "streamlined", "cut", "minimized"],
    "responsible for": ["owned", "led", "managed", "oversaw"],
    "learned":        ["mastered", "developed proficiency in", "acquired expertise in"],
    "handled":        ["managed", "oversaw", "coordinated", "governed"],
    "tried":          ["implemented", "explored", "prototyped", "developed"],
    "very good":      ["proficient", "expert", "highly skilled", "advanced"],
}

# ── ATS keyword banks by role ────────────────────────────────────────────────
ATS_KEYWORDS = {
    "Software Engineer (SDE)": [
        "data structures", "algorithms", "system design", "api",
        "microservices", "agile", "git", "docker", "ci/cd",
        "object-oriented", "design patterns", "scalability", "unit testing",
    ],
    "Data Analyst": [
        "sql", "python", "excel", "tableau", "power bi", "statistics",
        "data visualization", "etl", "dashboard", "regression",
        "hypothesis testing", "kpi", "reporting", "analytics",
    ],
    "ML / AI Engineer": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "computer vision", "tensorflow", "pytorch", "scikit-learn",
        "feature engineering", "model deployment", "mlops", "a/b testing",
    ],
    "Full Stack Developer": [
        "react", "nodejs", "mongodb", "rest api", "html", "css",
        "javascript", "typescript", "responsive design", "authentication",
        "frontend", "backend", "mvc", "database",
    ],
    "DevOps / Cloud": [
        "kubernetes", "docker", "aws", "gcp", "azure", "terraform",
        "ci/cd", "jenkins", "ansible", "monitoring", "linux", "automation",
    ],
    "Business Analyst": [
        "requirements", "stakeholder", "use case", "process mapping",
        "jira", "agile", "scrum", "user stories", "gap analysis",
        "sla", "kpi", "documentation", "presentation",
    ],
}

# ── Filler / informal words to flag in interview answers ─────────────────────
FILLER_WORDS = [
    "basically", "literally", "actually", "very", "really", "just",
    "stuff", "things", "kind of", "sort of", "a bit", "quite",
    "pretty much", "somewhat", "obviously", "honestly", "simply",
    "totally", "absolutely", "definitely", "i think", "i feel",
    "maybe", "perhaps", "probably", "try to", "hope to",
    "you know", "like",
]

# ── Power action verbs for resume bullets ────────────────────────────────────
POWER_VERBS = [
    "Architected", "Spearheaded", "Orchestrated", "Pioneered", "Engineered",
    "Optimized", "Accelerated", "Automated", "Streamlined", "Transformed",
    "Leveraged", "Delivered", "Exceeded", "Scaled", "Deployed",
    "Collaborated", "Mentored", "Analyzed", "Designed", "Implemented",
    "Integrated", "Refactored", "Resolved", "Validated", "Visualized",
    "Championed", "Modernized", "Bootstrapped", "Overhauled", "Launched",
]
