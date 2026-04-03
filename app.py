# esgenie_app.py
# ESGenie🧞 — Sustainable Portfolio Advisor  (redesigned)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESGenie",
    page_icon="🧞",
    layout="wide"
)

# ── Custom CSS theme ──────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Page background ── */
.stApp {
    background: linear-gradient(135deg, #0d1b2a 0%, #112233 60%, #0a2818 100%);
    color: #e8f5e9;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(120deg, #1a3a2a 0%, #0f2d1f 50%, #162d3a 100%);
    border: 1px solid #2e6b4a;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #a8e6c1;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 1rem;
    color: #7abf99;
    margin: 0.3rem 0 0 0;
    font-weight: 400;
}
.hero-badge {
    background: #2e6b4a;
    color: #a8e6c1;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    display: inline-block;
    margin-top: 0.5rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(145deg, #1a3a2a, #152d22);
    border: 1px solid #2e6b4a;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    height: 100%;
}
.metric-card-label {
    font-size: 0.75rem;
    color: #7abf99;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 0.4rem;
}
.metric-card-value {
    font-size: 1.7rem;
    font-weight: 700;
    color: #c8f0d8;
    line-height: 1.1;
}
.metric-card-delta {
    font-size: 0.78rem;
    color: #7abf99;
    margin-top: 0.3rem;
}

/* ── Section headers ── */
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #a8e6c1;
    border-left: 4px solid #3dba72;
    padding-left: 0.7rem;
    margin: 1.5rem 0 0.8rem 0;
}

/* ── Recommendation box ── */
.reco-box {
    background: linear-gradient(135deg, #1a3a2a, #0f2d1f);
    border: 1px solid #3dba72;
    border-left: 5px solid #3dba72;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    color: #c8f0d8;
    font-size: 0.96rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(61,186,114,0.1);
}

/* ── Info / warning ── */
.custom-info {
    background: rgba(29, 96, 153, 0.15);
    border: 1px solid #1d6099;
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    color: #93c8e8;
    font-size: 0.92rem;
}
.custom-warning {
    background: rgba(180, 120, 20, 0.15);
    border: 1px solid #b47814;
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    color: #f0d080;
    font-size: 0.92rem;
}

/* ── Tab styling ── */
[data-testid="stTabs"] [role="tab"] {
    color: #7abf99 !important;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.5rem 1.2rem;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #a8e6c1 !important;
    border-bottom: 3px solid #3dba72 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2318 0%, #0d1b2a 100%) !important;
    border-right: 1px solid #2e6b4a;
}
[data-testid="stSidebar"] * {
    color: #c8e6d4 !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stThumb"] {
    background-color: #3dba72 !important;
}

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2e8b57, #1e6b3e) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    padding: 0.6rem 1.2rem !important;
    box-shadow: 0 3px 14px rgba(46,139,87,0.35) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #3dba72, #2e8b57) !important;
    box-shadow: 0 5px 20px rgba(61,186,114,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #2e6b4a !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 1px solid #2e6b4a !important;
    margin: 1.5rem 0 !important;
}

/* ── Preset card ── */
.preset-card {
    background: #1a2e20;
    border: 1px solid #2e6b4a;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    font-size: 0.82rem;
    color: #a8e6c1;
    cursor: pointer;
    text-align: center;
}

/* ── Step card ── */
.step-card {
    background: linear-gradient(145deg, #1a3a2a, #152d22);
    border: 1px solid #2e6b4a;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}
.step-number {
    font-size: 2rem;
    font-weight: 700;
    color: #3dba72;
}
.step-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #a8e6c1;
    margin: 0.3rem 0;
}
.step-desc {
    font-size: 0.8rem;
    color: #7abf99;
}

/* ── ESG pill ── */
.esg-high   { background:#1a4d2a; color:#6fcf8a; border:1px solid #3dba72;
               border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.esg-mid    { background:#3d3010; color:#f0c060; border:1px solid #b47814;
               border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.esg-low    { background:#3d1010; color:#f08080; border:1px solid #b43030;
               border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:600; }

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1a4d6b, #0f3347) !important;
    border: 1px solid #1d6099 !important;
    color: #93c8e8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
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

def esg_pill(score):
    if score >= 80:
        return f'<span class="esg-high">🌿 High ESG {score:.0f}</span>'
    elif score >= 50:
        return f'<span class="esg-mid">⚡ Moderate ESG {score:.0f}</span>'
    else:
        return f'<span class="esg-low">⚠️ Low ESG {score:.0f}</span>'

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

# ── Matplotlib dark theme ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0f1f17",
    "axes.facecolor":    "#111f18",
    "axes.edgecolor":    "#2e6b4a",
    "axes.labelcolor":   "#a8e6c1",
    "axes.titlecolor":   "#c8f0d8",
    "xtick.color":       "#7abf99",
    "ytick.color":       "#7abf99",
    "grid.color":        "#1e4030",
    "text.color":        "#c8f0d8",
    "legend.facecolor":  "#0f1f17",
    "legend.edgecolor":  "#2e6b4a",
    "legend.labelcolor": "#a8e6c1",
})

# ── Hero header ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div style="font-size:3.5rem; line-height:1;">🧞</div>
  <div>
    <p class="hero-title">ESGenie</p>
    <p class="hero-subtitle">Your personalised sustainable investment portfolio advisor</p>
    <span class="hero-badge">🌿 Sustainable Finance · ESG Optimisation · Retail Investing</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Investor preset profiles ──────────────────────────────────────────
PRESETS = {
    "🌿 Eco-First":         dict(r_h=8,  sd_h=22, r_f=4,  sd_f=10, rho=0.15, rfree=2.0, risk=2,  theta=3.8, focus_idx=0, threshold=60),
    "⚖️ Balanced":          dict(r_h=8,  sd_h=20, r_f=4,  sd_f=10, rho=0.20, rfree=2.0, risk=1,  theta=2.0, focus_idx=3, threshold=0),
    "🛡️ Conservative Green": dict(r_h=6,  sd_h=14, r_f=3,  sd_f=7,  rho=0.10, rfree=2.0, risk=0,  theta=2.5, focus_idx=3, threshold=50),
    "🚀 Growth Hunter":      dict(r_h=14, sd_h=30, r_f=5,  sd_f=12, rho=0.25, rfree=2.0, risk=2,  theta=0.5, focus_idx=3, threshold=0),
    "🤝 Social Impact":      dict(r_h=7,  sd_h=18, r_f=4,  sd_f=9,  rho=0.18, rfree=2.0, risk=1,  theta=3.0, focus_idx=1, threshold=55),
}

# ── Session state for presets ─────────────────────────────────────────
if "preset" not in st.session_state:
    st.session_state.preset = None

# ── Sidebar inputs ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧞 ESGenie Inputs")
    st.caption("Complete all sections, then click **Run ESGenie**.")

    # ── Investor Presets ──────────────────────────────────────────────
    with st.expander("⚡ Quick-Start Presets", expanded=True):
        st.caption("Load a pre-built investor profile:")
        for pname in PRESETS:
            if st.button(pname, key=f"preset_{pname}", use_container_width=True):
                st.session_state.preset = pname

    active = PRESETS.get(st.session_state.preset, {})

    # ── Financial data ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 💰 Financial Data")

    asset1_name = st.text_input("Asset 1 name", value="Asset 1")
    r_h  = st.slider("Asset 1 expected return (%)", -50, 50, active.get("r_h", 8))  / 100
    sd_h = st.slider("Asset 1 standard deviation (%)", 0, 100, active.get("sd_h", 20)) / 100

    asset2_name = st.text_input("Asset 2 name", value="Asset 2")
    r_f  = st.slider("Asset 2 expected return (%)", -50, 50, active.get("r_f", 4))  / 100
    sd_f = st.slider("Asset 2 standard deviation (%)", 0, 100, active.get("sd_f", 10)) / 100

    rho_hf = st.slider("Correlation between assets", -1.0, 1.0,
                        active.get("rho", 0.2), step=0.01)
    r_free = st.slider("Risk-free rate (%)", 0.0, 10.0,
                        active.get("rfree", 2.0), step=0.1) / 100

    # ── Risk profile ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ⚖️ Risk Profile")
    risk_options = ["🛡️ Conservative", "⚖️ Balanced", "🚀 Aggressive"]
    risk_choice = st.radio(
        "Your attitude to investment risk:",
        options=risk_options,
        index=active.get("risk", 1)
    )
    risk_map = {
        "🛡️ Conservative": (10, "Conservative"),
        "⚖️ Balanced":     (5,  "Balanced"),
        "🚀 Aggressive":   (2,  "Aggressive")
    }
    risk_aversion, risk_label = risk_map[risk_choice]

    # ── ESG preferences ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌱 ESG Preferences")
    theta = st.slider(
        "ESG importance (θ)  —  0 = financial only, 4 = ESG first",
        0.0, 4.0, active.get("theta", 2.0), step=0.1
    )

    focus_options = [
        "🌍 Environmental focus  (E=0.60, S=0.20, G=0.20)",
        "🤝 Social focus         (E=0.20, S=0.60, G=0.20)",
        "🏛️ Governance focus     (E=0.20, S=0.20, G=0.60)",
        "⚖️ Balanced ESG         (E=0.34, S=0.33, G=0.33)",
        "✏️ Custom weights"
    ]
    esg_focus = st.selectbox(
        "ESG pillar focus:",
        options=focus_options,
        index=active.get("focus_idx", 3)
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
    st.markdown("---")
    st.markdown("### 📊 Asset ESG Scores")
    st.caption("Scores from 0 (worst) to 100 (best)")

    sector_options = ["Technology", "Healthcare", "Financial Services",
                      "Consumer Goods", "Energy", "Tobacco",
                      "Weapons & Defence", "Gambling", "Other"]

    with st.expander(f"📋 ESG scores for {asset1_name}"):
        sector1 = st.selectbox(f"{asset1_name} sector", sector_options, key="s1")
        E1 = st.slider(f"{asset1_name} — Environmental (E)", 0, 100, 60, key="e1")
        S1 = st.slider(f"{asset1_name} — Social (S)",        0, 100, 60, key="s1s")
        G1 = st.slider(f"{asset1_name} — Governance (G)",    0, 100, 60, key="g1")

    with st.expander(f"📋 ESG scores for {asset2_name}"):
        sector2 = st.selectbox(f"{asset2_name} sector", sector_options, key="s2")
        E2 = st.slider(f"{asset2_name} — Environmental (E)", 0, 100, 40, key="e2")
        S2 = st.slider(f"{asset2_name} — Social (S)",        0, 100, 40, key="s2s")
        G2 = st.slider(f"{asset2_name} — Governance (G)",    0, 100, 40, key="g2")

    # ── Ethical screening ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🛡️ Ethical Screening")

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
        0, 100, active.get("threshold", 0)
    )
    apply_threshold  = threshold > 0
    penalty_strength = 0.01 * theta

    # ── Run button ────────────────────────────────────────────────────
    st.markdown("---")
    run = st.button("✨ Run ESGenie", type="primary", use_container_width=True)

# ── Landing screen ────────────────────────────────────────────────────
if not run:
    col1, col2, col3 = st.columns(3)
    cards = [
        ("01", "Set Your Profile", "Fill in risk, ESG preferences & asset data in the sidebar"),
        ("02", "Run ESGenie", "Click the green button to optimise your portfolio"),
        ("03", "Explore Results", "Review allocation, charts & sensitivity analysis"),
    ]
    for col, (num, title, desc) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
            <div class="step-card">
              <div class="step-number">{num}</div>
              <div class="step-title">{title}</div>
              <div class="step-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-info">
    👈 &nbsp; Fill in your inputs in the sidebar, then click <strong>✨ Run ESGenie</strong> to see your personalised portfolio.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Guards ────────────────────────────────────────────────────────────
if "✏️ Custom weights" in esg_focus and abs(w_e + w_s + w_g - 1.0) > 0.01:
    st.error("❌ Custom ESG weights must sum to 1.0. Please adjust in the sidebar.")
    st.stop()

if sin_choice == 1 and len(excluded) == 2:
    st.error("❌ Both assets are in restricted sectors and have been excluded. No valid portfolio can be constructed.")
    st.stop()

# ── Compute ESG scores ────────────────────────────────────────────────
esg_h = compute_esg(E1, S1, G1, w_e, w_s, w_g)
esg_f = compute_esg(E2, S2, G2, w_e, w_s, w_g)

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

# ── Investor profile strip ────────────────────────────────────────────
st.markdown('<div class="section-header">👤 Investor Profile</div>', unsafe_allow_html=True)

if theta <= 1:
    esg_importance_label = "Low ESG preference"
elif theta <= 2.5:
    esg_importance_label = "Moderate ESG preference"
else:
    esg_importance_label = "High ESG preference"

c1, c2, c3, c4 = st.columns(4)
for col, label, value, delta in [
    (c1, "Risk Profile",    risk_label,              f"γ = {risk_aversion}"),
    (c2, "ESG Importance",  esg_importance_label,    f"θ = {theta}"),
    (c3, "ESG Focus",       esg_focus_label,         ""),
    (c4, "Min ESG Target",  f"{threshold}" if threshold > 0 else "None", "threshold"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-card-label">{label}</div>
          <div class="metric-card-value" style="font-size:1.15rem;">{value}</div>
          <div class="metric-card-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ESG score summary strip ───────────────────────────────────────────
st.markdown('<div class="section-header">🌱 ESG Score Summary</div>', unsafe_allow_html=True)

ca, cb = st.columns(2)
for col, aname, sector, esg_score, E, S, G in [
    (ca, asset1_name, sector1, esg_h, E1, S1, G1),
    (cb, asset2_name, sector2, esg_f, E2, S2, G2),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card" style="text-align:left; padding:1.2rem 1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
            <span style="font-size:1rem; font-weight:700; color:#c8f0d8;">{aname}</span>
            {esg_pill(esg_score)}
          </div>
          <div style="font-size:0.78rem; color:#7abf99; margin-bottom:0.4rem;">{sector}</div>
          <div style="font-size:0.82rem; color:#a8e6c1; margin-top:0.5rem;">
            🌿 E = {E} &nbsp;|&nbsp; 🤝 S = {S} &nbsp;|&nbsp; 🏛️ G = {G}
          </div>
          <div style="font-size:0.75rem; color:#5a9b78; margin-top:0.3rem;">
            Weights: E×{w_e:.2f} + S×{w_s:.2f} + G×{w_g:.2f}
          </div>
        </div>
        """, unsafe_allow_html=True)

if apply_threshold:
    if esg_h < threshold:
        st.warning(f"⚠️ {asset1_name} ESG score ({esg_h:.1f}) is below your threshold of {threshold}.")
    if esg_f < threshold:
        st.warning(f"⚠️ {asset2_name} ESG score ({esg_f:.1f}) is below your threshold of {threshold}.")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Recommendation", "📈 Charts", "🔬 Sensitivity Analysis"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — Portfolio Recommendation
# ════════════════════════════════════════════════════════════════════
with tab1:

    # ── Key metrics ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">📐 Recommended Portfolio Metrics</div>',
                unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    metric_data = [
        (m1, "Expected Return",   f"{res['ret_optimal']*100:.2f}%",  "annualised"),
        (m2, "Risk (Std Dev)",    f"{res['sd_optimal']*100:.2f}%",   "annualised"),
        (m3, "Sharpe Ratio",      f"{res['sr_optimal']:.3f}",        "risk-adjusted"),
        (m4, "ESG Score",         f"{res['esg_optimal']:.1f} / 100", classify_esg(res['esg_optimal'])),
        (m5, "ESG Premium",       f"{esg_premium:+.3f}",             "vs tangency Sharpe"),
    ]
    for col, label, value, delta in metric_data:
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-card-label">{label}</div>
              <div class="metric-card-value">{value}</div>
              <div class="metric-card-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Asset allocation ──────────────────────────────────────────────
    st.markdown('<div class="section-header">💼 Asset Allocation</div>', unsafe_allow_html=True)

    alloc_df = pd.DataFrame({
        "Asset":       [asset1_name, asset2_name, "Portfolio (weighted)"],
        "Weight":      [f"{w1_optimal*100:.1f}%", f"{w2_optimal*100:.1f}%", "100.0%"],
        "ESG Score":   [f"{esg_h:.1f}", f"{esg_f:.1f}", f"{res['esg_optimal']:.1f}"],
        "ESG Class":   [classify_esg(esg_h), classify_esg(esg_f), classify_esg(res['esg_optimal'])]
    })
    st.dataframe(alloc_df, use_container_width=True, hide_index=True)

    # ── Portfolio comparison ──────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Portfolio Comparison</div>', unsafe_allow_html=True)
    st.caption("See how your ESG-optimal portfolio compares to the pure financial alternatives.")

    chars_df = pd.DataFrame({
        "Metric":         ["Expected Return", "Risk (Std Dev)", "Sharpe Ratio", "ESG Score", "ESG Class"],
        "🟢 Recommended": [
            f"{res['ret_optimal']*100:.2f}%",
            f"{res['sd_optimal']*100:.2f}%",
            f"{res['sr_optimal']:.3f}",
            f"{res['esg_optimal']:.1f}",
            classify_esg(res['esg_optimal'])
        ],
        "📐 Tangency (Max Sharpe)": [
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

    if esg_premium > 0:
        st.markdown(f"""
        <div class="custom-warning">
        📉 <strong>ESG Premium:</strong> {esg_premium:+.3f} Sharpe points — your ESG preferences
        reduce risk-adjusted return relative to the purely financial tangency portfolio.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="reco-box">
        📈 <strong>ESG Premium:</strong> {esg_premium:+.3f} Sharpe points — your ESG preferences
        align with financial performance. No sacrifice in risk-adjusted return detected.
        </div>
        """, unsafe_allow_html=True)

    # ── Recommendation narrative ──────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💬 Why This Portfolio?</div>', unsafe_allow_html=True)

    dominant_asset  = asset1_name if w1_optimal >= w2_optimal else asset2_name
    secondary_asset = asset2_name if w1_optimal >= w2_optimal else asset1_name
    dominant_esg    = esg_h       if w1_optimal >= w2_optimal else esg_f
    secondary_esg   = esg_f       if w1_optimal >= w2_optimal else esg_h
    esg_driver      = dominant_esg > secondary_esg

    esg_driver_text = (
        f"The tilt toward <strong>{dominant_asset}</strong> is partly driven by its stronger ESG score "
        f"({dominant_esg:.1f} vs {secondary_esg:.1f}), consistent with your {esg_focus_label.lower()} "
        f"and ESG importance of θ={theta}."
    ) if esg_driver else (
        f"The tilt toward <strong>{dominant_asset}</strong> is driven primarily by its superior "
        f"risk-return profile rather than ESG performance."
    )

    st.markdown(f"""
    <div class="reco-box">
    Based on your <strong>{risk_label.lower()} risk profile</strong> (γ={risk_aversion}) and
    <strong>{esg_importance_label.lower()}</strong> (θ={theta}), ESGenie recommends allocating
    <strong>{w1_optimal*100:.1f}% to {asset1_name}</strong> and
    <strong>{w2_optimal*100:.1f}% to {asset2_name}</strong>.<br><br>
    {esg_driver_text}
    </div>
    """, unsafe_allow_html=True)

    if apply_threshold and (esg_h < threshold or esg_f < threshold):
        st.warning(f"One or more assets fell below your minimum ESG threshold of {threshold}. A utility penalty was applied.")

    if sin_choice == 1 and excluded:
        for name, sec in excluded.items():
            st.error(f"**{name}** ({sec}) was excluded from the portfolio per your ethical screening preferences.")

    # ── Download summary ──────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    summary_text = (
        f"ESGenie Portfolio Summary\n"
        f"==========================\n"
        f"Risk Profile: {risk_label}  (γ={risk_aversion})\n"
        f"ESG Importance: θ={theta}  ({esg_importance_label})\n"
        f"ESG Focus: {esg_focus_label}\n\n"
        f"Recommended Allocation\n"
        f"  {asset1_name}: {w1_optimal*100:.1f}%\n"
        f"  {asset2_name}: {w2_optimal*100:.1f}%\n\n"
        f"Portfolio Metrics\n"
        f"  Expected Return : {res['ret_optimal']*100:.2f}%\n"
        f"  Risk (Std Dev)  : {res['sd_optimal']*100:.2f}%\n"
        f"  Sharpe Ratio    : {res['sr_optimal']:.3f}\n"
        f"  ESG Score       : {res['esg_optimal']:.1f} / 100  ({classify_esg(res['esg_optimal'])})\n"
        f"  ESG Premium     : {esg_premium:+.3f} vs tangency Sharpe\n"
    )
    st.download_button(
        label="⬇️ Download Portfolio Summary",
        data=summary_text,
        file_name="esgenie_portfolio_summary.txt",
        mime="text/plain"
    )

# ════════════════════════════════════════════════════════════════════
# TAB 2 — Charts
# ════════════════════════════════════════════════════════════════════
with tab2:

    st.markdown('<div class="section-header">📈 ESG-Efficient Frontier & Utility</div>',
                unsafe_allow_html=True)

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
    fig.patch.set_facecolor("#0f1f17")
    fig.suptitle("ESGenie — Portfolio Analysis", fontsize=14, fontweight='bold', color="#c8f0d8")

    # Left: ESG-efficient frontier
    sc = ax1.scatter(risk_plot, ret_plot, c=esg_plot, cmap='RdYlGn', s=10, zorder=2, alpha=0.85)
    cbar = plt.colorbar(sc, ax=ax1)
    cbar.set_label('Portfolio ESG Score', color="#a8e6c1")
    cbar.ax.yaxis.set_tick_params(color="#7abf99")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#7abf99")

    cml_x     = np.linspace(0, max(risk_plot) * 1.2, 100)
    cml_slope = (res['ret_tangency'] - r_free) / res['sd_tangency']
    ax1.plot(cml_x, r_free + cml_slope * cml_x,
             linestyle='--', color='#5bc8f5', linewidth=1.5, label='Capital Market Line', alpha=0.8)
    ax1.scatter(0, r_free, marker='D', color='#5bc8f5', s=70, zorder=5,
                label=f'Risk-Free ({r_free*100:.1f}%)')
    ax1.scatter(res['sd_min_var'], res['ret_min_var'],
                marker='s', color='#bf7fff', s=110, zorder=5,
                label=f"Min Variance ({w1_min_var*100:.0f}% {asset1_name})")
    ax1.scatter(res['sd_tangency'], res['ret_tangency'],
                marker='^', color='#5bc8f5', s=130, zorder=5,
                label=f"Tangency ({w1_tangency*100:.0f}% {asset1_name})")
    ax1.scatter(res['sd_optimal'], res['ret_optimal'],
                marker='*', color='#3dba72', s=280, zorder=6,
                label=f"✨ Recommended ({w1_optimal*100:.0f}% {asset1_name})")

    for xy, label, color in [
        ((res['sd_min_var'],  res['ret_min_var']),  'Min Variance', '#bf7fff'),
        ((res['sd_tangency'], res['ret_tangency']),  'Tangency',     '#5bc8f5'),
        ((res['sd_optimal'],  res['ret_optimal']),   'Recommended',  '#3dba72'),
    ]:
        ax1.annotate(label, xy=xy, xytext=(10, 5),
                     textcoords='offset points', fontsize=8, color=color,
                     fontweight='bold')

    ax1.set_xlabel('Risk (Standard Deviation)')
    ax1.set_ylabel('Expected Return')
    ax1.set_title('ESG-Efficient Frontier')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.25)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.1f}%'))
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.1f}%'))

    # Right: Utility vs weight
    ax2.plot(weights_plot * 100, util_plot, color='#3dba72', linewidth=2.5, label='Utility U(w)')
    ax2.fill_between(weights_plot * 100, util_plot, alpha=0.08, color='#3dba72')
    ax2.axvline(x=w1_optimal*100, color='#3dba72', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.scatter(w1_optimal*100, utility(
        w1_optimal, r_h, r_f, sd_h, sd_f, rho_hf, r_free,
        risk_aversion, theta, esg_h, esg_f,
        sin_choice, excluded, asset1_name, asset2_name,
        apply_threshold, threshold, penalty_strength),
        marker='*', color='#3dba72', s=250, zorder=5,
        label=f'✨ Optimal: {w1_optimal*100:.1f}%')
    ax2.axvline(x=w1_tangency*100, color='#5bc8f5', linestyle=':', linewidth=1.5, alpha=0.8,
                label=f'Tangency: {w1_tangency*100:.1f}%')
    ax2.set_xlabel(f'Weight in {asset1_name} (%)')
    ax2.set_ylabel('Utility')
    ax2.set_title('Utility Function vs Portfolio Weight')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ════════════════════════════════════════════════════════════════════
# TAB 3 — Sensitivity Analysis
# ════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown('<div class="section-header">🔬 Sensitivity Analysis</div>', unsafe_allow_html=True)

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
    st.markdown(f'<div class="section-header">📋 θ Sensitivity Table  (γ fixed at {risk_aversion})</div>',
                unsafe_allow_html=True)
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
    fig_sa.patch.set_facecolor("#0f1f17")
    fig_sa.suptitle("ESGenie — Sensitivity Analysis", fontsize=13,
                    fontweight='bold', color="#c8f0d8")

    ax = axes[0, 0]
    ax.plot(theta_range, sa_weights, color='#3dba72', linewidth=2.5)
    ax.fill_between(theta_range, sa_weights, alpha=0.07, color='#3dba72')
    ax.axvline(x=theta, color='#a8e6c1', linestyle='--', linewidth=1.5, alpha=0.8,
               label=f"Your θ = {theta}")
    ax.axhline(y=sa_weights[np.argmin(np.abs(theta_range - theta))],
               color='#7abf99', linestyle=':', linewidth=1, alpha=0.5)
    ax.set_xlabel("ESG Preference (θ)")
    ax.set_ylabel(f"Weight in {asset1_name} (%)")
    ax.set_title(f"Allocation vs ESG Preference  (γ = {risk_aversion})")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.2); ax.set_xlim(0, 4)

    ax = axes[0, 1]
    ax.plot(theta_range, sa_esg, color='#6fcf8a', linewidth=2.5)
    ax.fill_between(theta_range, sa_esg, alpha=0.07, color='#6fcf8a')
    ax.axvline(x=theta, color='#a8e6c1', linestyle='--', linewidth=1.5, alpha=0.8,
               label=f"Your θ = {theta}")
    ax.axhspan(80, 100, alpha=0.06, color='#3dba72',  label='High ESG (≥80)')
    ax.axhspan(50,  80, alpha=0.06, color='#f0c060', label='Moderate ESG (50–80)')
    ax.axhspan(0,   50, alpha=0.06, color='#e05050',    label='Low ESG (<50)')
    ax.set_xlabel("ESG Preference (θ)")
    ax.set_ylabel("Portfolio ESG Score")
    ax.set_title(f"ESG Score vs ESG Preference  (γ = {risk_aversion})")
    ax.legend(fontsize=7); ax.grid(True, alpha=0.2)
    ax.set_xlim(0, 4); ax.set_ylim(0, 100)

    ax = axes[1, 0]
    ax.plot(gamma_range, sg_sharpes, color='#5bc8f5', linewidth=2.5, label='Sharpe ratio')
    ax.fill_between(gamma_range, sg_sharpes, alpha=0.07, color='#5bc8f5')
    ax.axvline(x=risk_aversion, color='#a8e6c1', linestyle='--', linewidth=1.5, alpha=0.8,
               label=f"Your γ = {risk_aversion}")
    ax.set_xlabel("Risk Aversion (γ)")
    ax.set_ylabel("Portfolio Sharpe Ratio")
    ax.set_title(f"Sharpe Ratio vs Risk Aversion  (θ = {theta})")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.2)

    ax = axes[1, 1]
    im = ax.imshow(heatmap, aspect='auto', origin='lower', cmap='RdYlGn',
                   vmin=0, vmax=100,
                   extent=[theta_grid[0], theta_grid[-1],
                           gamma_grid[0], gamma_grid[-1]])
    cbar2 = plt.colorbar(im, ax=ax)
    cbar2.set_label('Portfolio ESG Score', color="#a8e6c1")
    cbar2.ax.yaxis.set_tick_params(color="#7abf99")
    plt.setp(cbar2.ax.yaxis.get_ticklabels(), color="#7abf99")
    ax.scatter(theta, risk_aversion, marker='*', color='white', s=250, zorder=5,
               label='✨ Your profile')
    ax.set_xlabel("ESG Preference (θ)")
    ax.set_ylabel("Risk Aversion (γ)")
    ax.set_title("ESG Score across Parameter Space")
    ax.legend(fontsize=8, loc='upper left')

    plt.tight_layout()
    st.pyplot(fig_sa)
    plt.close()

# ── Footer ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:1rem; color:#3d7a56; font-size:0.78rem; 
            border-top:1px solid #2e6b4a; margin-top:1rem;">
  ESGenie 🧞 &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Sustainable Finance App
  &nbsp;·&nbsp; <span style="color:#2e6b4a;">🌿 Invest responsibly</span>
</div>
""", unsafe_allow_html=True)
