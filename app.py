# app.py
# ESGenie🧞 — Sustainable Portfolio Advisor
# Single-page Streamlit app

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESGenie",
    page_icon="🧞",
    layout="wide"
)

# ── Custom CSS — visual redesign only, zero logic changes ─────────────
st.markdown("""
<style>
/* ── Import fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ─────────────────────────────────────────── */
:root {
    --sage:       #4a7c59;
    --sage-light: #6a9e76;
    --sage-pale:  #c8dfc0;
    --cream:      #f4f1eb;
    --cream-dark: #e8e3d8;
    --forest:     #2d5016;
    --text:       #1e2e1a;
    --text-muted: #5a6e55;
    --white:      #ffffff;
    --amber:      #c9852a;
    --red-soft:   #b85c5c;
    --radius:     12px;
    --shadow:     0 2px 16px rgba(45,80,22,0.10);
}

/* ── Global page background ───────────────────────────────── */
.stApp {
    background-color: #edf4e8 !important;
    background-image:
        radial-gradient(ellipse at 10% 0%, rgba(106,158,118,0.18) 0%, transparent 55%),
        radial-gradient(ellipse at 90% 100%, rgba(74,124,89,0.12) 0%, transparent 55%);
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d5016 0%, #3d6b20 60%, #4a7c59 100%) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * {
    color: #e8f0e4 !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c8dfc0 !important;
    font-family: 'DM Serif Display', serif !important;
    letter-spacing: 0.01em;
}
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stSelectbox select {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(200,223,192,0.35) !important;
    color: #e8f0e4 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(200,223,192,0.35) !important;
    color: #e8f0e4 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #c8dfc0 !important;
}
section[data-testid="stSidebar"] caption,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] .stCaption {
    color: rgba(200,223,192,0.75) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(200,223,192,0.25) !important;
}

/* Sidebar expander */
section[data-testid="stSidebar"] details {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(200,223,192,0.20) !important;
    border-radius: 8px !important;
    padding: 4px 8px !important;
}

/* ── Run button ───────────────────────────────────────────── */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6a9e76 0%, #4a7c59 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 1rem !important;
    box-shadow: 0 4px 14px rgba(45,80,22,0.35) !important;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #7ab886 0%, #5a8e69 100%) !important;
    box-shadow: 0 6px 20px rgba(45,80,22,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Main area headings ───────────────────────────────────── */
.stMarkdown h1, .main h1, [data-testid="stHeading"] h1 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--forest) !important;
    font-size: 2.4rem !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 0.1em !important;
}
.stMarkdown h2, .main h2, [data-testid="stHeading"] h2 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--sage) !important;
    font-size: 1.5rem !important;
    font-style: italic;
}
.stMarkdown h3, .stMarkdown h4 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    color: var(--forest) !important;
    letter-spacing: 0.01em !important;
}

/* Main title subheader */
.stMarkdown p, .main p {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-muted) !important;
    line-height: 1.65 !important;
}

/* ── Metric cards ─────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    color: var(--forest) !important;
    font-size: 1.6rem !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

/* ── Dataframe / tables ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* ── Info / warning / error / success boxes ───────────────── */
[data-testid="stInfo"], .stAlert[data-baseweb="notification"][kind="info"] {
    background: rgba(200,223,192,0.35) !important;
    border-left: 4px solid var(--sage) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
    color: var(--forest) !important;
}
[data-testid="stWarning"] {
    background: rgba(201,133,42,0.12) !important;
    border-left: 4px solid var(--amber) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
}
[data-testid="stSuccess"] {
    background: rgba(74,124,89,0.12) !important;
    border-left: 4px solid var(--sage) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
}
[data-testid="stError"] {
    background: rgba(184,92,92,0.10) !important;
    border-left: 4px solid var(--red-soft) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
}

/* ── Horizontal dividers ──────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--sage-pale) !important;
    margin: 1.5rem 0 !important;
}

/* ── Spinner ──────────────────────────────────────────────── */
[data-testid="stSpinner"] > div {
    border-top-color: var(--sage) !important;
}

/* ── Radio buttons & checkboxes in sidebar ────────────────── */
section[data-testid="stSidebar"] [data-baseweb="radio"] label,
section[data-testid="stSidebar"] [data-baseweb="checkbox"] label {
    color: #e8f0e4 !important;
}

/* ── Caption / footer text ────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
}

/* ── Charts: give them a card treatment ───────────────────── */
[data-testid="stPyplotRootElement"] {
    background: var(--white) !important;
    border: 1px solid var(--sage-pale) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    box-shadow: var(--shadow) !important;
}

/* ── Subtle page-top leaf accent bar ──────────────────────── */
.main > div:first-child::before {
    content: '';
    display: block;
    height: 4px;
    background: linear-gradient(90deg, #2d5016, #6a9e76, #c8dfc0);
    border-radius: 0 0 4px 4px;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Shared functions ──────────────────────────────────────────────────

def classify_esg(score):
    if score >= 80:
        return "🟢 High ESG"
    elif score >= 50:
        return "🟡 Moderate ESG"
    else:
        return "🔴 Low ESG"

def compute_esg(E, S, G, w_e, w_s, w_g):
    return w_e * E + w_s * S + w_g * G

def portfolio_ret(w1, r1, r2):
    return w1 * r1 + (1 - w1) * r2

def portfolio_sd(w1, sd1, sd2, rho):
    variance = (
        w1**2 * sd1**2 +
        (1 - w1)**2 * sd2**2 +
        2 * rho * w1 * (1 - w1) * sd1 * sd2
    )
    return np.sqrt(variance)

def portfolio_esg(w1, esg1, esg2):
    return w1 * esg1 + (1 - w1) * esg2

def sharpe_ratio(w1, r1, r2, sd1, sd2, rho, r_free):
    ret = portfolio_ret(w1, r1, r2)
    sd  = portfolio_sd(w1, sd1, sd2, rho)
    if sd == 0:
        return 0
    return (ret - r_free) / sd

def utility(w1, r_h, r_f, sd_h, sd_f, rho_hf, r_free,
            risk_aversion, theta, esg_h, esg_f,
            sin_choice, excluded, asset1_name, asset2_name,
            apply_threshold, threshold, penalty_strength):
    ret = portfolio_ret(w1, r_h, r_f)
    sd  = portfolio_sd(w1, sd_h, sd_f, rho_hf)
    esg = portfolio_esg(w1, esg_h, esg_f)

    base_utility = (ret - r_free) - (risk_aversion / 2) * (sd ** 2) + theta * (esg / 100)

    exclusion_penalty = 0
    if sin_choice == 1:
        if asset1_name in excluded and w1 > 0:
            exclusion_penalty -= 1e6 * w1
        if asset2_name in excluded and w1 < 1:
            exclusion_penalty -= 1e6 * (1 - w1)

    threshold_penalty = 0
    if apply_threshold and esg < threshold:
        shortfall = (threshold - esg) / 100
        threshold_penalty = -penalty_strength * shortfall

    return base_utility + exclusion_penalty + threshold_penalty

def run_optimisation(r_h, r_f, sd_h, sd_f, rho_hf, r_free,
                     risk_aversion, theta, esg_h, esg_f,
                     sin_choice, excluded, asset1_name, asset2_name,
                     apply_threshold, threshold, penalty_strength):
    weights = np.linspace(0, 1, 1000)
    utilities, sharpes, returns, risks, esg_scores = [], [], [], [], []

    for w in weights:
        utilities.append(utility(
            w, r_h, r_f, sd_h, sd_f, rho_hf, r_free,
            risk_aversion, theta, esg_h, esg_f,
            sin_choice, excluded, asset1_name, asset2_name,
            apply_threshold, threshold, penalty_strength
        ))
        sharpes.append(sharpe_ratio(w, r_h, r_f, sd_h, sd_f, rho_hf, r_free))
        returns.append(portfolio_ret(w, r_h, r_f))
        risks.append(portfolio_sd(w, sd_h, sd_f, rho_hf))
        esg_scores.append(portfolio_esg(w, esg_h, esg_f))

    utilities  = np.array(utilities)
    sharpes    = np.array(sharpes)
    returns    = np.array(returns)
    risks      = np.array(risks)
    esg_scores = np.array(esg_scores)

    i_util  = np.argmax(utilities)
    i_sharp = np.argmax(sharpes)
    i_minv  = np.argmin(risks)

    return {
        "weights": weights, "utilities": utilities, "sharpes": sharpes,
        "returns": returns, "risks": risks, "esg_scores": esg_scores,
        "w1_optimal":   weights[i_util],  "ret_optimal":  returns[i_util],
        "sd_optimal":   risks[i_util],    "esg_optimal":  esg_scores[i_util],
        "sr_optimal":   sharpes[i_util],
        "w1_tangency":  weights[i_sharp], "ret_tangency": returns[i_sharp],
        "sd_tangency":  risks[i_sharp],   "esg_tangency": esg_scores[i_sharp],
        "sr_tangency":  sharpes[i_sharp],
        "w1_min_var":   weights[i_minv],  "ret_min_var":  returns[i_minv],
        "sd_min_var":   risks[i_minv],    "esg_min_var":  esg_scores[i_minv],
        "sr_min_var":   sharpes[i_minv],
    }

def optimise_for_params(theta_val, gamma_val, weights,
                        r_h, r_f, sd_h, sd_f, rho_hf, r_free,
                        esg_h, esg_f, sin_choice, excluded,
                        asset1_name, asset2_name,
                        apply_threshold, threshold, penalty_strength):
    best_u, best_w = -np.inf, 0.0
    for w in weights:
        u = utility(
            w, r_h, r_f, sd_h, sd_f, rho_hf, r_free,
            gamma_val, theta_val, esg_h, esg_f,
            sin_choice, excluded, asset1_name, asset2_name,
            apply_threshold, threshold, penalty_strength
        )
        if u > best_u:
            best_u, best_w = u, w
    return best_w

# ── Header ────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.25rem;">
  <span style="font-size:2.6rem; line-height:1;">🧞</span>
  <span style="font-family:'DM Serif Display',serif; font-size:2.4rem; color:#2d5016; letter-spacing:-0.01em;">ESGenie</span>
</div>
<p style="font-family:'DM Sans',sans-serif; color:#5a6e55; font-size:1.05rem; margin-top:0; margin-bottom:1.5rem;">
  Your personalised sustainable investment portfolio advisor
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Sidebar inputs ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1rem;">
      <span style="font-family:'DM Serif Display',serif; font-size:1.5rem; color:#c8dfc0; letter-spacing:0.02em;">📋 Your Inputs</span>
      <p style="font-size:0.78rem; color:rgba(200,223,192,0.65); margin-top:0.25rem;">Fill in all sections then click Run ESGenie.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Financial data ────────────────────────────────────────────────
    st.subheader("💰 Financial Data")

    asset1_name = st.text_input("Asset 1 name", value="Asset 1")
    r_h  = st.slider("Asset 1 expected return (%)", -50, 50, 8)  / 100
    sd_h = st.slider("Asset 1 standard deviation (%)", 0, 100, 20) / 100

    asset2_name = st.text_input("Asset 2 name", value="Asset 2")
    r_f  = st.slider("Asset 2 expected return (%)", -50, 50, 4)  / 100
    sd_f = st.slider("Asset 2 standard deviation (%)", 0, 100, 10) / 100

    rho_hf = st.slider("Correlation between assets", -1.0, 1.0, 0.2, step=0.01)
    r_free = st.slider("Risk-free rate (%)", 0.0, 10.0, 2.0, step=0.1) / 100

    # ── Risk profile ──────────────────────────────────────────────────
    st.subheader("⚖️ Risk Profile")
    risk_choice = st.radio(
        "Your attitude to investment risk:",
        options=["🛡️ Conservative", "⚖️ Balanced", "🚀 Aggressive"],
        index=1
    )
    risk_map = {
        "🛡️ Conservative": (10, "Conservative"),
        "⚖️ Balanced":     (5,  "Balanced"),
        "🚀 Aggressive":   (2,  "Aggressive")
    }
    risk_aversion, risk_label = risk_map[risk_choice]

    # ── ESG preferences ───────────────────────────────────────────────
    st.subheader("🌱 ESG Preferences")
    theta = st.slider(
        "ESG importance (θ)  —  0 = financial only, 4 = ESG first",
        0.0, 4.0, 2.0, step=0.1
    )

    esg_focus = st.selectbox(
        "ESG pillar focus:",
        options=[
            "🌍 Environmental focus  (E=0.60, S=0.20, G=0.20)",
            "🤝 Social focus         (E=0.20, S=0.60, G=0.20)",
            "🏛️ Governance focus     (E=0.20, S=0.20, G=0.60)",
            "⚖️ Balanced ESG         (E=0.34, S=0.33, G=0.33)",
            "✏️ Custom weights"
        ]
    )

    esg_focus_map = {
        "🌍 Environmental focus  (E=0.60, S=0.20, G=0.20)": (0.60, 0.20, 0.20, "Environmental focus"),
        "🤝 Social focus         (E=0.20, S=0.60, G=0.20)": (0.20, 0.60, 0.20, "Social focus"),
        "🏛️ Governance focus     (E=0.20, S=0.20, G=0.60)": (0.20, 0.20, 0.60, "Governance focus"),
        "⚖️ Balanced ESG         (E=0.34, S=0.33, G=0.33)": (0.34, 0.33, 0.33, "Balanced ESG"),
    }

    if "✏️ Custom weights" in esg_focus:
        st.caption("Weights must sum to 1.0")
        w_e = st.slider("Environment (E) weight", 0.0, 1.0, 0.34, step=0.01)
        w_s = st.slider("Social (S) weight",       0.0, 1.0, 0.33, step=0.01)
        w_g = st.slider("Governance (G) weight",   0.0, 1.0, 0.33, step=0.01)
        weight_sum = w_e + w_s + w_g
        if abs(weight_sum - 1.0) > 0.01:
            st.warning(f"⚠️ Weights sum to {weight_sum:.2f} — must equal 1.0")
        esg_focus_label = "Custom"
    else:
        w_e, w_s, w_g, esg_focus_label = esg_focus_map[esg_focus]

    # ── Asset ESG scores ──────────────────────────────────────────────
    st.subheader("📊 Asset ESG Scores")
    st.caption("Scores from 0 (worst) to 100 (best)")

    with st.expander(f"ESG scores for {asset1_name}"):
        sector_options = ["Technology", "Healthcare", "Financial Services",
                          "Consumer Goods", "Energy", "Tobacco",
                          "Weapons & Defence", "Gambling", "Other"]
        sector1 = st.selectbox(f"{asset1_name} sector", sector_options, key="s1")
        E1 = st.slider(f"{asset1_name} — Environmental (E)", 0, 100, 60, key="e1")
        S1 = st.slider(f"{asset1_name} — Social (S)",        0, 100, 60, key="s1s")
        G1 = st.slider(f"{asset1_name} — Governance (G)",    0, 100, 60, key="g1")

    with st.expander(f"ESG scores for {asset2_name}"):
        sector2 = st.selectbox(f"{asset2_name} sector", sector_options, key="s2")
        E2 = st.slider(f"{asset2_name} — Environmental (E)", 0, 100, 40, key="e2")
        S2 = st.slider(f"{asset2_name} — Social (S)",        0, 100, 40, key="s2s")
        G2 = st.slider(f"{asset2_name} — Governance (G)",    0, 100, 40, key="g2")

    # ── Ethical screening ─────────────────────────────────────────────
    st.subheader("🛡️ Ethical Screening")

    SIN_SECTORS = {"Tobacco", "Weapons & Defence", "Gambling"}
    excluded = {}
    for name, sector in [(asset1_name, sector1), (asset2_name, sector2)]:
        if sector in SIN_SECTORS:
            excluded[name] = sector

    if excluded:
        st.warning(f"⚠️ Restricted sector detected: {', '.join(excluded.values())}")
        sin_option = st.radio(
            "How to handle restricted sectors?",
            options=[
                "❌ Exclude entirely (weight = 0%)",
                "⚠️ Apply utility penalty",
                "✅ Proceed without restriction"
            ]
        )
        sin_choice = [
            "❌ Exclude entirely (weight = 0%)",
            "⚠️ Apply utility penalty",
            "✅ Proceed without restriction"
        ].index(sin_option) + 1
    else:
        st.success("✅ No restricted sectors detected.")
        sin_choice = 3

    threshold = st.slider(
        "Minimum ESG score threshold  (0 = no threshold)",
        0, 100, 0
    )
    apply_threshold  = threshold > 0
    penalty_strength = 0.01 * theta

    # ── Run button ────────────────────────────────────────────────────
    st.markdown("---")
    run = st.button("✨ Run ESGenie", type="primary", use_container_width=True)

# ── Main area — only renders after button click ───────────────────────
if not run:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(74,124,89,0.10) 0%, rgba(200,223,192,0.20) 100%);
        border: 1px solid rgba(74,124,89,0.25);
        border-radius: 14px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
    ">
      <p style="font-family:'DM Serif Display',serif; font-size:1.3rem; color:#2d5016; margin:0 0 0.5rem;">
        Welcome to ESGenie 🧞
      </p>
      <p style="color:#5a6e55; font-size:0.95rem; margin:0;">
        Complete the inputs in the sidebar on the left, then hit <strong>✨ Run ESGenie</strong> to generate your personalised sustainable portfolio recommendation.
      </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Step 1", "Fill inputs", "Sidebar →")
    with col2:
        st.metric("📊 Step 2", "Run ESGenie", "Click button")
    with col3:
        st.metric("🔬 Step 3", "Explore results", "Scroll down")
    st.stop()

# ── Guard: custom weights must sum to 1 ──────────────────────────────
if "✏️ Custom weights" in esg_focus and abs(w_e + w_s + w_g - 1.0) > 0.01:
    st.error("❌ Custom ESG weights must sum to 1.0. Please adjust in the sidebar.")
    st.stop()

# ── Guard: both assets excluded ───────────────────────────────────────
if sin_choice == 1 and len(excluded) == 2:
    st.error("❌ Both assets are in restricted sectors and have been excluded. No valid portfolio can be constructed.")
    st.stop()

# ── Compute ESG scores ────────────────────────────────────────────────
esg_h = compute_esg(E1, S1, G1, w_e, w_s, w_g)
esg_f = compute_esg(E2, S2, G2, w_e, w_s, w_g)

# ── ESG score summary ─────────────────────────────────────────────────
st.header("🌱 ESG Score Summary")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{asset1_name}** ({sector1})")
    st.metric("Composite ESG Score", f"{esg_h:.1f} / 100", classify_esg(esg_h))
    st.caption(f"E={E1} × {w_e:.2f}  +  S={S1} × {w_s:.2f}  +  G={G1} × {w_g:.2f}")

with col2:
    st.markdown(f"**{asset2_name}** ({sector2})")
    st.metric("Composite ESG Score", f"{esg_f:.1f} / 100", classify_esg(esg_f))
    st.caption(f"E={E2} × {w_e:.2f}  +  S={S2} × {w_s:.2f}  +  G={G2} × {w_g:.2f}")

if apply_threshold:
    if esg_h < threshold:
        st.warning(f"⚠️ {asset1_name} ESG score ({esg_h:.1f}) is below your threshold of {threshold}.")
    if esg_f < threshold:
        st.warning(f"⚠️ {asset2_name} ESG score ({esg_f:.1f}) is below your threshold of {threshold}.")

st.markdown("---")

# ── Run optimisation ──────────────────────────────────────────────────
with st.spinner("🧞 ESGenie is working its magic..."):
    res = run_optimisation(
        r_h, r_f, sd_h, sd_f, rho_hf, r_free,
        risk_aversion, theta, esg_h, esg_f,
        sin_choice, excluded, asset1_name, asset2_name,
        apply_threshold, threshold, penalty_strength
    )

w1_optimal  = res["w1_optimal"];  w2_optimal  = 1 - w1_optimal
w1_tangency = res["w1_tangency"]; w2_tangency = 1 - w1_tangency
w1_min_var  = res["w1_min_var"];  w2_min_var  = 1 - w1_min_var
esg_premium = res["sr_tangency"] - res["sr_optimal"]

# ── Portfolio results ─────────────────────────────────────────────────
st.header("📊 Portfolio Results")

# Investor profile
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("⚖️ Risk Profile", risk_label, f"γ = {risk_aversion}")
with col2:
    if theta <= 1:
        esg_importance_label = "Low ESG preference"
    elif theta <= 2.5:
        esg_importance_label = "Moderate ESG preference"
    else:
        esg_importance_label = "High ESG preference"
    st.metric("🌱 ESG Importance", esg_importance_label, f"θ = {theta}")
with col3:
    st.metric("🎯 ESG Focus", esg_focus_label)

st.markdown("#### 💼 Asset Allocation")
import pandas as pd

alloc_df = pd.DataFrame({
    "Asset":       [asset1_name, asset2_name, "Portfolio (weighted)"],
    "Weight":      [f"{w1_optimal*100:.1f}%", f"{w2_optimal*100:.1f}%", "100.0%"],
    "ESG Score":   [f"{esg_h:.1f}", f"{esg_f:.1f}", f"{res['esg_optimal']:.1f}"],
    "ESG Class":   [classify_esg(esg_h), classify_esg(esg_f), classify_esg(res['esg_optimal'])]
})
st.dataframe(alloc_df, use_container_width=True, hide_index=True)

st.markdown("#### 📈 Portfolio Characteristics")
chars_df = pd.DataFrame({
    "Metric":      ["Expected Return", "Risk (Std Dev)", "Sharpe Ratio", "ESG Score", "ESG Class"],
    "🟢 Recommended": [
        f"{res['ret_optimal']*100:.2f}%",
        f"{res['sd_optimal']*100:.2f}%",
        f"{res['sr_optimal']:.3f}",
        f"{res['esg_optimal']:.1f}",
        classify_esg(res['esg_optimal'])
    ],
    "📐 Tangency": [
        f"{res['ret_tangency']*100:.2f}%",
        f"{res['sd_tangency']*100:.2f}%",
        f"{res['sr_tangency']:.3f}",
        f"{res['esg_tangency']:.1f}",
        classify_esg(res['esg_tangency'])
    ],
    "🛡️ Min Variance": [
        f"{res['ret_min_var']*100:.2f}%",
        f"{res['sd_min_var']*100:.2f}%",
        f"{res['sr_min_var']:.3f}",
        f"{res['esg_min_var']:.1f}",
        classify_esg(res['esg_min_var'])
    ],
})
st.dataframe(chars_df, use_container_width=True, hide_index=True)

# ESG premium
if esg_premium > 0:
    st.warning(f"📉 ESG Premium: **{esg_premium:+.3f} Sharpe points** — your ESG preferences reduce risk-adjusted return relative to the purely financial tangency portfolio.")
else:
    st.success(f"📈 ESG Premium: **{esg_premium:+.3f} Sharpe points** — your ESG preferences align with financial performance. No sacrifice in risk-adjusted return detected.")

# Dynamic narrative
dominant_asset  = asset1_name if w1_optimal >= w2_optimal else asset2_name
secondary_asset = asset2_name if w1_optimal >= w2_optimal else asset1_name
dominant_esg    = esg_h       if w1_optimal >= w2_optimal else esg_f
secondary_esg   = esg_f       if w1_optimal >= w2_optimal else esg_h
esg_driver      = dominant_esg > secondary_esg

st.markdown("#### 💬 Recommendation")
st.info(
    f"Based on your **{risk_label.lower()} risk profile** (γ={risk_aversion}) and "
    f"**{esg_importance_label.lower()}** (θ={theta}), ESGenie recommends allocating "
    f"**{w1_optimal*100:.1f}% to {asset1_name}** and **{w2_optimal*100:.1f}% to {asset2_name}**."
)

if esg_driver:
    st.write(
        f"The tilt toward **{dominant_asset}** is partly driven by its stronger ESG score "
        f"({dominant_esg:.1f} vs {secondary_esg:.1f}), consistent with your "
        f"{esg_focus_label.lower()} and ESG importance of {theta}."
    )
else:
    st.write(
        f"The tilt toward **{dominant_asset}** is driven primarily by its superior "
        f"risk-return profile rather than ESG performance."
    )

if apply_threshold and (esg_h < threshold or esg_f < threshold):
    st.warning(f"One or more assets fell below your minimum ESG threshold of {threshold}. A utility penalty was applied.")

if sin_choice == 1 and excluded:
    for name, sec in excluded.items():
        st.error(f"**{name}** ({sec}) was excluded from the portfolio per your ethical screening preferences.")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────
st.header("📈 Charts")

weights_plot = np.linspace(0, 1, 500)
ret_plot  = np.array([portfolio_ret(w, r_h, r_f)          for w in weights_plot])
risk_plot = np.array([portfolio_sd(w, sd_h, sd_f, rho_hf) for w in weights_plot])
esg_plot  = np.array([portfolio_esg(w, esg_h, esg_f)      for w in weights_plot])
util_plot = np.array([utility(
    w, r_h, r_f, sd_h, sd_f, rho_hf, r_free,
    risk_aversion, theta, esg_h, esg_f,
    sin_choice, excluded, asset1_name, asset2_name,
    apply_threshold, threshold, penalty_strength
) for w in weights_plot])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#f4f1eb')
for ax in (ax1, ax2):
    ax.set_facecolor('#f9f7f2')
    for spine in ax.spines.values():
        spine.set_edgecolor('#c8dfc0')
        spine.set_linewidth(0.8)
fig.suptitle("ESGenie — Portfolio Analysis", fontsize=14, fontweight='bold', color='#2d5016')

# Left: ESG-efficient frontier
sc = ax1.scatter(risk_plot, ret_plot, c=esg_plot, cmap='RdYlGn', s=8, zorder=2)
plt.colorbar(sc, ax=ax1, label='Portfolio ESG Score')

cml_x     = np.linspace(0, max(risk_plot) * 1.2, 100)
cml_slope = (res['ret_tangency'] - r_free) / res['sd_tangency']
ax1.plot(cml_x, r_free + cml_slope * cml_x,
         linestyle='--', color='#4a7c59', linewidth=1, label='Capital Market Line')
ax1.scatter(0, r_free, marker='D', color='#4a7c59', s=60, zorder=5,
            label=f'Risk-Free Rate ({r_free*100:.1f}%)')
ax1.scatter(res['sd_min_var'], res['ret_min_var'],
            marker='s', color='#7b5ea7', s=100, zorder=5,
            label=f"Min Variance ({w1_min_var*100:.0f}% {asset1_name})")
ax1.scatter(res['sd_tangency'], res['ret_tangency'],
            marker='^', color='#4a7c59', s=120, zorder=5,
            label=f"Tangency ({w1_tangency*100:.0f}% {asset1_name})")
ax1.scatter(res['sd_optimal'], res['ret_optimal'],
            marker='*', color='#2d5016', s=220, zorder=5,
            label=f"Recommended ({w1_optimal*100:.0f}% {asset1_name})")
ax1.annotate('Min Variance', xy=(res['sd_min_var'], res['ret_min_var']),
             xytext=(10,-15), textcoords='offset points', fontsize=8, color='#7b5ea7')
ax1.annotate('Tangency', xy=(res['sd_tangency'], res['ret_tangency']),
             xytext=(10,5), textcoords='offset points', fontsize=8, color='#4a7c59')
ax1.annotate('Recommended', xy=(res['sd_optimal'], res['ret_optimal']),
             xytext=(10,5), textcoords='offset points', fontsize=8, color='#2d5016')
ax1.set_xlabel('Risk (Standard Deviation)', color='#5a6e55')
ax1.set_ylabel('Expected Return', color='#5a6e55')
ax1.set_title('ESG-Efficient Frontier', color='#2d5016', fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.25, color='#c8dfc0')
ax1.tick_params(colors='#5a6e55')
ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.1f}%'))
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.1f}%'))

# Right: Utility vs weight
ax2.plot(weights_plot * 100, util_plot, color='#4a7c59', linewidth=2, label='Utility U(w)')
ax2.axvline(x=w1_optimal*100, color='#2d5016', linestyle='--', linewidth=1, alpha=0.7)
ax2.scatter(w1_optimal*100, utility(
    w1_optimal, r_h, r_f, sd_h, sd_f, rho_hf, r_free,
    risk_aversion, theta, esg_h, esg_f,
    sin_choice, excluded, asset1_name, asset2_name,
    apply_threshold, threshold, penalty_strength),
    marker='*', color='#2d5016', s=220, zorder=5,
    label=f'Optimal: {w1_optimal*100:.1f}%')
ax2.axvline(x=w1_tangency*100, color='#6a9e76', linestyle=':', linewidth=1, alpha=0.7,
            label=f'Tangency: {w1_tangency*100:.1f}%')
ax2.set_xlabel(f'Weight in {asset1_name} (%)', color='#5a6e55')
ax2.set_ylabel('Utility', color='#5a6e55')
ax2.set_title('Utility Function vs Portfolio Weight', color='#2d5016', fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.25, color='#c8dfc0')
ax2.tick_params(colors='#5a6e55')

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Sensitivity analysis ──────────────────────────────────────────────
st.header("🔬 Sensitivity Analysis")

with st.spinner("🧞 Computing sensitivity across parameter space..."):
    weights_sa  = np.linspace(0, 1, 1000)
    theta_range = np.linspace(0, 4, 80)
    gamma_range = np.linspace(1, 15, 80)

    sa_weights, sa_esg, sa_sharpes = [], [], []
    for t in theta_range:
        w_opt = optimise_for_params(
            t, risk_aversion, weights_sa,
            r_h, r_f, sd_h, sd_f, rho_hf, r_free,
            esg_h, esg_f, sin_choice, excluded,
            asset1_name, asset2_name,
            apply_threshold, threshold, penalty_strength
        )
        sa_weights.append(w_opt * 100)
        sa_esg.append(portfolio_esg(w_opt, esg_h, esg_f))
        sa_sharpes.append(sharpe_ratio(w_opt, r_h, r_f, sd_h, sd_f, rho_hf, r_free))

    sg_sharpes = []
    for g in gamma_range:
        w_opt = optimise_for_params(
            theta, g, weights_sa,
            r_h, r_f, sd_h, sd_f, rho_hf, r_free,
            esg_h, esg_f, sin_choice, excluded,
            asset1_name, asset2_name,
            apply_threshold, threshold, penalty_strength
        )
        sg_sharpes.append(sharpe_ratio(w_opt, r_h, r_f, sd_h, sd_f, rho_hf, r_free))

    theta_grid = np.linspace(0, 4, 15)
    gamma_grid = np.linspace(1, 15, 15)
    heatmap    = np.zeros((len(gamma_grid), len(theta_grid)))
    for i, g in enumerate(gamma_grid):
        for j, t in enumerate(theta_grid):
            w_opt = optimise_for_params(
                t, g, weights_sa,
                r_h, r_f, sd_h, sd_f, rho_hf, r_free,
                esg_h, esg_f, sin_choice, excluded,
                asset1_name, asset2_name,
                apply_threshold, threshold, penalty_strength
            )
            heatmap[i, j] = portfolio_esg(w_opt, esg_h, esg_f)

sa_weights = np.array(sa_weights)
sa_esg     = np.array(sa_esg)
sa_sharpes = np.array(sa_sharpes)
sg_sharpes = np.array(sg_sharpes)

# Sensitivity table
st.markdown(f"#### 📋 Theta sensitivity table  (γ fixed at {risk_aversion})")
table_indices = np.linspace(0, len(theta_range)-1, 9, dtype=int)
table_rows = []
for idx in table_indices:
    t_val = theta_range[idx]
    marker = " ← your θ" if abs(t_val - theta) < 0.25 else ""
    table_rows.append({
        "θ":                        f"{t_val:.2f}{marker}",
        f"Weight in {asset1_name}": f"{sa_weights[idx]:.1f}%",
        "Portfolio ESG":            f"{sa_esg[idx]:.1f}",
        "ESG Class":                classify_esg(sa_esg[idx]),
        "Sharpe":                   f"{sa_sharpes[idx]:.3f}"
    })
st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

# Sensitivity plots
fig_sa, axes = plt.subplots(2, 2, figsize=(14, 10))
fig_sa.patch.set_facecolor('#f4f1eb')
for row in axes:
    for ax in row:
        ax.set_facecolor('#f9f7f2')
        for spine in ax.spines.values():
            spine.set_edgecolor('#c8dfc0')
            spine.set_linewidth(0.8)
        ax.tick_params(colors='#5a6e55')
fig_sa.suptitle("ESGenie — Sensitivity Analysis", fontsize=13, fontweight='bold', color='#2d5016')

ax = axes[0, 0]
ax.plot(theta_range, sa_weights, color='#4a7c59', linewidth=2)
ax.axvline(x=theta, color='#2d5016', linestyle='--', linewidth=1, alpha=0.7, label=f"Your θ = {theta}")
ax.axhline(y=sa_weights[np.argmin(np.abs(theta_range - theta))],
           color='#c8dfc0', linestyle=':', linewidth=1, alpha=0.8)
ax.set_xlabel("ESG Preference (θ)", color='#5a6e55')
ax.set_ylabel(f"Weight in {asset1_name} (%)", color='#5a6e55')
ax.set_title(f"Allocation vs ESG Preference  (γ = {risk_aversion})", color='#2d5016', fontweight='bold')
ax.legend(fontsize=8); ax.grid(True, alpha=0.25, color='#c8dfc0'); ax.set_xlim(0, 4)

ax = axes[0, 1]
ax.plot(theta_range, sa_esg, color='#6a9e76', linewidth=2)
ax.axvline(x=theta, color='#2d5016', linestyle='--', linewidth=1, alpha=0.7, label=f"Your θ = {theta}")
ax.axhspan(80, 100, alpha=0.08, color='green',  label='High ESG (≥80)')
ax.axhspan(50,  80, alpha=0.08, color='yellow', label='Moderate ESG (50–80)')
ax.axhspan(0,   50, alpha=0.08, color='red',    label='Low ESG (<50)')
ax.set_xlabel("ESG Preference (θ)", color='#5a6e55')
ax.set_ylabel("Portfolio ESG Score", color='#5a6e55')
ax.set_title(f"ESG Score vs ESG Preference  (γ = {risk_aversion})", color='#2d5016', fontweight='bold')
ax.legend(fontsize=7); ax.grid(True, alpha=0.25, color='#c8dfc0')
ax.set_xlim(0, 4); ax.set_ylim(0, 100)

ax = axes[1, 0]
ax.plot(gamma_range, sg_sharpes, color='#4a7c59', linewidth=2, label='Sharpe ratio')
ax.axvline(x=risk_aversion, color='#2d5016', linestyle='--', linewidth=1, alpha=0.7,
           label=f"Your γ = {risk_aversion}")
ax.set_xlabel("Risk Aversion (γ)", color='#5a6e55')
ax.set_ylabel("Portfolio Sharpe Ratio", color='#5a6e55')
ax.set_title(f"Sharpe Ratio vs Risk Aversion  (θ = {theta})", color='#2d5016', fontweight='bold')
ax.legend(fontsize=8); ax.grid(True, alpha=0.25, color='#c8dfc0')

ax = axes[1, 1]
im = ax.imshow(heatmap, aspect='auto', origin='lower', cmap='RdYlGn',
               vmin=0, vmax=100,
               extent=[theta_grid[0], theta_grid[-1],
                       gamma_grid[0], gamma_grid[-1]])
plt.colorbar(im, ax=ax, label='Portfolio ESG Score')
ax.scatter(theta, risk_aversion, marker='*', color='#2d5016', s=220, zorder=5, label='Your profile')
ax.set_xlabel("ESG Preference (θ)", color='#5a6e55')
ax.set_ylabel("Risk Aversion (γ)", color='#5a6e55')
ax.set_title("ESG Score across Parameter Space", color='#2d5016', fontweight='bold')
ax.legend(fontsize=8, loc='upper left')

plt.tight_layout()
st.pyplot(fig_sa)
plt.close()

st.markdown("---")
st.caption("ESGenie🧞 — built with Streamlit · Sustainable Finance App")
