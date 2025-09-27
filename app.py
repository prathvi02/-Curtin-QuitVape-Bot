import os
import time
import base64
from typing import Dict, List, Optional, Callable
import streamlit as st

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="Curtin QuitVape Bot", page_icon="💬", layout="centered")

# ---- IMAGE PATHS ----
LOGO_IMAGE  = "assets/curtin_quitvape_bot.png"
QUOTE_IMAGE = "assets/tiny_steps_quote.png"

# ---- DEMO CREDENTIALS (prototype only) ----
HARDCODED_EMAIL = "harshini3030@gmail.com"
HARDCODED_PASSWORD = "harshini123"
DISPLAY_NAME = "Harshini N"

# ---- PALETTE ----
PRIMARY="#6C63FF"; ACCENT="#FF6584"; GREEN="#2EC4B6"; YELLOW="#FFBF69"; INDIGO="#9B5DE5"
BG="#0E1117"; CARD="#161A22"; TEXT="#E6E6E6"

def _rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

# ====================== UTILS ======================
def img_to_base64(path: str) -> Optional[str]:
    if not path or not os.path.exists(path): return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def data_url_from_path(path: str) -> Optional[str]:
    b64 = img_to_base64(path)
    if not b64: return None
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext in (".png", ".webp") else "image/jpeg"
    return f"data:{mime};base64,{b64}"

# ====================== GLOBAL STYLES ======================
def inject_styles():
    st.markdown(f"""
    <style>
      :root {{
        --bg:{BG}; --text:{TEXT}; --card:{CARD}; --muted:rgba(255,255,255,.10);
        --primary:{PRIMARY}; --accent:{ACCENT}; --shadow:0 22px 70px rgba(0,0,0,.50);
        --title-size:28px; --yellow:{YELLOW};
      }}
      html, body, [class*="css"] {{ background:var(--bg); color:var(--text); }}
      .main .block-container{{ padding-top:.5rem; padding-bottom:1rem; max-width:1000px; }}

      /* ---------- Title (fixed 28px) ---------- */
      .g-title {{
        font-weight:900; font-size:var(--title-size);
        background:linear-gradient(90deg, var(--primary), var(--accent));
        -webkit-background-clip:text; background-clip:text; color:transparent;
        line-height:1.12; margin:0;
      }}
      .divider {{ height:1px; background:rgba(255,255,255,.08); margin:.35rem 0 .75rem; }}

      /* tighten markdown container */
      [data-testid="stMarkdownContainer"] {{ margin: 0 !important; }}

      /* ---------- Header ---------- */
      .hdr-row {{ display:block; }}
      .hdr-row [data-testid="column"] {{ display:flex; align-items:center; }}
      .hdr-left  {{ justify-content:flex-start;  white-space:nowrap; }}
      .hdr-mid   {{ justify-content:center;     white-space:nowrap; }}
      .hdr-right {{ justify-content:flex-end;   white-space:nowrap; gap:10px; }}
      .badge{{ display:inline-flex; align-items:center; gap:6px; background:#151a22; border:1px solid var(--muted);
               padding:8px 12px; border-radius:999px; white-space:nowrap; font-weight:700; }}
      .hdr-row .stButton>button {{
        width:auto !important; padding:8px 14px; white-space:nowrap; border:0; outline:0; font-weight:800;
        border-radius:12px; color:#fff;
        background:linear-gradient(90deg, var(--primary), var(--accent));
        box-shadow:0 10px 24px rgba(108,99,255,.22);
      }}

      /* ---------- Splash/Login aesthetic ---------- */
      .splash-wrap {{
        width:min(980px,96%); margin:7vh auto 1rem; display:grid; place-items:center; gap:8px;
        background:
          radial-gradient(1200px 500px at 10% -10%, rgba(108,99,255,.15), transparent 60%),
          radial-gradient(900px 500px at 120% 10%, rgba(155,93,229,.12), transparent 60%);
        border-radius:22px; border:1px solid var(--muted); padding:24px 16px 20px; box-shadow:var(--shadow);
      }}
      .splash-logo {{ width:clamp(130px,21vw,190px); border-radius:18px; display:block; margin:0 auto 4px;
                      box-shadow:0 0 0 1px rgba(255,255,255,.06), 0 20px 60px rgba(0,0,0,.50); }}
      .splash-title {{ font-weight:900; text-align:center; margin:0; font-size:var(--title-size);
                       background:linear-gradient(90deg, var(--primary), var(--accent)); -webkit-background-clip:text; background-clip:text; color:transparent; }}
      .splash-sub {{ opacity:.9; text-align:center; font-size:.94rem; margin-top:-2px; }}
      .splash-bar {{ width:84%; height:10px; border-radius:999px; background:rgba(255,255,255,.06);
                     border:1px solid rgba(255,255,255,.12); overflow:hidden; margin:6px auto 0; box-shadow:inset 0 0 12px rgba(0,0,0,.25); }}
      .splash-fill {{ height:100%; width:0%; background:linear-gradient(90deg, var(--primary), var(--accent)); transition:width .06s ease; }}

      .login-row [data-testid="stHorizontalBlock"] {{ display:flex; gap:12px; flex-wrap:wrap; align-items:stretch; }}
      .logo-card {{ background:linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02)); border:1px solid var(--muted);
                    border-radius:22px; padding:10px; box-shadow:var(--shadow); width:100%; }}
      .logo-img {{ display:block; margin:0 auto; width:clamp(130px,34vw,226px); border-radius:18px;
                   box-shadow:0 0 0 1px rgba(255,255,255,.06), 0 20px 60px rgba(0,0,0,.50); }}
      .logo-glow {{ width:92%; height:30px; border-radius:999px; margin:6px auto 0;
                    background:radial-gradient(ellipse at center, rgba(108,99,255,.60) 0%, rgba(155,93,229,.28) 45%, rgba(0,0,0,0) 70%);
                    filter:blur(10px); box-shadow:0 0 22px rgba(108,99,255,.28), 0 0 42px rgba(155,93,229,.18); }}
      form[data-testid="stForm"] {{ background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03)); border:1px solid var(--muted);
                                   border-radius:20px; padding:12px; box-shadow:var(--shadow); width:100%; }}
      form[data-testid="stForm"] .stTextInput input, form[data-testid="stForm"] .stPassword input {{
        background:#0f1420 !important; color:var(--text) !important; border:1px solid rgba(255,255,255,.12) !important; border-radius:12px !important;
      }}
      .btn-primary .stButton>button {{ border:0; outline:0; font-weight:800; padding:.78rem 1rem; border-radius:12px; color:#fff;
                                       background:linear-gradient(90deg, var(--primary), var(--accent)); box-shadow:0 10px 24px rgba(108,99,255,.22); }}

      /* ==================== CATEGORY CARD + CLICKABLE PILL ==================== */

      .cat-stack {{ margin: 14px 0 22px; }}
      .cat-stack{{ --cat-accent: var(--accent); }}

      .cat-card {{
        background: var(--card);
        border: 1px solid rgba(255,255,255,.08);
        border-left: 6px solid var(--cat-accent);
        border-radius: 20px;
        padding: 16px 18px;
        box-shadow: 0 14px 28px rgba(0,0,0,.28);
      }}
      .cat-card .title {{
        display:flex; align-items:center; gap:10px;
        font-weight:900; font-size:1.05rem; color: var(--cat-accent);
        margin-bottom:.25rem;
      }}
      .cat-card .subtitle {{ opacity:.8; font-size:.92rem; }}

      .cat-btn .stButton {{ width:100%; }}
      .cat-btn .stButton>button,
      .cat-btn [data-testid="stBaseButton-secondary"],
      .cat-btn [data-testid="baseButton-secondary"] {{
        width:100%;
        text-align:center;
        font-weight:850;
        padding:10px 16px;
        min-height:44px;
        border-radius:12px;
        background:#171c24;
        border:1px solid rgba(255,255,255,.16);
        box-shadow: 0 8px 18px rgba(0,0,0,.24);
        color:var(--text);
        transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
      }}
      .cat-btn .stButton>button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 12px 22px rgba(0,0,0,.30);
        border-color: rgba(255,255,255,.26);
      }}
      .cat-btn .stButton>button:focus-visible {{
        outline:0;
        box-shadow:0 0 0 3px color-mix(in srgb, var(--cat-accent), #fff 25%), 0 10px 20px rgba(0,0,0,.28);
      }}

      /* ==================== BIG TIMER & PHASE ==================== */
      .timer {{
        font-size: clamp(28px, 7vw, 52px);
        font-weight: 900;
        letter-spacing: .5px;
        color: var(--yellow);
        text-shadow: 0 0 12px rgba(255,191,105,.35);
        text-align: center;
      }}
      .phase {{ text-align:center; font-weight:800; font-size: clamp(22px, 5vw, 40px); }}
      .phase-sub {{ text-align:center; opacity:.9; }}

      /* End page tweaks */
      .center-wrap {{ display:flex; justify-content:center; }}
      .end-img {{ border-radius:16px; box-shadow:0 10px 28px rgba(0,0,0,.35); max-width:420px; width:92%; }}
    </style>
    """, unsafe_allow_html=True)

inject_styles()

# ====================== STATE ======================
def _init_state():
    ss = st.session_state
    ss.setdefault("stage", "splash")  # stages: splash -> login -> show_categories -> in_category -> in_answer -> ended
    ss.setdefault("authenticated", False)
    ss.setdefault("user_email", None)

    ss.setdefault("selected_category", None)
    ss.setdefault("selected_question", None)

    # interactive trackers
    ss.setdefault("active_swap", None)
    ss.setdefault("water_sips", 0)
    ss.setdefault("shoulder_rolls", 0)
    ss.setdefault("neck_stretches", 0)
    ss.setdefault("see5_count", 0)
    ss.setdefault("gum_chews", 0)

    # grounding counts
    ss.setdefault("g_see", 0); ss.setdefault("g_feel", 0); ss.setdefault("g_hear", 0)
    ss.setdefault("g_smell", 0); ss.setdefault("g_taste", 0)

    ss.setdefault("rating", 0)

_init_state()

# ====================== CONTENT ======================
CATEGORIES: List[Dict] = [
    {"title":"CRAVING TO VAPE", "subtitle":"Tap to see options.", "emoji":"🌊", "color": PRIMARY, "key":"cravings"},
    {"title":"STRESS TURNING TO VAPING", "subtitle":"Tap to see options.", "emoji":"⚡", "color": ACCENT, "key":"stress"},
    {"title":"SOCIAL VAPING SITUATIONS", "subtitle":"Tap to see options.", "emoji":"👥", "color": GREEN, "key":"social"},
    {"title":"HEALTH RISKS OF VAPING AND AWARENESS", "subtitle":"Tap to see options.", "emoji":"🧠", "color": YELLOW, "key":"health"},
    {"title":"QUIT SUPPORT AND RESOURCES", "subtitle":"Tap to see options.", "emoji":"🧭", "color": INDIGO, "key":"support"},
]

CRAVINGS_QUESTIONS = [
    {"id":"want_to_vape_now","q":"I want to vape right now",
     "a":"Cravings feel intense but usually pass in **2–5 minutes**. Want me to guide you through a **90-second Craving SOS**?",
     "actions":["sos_90","breath_90"]},
    {"id":"how_long","q":"How long do cravings last?",
     "a":"Most urges **peak quickly** and fade within minutes—like waves. Want a **3-minute timer** to ride this one out?",
     "actions":["timer_3m","focus_3m"]},
    {"id":"what_instead","q":"What can I do instead of vaping?",
     "a":"Try a healthy swap. Choose one below for a guided mini-activity.",
     "actions":["swap_gum","swap_water","swap_stretch","swap_more"]},
    {"id":"distract_now","q":"Can you distract me right now?",
     "a":"Pick one: a focus timer, a breathing exercise, or a mini challenge.",
     "actions":["focus_3m","breath_60","mini_challenge"]},
]

STRESS_OR_SOCIAL_QUESTIONS = [
    {"id":"stress_exams","q":"You vape when you're stressed about exams?",
     "a":"That’s really common. Want a **2-minute stress relief** exercise or a **study break timer**?",
     "actions":["stress_relief_2m","study_break_5m"]},
    {"id":"focus_without_vape","q":"You feel like you can't focus without vaping?",
     "a":"Nicotine can feel like a boost, but it harms focus over time. Try **Pomodoro**: 25-min study + 5-min break.",
     "actions":["pomodoro_25_5"]},
    {"id":"anxious_without_vape","q":"You feel anxious if you don't vape?",
     "a":"Quick grounding helps: **5-4-3-2-1** (see, feel, hear, smell, taste). Want to try it now?",
     "actions":["grounding_54321"]},
]

# ====================== HELPERS ======================
def goto_home():
    st.session_state.stage = "show_categories"
    st.session_state.selected_category = None
    st.session_state.selected_question = None
    st.session_state.active_swap = None

def goto_login():
    st.session_state.stage = "login"
    st.session_state.selected_category = None
    st.session_state.selected_question = None
    st.session_state.active_swap = None

def logout():
    st.session_state.authenticated = False
    st.session_state.user_email = None
    goto_login()

def back_to_questions():
    st.session_state.stage = "in_category"
    st.session_state.selected_question = None

def select_category(i: int):
    st.session_state.selected_category = i
    st.session_state.stage = "in_category"
    st.session_state.selected_question = None
    st.session_state.active_swap = None

def select_question(qid: str):
    st.session_state.selected_question = qid
    st.session_state.stage = "in_answer"
    st.session_state.active_swap = None

def _safe_progress(v: int, text: Optional[str] = None):
    try: return st.progress(v, text=text)
    except TypeError: return st.progress(v)

def run_countdown(seconds: int, label: str, phase_cb: Optional[Callable[[int,int], None]] = None):
    holder = st.container()
    bar = holder.progress(0); txt = holder.empty(); coach = holder.empty()
    end = time.time() + seconds
    while True:
        remaining = max(0, int(end - time.time()))
        elapsed = seconds - remaining
        m, s = divmod(remaining, 60)
        txt.markdown(f'<div class="timer">{m:02d}:{s:02d}</div>', unsafe_allow_html=True)
        if seconds > 0:
            pct = min(100, int(elapsed / seconds * 100))
            bar.progress(pct)
        if phase_cb:
            with coach: phase_cb(elapsed, remaining)
        if remaining == 0: break
        time.sleep(1)
    st.success(f"✅ {label} done!")
    st.balloons()

# ====================== UI PRIMITIVES ======================
def gradient_title(emoji: str, title: str, subtitle: Optional[str] = None):
    st.markdown(
        f"""<div>
              <div class="g-title">{emoji} {title}</div>
              <div class="g-sub">{subtitle or ""}</div>
            </div>""",
        unsafe_allow_html=True,
    )

def top_header():
    st.markdown('<div class="hdr-row">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([6, 3, 2], vertical_alignment="center")
    with c1:
        st.markdown('<div class="hdr-left"><div class="g-title">💜 Curtin QuitVape Bot</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="hdr-mid"><span class="badge">👤 {DISPLAY_NAME}</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="hdr-right">', unsafe_allow_html=True)
        st.button("Logout", on_click=logout, key="logout_top")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def footer_nav(prefix: str, show_questions: bool = False):
    if show_questions:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.button("⬅️ Back", key=f"{prefix}_back_qs", on_click=back_to_questions)
        with c2: st.button("📂 Categories", key=f"{prefix}_cats", on_click=goto_home)
        with c3: st.button("🏠 Home", key=f"{prefix}_home", on_click=goto_home)
        with c4: st.button("🔚 End Chat", key=f"{prefix}_end", on_click=lambda: setattr(st.session_state, "stage", "ended"))
    else:
        c1, c2, c3 = st.columns(3)
        with c1: st.button("📂 Categories", key=f"{prefix}_cats", on_click=goto_home)
        with c2: st.button("🏠 Home", key=f"{prefix}_home", on_click=goto_home)
        with c3: st.button("🔚 End Chat", key=f"{prefix}_end", on_click=lambda: setattr(st.session_state, "stage", "ended"))

# ====================== PANELS ======================
def splash_screen():
    logo_url = data_url_from_path(LOGO_IMAGE)
    placeholder = st.empty()
    for pct in range(0, 101, 5):
        html = f"""
        <div class="splash-wrap">
          {'<img class="splash-logo" src="'+logo_url+'" />' if logo_url else '<div class="splash-logo" style="width:150px;height:150px;background:#222;border:1px solid var(--muted);"></div>'}
          <div class="splash-title">Curtin QuitVape Bot</div>
          <div class="splash-sub">Tiny steps today, big changes tomorrow.</div>
          <div class="splash-bar"><div class="splash-fill" style="width:{pct}%"></div></div>
        </div>
        """
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.03 if pct < 100 else 0.35)
    st.session_state.stage = "login"
    _rerun()

def _demo_login():
    st.session_state.authenticated = True
    st.session_state.user_email = HARDCODED_EMAIL
    st.session_state.stage = "show_categories"
    st.toast("Signed in with demo account ✨", icon="✅")

def login_panel():
    st.markdown('<div class="login-row">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.1])

    with c1:
        logo_url = data_url_from_path(LOGO_IMAGE)
        left_html = f"""
        <div class="logo-card">
          {'<img class="logo-img" src="'+logo_url+'" />' if logo_url else '<div class="logo-img" style="width:210px;height:210px;background:#222;border:1px solid var(--muted);margin:0 auto;"></div>'}
          <div class="logo-glow"></div>
        </div>
        """
        st.markdown(left_html, unsafe_allow_html=True)

    with c2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div class="g-title">Welcome back</div>', unsafe_allow_html=True)
            st.caption("Sign in to continue to Curtin QuitVape Bot.")
            email = st.text_input("Email address", placeholder="name@domain.com", value="", key="login_email")
            pwd = st.text_input("Password", placeholder="••••••••", type="password", value="", key="login_pwd")
            col_a, col_b = st.columns([1,1])
            with col_a: st.checkbox("Remember me", value=True)
            with col_b: st.caption("Prototype sign-in")
            submitted = st.form_submit_button("Sign in")
            if submitted:
                if email.strip().lower() == HARDCODED_EMAIL and pwd == HARDCODED_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email.strip()
                    st.toast("Signed in successfully ✨", icon="✅")
                    goto_home(); _rerun()
                else:
                    st.error("Invalid email or password. Please try again.")
        st.markdown('<div class="btn-primary" style="margin-top:6px;">', unsafe_allow_html=True)
        st.button("Use demo account", on_click=_demo_login)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ----- Category renderer: info card + clickable pill -----
def render_category_card(idx: int, cat: Dict):
    st.markdown(f'''
      <div class="cat-stack" style="--cat-accent:{cat["color"]};">
        <div class="cat-card">
          <div class="title">{cat["emoji"]} {cat["title"]}</div>
          <div class="subtitle">{cat["subtitle"]}</div>
        </div>
      </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="cat-btn">', unsafe_allow_html=True)
    if st.button(f'{cat["emoji"]} {cat["title"]}', key=f"cat_btn_{idx}"):
        select_category(idx); _rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def categories_panel():
    top_header()
    gradient_title("💬", "How can I help you today?")
    st.caption("Pick a topic to get started.")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    for i, cat in enumerate(CATEGORIES):
        render_category_card(i, cat)

    footer_nav("cats")

def _header_for_key(key: str) -> str:
    mapping = {
        "cravings": "CRAVING TO VAPE",
        "stress": "STRESS TURNING TO VAPING",
        "social": "SOCIAL VAPING SITUATIONS",
        "health": "HEALTH RISKS OF VAPING AND AWARENESS",
        "support": "QUIT SUPPORT AND RESOURCES",
    }
    return mapping.get(key, "QuitVape")

def questions_panel(title: str, questions: List[Dict], emoji: str, prefix: str):
    top_header()
    gradient_title(emoji, title)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    for q in questions:
        if st.button(f"❓ {q['q']}", key=f"{prefix}_q_{q['id']}"):
            select_question(q["id"]); _rerun()
    footer_nav(f"{prefix}_qs")

# ---------- Swaps ----------
def swaps_toolbar(actions: List[str]):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if "swap_gum" in actions and st.button("🍬 Chew gum", key="swap_gum_btn"): st.session_state.active_swap = "gum"; _rerun()
    with c2:
        if "swap_water" in actions and st.button("🥤 Sip cold water", key="swap_water_btn"): st.session_state.active_swap = "water"; _rerun()
    with c3:
        if "swap_stretch" in actions and st.button("🤸 2-min stretch", key="swap_stretch_btn"): st.session_state.active_swap = "stretch"; _rerun()
    with c4:
        if "swap_more" in actions and st.button("➕ More ideas", key="swap_more_btn"): st.session_state.active_swap = "more"; _rerun()

def swap_panel():
    which = st.session_state.active_swap
    if which is None: return
    st.markdown("")
    if which == "gum":
        st.markdown("**🍬 Chew gum (90s + playful counter)**")
        st.caption("Focus on flavor → switch sides → breathe slow. Use the counter for fun.")
        def gum_phase(elapsed, _rem):
            if elapsed < 30: st.info("👅 Focus on flavor notes. Small, mindful chews.")
            elif elapsed < 60: st.info("🔁 Switch sides occasionally. Relax your jaw.")
            else: st.info("🫁 Box breathing: 4-4-4-4 rhythm.")
        if st.button("▶️ Start 90s Chew", key="gum_start"):
            run_countdown(90, "Chew Gum (90s)", gum_phase)

        c1, c2, _ = st.columns([1, 1, 1])
        with c1:
            if st.button("🦷 Chew +1", key="gum_chew_plus"):
                st.session_state.gum_chews = min(30, st.session_state.gum_chews + 1)
        with c2:
            if st.button("🔄 Reset chews", key="gum_chew_reset"):
                st.session_state.gum_chews = 0
        st.write(f"Chews: {st.session_state.gum_chews}/30")
        _safe_progress(int(st.session_state.gum_chews / 30 * 100))
        if st.session_state.gum_chews >= 30: st.success("Great! Mouth feels busy; urge should be easing. 🟢")

    elif which == "water":
        st.markdown("**🥤 Sip cold water (10 sips)**")
        st.caption("Small, slow sips. Aim for 10.")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("➕ Add sip", key="sip_add"):
                st.session_state.water_sips = min(10, st.session_state.water_sips + 1)
        with c2:
            if st.button("➖ Remove sip", key="sip_remove"):
                st.session_state.water_sips = max(0, st.session_state.water_sips - 1)
        with c3:
            if st.button("🔄 Reset", key="sip_reset"):
                st.session_state.water_sips = 0
        st.write(f"Sips: {st.session_state.water_sips}/10")
        _safe_progress(int(st.session_state.water_sips * 10))
        if st.session_state.water_sips == 5: st.info("Halfway! Notice the cool sensation. ❄️")
        if st.session_state.water_sips >= 10:
            st.success("Hydration done—fresh mouth feel can shrink cravings."); st.balloons()

    elif which == "stretch":
        st.markdown("**🤸 2-minute stretch (3 × 20s holds)**")
        st.caption("Shoulders → Neck → Toe touch. Slow, smooth, painless range.")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶️ Shoulders 20s", key="stretch_shoulders_btn"): run_countdown(20, "Shoulder rolls (20s)")
        with c2:
            if st.button("▶️ Neck 20s", key="stretch_neck_btn"): run_countdown(20, "Neck stretch (20s)")
        with c3:
            if st.button("▶️ Toe touch 20s", key="stretch_toe_btn"): run_countdown(20, "Toe touch (20s)")
        st.markdown('<div class="hint">Tip: stop if it hurts; we want comfort + blood flow.</div>', unsafe_allow_html=True)

    elif which == "more":
        st.info("More ideas:")
        for idea in ["Crunch on carrots or an apple slice.","Take a brisk 3-minute walk.","Toothpick or cinnamon stick as an oral habit swap.","Do 20 slow deep breaths."]:
            st.markdown(f'<span class="badge">💡 {idea}</span>', unsafe_allow_html=True)

def stress_relief_phase(elapsed: int, _rem: int):
    if elapsed < 30:
        phase = ["Inhale ⬆️", "Hold ✋", "Exhale ⬇️", "Hold ✋"][(elapsed % 16) // 4]
        st.info(f"Box breathing — {phase}", icon="🫁")
    elif elapsed < 60:
        st.info("Roll shoulders + gentle neck circles. Unclench jaw.", icon="🧘")
    else:
        st.info("Soft-focus on one point. Breathe slowly.", icon="🎯")

def run_pomodoro():
    st.success("Pomodoro started: **25 min study** → **5 min break**")
    run_countdown(25 * 60, "Pomodoro — Study (25m)")
    st.toast("Study done. Break time!", icon="☕")
    run_countdown(5 * 60, "Pomodoro — Break (5m)")
    st.success("Pomodoro complete! 🎉")

def grounding_54321_panel():
    st.caption("Tap to complete each step.")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("👀 +1 see", key="gsee_add"): st.session_state.g_see = min(5, st.session_state.g_see + 1)
        if st.button("🔄 reset see", key="gsee_reset"): st.session_state.g_see = 0
        st.write(f"See: {st.session_state.g_see}/5"); _safe_progress(int(st.session_state.g_see / 5 * 100))
    with c2:
        if st.button("✋ +1 feel", key="gfeel_add"): st.session_state.g_feel = min(4, st.session_state.g_feel + 1)
        if st.button("🔄 reset feel", key="gfeel_reset"): st.session_state.g_feel = 0
        st.write(f"Feel: {st.session_state.g_feel}/4"); _safe_progress(int(st.session_state.g_feel / 4 * 100))
    with c3:
        if st.button("👂 +1 hear", key="ghear_add"): st.session_state.g_hear = min(3, st.session_state.g_hear + 1)
        if st.button("🔄 reset hear", key="ghear_reset"): st.session_state.g_hear = 0
        st.write(f"Hear: {st.session_state.g_hear}/3"); _safe_progress(int(st.session_state.g_hear / 3 * 100))
    c4, c5 = st.columns(2)
    with c4:
        if st.button("👃 +1 smell", key="gsmell_add"): st.session_state.g_smell = min(2, st.session_state.g_smell + 1)
        if st.button("🔄 reset smell", key="gsmell_reset"): st.session_state.g_smell = 0
        st.write(f"Smell: {st.session_state.g_smell}/2"); _safe_progress(int(st.session_state.g_smell / 2 * 100))
    with c5:
        if st.button("👅 +1 taste", key="gtaste_add"): st.session_state.g_taste = min(1, st.session_state.g_taste + 1)
        if st.button("🔄 reset taste", key="gtaste_reset"): st.session_state.g_taste = 0
        st.write(f"Taste: {st.session_state.g_taste}/1"); _safe_progress(int(st.session_state.g_taste / 1 * 100))
    if (st.session_state.g_see == 5 and st.session_state.g_feel == 4 and
        st.session_state.g_hear == 3 and st.session_state.g_smell == 2 and
        st.session_state.g_taste == 1):
        st.success("Grounding complete. 🌿")

# ---------- Answers ----------
def cravings_answer_panel():
    top_header()
    gradient_title("🌊", "CRAVING TO VAPE")
    q = next((x for x in CRAVINGS_QUESTIONS if x["id"] == st.session_state.selected_question), None)
    if not q:
        return
    st.markdown(f'<div class="qtxt" style="margin-top:8px;">Q: {q["q"]}</div>', unsafe_allow_html=True)
    st.write(q["a"])
    actions = q["actions"]

    if "sos_90" in actions:
        st.markdown("**🚨 90-second Craving SOS**")
        if st.button("▶️ Start 90-sec SOS", key="start_sos"): run_countdown(90, "Craving SOS (90s)")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "breath_90" in actions:
        st.markdown("**🫁 Box Breathing (90s)**")
        def breath_phase(elapsed, _r):
            phase = ["Inhale ⬆️", "Hold ✋", "Exhale ⬇️", "Hold ✋"][(elapsed % 16) // 4]
            nxt = 4 - (elapsed % 4)
            st.markdown(
                f"<div class='phase'>{phase}</div>"
                f"<div class='phase-sub'>Next in {nxt}s</div>",
                unsafe_allow_html=True
            )
        if st.button("▶️ Start Breathing (90s)", key="start_breath_90"): run_countdown(90, "Box Breathing (90s)", breath_phase)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "timer_3m" in actions:
        st.markdown("**⏱️ 3-minute Timer**")
        if st.button("▶️ Start 3-min Timer", key="start_3m"): run_countdown(180, "3-minute Craving Timer")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "focus_3m" in actions:
        st.markdown("**🎯 Focus Timer (3m)**")
        st.caption("Pick one small task and stick with it until the timer ends.")
        if st.button("▶️ Start Focus Timer (3m)", key="start_focus_3m"): run_countdown(180, "Focus Timer (3m)")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if any(a in actions for a in ("swap_gum","swap_water","swap_stretch","swap_more")):
        st.markdown("**Healthy swaps (interactive)**")
        swaps_toolbar(actions); swap_panel()

    if "breath_60" in actions:
        st.markdown("**🫁 Breathing (60s)**")
        def breath_phase_60(elapsed, _r):
            phase = ["Inhale ⬆️", "Hold ✋", "Exhale ⬇️", "Hold ✋"][(elapsed % 16) // 4]
            nxt = 4 - (elapsed % 4)
            st.markdown(
                f"<div class='phase'>{phase}</div>"
                f"<div class='phase-sub'>Next in {nxt}s</div>",
                unsafe_allow_html=True
            )
        if st.button("▶️ Start Breathing (60s)", key="start_breath_60"): run_countdown(60, "Breathing (60s)", breath_phase_60)

    footer_nav("crav_ans", show_questions=True)

def stress_or_social_answer_panel():
    top_header()
    gradient_title("⚡", "STRESS TURNING TO VAPING / SOCIAL VAPING SITUATIONS")
    q = next((x for x in STRESS_OR_SOCIAL_QUESTIONS if x["id"] == st.session_state.selected_question), None)
    if not q:
        return
    st.markdown(f'<div class="qtxt" style="margin-top:8px;">Q: {q["q"]}</div>', unsafe_allow_html=True)
    st.write(q["a"])
    actions = q["actions"]

    if "stress_relief_2m" in actions:
        st.markdown("**🧘 2-minute Stress Relief**")
        if st.button("▶️ Start 2-min Relief", key="start_relief_2m"): run_countdown(120, "Stress Relief (2m)", stress_relief_phase)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "study_break_5m" in actions:
        st.markdown("**☕ Study Break Timer (5m)**")
        if st.button("▶️ Start 5-min Break", key="start_break_5m"): run_countdown(300, "Study Break (5m)")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "pomodoro_25_5" in actions:
        st.markdown("**📚 Pomodoro (25 + 5)**")
        if st.button("▶️ Start Pomodoro", key="start_pomo"): run_pomodoro()
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if "grounding_54321" in actions:
        st.markdown("**🌿 5-4-3-2-1 Grounding**")
        grounding_54321_panel()

    footer_nav("social_ans", show_questions=True)

def end_chat_panel():
    top_header()
    gradient_title("🌗", "Thanks for using Curtin QuitVape Bot")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if os.path.exists(QUOTE_IMAGE):
        img_url = data_url_from_path(QUOTE_IMAGE)
        if img_url:
            st.markdown(f'<div class="center-wrap"><img class="end-img" src="{img_url}" /></div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.write("How was this experience?")
    cols = st.columns(5)
    for i, col in enumerate(cols, start=1):
        with col:
            filled = "⭐" if st.session_state.get("rating", 0) >= i else "☆"
            if st.button(filled, key=f"rating_star_{i}"):
                st.session_state["rating"] = i; _rerun()
    st.caption(f"Your rating: {st.session_state.get('rating',0)}/5")
    if st.session_state.get("rating", 0) > 0: st.success("Thanks for the rating! Want to start again?")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("📂 Categories", key="end_cats", on_click=goto_home)
    with c2: st.button("🏠 Home", key="end_home", on_click=goto_home)
    with c3: st.button("🔚 End Chat", key="end_end", on_click=lambda: setattr(st.session_state, "stage", "ended"))

# ====================== ROUTER ======================
def category_router():
    idx = st.session_state.selected_category
    if idx is None:
        return categories_panel()
    key = CATEGORIES[idx]["key"]

    if key == "cravings":
        if st.session_state.stage == "in_category":
            questions_panel("CRAVING TO VAPE", CRAVINGS_QUESTIONS, "🌊", "crav")
        elif st.session_state.stage == "in_answer":
            cravings_answer_panel()
        else:
            questions_panel("CRAVING TO VAPE", CRAVINGS_QUESTIONS, "🌊", "crav")

    elif key in ("stress", "social"):
        if st.session_state.stage == "in_category":
            questions_panel("STRESS TURNING TO VAPING / SOCIAL VAPING SITUATIONS", STRESS_OR_SOCIAL_QUESTIONS, "⚡", "social")
        elif st.session_state.stage == "in_answer":
            stress_or_social_answer_panel()
        else:
            questions_panel("STRESS TURNING TO VAPING / SOCIAL VAPING SITUATIONS", STRESS_OR_SOCIAL_QUESTIONS, "⚡", "social")

    else:
        label = _header_for_key(key)
        top_header()
        gradient_title("🧭", label, "Content coming soon. Pick another topic or go back.")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        footer_nav("comingsoon")

def app_flow():
    stage = st.session_state.stage
    if not st.session_state.authenticated:
        if stage == "splash":
            splash_screen()
        else:
            login_panel()
        return

    if stage == "show_categories":
        categories_panel()
    elif stage in ("in_category", "in_answer"):
        category_router()
    elif stage == "ended":
        end_chat_panel()
    else:
        goto_home()
        categories_panel()

# ====================== RUN ======================
app_flow()

if "exit_quote_shown" not in st.session_state:
    st.session_state.exit_quote_shown = True
    st.toast("“You only need to be stronger than your craving for a few minutes.”", icon="💜")
