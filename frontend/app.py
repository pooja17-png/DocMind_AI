import requests
import streamlit as st

BACKEND_URL = "https://docmind-ai-a48c.onrender.com/"

st.set_page_config(
    page_title="DocMind AI",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ====================================================================
#  STYLES — minimal, centered assistant landing (ChatGPT/Claude style)
# ====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root{
    --bg:#FAFAFA;
    --card:#FFFFFF;
    --ink:#141417;          /* near-black primary text */
    --ink-soft:#52525B;     /* darker secondary text — readable */
    --line:#E2E2E4;
    --line-soft:#EDEDEF;
    --accent:#33414C;
}

html, body, [class*="css"]{ font-family:'Inter', sans-serif; }
.stApp{ background:var(--bg); color:var(--ink); }
#MainMenu, footer, header{ visibility:hidden; }
.block-container{ padding-top:1.1rem; padding-bottom:2rem; max-width:880px; }

@keyframes fadeUp{ from{opacity:0; transform:translateY(14px);} to{opacity:1; transform:translateY(0);} }

/* ---------------- NAVBAR ---------------- */
.nav{ display:flex; align-items:center; justify-content:space-between; padding:4px 2px 0; }
.nav-brand{ display:flex; align-items:center; gap:11px; font-weight:700; font-size:17px; letter-spacing:-.3px; }
.nav-logo{
    width:32px; height:32px; border-radius:10px; color:#fff;
    display:flex; align-items:center; justify-content:center; font-size:15px;
    background:var(--accent);
}
.nav-right{ display:flex; align-items:center; gap:12px; }
.nav-pill{
    display:inline-flex; align-items:center; gap:7px; padding:6px 13px; border-radius:999px;
    background:var(--card); border:1px solid var(--line); font-size:12.5px; font-weight:500; color:var(--ink-soft);
}
.dot{ width:7px; height:7px; border-radius:50%; background:#34C759; }
.dot.off{ background:#FF3B30; }
.nav-ico{ font-size:16px; color:var(--ink-soft); }

/* ---------------- HERO ---------------- */
.hero{ text-align:center; padding:120px 0 0; animation:fadeUp .6s ease both; }
.hero-title{ font-size:44px; font-weight:800; letter-spacing:-1.4px; color:var(--ink); margin:0; }
.hero-sub{ margin:18px auto 0; max-width:440px; font-size:16.5px; line-height:1.55; color:#3F3F46; font-weight:450; }

/* ---------------- INPUT BOX (native chat_input) ---------------- */
.st-key-chatbox [data-testid="stChatInput"]{
    background:var(--card) !important; border:1px solid var(--line) !important;
    border-radius:20px !important; box-shadow:0 8px 26px -18px rgba(0,0,0,0.20) !important;
}
.st-key-chatbox [data-testid="stChatInput"]:focus-within{ border-color:#C9C9CE !important; }
.st-key-chatbox [data-testid="stChatInput"] textarea{
    font-size:16px !important; color:var(--ink) !important; background:transparent !important;
}
.st-key-chatbox [data-testid="stChatInput"] textarea::placeholder{ color:#6E6E78 !important; opacity:1 !important; }
/* send arrow → solid slate */
.st-key-chatbox [data-testid="stChatInputSubmitButton"]{
    background:var(--accent) !important; color:#fff !important; border-radius:11px !important;
}
.st-key-chatbox [data-testid="stChatInputSubmitButton"]:hover{ background:#1F2A33 !important; }
.st-key-chatbox [data-testid="stChatInputSubmitButton"] svg{ fill:#fff !important; color:#fff !important; }

/* Upload PDF — small ghost button centered under the box */
.st-key-up_pill button{
    width:auto !important; background:transparent !important; color:#3F3F46 !important;
    border:none !important; box-shadow:none !important; padding:6px 10px !important;
    font-size:13.5px !important; font-weight:600 !important; margin:0 auto !important;
}
.st-key-up_pill button:hover{ background:#F1F1F2 !important; border-radius:9px !important; color:var(--ink) !important; transform:none !important; }
.st-key-up_pill{ display:flex; justify-content:center; }

.stChatMessage{ background:transparent !important; }

/* ---------------- ACTION PILLS ---------------- */
.stButton>button{
    width:100%;
    background:var(--card) !important; color:var(--ink) !important;
    border:1px solid var(--line) !important; border-radius:12px !important;
    padding:11px 14px !important; font-weight:550 !important; font-size:13.5px !important;
    box-shadow:none !important; transition:background .18s, border-color .18s, transform .18s;
}
.stButton>button:hover{ background:#F5F5F6 !important; border-color:#E0E0E2 !important; transform:translateY(-1px); }
.stButton>button:disabled{ color:#BDBDC4 !important; background:var(--card) !important; }

/* download button = subtle */
.stDownloadButton>button{
    width:auto; background:var(--card) !important; color:var(--ink-soft) !important;
    border:1px solid var(--line) !important; border-radius:10px !important;
    padding:7px 14px !important; font-size:12.5px !important; font-weight:500 !important; box-shadow:none !important;
}
.stDownloadButton>button:hover{ background:#F5F5F6 !important; }

/* uploader (appears inline under the box when paperclip clicked) */
[data-testid="stFileUploaderDropzone"]{
    background:#FAFAFA !important; border:1px dashed #DADADA !important;
    border-radius:12px !important; padding:14px !important; min-height:auto !important;
}
[data-testid="stFileUploader"] *{ color:var(--ink-soft) !important; }
[data-testid="stFileUploaderDropzone"] button{
    background:var(--accent) !important; color:#fff !important; border:none !important; border-radius:9px !important; font-weight:500 !important;
}

/* ---------------- RESULT CARD ---------------- */
.result-card{
    background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:20px 24px; margin-top:10px; line-height:1.7; color:var(--ink); animation:fadeUp .4s ease both;
}
.label{ font-size:12px; font-weight:600; color:#3F3F46; letter-spacing:.4px; margin:6px 0 2px; }

/* ---------------- FOOTER ---------------- */
.foot{ text-align:center; color:#3F3F46; font-size:12.5px; line-height:1.7; padding:60px 0 6px; }
.foot .mut{ color:#6E6E78; }
.stSpinner > div{ border-top-color:var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# ====================================================================
#  HELPERS  (backend integration — unchanged endpoints)
# ====================================================================
def backend_alive():
    try:
        return requests.get(f"{BACKEND_URL}/health", timeout=2).status_code == 200
    except Exception:
        return False


def post(path, **kw):
    """POST wrapper -> (ok, json|error_str)."""
    try:
        r = requests.post(f"{BACKEND_URL}{path}", timeout=120, **kw)
        if r.status_code != 200:
            return False, f"Server returned {r.status_code}"
        return True, r.json()
    except requests.exceptions.ConnectionError:
        return False, "Cannot reach backend. Is it running on :8000?"
    except Exception as e:
        return False, str(e)


# ====================================================================
#  SESSION STATE
# ====================================================================
for key, default in {
    "chat": [],
    "doc_name": None,
    "doc_chars": 0,
    "last_file": None,
    "result": None,
    "result_label": None,
    "result_key": None,
    "show_upload": False,
}.items():
    st.session_state.setdefault(key, default)

online = backend_alive()
ready = st.session_state.doc_name is not None


# ====================================================================
#  NAVBAR
# ====================================================================
nav_dot = "dot" if online else "dot off"
nav_txt = "API connected" if online else "API offline"
st.markdown(f"""
<div class="nav">
    <div class="nav-brand"><div class="nav-logo">📄</div> DocMind AI</div>
    <div class="nav-right">
        <div class="nav-pill"><span class="{nav_dot}"></span> {nav_txt}</div>
        <span class="nav-ico">☀️</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ====================================================================
#  HERO
# ====================================================================
st.markdown("""
<div class="hero">
    <h1 class="hero-title">What can I help you with?</h1>
    <p class="hero-sub">
        Upload a PDF, ask questions, get summaries,<br/>
        flashcards, and interview prep — all in one place.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)


# ====================================================================
#  CENTRAL INPUT  — native chat box + Upload PDF button below
# ====================================================================
with st.container(key="chatbox"):
    prompt = st.chat_input(
        "Ask anything about your document…" if ready
        else "Upload a PDF, then ask anything about it…",
    )

# Upload PDF control — centered just under the box
uc_l, uc_c, uc_r = st.columns([2, 1, 2])
with uc_c:
    with st.container(key="up_pill"):
        if st.button("📎 Upload PDF", key="toggle_upload"):
            st.session_state.show_upload = not st.session_state.show_upload

if ready:
    st.markdown(
        f"<div class='label' style='text-align:center'>📄 {st.session_state.doc_name} · "
        f"{st.session_state.doc_chars:,} chars</div>",
        unsafe_allow_html=True,
    )

if st.session_state.show_upload:
    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_pdf is not None and uploaded_pdf.name != st.session_state.last_file:
        files = {"file": (uploaded_pdf.name, uploaded_pdf, "application/pdf")}
        with st.spinner("Reading & indexing your document…"):
            ok, data = post("/upload-pdf", files=files)
        if ok:
            st.session_state.last_file = uploaded_pdf.name
            st.session_state.doc_name = uploaded_pdf.name
            st.session_state.doc_chars = data.get("characters", 0)
            st.session_state.chat = []
            st.session_state.show_upload = False
            st.toast("Document ready!", icon="🚀")
            st.rerun()
        else:
            st.error(f"Upload failed: {data}", icon="🚫")

if not online:
    st.warning(
        "Backend not reachable on `http://127.0.0.1:8000`. "
        "Start it with `uvicorn app:app --reload` inside the `backend` folder.",
        icon="🔌",
    )


# ====================================================================
#  ACTION PILLS
# ====================================================================
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

ACTIONS = [
    ("📄 Summarize this PDF", "summary", "/summary", None),
    ("🗂️ Create flashcards", "flashcards", "/flashcards", None),
    ("👤 Generate interview Q&A", "questions", "/interview-questions", None),
    ("💡 Explain key concepts", "concepts", "/ask",
     "Explain the key concepts in this document clearly and concisely."),
]

acols = st.columns(4, gap="small")
for col, (label, key, endpoint, question) in zip(acols, ACTIONS):
    with col:
        if st.button(label, key=f"act_{key}", disabled=not ready):
            with st.spinner("Working…"):
                if question is not None:
                    ok, data = post(endpoint, json={"question": question})
                    content = (data.get("answer") or data.get("error")) if ok else f"⚠️ {data}"
                else:
                    ok, data = post(endpoint)
                    content = (data.get(key) or data.get("error")) if ok else f"⚠️ {data}"
            st.session_state.result = content or "Nothing generated."
            st.session_state.result_label = label
            st.session_state.result_key = key


# ====================================================================
#  CHAT SUBMIT
# ====================================================================
if prompt and prompt.strip():
    if not ready:
        st.warning("Upload a PDF first, then ask your question.", icon="📄")
    else:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.spinner("Thinking…"):
            ok, data = post("/ask", json={"question": prompt})
        answer = (data.get("answer") or data.get("error")) if ok else f"⚠️ {data}"
        st.session_state.chat.append({"role": "assistant", "content": answer or "No answer returned."})


# ====================================================================
#  OUTPUT  (chat thread + tool result)
# ====================================================================
if st.session_state.chat:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

if st.session_state.result:
    st.markdown(f"<div class='label'>{st.session_state.result_label}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-card'>{st.session_state.result}</div>", unsafe_allow_html=True)
    st.download_button(
        "⬇️ Download",
        data=st.session_state.result,
        file_name=f"{st.session_state.result_key}.md",
        mime="text/markdown",
        key="dl_result",
    )


# ====================================================================
#  FOOTER
# ====================================================================
st.markdown("""
<div class="foot">
    ⚡ Powered by Gemini + FastAPI<br/>
    <span class="mut">DocMind AI can make mistakes. Please verify important information.</span>
</div>
""", unsafe_allow_html=True)
