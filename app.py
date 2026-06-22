import os
import streamlit as st
from src.chains import ask_legal_assistant

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Citizen Rights Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------
# ASSETS & DATA PATHS
# ---------------------------------

ASSETS_DIR      = "assets"
DATA_DIR        = "data"

LOGO            = os.path.join(ASSETS_DIR, "scale.png")
HERO            = os.path.join(ASSETS_DIR, "hero-banner.jpg")
AMBEDKAR        = os.path.join(ASSETS_DIR, "dr_ambedkar.jpg")
SUPREME_COURT   = os.path.join(ASSETS_DIR, "supreme_court.jpg")

CONSTITUTION_MD = os.path.join(DATA_DIR, "constitutionOfIndia.md")
IPC_MD          = os.path.join(DATA_DIR, "ipc.md")

# ---------------------------------
# SESSION STATE
# ---------------------------------

if "dark_mode"   not in st.session_state:
    st.session_state.dark_mode   = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# ---------------------------------
# THEME TOKENS
# ---------------------------------

dark      = st.session_state.dark_mode
BG_PAGE   = "#0f172a" if dark else "#f0f4f8"
BG_CARD   = "#1e293b" if dark else "#ffffff"
BG_SIDE   = "#0f172a" if dark else "#1a2744"
TEXT_MAIN = "#f1f5f9" if dark else "#1e293b"
TEXT_SUB  = "#94a3b8" if dark else "#64748b"
BORDER    = "#334155" if dark else "#e2e8f0"
ACCENT    = "#3b82f6"
ACCENT_BG = "rgba(59,130,246,0.15)"

# ---------------------------------
# CSS  ── immune to system dark mode
# ---------------------------------

st.markdown(f"""
<style>
/* === Force light colour-scheme; override OS dark mode completely === */
:root {{ color-scheme: light !important; }}
@media (prefers-color-scheme: dark) {{
    :root {{ color-scheme: light !important; }}
    html, body {{ background-color: {BG_PAGE} !important; color: {TEXT_MAIN} !important; }}
}}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    color-scheme: light !important;
}}
.stApp {{ background-color: {BG_PAGE} !important; }}

/* === Sidebar === */
section[data-testid="stSidebar"] > div:first-child {{
    background-color: {BG_SIDE} !important;
}}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label {{
    color: #e2e8f0 !important;
}}

/* Nav buttons */
section[data-testid="stSidebar"] .stButton > button {{
    background-color: transparent !important;
    color: #cbd5e1 !important;
    border: none !important;
    border-radius: 10px !important;
    text-align: left !important;
    padding: 9px 14px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    width: 100% !important;
    margin-bottom: 2px !important;
    transition: background 0.15s, color 0.15s !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background-color: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] .nav-active .stButton > button {{
    background-color: {ACCENT_BG} !important;
    color: #60a5fa !important;
    font-weight: 600 !important;
}}

/* === Main container === */
.block-container {{
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1100px !important;
}}

/* === Hero card === */
.hero-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT};
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 24px;
}}
.hero-card h1 {{
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem; font-weight: 700;
    color: {TEXT_MAIN} !important;
    margin: 0 0 8px 0; line-height: 1.25;
}}
.hero-card h1 span {{ color: {ACCENT}; }}
.hero-card p {{ font-size: 15px; color: {TEXT_SUB} !important; margin: 0; }}

/* === Feature pills === */
.feature-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0 24px 0; }}
.feature-pill {{
    display: flex; align-items: center; gap: 8px;
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 999px; padding: 7px 16px;
    font-size: 13px; font-weight: 500; color: {TEXT_MAIN} !important;
}}
.pill-sub {{ font-size: 11px; color: {TEXT_SUB} !important; display: block; margin-top: 1px; }}

/* === Section title === */
.section-title {{
    font-size: 17px; font-weight: 600;
    color: {TEXT_MAIN} !important; margin: 0 0 12px 0;
}}

/* === Answer grid === */
.answer-grid {{
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 16px; margin-top: 12px;
}}
.answer-tile {{
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 20px;
}}
.answer-tile h4 {{
    font-size: 14px; font-weight: 600;
    color: {TEXT_MAIN} !important; margin: 0 0 12px 0;
}}
.answer-tile p {{
    font-size: 14px; color: {TEXT_SUB} !important;
    margin: 0; line-height: 1.6;
}}

/* === Action items === */
.action-item {{
    display: flex; align-items: flex-start; gap: 10px;
    padding: 8px 0; font-size: 14px;
    color: {TEXT_MAIN} !important; border-bottom: 1px solid {BORDER};
}}
.action-item:last-child {{ border-bottom: none; }}
.action-dot {{
    width: 20px; height: 20px; border-radius: 50%;
    background: #22c55e22; border: 1.5px solid #22c55e;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px; font-size: 11px; color: #22c55e;
}}

/* === KB stats card === */
.kb-card {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px; padding: 14px 16px; margin-top: 6px;
}}
.kb-stat {{
    display: flex; justify-content: space-between;
    padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.08);
    font-size: 12px; color: #94a3b8 !important;
}}
.kb-stat:last-child {{ border-bottom: none; }}
.kb-stat span:last-child {{ font-weight: 600; color: #e2e8f0 !important; }}

/* === Doc viewer === */
.doc-header {{
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 24px 28px; margin-bottom: 16px;
}}
.doc-header h2 {{ color: {TEXT_MAIN} !important; margin: 0 0 6px 0; font-size: 1.4rem; }}
.doc-header p  {{ color: {TEXT_SUB}  !important; margin: 0; font-size: 14px; }}

.doc-search-bar input {{
    background: {BG_CARD} !important; color: {TEXT_MAIN} !important;
    border: 1px solid {BORDER} !important; border-radius: 10px !important;
}}

/* Markdown doc body */
.doc-body {{
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 28px 32px;
    color: {TEXT_MAIN} !important; line-height: 1.8; font-size: 14px;
}}
.doc-body h1, .doc-body h2, .doc-body h3 {{
    color: {TEXT_MAIN} !important; margin-top: 24px;
}}
.doc-body h2 {{ border-bottom: 1px solid {BORDER}; padding-bottom: 6px; }}
.doc-body p  {{ color: {TEXT_SUB} !important; }}
.doc-body strong {{ color: {TEXT_MAIN} !important; }}

/* === About cards === */
.about-card {{
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 22px 24px; margin-bottom: 16px;
}}
.about-card h3 {{ color: {TEXT_MAIN} !important; margin: 0 0 10px 0; font-size: 16px; }}
.about-card p  {{ color: {TEXT_SUB}  !important; font-size: 14px; line-height: 1.7; margin: 0; }}
.tag {{
    display: inline-block; background: {ACCENT_BG};
    color: {ACCENT} !important; border-radius: 999px;
    padding: 3px 12px; font-size: 12px; font-weight: 600; margin: 4px 4px 0 0;
}}

/* === Disclaimer === */
.disclaimer {{
    background: {"#1e3a5f" if dark else "#eff6ff"};
    border: 1px solid {"#2563eb55" if dark else "#bfdbfe"};
    border-radius: 10px; padding: 12px 16px;
    font-size: 13px; color: {TEXT_SUB} !important;
    margin-top: 20px; display: flex; gap: 10px; align-items: flex-start;
}}

/* === Streamlit widget resets === */
.stTextArea textarea {{
    background: {BG_CARD} !important; color: {TEXT_MAIN} !important;
    border: 1px solid {BORDER} !important; border-radius: 10px !important;
    font-size: 14px !important;
}}
.main-cta .stButton > button {{
    background: {ACCENT} !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; font-size: 15px !important;
    padding: 12px 24px !important; width: 100% !important;
}}
.main-cta .stButton > button:hover {{ opacity: 0.88 !important; }}
.stSelectbox > div {{
    background: {BG_CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 10px !important; color: {TEXT_MAIN} !important;
}}
div[data-testid="stExpander"] {{
    background: {BG_CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# HELPERS
# ---------------------------------

@st.cache_data
def load_md(path: str) -> str:
    """Load a markdown file from disk, return empty string if missing."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def render_doc_page(title: str, icon: str, accent: str, description: str,
                    md_path: str, source_label: str):
    """Render a full-document viewer page (Constitution or IPC)."""

    content = load_md(md_path)

    # Header
    st.markdown(f"""
    <div class="doc-header" style="border-left:4px solid {accent}">
        <h2>{icon} {title}</h2>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

    if not content:
        st.warning(f"Document not found at `{md_path}`. Please add the file to the `data/` folder.")
        return

    # Search / filter
    search_col, stat_col = st.columns([4, 1])
    with search_col:
        query = st.text_input("", placeholder=f"🔍  Search within {title}…",
                              key=f"search_{title}", label_visibility="collapsed")
    with stat_col:
        word_count = len(content.split())
        st.markdown(f"""
        <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;
                    padding:8px 14px;text-align:center">
            <div style="font-size:18px;font-weight:700;color:{accent}">{word_count:,}</div>
            <div style="font-size:11px;color:{TEXT_SUB}">words</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Filter content by search query
    if query.strip():
        lines = content.split("\n")
        matched = []
        for line in lines:
            if query.lower() in line.lower():
                matched.append(f"**→** {line}")
        if matched:
            filtered = "\n\n".join(matched[:200])  # cap at 200 hits
            st.markdown(f"""
            <div class="doc-body">
            """, unsafe_allow_html=True)
            st.markdown(f"_Showing {len(matched)} results for **\"{query}\"**_")
            st.markdown(filtered)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(f"No results found for **\"{query}\"**.")
    else:
        # Full document rendered as markdown inside styled container
        st.markdown('<div class="doc-body">', unsafe_allow_html=True)
        st.markdown(content, unsafe_allow_html=False)
        st.markdown("</div>", unsafe_allow_html=True)

    # Download button
    st.write("")
    st.download_button(
        f"⬇ Download {source_label}",
        data=content,
        file_name=os.path.basename(md_path),
        mime="text/markdown",
        use_container_width=False
    )

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    logo_col, title_col = st.columns([1, 2.4])
    with logo_col:
        st.image(LOGO, width=48)
    with title_col:
        st.markdown("""
        <div style="padding-top:6px;line-height:1.3">
            <div style="font-size:15px;font-weight:700;color:#ffffff">Citizen Rights</div>
            <div style="font-size:13px;font-weight:600;color:#f59e0b">Assistant</div>
            <div style="font-size:11px;color:#94a3b8;margin-top:2px">Legal Rights. Simplified.</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Navigation (5 pages; Fundamental Rights & Duties removed) ────────────
    NAV_PAGES = [
        ("🏠",  "Home"),
        ("💬",  "Ask a Question"),
        ("📜",  "Constitution"),
        ("⚖️",  "IPC (Indian Penal Code)"),
        ("ℹ️",  "About Project"),
    ]

    for icon, label in NAV_PAGES:
        is_active    = st.session_state.active_page == label
        wrapper_class = "nav-active" if is_active else "nav-inactive"
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.active_page = label
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Knowledge Base stats
    st.markdown("<div style='font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:4px'>📚 Knowledge Base</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class="kb-card">
        <div class="kb-stat"><span>Documents</span><span>2</span></div>
        <div class="kb-stat"><span>Total Sections</span><span>120+</span></div>
        <div class="kb-stat"><span>Sources</span><span>Constitution, IPC</span></div>
    </div>
    <div style="margin-top:6px">
        <a style="font-size:12px;color:#60a5fa;text-decoration:none;cursor:pointer">View Details →</a>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Ambedkar quote
    st.markdown("""
    <div style="font-size:26px;color:#f59e0b;line-height:1">"</div>
    <div style="font-size:12px;color:#cbd5e1;line-height:1.65;font-style:italic;margin-top:2px">
        The Constitution is not just a lawyers' document,
        it is a vehicle of Life, and its spirit is always the spirit of Age.
    </div>
    <div style="font-size:11px;color:#94a3b8;margin-top:6px">— Dr. B.R. Ambedkar</div>
    """, unsafe_allow_html=True)

    st.image(AMBEDKAR, use_container_width=True)

    st.divider()

    st.markdown("""
    <div style="text-align:center;font-size:12px;color:#94a3b8;padding-bottom:8px">
        Made with ❤️ in India<br>
        <span style="color:#64748b">Empowering Citizens. Strengthening Democracy.</span>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# PAGE ROUTING
# ---------------------------------

page = st.session_state.active_page

# ── Constitution ──────────────────────────────────────────────────────────────
if page == "Constitution":
    render_doc_page(
        title        = "Constitution of India",
        icon         = "📜",
        accent       = "#10b981",
        description  = "The supreme law of India — browse all Parts, Articles, Schedules and Amendments.",
        md_path      = CONSTITUTION_MD,
        source_label = "constitution.md",
    )
    st.stop()

# ── IPC ───────────────────────────────────────────────────────────────────────
if page == "IPC (Indian Penal Code)":
    render_doc_page(
        title        = "Indian Penal Code (IPC)",
        icon         = "⚖️",
        accent       = "#f59e0b",
        description  = "India's main criminal code — covering offences, punishments and procedures from Section 1 onwards.",
        md_path      = IPC_MD,
        source_label = "ipc.md",
    )
    st.stop()

# ── Ask a Question ────────────────────────────────────────────────────────────
if page == "Ask a Question":
    st.markdown(f"""
    <div class="doc-header" style="border-left:4px solid {ACCENT}">
        <h2>💬 Ask a Legal Question</h2>
        <p>Type your question and get an AI-powered answer grounded in the Constitution and IPC.</p>
    </div>
    """, unsafe_allow_html=True)

    question2 = st.text_area("", height=150,
                              placeholder="e.g. What happens if someone forges my signature?",
                              label_visibility="collapsed")
    st.markdown('<div class="main-cta">', unsafe_allow_html=True)
    if st.button("🔍 Get Answer", key="ask_btn2", use_container_width=True):
        if question2.strip():
            with st.spinner("Analyzing legal documents…"):
                try:
                    resp = ask_legal_assistant(question2)
                    actions_html = "".join(
                        f'<div class="action-item"><div class="action-dot">✓</div><span>{a}</span></div>'
                        for a in (resp.possible_actions or ["No specific actions available."])
                    )
                    st.markdown(f"""
                    <div class="answer-grid">
                        <div class="answer-tile">
                            <h4>📖 Legal Explanation</h4>
                            <p>{resp.answer}</p>
                        </div>
                        <div class="answer-tile">
                            <h4>⚖️ Relevant Law</h4>
                            <p style="font-size:12px;color:{TEXT_SUB}">Article / Section</p>
                            <p>{resp.relevant_law}</p>
                            <br>
                            <h4>📚 Source</h4>
                            <p style="font-size:12px;color:{TEXT_SUB}">Document</p>
                            <p>{resp.source}</p>
                        </div>
                        <div class="answer-tile">
                            <h4>✅ Suggested Actions</h4>
                            <p style="font-size:12px;color:{TEXT_SUB};margin-bottom:12px">Steps you can take:</p>
                            {actions_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as exc:
                    st.error(str(exc))
        else:
            st.warning("Please enter a question.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ── About Project ─────────────────────────────────────────────────────────────
if page == "About Project":

    st.markdown(f"""
    <div class="doc-header" style="border-left:4px solid #8b5cf6">
        <h2>ℹ️ About This Project</h2>
        <p>How it works, why it was built, and the technology powering it.</p>
    </div>
    """, unsafe_allow_html=True)

    # What we are doing
    st.markdown(f"""
    <div class="about-card">
        <h3>🎯 What This Project Does</h3>
        <p>
            <strong>Citizen Rights Assistant</strong> is an AI-powered legal information tool built for
            everyday Indian citizens. It lets anyone ask plain-language questions about Indian law and
            receive clear, source-grounded answers — without needing a lawyer or a law degree.
        </p>
        <p style="margin-top:10px">
            Under the hood it uses <strong>Retrieval-Augmented Generation (RAG)</strong>: when you ask
            a question, the system searches the full text of the Constitution of India and the Indian
            Penal Code (IPC), retrieves the most relevant passages, and feeds them as context to a
            large language model (LLM) that composes a structured answer.  Every answer comes with
            the specific Article or IPC Section it was drawn from, so you can verify it yourself.
        </p>
        <br>
        <span class="tag">RAG Pipeline</span>
        <span class="tag">Vector Search</span>
        <span class="tag">LLM (Claude / OpenAI)</span>
        <span class="tag">LangChain</span>
        <span class="tag">Streamlit</span>
    </div>

    <div class="about-card">
        <h3>🔧 Technical Architecture</h3>
        <p>
            The pipeline has three stages:
        </p>
        <p style="margin-top:8px">
            <strong>1. Ingestion</strong> — The Constitution and IPC markdown files are chunked into
            overlapping passages and embedded using a sentence-transformer model.  Embeddings are
            stored in a local vector store (FAISS / Chroma).
        </p>
        <p style="margin-top:8px">
            <strong>2. Retrieval</strong> — At query time, the question is embedded and a cosine
            similarity search returns the top-k most relevant passages from the knowledge base.
        </p>
        <p style="margin-top:8px">
            <strong>3. Generation</strong> — The retrieved passages plus the original question are
            sent to an LLM via a structured prompt.  The model returns a JSON-structured response
            containing the legal explanation, relevant law, source document, and suggested actions.
        </p>
        <br>
        <span class="tag">FAISS / Chroma</span>
        <span class="tag">Sentence Transformers</span>
        <span class="tag">Structured Output</span>
        <span class="tag">Pydantic</span>
    </div>

    <div class="about-card">
        <h3>💡 Motivation</h3>
        <p>
            India has one of the world's longest written constitutions and a vast body of criminal law,
            yet access to legal knowledge remains deeply unequal.  Most citizens cannot afford a
            lawyer for routine questions, and the source documents — while publicly available — are
            dense, technical, and hundreds of pages long.
        </p>
        <p style="margin-top:10px">
            This project was built on the belief that <strong>legal literacy is a civic right</strong>.
            If a person can ask "what can I do if someone threatens me?" in plain English and get a
            clear, cited answer in seconds, they are better equipped to protect themselves, challenge
            injustice, and participate in democracy.
        </p>
        <p style="margin-top:10px">
            We chose RAG over fine-tuning deliberately: grounding answers in the actual source
            documents means the system cannot hallucinate laws that don't exist.  Every claim is
            traceable back to a real Article or Section.
        </p>
        <br>
        <span class="tag">Legal Literacy</span>
        <span class="tag">Civic Tech</span>
        <span class="tag">Open Knowledge</span>
        <span class="tag">Built in India 🇮🇳</span>
    </div>

    <div class="about-card">
        <h3>⚠️ Disclaimer</h3>
        <p>
            This tool provides <strong>educational legal information only</strong>.  It is not a
            substitute for professional legal advice.  For any real legal matter, please consult a
            qualified advocate.  The answers are grounded in the source documents but the LLM can
            still make mistakes — always verify citations independently.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# =============================================================================
# HOME PAGE
# =============================================================================

_, mode_col = st.columns([9, 1])
with mode_col:
    mode_label = "🌙 Dark" if not dark else "☀️ Light"
    if st.button(mode_label, key="toggle_mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Hero
hero_col, img_col = st.columns([3, 2])
with hero_col:
    st.markdown(f"""
    <div class="hero-card">
        <h1>Know Your Rights.<br><span>Protect Your Future.</span></h1>
        <p>Ask any legal question related to Indian laws and get<br>
           clear, reliable and actionable answers instantly.</p>
    </div>
    """, unsafe_allow_html=True)
with img_col:
    st.image(HERO, use_container_width=True)

# Feature pills
st.markdown(f"""
<div class="feature-row">
    <div class="feature-pill">🛡️
        <div><strong>Reliable</strong><span class="pill-sub">100% Legal Sources</span></div>
    </div>
    <div class="feature-pill">🧠
        <div><strong>Intelligent</strong><span class="pill-sub">AI-Powered</span></div>
    </div>
    <div class="feature-pill">🔒
        <div><strong>Private</strong><span class="pill-sub">Your queries are safe</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Question input
st.markdown(f"<div class='section-title'>💬 Ask Your Legal Question</div>", unsafe_allow_html=True)

question = st.text_area(
    "", height=130,
    placeholder="e.g. What are my fundamental rights as an Indian citizen?",
    max_chars=500, label_visibility="collapsed"
)

q_col, btn_col = st.columns([2, 2])
with q_col:
    # Fundamental Rights & Duties removed from dropdown
    query_type = st.selectbox(
        "",
        ["General Legal Query", "Constitutional Right", "IPC Section"],
        label_visibility="collapsed"
    )
with btn_col:
    st.markdown('<div class="main-cta">', unsafe_allow_html=True)
    search_clicked = st.button("🔍 Get Answer", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Secondary tags
st.markdown(f"""
<div class="feature-row" style="margin-top:8px;margin-bottom:4px">
    <div class="feature-pill">✨ <strong style="margin-left:4px">AI-Powered</strong>
        <span class="pill-sub" style="display:inline;margin-left:4px">Advanced RAG</span></div>
    <div class="feature-pill">📚 Source Based
        <span class="pill-sub" style="display:inline;margin-left:4px">From Indian Laws</span></div>
    <div class="feature-pill">⚖️ Actionable
        <span class="pill-sub" style="display:inline;margin-left:4px">Practical Guidance</span></div>
    <div class="feature-pill">✅ Trusted
        <span class="pill-sub" style="display:inline;margin-left:4px">Verified & Reliable</span></div>
</div>
""", unsafe_allow_html=True)

# Answer section
ans_hdr, export_col = st.columns([7, 1])
with ans_hdr:
    st.markdown(f"<div class='section-title' style='margin-top:8px'>📄 Your Answer</div>",
                unsafe_allow_html=True)

if not search_clicked:
    st.markdown(f"""
    <div class="answer-grid">
        <div class="answer-tile">
            <h4>📖 Legal Explanation</h4>
            <p>Here is the answer to your question based on Indian laws and constitutional provisions…</p>
        </div>
        <div class="answer-tile">
            <h4>⚖️ Relevant Law</h4>
            <p style="font-size:12px;color:{TEXT_SUB}">Article / Section</p><p>--</p><br>
            <h4>📚 Source</h4>
            <p style="font-size:12px;color:{TEXT_SUB}">Document</p><p>--</p>
        </div>
        <div class="answer-tile">
            <h4>✅ Suggested Actions</h4>
            <p style="font-size:12px;color:{TEXT_SUB};margin-bottom:12px">Steps you can take:</p>
            <div class="action-item"><div class="action-dot">✓</div><span>Action item will appear here</span></div>
            <div class="action-item"><div class="action-dot">✓</div><span>Action item will appear here</span></div>
            <div class="action-item"><div class="action-dot">✓</div><span>Action item will appear here</span></div>
            <div class="action-item"><div class="action-dot">✓</div><span>Action item will appear here</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    with export_col:
        st.download_button("⬇ Export", data="", file_name="answer.txt",
                           use_container_width=True, disabled=True)
else:
    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Analyzing legal documents…"):
        try:
            response     = ask_legal_assistant(question)
            actions_html = "".join(
                f'<div class="action-item"><div class="action-dot">✓</div><span>{a}</span></div>'
                for a in (response.possible_actions or ["No specific actions available."])
            )
            st.markdown(f"""
            <div class="answer-grid">
                <div class="answer-tile">
                    <h4>📖 Legal Explanation</h4>
                    <p>{response.answer}</p>
                </div>
                <div class="answer-tile">
                    <h4>⚖️ Relevant Law</h4>
                    <p style="font-size:12px;color:{TEXT_SUB}">Article / Section</p>
                    <p>{response.relevant_law}</p><br>
                    <h4>📚 Source</h4>
                    <p style="font-size:12px;color:{TEXT_SUB}">Document</p>
                    <p>{response.source}</p>
                </div>
                <div class="answer-tile">
                    <h4>✅ Suggested Actions</h4>
                    <p style="font-size:12px;color:{TEXT_SUB};margin-bottom:12px">Steps you can take:</p>
                    {actions_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            export_text = (
                f"Legal Question: {question}\n\n"
                f"Legal Explanation:\n{response.answer}\n\n"
                f"Relevant Law: {response.relevant_law}\n"
                f"Source: {response.source}\n\n"
                "Suggested Actions:\n" +
                "\n".join(f"• {a}" for a in (response.possible_actions or []))
            )
            with export_col:
                st.download_button("⬇ Export", data=export_text,
                                   file_name="legal_answer.txt",
                                   use_container_width=True)
        except Exception as e:
            st.error(str(e))

# Retrieved context
with st.expander("🔍 Retrieved Context (Sources Used) — click to expand"):
    st.info("Source sections will appear here after you ask a question.")

# Disclaimer
st.markdown(f"""
<div class="disclaimer">
    <span style="font-size:16px">ℹ️</span>
    <span><strong>Disclaimer:</strong> This AI assistant provides general legal information only
    and should not be considered a substitute for professional legal advice.
    Always consult a qualified lawyer for specific legal matters.</span>
</div>
""", unsafe_allow_html=True)

# Example questions
with st.expander("📌 Example Questions"):
    st.markdown("""
    - What are the fundamental rights guaranteed by the Constitution?
    - What is theft according to IPC?
    - What punishment exists for cheating?
    - What legal action can I take if someone threatens me?
    - What does the Constitution say about freedom of speech?
    """)