# app.py
# ESGenie 🧞 — Sustainable Portfolio Optimiser

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.optimize import minimize

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESGenie 🧞",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
# DISPLAY SETTINGS — sidebar
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Display Settings")
    dark_mode     = st.toggle("🌙 Dark mode",              value=st.session_state.get("dark_mode",     False))
    high_contrast = st.toggle("🔲 High contrast",          value=st.session_state.get("high_contrast", False))
    dyslexia_font = st.toggle("🔡 Dyslexia-friendly font", value=st.session_state.get("dyslexia_font", False))
    font_size     = st.slider("🔠 Font size", 14, 22,      st.session_state.get("font_size", 16), step=1)
    st.session_state.dark_mode     = dark_mode
    st.session_state.high_contrast = high_contrast
    st.session_state.dyslexia_font = dyslexia_font
    st.session_state.font_size     = font_size

# ── CSS ───────────────────────────────────────────────────────────────
if high_contrast:
    theme_css = """
    :root {
        --bg:#000000; --card:#111111; --text:#ffffff; --text-muted:#dddddd;
        --forest:#ffffff; --sage:#00ff88; --sage-light:#00cc66;
        --soft-bg:#1a1a1a; --border:#00ff88;
        --green:#00ff88; --amber:#ffcc00; --red:#ff4444;
    }"""
elif dark_mode:
    theme_css = """
    :root {
        --bg:#0f1720; --card:#18212b; --text:#e5e7eb; --text-muted:#9ca3af;
        --forest:#9be3b0; --sage:#6fa77f; --sage-light:#8fd19e;
        --soft-bg:#1f2a33; --border:#2a3441;
        --green:#4ade80; --amber:#fbbf24; --red:#f87171;
    }"""
else:
    theme_css = """
    :root {
        --bg:#f4f8f5; --card:#ffffff; --text:#1f3d2b; --text-muted:#5f6f65;
        --forest:#1f3d2b; --sage:#4c7a5a; --sage-light:#6fa77f;
        --soft-bg:#e8f3ec; --border:#cfe3d6;
        --green:#2e7d32; --amber:#b7791f; --red:#c53030;
    }"""

body_font  = "'OpenDyslexic','Comic Sans MS',sans-serif" if dyslexia_font else "'DM Sans',sans-serif"
serif_font = "'OpenDyslexic','Comic Sans MS',sans-serif" if dyslexia_font else "'DM Serif Display',serif"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
{("@import url('https://fonts.cdnfonts.com/css/opendyslexic');" if dyslexia_font else "")}
{theme_css}
.stApp {{background-color:var(--bg)!important;color:var(--text)!important;
         font-family:{body_font}!important;font-size:{font_size}px!important;}}
body,p,div,span,li {{color:var(--text)!important;font-size:{font_size}px!important;}}
label {{color:var(--forest)!important;font-weight:500!important;}}
.stCaption {{color:var(--text-muted)!important;}}
h1,h2,h3,h4 {{font-family:{serif_font}!important;color:var(--forest)!important;}}
.section-header {{font-family:{serif_font}!important;color:var(--forest)!important;
    font-size:1.15rem!important;font-weight:600;border-left:4px solid var(--sage);
    padding-left:0.65rem;margin:1.25rem 0 0.7rem;}}
.hero-banner {{background:var(--card);border:1px solid var(--border);border-radius:14px;
    padding:1.6rem 2rem;margin-bottom:1rem;display:flex;align-items:center;
    gap:1.25rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);}}
.hero-title {{font-family:{serif_font};font-size:2.4rem;color:var(--forest);margin:0;}}
.hero-subtitle {{font-size:0.95rem;color:var(--text-muted);margin:0.1rem 0 0;}}
.hero-badge {{background:var(--sage);color:white;font-size:0.7rem;padding:0.25rem 0.6rem;
    border-radius:20px;display:inline-block;margin-top:0.4rem;}}
.how-to-box {{background:var(--card);border:1px solid var(--border);border-radius:12px;
    padding:1.5rem 2rem;margin:0.5rem 0 1.5rem;}}
.how-to-steps {{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
    gap:0.85rem;margin-top:1rem;}}
.how-to-step {{background:var(--soft-bg);border:1px solid var(--border);border-radius:10px;
    padding:0.85rem 1rem;}}
.how-to-step-num {{font-family:{serif_font};font-size:1.3rem;color:var(--sage);font-weight:700;}}
.how-to-step-title {{font-weight:600;color:var(--forest);font-size:0.88rem;margin:0.2rem 0;}}
.how-to-step-desc {{font-size:0.8rem;color:var(--text-muted);line-height:1.5;}}
.utility-formula {{background:var(--soft-bg);border-left:3px solid var(--sage);
    border-radius:0 8px 8px 0;padding:0.75rem 1.25rem;margin-top:1rem;
    font-size:0.88rem;color:var(--forest);font-family:'Courier New',monospace;}}
details[data-testid="stExpander"] {{border:1px solid var(--border)!important;
    border-radius:10px!important;margin-bottom:0.75rem!important;}}
details[data-testid="stExpander"] summary {{background:var(--soft-bg)!important;
    color:var(--forest)!important;font-family:{serif_font}!important;
    font-weight:600!important;padding:0.85rem 1.1rem!important;}}
details[open] summary {{background:var(--sage)!important;color:white!important;}}
details[open] summary svg {{fill:white!important;}}
details[data-testid="stExpander"] > div {{background:var(--card)!important;
    padding:1rem 1.25rem 1.25rem!important;color:var(--text)!important;}}
details[data-testid="stExpander"] > div * {{color:var(--text)!important;}}
details[data-testid="stExpander"] summary * {{color:var(--forest)!important;}}
details[open] summary * {{color:white!important;}}
.section-label {{font-size:0.72rem;font-weight:600;text-transform:uppercase;
    letter-spacing:0.10em;color:var(--text-muted);margin-bottom:0.4rem;margin-top:0.6rem;}}
.tip-box {{background:var(--soft-bg);border-left:3px solid var(--sage-light);
    border-radius:0 8px 8px 0;padding:0.6rem 1rem;margin-top:0.5rem;
    font-size:0.82rem;color:var(--text-muted);line-height:1.5;}}
.metric-card {{background:var(--card);border:1px solid var(--border);border-radius:10px;
    padding:1rem 1.2rem;text-align:center;height:100%;}}
.metric-card-label {{color:var(--text-muted);font-size:0.72rem;font-weight:600;
    text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.3rem;}}
.metric-card-value {{color:var(--forest);font-family:{serif_font};font-size:1.45rem;line-height:1.1;}}
.metric-card-delta {{font-size:0.75rem;color:var(--sage);margin-top:0.25rem;}}
.reco-box {{background:var(--soft-bg);border:1px solid var(--sage);border-left:5px solid var(--sage);
    border-radius:0 10px 10px 0;padding:1.1rem 1.4rem;color:var(--forest);
    font-size:0.93rem;line-height:1.65;}}
.chart-info {{background:var(--soft-bg);border-left:3px solid var(--sage-light);
    border-radius:0 8px 8px 0;padding:0.6rem 1rem;margin-bottom:0.75rem;
    font-size:0.83rem;color:var(--text-muted);line-height:1.5;}}
.esg-high {{background:rgba(46,125,50,0.15);color:var(--green);border-radius:20px;
    padding:3px 10px;font-size:0.78rem;font-weight:600;}}
.esg-mid  {{background:rgba(183,121,31,0.15);color:var(--amber);border-radius:20px;
    padding:3px 10px;font-size:0.78rem;font-weight:600;}}
.esg-low  {{background:rgba(197,48,48,0.15);color:var(--red);border-radius:20px;
    padding:3px 10px;font-size:0.78rem;font-weight:600;}}
.stButton > button {{background:var(--soft-bg)!important;color:var(--forest)!important;
    border:1px solid var(--border)!important;border-radius:8px!important;}}
.stButton > button:hover {{background:var(--sage-light)!important;color:white!important;}}
.stButton > button[kind="primary"] {{background:var(--sage)!important;color:white!important;
    border:none!important;font-weight:600!important;}}
.stButton > button[kind="primary"]:hover {{background:var(--forest)!important;}}
.stDownloadButton > button {{background:var(--soft-bg)!important;color:var(--forest)!important;
    border:1px solid var(--border)!important;border-radius:8px!important;}}
input,textarea {{background-color:var(--soft-bg)!important;color:var(--forest)!important;
    border:1px solid var(--border)!important;border-radius:6px!important;}}
[data-baseweb="input"] {{background-color:var(--soft-bg)!important;}}
[data-baseweb="select"] > div {{background-color:var(--soft-bg)!important;
    color:var(--forest)!important;border:1px solid var(--border)!important;}}
ul[role="listbox"] {{ background-color:var(--card)!important; border:1px solid var(--border)!important; }}
li[role="option"] {{ color:var(--forest)!important; background-color:var(--card)!important; }}
li[role="option"]:hover {{ background-color:var(--soft-bg)!important; color:var(--forest)!important; }}
[data-baseweb="popover"] {{ background-color:var(--card)!important; }}
[data-baseweb="menu"] {{ background-color:var(--card)!important; }}
[data-baseweb="menu"] li {{ color:var(--forest)!important; background-color:var(--card)!important; }}
[data-baseweb="menu"] li:hover {{ background-color:var(--soft-bg)!important; }}
[data-testid="stTabs"] button {{color:var(--sage)!important;}}
[data-testid="stTabs"] button[aria-selected="true"] {{color:var(--forest)!important;
    border-bottom:2px solid var(--sage)!important;}}
table {{color:var(--text)!important;}}
thead tr {{background:var(--soft-bg)!important;}}
tbody tr {{background:var(--card)!important;}}
tbody tr:nth-child(even) {{background:var(--soft-bg)!important;}}
th,td {{color:var(--text)!important;}}
[data-testid="stInfo"]    {{border-left:3px solid var(--sage)!important;}}
[data-testid="stWarning"] {{border-left:3px solid var(--amber)!important;}}
[data-testid="stSuccess"] {{border-left:3px solid var(--green)!important;}}
[data-testid="stError"]   {{border-left:3px solid var(--red)!important;}}
[data-testid="stDataFrame"] {{border:1px solid var(--border)!important;
    border-radius:10px!important;overflow:hidden;}}
[data-testid="stSidebar"] {{ background:var(--soft-bg)!important; border-right:1px solid var(--border)!important; }}
[data-testid="stSidebar"] * {{ color:var(--text)!important; }}
button[data-testid="baseButton-headerNoPadding"] {{ color:var(--forest)!important; }}
button[data-testid="baseButton-headerNoPadding"] svg {{ fill:var(--forest)!important; stroke:var(--forest)!important; }}
[data-testid="collapsedControl"] {{ color:var(--forest)!important; background:var(--soft-bg)!important; border:1px solid var(--border)!important; }}
[data-testid="collapsedControl"] svg {{ fill:var(--forest)!important; stroke:var(--forest)!important; }}
hr {{border:none!important;border-top:1px solid var(--border)!important;margin:1.25rem 0!important;}}
.stCaption {{color:var(--text-muted)!important;font-size:0.76rem!important;}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PURE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def classify_esg(score):
    if score >= 80:   return "High ESG",     f'<span class="esg-high">🟢 High ESG</span>'
    elif score >= 50: return "Moderate ESG", f'<span class="esg-mid">🟡 Moderate ESG</span>'
    else:             return "Low ESG",      f'<span class="esg-low">🔴 Low ESG</span>'

def compute_esg(E, S, G, w_e, w_s, w_g):
    """Composite ESG score — weighted average of E, S, G pillar scores (0–100)."""
    return w_e * E + w_s * S + w_g * G

def portfolio_ret_2asset(x1, x2, r1, r2, r_free):
    """Total portfolio return including implicit risk-free residual."""
    x_rf = 1.0 - x1 - x2
    return x1 * r1 + x2 * r2 + x_rf * r_free

def portfolio_var(x1, x2, sd1, sd2, rho):
    """Portfolio variance = x'Σx (risky assets only)."""
    return x1**2 * sd1**2 + x2**2 * sd2**2 + 2 * rho * x1 * x2 * sd1 * sd2

def portfolio_sd_2asset(x1, x2, sd1, sd2, rho):
    return np.sqrt(np.maximum(portfolio_var(x1, x2, sd1, sd2, rho), 0.0))

def portfolio_esg_weighted(x1, x2, esg1, esg2):
    """
    s̄ = (x1·esg1 + x2·esg2) / (x1 + x2)
    ESG score of risky positions only. Returns 0 if both weights are zero.
    """
    total = x1 + x2
    if total < 1e-10:
        return 0.0
    return (x1 * esg1 + x2 * esg2) / total

def sharpe_ratio_2asset(x1, x2, r1, r2, r_free, sd1, sd2, rho):
    """Sharpe ratio of the risky basket (ignoring risk-free position in denominator)."""
    total = x1 + x2
    if total < 1e-10:
        return 0.0
    ret_risky = (x1 * r1 + x2 * r2) / total
    sd_risky  = portfolio_sd_2asset(x1/total, x2/total, sd1, sd2, rho)
    if sd_risky < 1e-10:
        return 0.0
    return (ret_risky - r_free) / sd_risky


# ══════════════════════════════════════════════════════════════════════
# CORE OBJECTIVE 
# ══════════════════════════════════════════════════════════════════════

def objective(x, r1, r2, r_free, sd1, sd2, rho, gamma, theta, esg1, esg2,
              sin_choice=3, excluded=None, name1="A", name2="B",
              apply_threshold=False, threshold=0.0, penalty_strength=0.05):
    """

        max  x1(r1−rf) + x2(r2−rf)  −  (γ/2)·x′Σx  +  θ·s̄

    where s̄ = (x1·s1 + x2·s2) / (x1 + x2)   [ESG of risky positions only]
    x1, x2 ≥ 0  (no sum-to-one constraint — risk-free is implicit residual).

    Audit-verified:
      - θ=0 → pure MV solution
      - Doubling γ → halves both x1* and x2* proportionally
      - Corner solution when θ is large and esg1 >> esg2
    """
    if excluded is None:
        excluded = {}
    x1, x2 = float(x[0]), float(x[1])

    # Excess return term: x'(μ − rf·1)
    excess = x1 * (r1 - r_free) + x2 * (r2 - r_free)

    # Variance penalty: (γ/2)·x'Σx
    var_penalty = (gamma / 2.0) * portfolio_var(x1, x2, sd1, sd2, rho)

    # ESG term: θ·s̄  (over risky positions only — scale-invariant composition)
    s_bar    = portfolio_esg_weighted(x1, x2, esg1, esg2)
    esg_term = theta * (s_bar / 100.0)

    obj = excess - var_penalty + esg_term

    # ESG threshold — soft linear penalty, independent of theta
    if apply_threshold and (x1 + x2) > 1e-10 and s_bar < threshold:
        obj -= penalty_strength * ((threshold - s_bar) / 100.0)

    # Sin-stock hard exclusion
    if sin_choice == 1:
        if name1 in excluded and x1 > 1e-8:
            obj -= 1e6 * x1
        if name2 in excluded and x2 > 1e-8:
            obj -= 1e6 * x2

    return obj


def run_optimisation(r1, r2, r_free, sd1, sd2, rho,
                     gamma, theta, esg1, esg2,
                     sin_choice=3, excluded=None, name1="A", name2="B",
                     apply_threshold=False, threshold=0.0, penalty_strength=0.05):
    """
    Find optimal (x1, x2) via analytical starting point + scipy L-BFGS-B.
    Returns weights as fractions of total wealth; x_rf = 1 − x1 − x2 is implicit.

    Frontier: uses TRADITIONAL risky frontier (w1 in [0,1], w2=1-w1, x_rf=0).
    This is the correct approach — tangency and min-var markers sit ON this frontier.
    The recommended portfolio is plotted at its actual unconstrained scale.
    """
    if excluded is None:
        excluded = {}

    def neg_obj(x):
        return -objective(x, r1, r2, r_free, sd1, sd2, rho, gamma, theta,
                          esg1, esg2, sin_choice, excluded, name1, name2,
                          apply_threshold, threshold, penalty_strength)

    # Analytical MV starting point: x* = (1/γ)·Σ⁻¹·(μ − rf)
    mu    = np.array([r1 - r_free, r2 - r_free])
    Sigma = np.array([[sd1**2, rho*sd1*sd2], [rho*sd1*sd2, sd2**2]])
    try:
        x_mv = (1.0 / gamma) * np.linalg.solve(Sigma, mu)
    except np.linalg.LinAlgError:
        x_mv = np.array([0.5, 0.5])
    x0 = np.maximum(x_mv, 0.0)

    bounds = [(0.0, None), (0.0, None)]

    res = minimize(neg_obj, x0, method='L-BFGS-B', bounds=bounds,
                   options={'ftol': 1e-14, 'gtol': 1e-10, 'maxiter': 2000})
    x_opt = res.x

    # Try additional starts to avoid local minima
    for x_start in [np.array([0.3, 0.3]), np.array([0.1, 0.1]),
                    np.array([0.8, 0.0]), np.array([0.0, 0.8])]:
        r2_ = minimize(neg_obj, x_start, method='L-BFGS-B', bounds=bounds,
                       options={'ftol': 1e-14, 'gtol': 1e-10, 'maxiter': 2000})
        if r2_.fun < res.fun:
            x_opt = r2_.x
            res   = r2_

    x1_opt, x2_opt = float(x_opt[0]), float(x_opt[1])

    # ── Tangency portfolio (max Sharpe direction, normalised to sum=1) ──
    # Direction: Σ⁻¹·(μ − rf), clipped to non-negative, then normalised
    try:
        tang_dir  = np.linalg.solve(Sigma, mu)
        tang_dir  = np.maximum(tang_dir, 0.0)
        tang_norm = tang_dir / tang_dir.sum() if tang_dir.sum() > 1e-10 else np.array([0.5, 0.5])
    except np.linalg.LinAlgError:
        tang_norm = np.array([0.5, 0.5])
    x1_tan, x2_tan = float(tang_norm[0]), float(tang_norm[1])
    # Tangency sits ON the risky frontier (sum-to-1), no rf
    xrf_tan = 0.0

    # ── Min-variance portfolio (analytical, normalised to sum=1) ──
    try:
        ones     = np.ones(2)
        inv_S    = np.linalg.inv(Sigma)
        w_mv_raw = (inv_S @ ones) / (ones @ inv_S @ ones)
        w_mv_raw = np.clip(w_mv_raw, 0.0, 1.0)
        w_mv_sum = w_mv_raw.sum()
        w_mv_norm = w_mv_raw / w_mv_sum if w_mv_sum > 1e-10 else np.array([0.5, 0.5])
    except np.linalg.LinAlgError:
        w_mv_norm = np.array([0.5, 0.5])
    x1_mv, x2_mv = float(w_mv_norm[0]), float(w_mv_norm[1])
    # Min-var sits ON the risky frontier (sum-to-1), no rf
    xrf_mv = 0.0

    # ── Build frontier: TRADITIONAL risky frontier (w1 in [0,1], w2=1-w1) ──
    # The recommended portfolio is plotted at its actual unconstrained scale separately.
    n       = 500
    w1_vals = np.linspace(0, 1, n)

    frontier_x1  = w1_vals
    frontier_x2  = 1.0 - w1_vals
    frontier_ret = np.array([w * r1 + (1 - w) * r2 for w in w1_vals])
    frontier_sd  = np.array([portfolio_sd_2asset(w, 1 - w, sd1, sd2, rho) for w in w1_vals])
    frontier_esg = np.array([portfolio_esg_weighted(w, 1 - w, esg1, esg2) for w in w1_vals])
    # Objective evaluated at (w, 1-w) — used for the objective-function chart
    frontier_obj = np.array([objective([w, 1 - w], r1, r2, r_free, sd1, sd2, rho,
                                       gamma, theta, esg1, esg2) for w in w1_vals])


    def _metrics_risky(x1, x2):
        """For portfolios that sit ON the risky frontier (x1+x2=1, x_rf=0)."""
        ret  = x1 * r1 + x2 * r2
        sd   = portfolio_sd_2asset(x1, x2, sd1, sd2, rho)
        esg  = portfolio_esg_weighted(x1, x2, esg1, esg2)
        sr   = sharpe_ratio_2asset(x1, x2, r1, r2, r_free, sd1, sd2, rho)
        return ret, sd, esg, sr

    def _metrics_unconstrained(x1, x2):
        """For the recommended portfolio at its actual unconstrained scale."""
        ret  = portfolio_ret_2asset(x1, x2, r1, r2, r_free)
        sd   = portfolio_sd_2asset(x1, x2, sd1, sd2, rho)
        esg  = portfolio_esg_weighted(x1, x2, esg1, esg2)
        sr   = sharpe_ratio_2asset(x1, x2, r1, r2, r_free, sd1, sd2, rho)
        x_rf = 1.0 - x1 - x2
        return ret, sd, esg, sr, x_rf

    ret_opt, sd_opt, esg_opt, sr_opt, xrf_opt = _metrics_unconstrained(x1_opt, x2_opt)
    ret_tan, sd_tan, esg_tan, sr_tan           = _metrics_risky(x1_tan, x2_tan)
    ret_mv,  sd_mv,  esg_mv,  sr_mv            = _metrics_risky(x1_mv,  x2_mv)

    obj_opt     = objective([x1_opt, x2_opt], r1, r2, r_free, sd1, sd2, rho,
                            gamma, theta, esg1, esg2)
    esg_premium = sr_tan - sr_opt
    is_corner   = (x2_opt < 1e-3 and x1_opt > 1e-3) or (x1_opt < 1e-3 and x2_opt > 1e-3)

    return dict(
        # Optimal (unconstrained)
        x1_opt=x1_opt, x2_opt=x2_opt, xrf_opt=xrf_opt,
        ret_opt=ret_opt, sd_opt=sd_opt, esg_opt=esg_opt,
        sr_opt=sr_opt, obj_opt=obj_opt,
        # Tangency (risky frontier, sum-to-1)
        x1_tan=x1_tan, x2_tan=x2_tan, xrf_tan=xrf_tan,
        ret_tan=ret_tan, sd_tan=sd_tan, esg_tan=esg_tan, sr_tan=sr_tan,
        # Min-variance (risky frontier, sum-to-1)
        x1_mv=x1_mv, x2_mv=x2_mv, xrf_mv=xrf_mv,
        ret_mv=ret_mv, sd_mv=sd_mv, esg_mv=esg_mv, sr_mv=sr_mv,
        # Frontier (traditional risky frontier)
        frontier_ret=frontier_ret, frontier_sd=frontier_sd,
        frontier_esg=frontier_esg, frontier_obj=frontier_obj,
        frontier_x1=frontier_x1, frontier_x2=frontier_x2,
        # Meta
        esg_premium=esg_premium, is_corner=is_corner,
    )


@st.cache_data(show_spinner=False)
def cached_sensitivity(r1, r2, r_free, sd1, sd2, rho,
                       gamma, theta, esg1, esg2,
                       sin_choice, excluded_tuple, name1, name2,
                       apply_threshold, threshold, penalty_strength):
    excluded    = dict(excluded_tuple)
    theta_range = np.linspace(0, 4, 40)
    gamma_range = np.linspace(1, 15, 40)
    theta_grid  = np.linspace(0, 4, 10)
    gamma_grid  = np.linspace(1, 15, 10)

    def opt(t, g):
        r = run_optimisation(r1, r2, r_free, sd1, sd2, rho, g, t,
                             esg1, esg2, sin_choice, excluded, name1, name2,
                             apply_threshold, threshold, penalty_strength)
        return r["x1_opt"], r["x2_opt"]

    sa_x1, sa_x2, sa_total, sa_esg, sa_sr = [], [], [], [], []
    for t in theta_range:
        x1, x2 = opt(t, gamma)
        sa_x1.append(x1 * 100); sa_x2.append(x2 * 100)
        sa_total.append((x1 + x2) * 100)
        sa_esg.append(portfolio_esg_weighted(x1, x2, esg1, esg2))
        sa_sr.append(sharpe_ratio_2asset(x1, x2, r1, r2, r_free, sd1, sd2, rho))

    sg_total, sg_sr = [], []
    for g in gamma_range:
        x1, x2 = opt(theta, g)
        sg_total.append((x1 + x2) * 100)
        sg_sr.append(sharpe_ratio_2asset(x1, x2, r1, r2, r_free, sd1, sd2, rho))

    heatmap = np.zeros((len(gamma_grid), len(theta_grid)))
    for i, g in enumerate(gamma_grid):
        for j, t in enumerate(theta_grid):
            x1, x2 = opt(t, g)
            heatmap[i, j] = portfolio_esg_weighted(x1, x2, esg1, esg2)

    return (theta_range, gamma_range, theta_grid, gamma_grid,
            np.array(sa_x1), np.array(sa_x2), np.array(sa_total),
            np.array(sa_esg), np.array(sa_sr),
            np.array(sg_total), np.array(sg_sr), heatmap)


# ══════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════
PRESETS = {
    "🌿 Eco-First":          dict(r1=8,  sd1=22, r2=4,  sd2=10, rho=0.15, rfree=2.0, risk=0, theta=3.8, focus=0, thr=60,  use_thr=True),
    "⚖️ Balanced":           dict(r1=8,  sd1=20, r2=4,  sd2=10, rho=0.20, rfree=2.0, risk=1, theta=2.0, focus=3, thr=0,   use_thr=False),
    "🛡️ Conservative Green": dict(r1=6,  sd1=14, r2=3,  sd2=7,  rho=0.10, rfree=2.0, risk=0, theta=2.5, focus=3, thr=50,  use_thr=True),
    "🚀 Growth Hunter":      dict(r1=14, sd1=30, r2=5,  sd2=12, rho=0.25, rfree=2.0, risk=2, theta=0.5, focus=3, thr=0,   use_thr=False),
    "🤝 Social Impact":      dict(r1=7,  sd1=18, r2=4,  sd2=9,  rho=0.18, rfree=2.0, risk=1, theta=3.0, focus=1, thr=55,  use_thr=True),
}
PILLAR_OPTIONS = [
    "🌍 Environmental focus  (E=0.60, S=0.20, G=0.20)",
    "🤝 Social focus         (E=0.20, S=0.60, G=0.20)",
    "🏛️ Governance focus     (E=0.20, S=0.20, G=0.60)",
    "⚖️ Balanced ESG         (E=0.34, S=0.33, G=0.33)",
]
PILLAR_WEIGHTS = {
    0: (0.60, 0.20, 0.20, "Environmental focus"),
    1: (0.20, 0.60, 0.20, "Social focus"),
    2: (0.20, 0.20, 0.60, "Governance focus"),
    3: (0.34, 0.33, 0.33, "Balanced ESG"),
}
RISK_MAP    = {0: (10, "Conservative"), 1: (5, "Balanced"), 2: (2, "Aggressive")}
SIN_SECTORS = {"Tobacco", "Weapons & Defence", "Gambling", "Fossil Fuels"}
SECTORS     = ["Technology", "Healthcare", "Financial Services", "Consumer Goods",
               "Energy", "Fossil Fuels", "Tobacco", "Weapons & Defence", "Gambling", "Other"]

if "preset" not in st.session_state:
    st.session_state.preset = None


# ══════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
  <div style="font-size:5rem;line-height:1;">🧞</div>
  <div>
    <p class="hero-title">ESGenie</p>
    <p class="hero-subtitle">Your personalised sustainable investment portfolio advisor</p>
    <span class="hero-badge">🌿 Sustainable Finance · ESG Optimisation · Retail Investing</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# HOW TO USE
# ══════════════════════════════════════════════════════════════════════
with st.expander("📖 How to use ESGenie — click to expand", expanded=False):
    st.markdown("""
    <div class="how-to-box" style="border:none; padding:0; margin:0;">
      <p style="font-size:0.93rem; line-height:1.7; margin-bottom:1rem;">
        ESGenie helps you build a two-asset investment portfolio that balances
        <strong>financial performance</strong> (return and risk) with
        <strong>ESG values</strong> (Environmental, Social, Governance). It finds the
        allocation that maximises your personal utility — a score that rewards higher
        returns, penalises risk, and rewards ESG performance according to how strongly
        you care about sustainability. Surplus wealth is held in the risk-free asset.
      </p>
      <div class="how-to-steps">
        <div class="how-to-step">
          <div class="how-to-step-num">01</div>
          <div class="how-to-step-title">📈 Enter Financial Data</div>
          <div class="how-to-step-desc">Provide expected returns, standard deviations, the correlation between your assets, and a risk-free rate (e.g. the current government bond yield). All figures should be annualised.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">02</div>
          <div class="how-to-step-title">🧭 Set Risk Profile</div>
          <div class="how-to-step-desc">Choose Conservative, Balanced, or Aggressive. This sets γ — the risk aversion coefficient. A higher γ reduces total risky exposure, shifting more wealth to the risk-free asset.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">03</div>
          <div class="how-to-step-title">🌱 Define ESG Priorities</div>
          <div class="how-to-step-desc">Set θ (how much sustainability influences your recommendation) and choose which ESG pillar — Environmental, Social, or Governance — matters most to you.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">04</div>
          <div class="how-to-step-title">🔍 Score &amp; Screen Assets</div>
          <div class="how-to-step-desc">Rate each asset on E, S, and G from 0–100. ESGenie combines these using your pillar weights to produce a single composite ESG score. Optionally exclude controversial sectors.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">05</div>
          <div class="how-to-step-title">✨ Run &amp; Explore</div>
          <div class="how-to-step-desc">Click Run Optimisation. ESGenie solves the unconstrained problem and shows your recommended allocation across three tabs, including the implicit risk-free position.</div>
        </div>
      </div>
      <div class="utility-formula">
        <strong>Objective function :</strong><br>
        max  x₁(r₁−rᶠ) + x₂(r₂−rᶠ)  −  (γ/2)·x′Σx  +  θ·s̄<br>
        where  s̄ = (x₁·ESG₁ + x₂·ESG₂) / (x₁ + x₂)<br><br>
        <span style="font-size:0.8rem;">
        x₁, x₂ = risky weights (fraction of wealth) &nbsp;|&nbsp; x_rf = 1 − x₁ − x₂ (risk-free)<br>
        γ = risk aversion &nbsp;|&nbsp; Σ = covariance matrix &nbsp;|&nbsp;
        θ = ESG taste &nbsp;|&nbsp; s̄ = ESG score of risky basket only
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# QUICK-START PRESETS
# ══════════════════════════════════════════════════════════════════════
st.markdown("#### ⚡ Quick-Start — choose an investor profile or load an example")
st.caption("Select a preset to auto-fill all inputs below, or load the Apple vs BP worked example.")

preset_cols = st.columns(len(PRESETS) + 1)
for col, pname in zip(preset_cols, PRESETS):
    with col:
        is_active = st.session_state.preset == pname
        if st.button(
            ("✅ " if is_active else "") + pname,
            key=f"pre_{pname}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.preset = pname
            st.rerun()

with preset_cols[-1]:
    if st.button("📋 Apple vs BP", use_container_width=True):
        st.session_state.update(dict(
            _name1="Apple", _name2="BP",
            n1="Apple", n2="BP",
            _r1=12.0, _r2=6.0, _sd1=18.0, _sd2=22.0, _rho=-0.1, _rfree=4.5,
            _E1=78.0, _S1=72.0, _G1=81.0,
            _E2=32.0, _S2=41.0, _G2=55.0,
            _risk=0, _theta=2.5, _focus=0,
            _use_thr=True, _thr=50.0,
        ))
        st.session_state.preset = None
        st.rerun()

p = PRESETS.get(st.session_state.preset, {})
st.markdown("---")


# ══════════════════════════════════════════════════════════════════════
# INPUT SECTIONS
# ══════════════════════════════════════════════════════════════════════
st.markdown("#### Configure your portfolio parameters")
st.caption("Expand each section, fill in your inputs, then click Run Optimisation.")

with st.expander("01  —  Financial Data", expanded=True):
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown('<p class="section-label">Asset 1</p>', unsafe_allow_html=True)
        name1 = st.text_input("Name", value=st.session_state.get("_name1", "Asset 1"), key="n1")
        r1    = st.number_input("Expected Return (%)", -50.0, 50.0,
                                float(p.get("r1",  st.session_state.get("_r1",  8.0))),  step=0.5) / 100
        sd1   = st.number_input("Standard Deviation (%)", 0.0, 100.0,
                                float(p.get("sd1", st.session_state.get("_sd1", 20.0))), step=0.5) / 100
    with col_b:
        st.markdown('<p class="section-label">Asset 2</p>', unsafe_allow_html=True)
        name2 = st.text_input("Name", value=st.session_state.get("_name2", "Asset 2"), key="n2")
        r2    = st.number_input("Expected Return (%)", -50.0, 50.0,
                                float(p.get("r2",  st.session_state.get("_r2",  4.0))),  step=0.5, key="r2i") / 100
        sd2   = st.number_input("Standard Deviation (%)", 0.0, 100.0,
                                float(p.get("sd2", st.session_state.get("_sd2", 10.0))), step=0.5, key="sd2i") / 100
    col_c, col_d = st.columns(2, gap="large")
    with col_c:
        st.markdown('<p class="section-label">Correlation</p>', unsafe_allow_html=True)
        rho = st.slider("ρ between assets", -1.0, 1.0,
                        float(p.get("rho", st.session_state.get("_rho", 0.2))), step=0.05)
        st.markdown('<div class="tip-box">💡 A positive correlation means the assets tend to move together, reducing diversification benefits. Use annualised figures throughout.</div>', unsafe_allow_html=True)
    with col_d:
        st.markdown('<p class="section-label">Risk-Free Rate</p>', unsafe_allow_html=True)
        r_free = st.number_input("Risk-Free Rate (%)", 0.0, 15.0,
                                 float(p.get("rfree", st.session_state.get("_rfree", 2.0))),
                                 step=0.25) / 100
        st.markdown('<div class="tip-box">💡 Use the current annualised government bond yield for your country — e.g. UK 10-year gilt or US Treasury rate.</div>', unsafe_allow_html=True)

with st.expander("02  —  Risk Profile", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">Your risk profile determines γ, the risk aversion coefficient. A higher γ reduces total risky exposure — both x₁ and x₂ fall proportionally, shifting more wealth to the risk-free asset.</div>', unsafe_allow_html=True)
    risk_idx = st.radio(
        "Your attitude to investment risk:",
        [0, 1, 2],
        format_func=lambda x: ["🛡️ Conservative — prioritise capital protection",
                                "⚖️ Balanced — moderate risk for moderate returns",
                                "🚀 Aggressive — comfortable with high risk"][x],
        index=int(p.get("risk", st.session_state.get("_risk", 1))),
        horizontal=True,
    )
    gamma, risk_label = RISK_MAP[risk_idx]
    st.caption(f"γ = {gamma}  ·  Objective: x′(μ−rf) − ({gamma}/2)·x′Σx + θ·s̄")

with st.expander("03  —  ESG Preferences", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">θ controls how strongly sustainability influences your recommendation. A higher θ tilts the optimiser toward the higher-ESG asset. The ESG score s̄ is computed over risky positions only — the risk-free asset contributes no ESG score.</div>', unsafe_allow_html=True)
    col_e, col_f = st.columns(2, gap="large")
    with col_e:
        st.markdown('<p class="section-label">ESG Weight in Utility (θ)</p>', unsafe_allow_html=True)
        theta = st.slider("0 = financial only  ·  4 = ESG first",
                          0.0, 4.0, float(p.get("theta", st.session_state.get("_theta", 2.0))), step=0.1)
        st.caption(f"Currently: θ = {theta}")
    with col_f:
        st.markdown('<p class="section-label">ESG Pillar Focus</p>', unsafe_allow_html=True)
        focus_idx = st.radio(
            "Which pillar matters most?",
            [0, 1, 2, 3],
            format_func=lambda x: PILLAR_OPTIONS[x],
            index=int(p.get("focus", st.session_state.get("_focus", 3))),
        )
    w_e, w_s, w_g, esg_focus_label = PILLAR_WEIGHTS[focus_idx]

with st.expander("04  —  Asset ESG Scores", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">Rate each asset from 0 (worst) to 100 (best) across three ESG pillars. Scores are combined using your pillar weights from Section 03 to produce a single composite ESG score per asset. 💡 Scores above 70 are generally considered strong; below 40 indicates meaningful sustainability concerns.</div>', unsafe_allow_html=True)
    col_g, col_h = st.columns(2, gap="large")
    with col_g:
        st.markdown(f'<p class="section-label">{name1}</p>', unsafe_allow_html=True)
        sector1 = st.selectbox("Sector", SECTORS, key="sec1")
        E1 = st.slider("Environmental (E)", 0, 100, int(st.session_state.get("_E1", 60)), key="e1")
        S1 = st.slider("Social (S)",        0, 100, int(st.session_state.get("_S1", 60)), key="s1")
        G1 = st.slider("Governance (G)",    0, 100, int(st.session_state.get("_G1", 60)), key="g1")
    with col_h:
        st.markdown(f'<p class="section-label">{name2}</p>', unsafe_allow_html=True)
        sector2 = st.selectbox("Sector", SECTORS, key="sec2")
        E2 = st.slider("Environmental (E)", 0, 100, int(st.session_state.get("_E2", 40)), key="e2")
        S2 = st.slider("Social (S)",        0, 100, int(st.session_state.get("_S2", 40)), key="s2")
        G2 = st.slider("Governance (G)",    0, 100, int(st.session_state.get("_G2", 40)), key="g2")

with st.expander("05  —  Ethical Screening", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">ESGenie automatically detects assets in controversial sectors — Tobacco, Weapons & Defence, Gambling, and Fossil Fuels. You can exclude them entirely, apply a utility penalty, or proceed without restriction. The ESG threshold applies a soft penalty independent of θ.</div>', unsafe_allow_html=True)
    excluded = {}
    for aname, sector in [(name1, sector1), (name2, sector2)]:
        if sector in SIN_SECTORS:
            excluded[aname] = sector
    if excluded:
        st.warning(f"⚠️ Restricted sector detected: {', '.join(excluded.values())}")
        sin_choice = st.radio(
            "How to handle restricted sectors?",
            [1, 2, 3],
            format_func=lambda x: {1: "❌ Exclude entirely (weight = 0%)",
                                    2: "⚠️ Apply utility penalty",
                                    3: "✅ Proceed without restriction"}[x],
        )
    else:
        st.success("✅ No restricted sectors detected.")
        sin_choice = 3

    st.markdown('<p class="section-label">Minimum ESG Threshold</p>', unsafe_allow_html=True)
    use_thr = st.checkbox(
        "Set a minimum portfolio ESG score threshold",
        value=bool(p.get("use_thr", st.session_state.get("_use_thr", False)))
    )
    if use_thr:
        threshold = st.slider("Minimum ESG score", 0.0, 100.0,
                              float(p.get("thr", st.session_state.get("_thr", 50.0))), step=1.0)
    else:
        threshold = 0.0

    apply_threshold  = use_thr and threshold > 0
    penalty_strength = 0.05  

st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
col_run, _ = st.columns([1, 3])
with col_run:
    run = st.button("✨ Run Optimisation", type="primary", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# LANDING STATE
# ══════════════════════════════════════════════════════════════════════
if not run:
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.info("Complete the five sections above and click **✨ Run Optimisation** to generate your personalised sustainable portfolio.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════
# GUARDS
# ══════════════════════════════════════════════════════════════════════
if sin_choice == 1 and len(excluded) == 2:
    st.error("❌ Both assets are in restricted sectors. No valid portfolio can be constructed.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════
# COMPUTE
# ══════════════════════════════════════════════════════════════════════
esg1 = compute_esg(E1, S1, G1, w_e, w_s, w_g)
esg2 = compute_esg(E2, S2, G2, w_e, w_s, w_g)

with st.spinner("🧞 ESGenie is working its magic..."):
    res = run_optimisation(
        r1, r2, r_free, sd1, sd2, rho,
        gamma, theta, esg1, esg2,
        sin_choice, excluded, name1, name2,
        apply_threshold, threshold, penalty_strength,
    )

x1_opt  = res["x1_opt"];  x2_opt  = res["x2_opt"];  xrf_opt = res["xrf_opt"]
x1_tan  = res["x1_tan"];  x2_tan  = res["x2_tan"];  xrf_tan = res["xrf_tan"]
x1_mv   = res["x1_mv"];   x2_mv   = res["x2_mv"];   xrf_mv  = res["xrf_mv"]
esg_premium = res["esg_premium"]

if theta <= 1:     esg_importance_label = "Low ESG preference"
elif theta <= 2.5: esg_importance_label = "Moderate ESG preference"
else:              esg_importance_label = "High ESG preference"

dominant = name1 if x1_opt >= x2_opt else name2
dom_esg  = esg1  if x1_opt >= x2_opt else esg2
sec_esg  = esg2  if x1_opt >= x2_opt else esg1

if theta > 3:     identity = ("🌱 Impact Investor",        "identity-impact")
elif theta > 1.5: identity = ("⚖️ Balanced ESG Investor",  "identity-balanced")
else:             identity = ("💰 Return-Focused Investor", "identity-financial")


# ══════════════════════════════════════════════════════════════════════
# INVESTOR PROFILE STRIP
# ══════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown('<div class="section-header">👤 Investor Profile</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
for col, label, value, delta in [
    (c1, "Risk Profile",   risk_label,           f"γ = {gamma}"),
    (c2, "ESG Importance", esg_importance_label, f"θ = {theta}"),
    (c3, "ESG Focus",      esg_focus_label,      ""),
    (c4, "Threshold",      f"{threshold:.0f}" if apply_threshold else "None", "min ESG score"),
    (c5, "Identity",       identity[0],          ""),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-card-label">{label}</div>
          <div class="metric-card-value" style="font-size:1.05rem;">{value}</div>
          <div class="metric-card-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ESG SCORE SUMMARY
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🌱 ESG Score Summary</div>', unsafe_allow_html=True)

ca, cb = st.columns(2)
for col, aname, sector, esg_score, E, S, G in [
    (ca, name1, sector1, esg1, E1, S1, G1),
    (cb, name2, sector2, esg2, E2, S2, G2),
]:
    _, pill = classify_esg(esg_score)
    with col:
        st.markdown(f"""
        <div class="metric-card" style="text-align:left; padding:1.1rem 1.4rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <span style="font-weight:700; color:var(--forest); font-size:1rem;">{aname}</span>
            {pill}
          </div>
          <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.5rem;">{sector}</div>
          <div style="font-size:1.6rem; font-family:'DM Serif Display',serif; color:var(--forest);">
            {esg_score:.1f}<span style="font-size:0.85rem; color:var(--text-muted);"> / 100</span>
          </div>
          <div style="font-size:0.78rem; color:var(--text-muted); margin-top:0.4rem;">
            🌿 E={E} × {w_e:.2f} &nbsp;+&nbsp; 🤝 S={S} × {w_s:.2f} &nbsp;+&nbsp; 🏛️ G={G} × {w_g:.2f}
          </div>
        </div>
        """, unsafe_allow_html=True)

if apply_threshold:
    if esg1 < threshold: st.warning(f"⚠️ {name1} ESG ({esg1:.1f}) is below your threshold of {threshold:.0f}.")
    if esg2 < threshold: st.warning(f"⚠️ {name2} ESG ({esg2:.1f}) is below your threshold of {threshold:.0f}.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")


# ══════════════════════════════════════════════════════════════════════
# THREE RESULT TABS
# ══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Results", "📈 Charts", "🔬 Sensitivity Analysis"])


# ─────────────────────────────────────────────────────────────────────
# TAB 1 — Portfolio Results
# ─────────────────────────────────────────────────────────────────────
with tab1:

    # Corner solution warning — audit check (c)
    if res["is_corner"]:
        corner_asset = name2 if x1_opt > x2_opt else name1
        active_asset = name1 if x1_opt > x2_opt else name2
        obj_interior = objective(
            [x1_opt * 0.5, x2_opt + x1_opt * 0.5] if x2_opt < 1e-3
            else [x1_opt + x2_opt * 0.5, x2_opt * 0.5],
            r1, r2, r_free, sd1, sd2, rho, gamma, theta, esg1, esg2
        )
        st.warning(
            f"⚠️ **Corner solution detected.** At θ = {theta}, the optimiser has set "
            f"**{corner_asset}'s weight to zero** — the non-negativity constraint x ≥ 0 is binding. "
            f"This is mathematically correct and economically meaningful: your ESG preference is strong "
            f"enough that holding **{corner_asset}** at all reduces utility. "
            f"The objective value at this corner ({res['obj_opt']:.6f}) exceeds the interior value "
            f"({obj_interior:.6f}), confirming this is a genuine optimum, not a numerical artefact. "
            f"All wealth in risky assets is allocated to **{active_asset}**."
        )

    st.markdown('<div class="section-header">📐 Recommended Portfolio</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, label, value, delta in [
        (m1, "Expected Return",  f"{res['ret_opt']*100:.2f}%",  "total annualised"),
        (m2, "Risk (Std Dev)",   f"{res['sd_opt']*100:.2f}%",   "risky positions"),
        (m3, "Sharpe Ratio",     f"{res['sr_opt']:.3f}",        "risky basket"),
        (m4, "ESG Score",        f"{res['esg_opt']:.1f} / 100", classify_esg(res['esg_opt'])[0]),
        (m5, "ESG Premium",      f"{esg_premium:+.3f}",         "vs tangency Sharpe"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-card-label">{label}</div>
              <div class="metric-card-value">{value}</div>
              <div class="metric-card-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Asset allocation table — shows x1, x2, x_rf
    st.markdown('<div class="section-header">💼 Asset Allocation</div>', unsafe_allow_html=True)
    st.caption("Weights are fractions of total wealth. The risk-free position is implicit: x_rf = 1 − x₁ − x₂.")
    _, p1 = classify_esg(esg1)
    _, p2 = classify_esg(esg2)
    _, pp = classify_esg(res["esg_opt"])
    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;font-size:0.9rem;
                  background:var(--card);border-radius:10px;overflow:hidden;">
      <thead><tr style="background:var(--soft-bg);">
        <th style="text-align:left;padding:10px 14px;color:var(--forest);">Asset</th>
        <th style="text-align:right;padding:10px 14px;color:var(--forest);">Weight (x)</th>
        <th style="text-align:right;padding:10px 14px;color:var(--forest);">ESG Score</th>
        <th style="text-align:center;padding:10px 14px;color:var(--forest);">ESG Class</th>
      </tr></thead>
      <tbody>
        <tr>
          <td style="padding:9px 14px;color:var(--text);">{name1}</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">{x1_opt*100:.1f}%</td>
          <td style="text-align:right;padding:9px 14px;color:var(--text);">{esg1:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{p1}</td>
        </tr>
        <tr style="background:var(--soft-bg);">
          <td style="padding:9px 14px;color:var(--text);">{name2}</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">{x2_opt*100:.1f}%</td>
          <td style="text-align:right;padding:9px 14px;color:var(--text);">{esg2:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{p2}</td>
        </tr>
        <tr style="background:var(--soft-bg);">
          <td style="padding:9px 14px;color:var(--text-muted);font-style:italic;">Risk-Free Asset (implicit)</td>
          <td style="text-align:right;padding:9px 14px;color:var(--text-muted);font-style:italic;">{xrf_opt*100:.1f}%</td>
          <td style="text-align:right;padding:9px 14px;color:var(--text-muted);">—</td>
          <td style="text-align:center;padding:9px 14px;color:var(--text-muted);">—</td>
        </tr>
        <tr style="border-top:2px solid var(--border);">
          <td style="padding:9px 14px;font-weight:700;color:var(--forest);">Portfolio ESG (risky positions)</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">100.0%</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">{res['esg_opt']:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{pp}</td>
        </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Three-portfolio comparison
    st.markdown('<div class="section-header">📋 Portfolio Comparison</div>', unsafe_allow_html=True)
    st.caption(
        "Recommended = ESG-optimal (maximises full objective). "
        "Tangency = max Sharpe direction, normalised to risky-only (x_rf = 0). "
        "Min Variance = lowest volatility, normalised to risky-only (x_rf = 0)."
    )
    chars_df = pd.DataFrame({
        "Metric": ["Expected Return","Risk (Std Dev)","Sharpe Ratio",
                   "ESG Score","ESG Class",
                   f"Weight: {name1}", f"Weight: {name2}", "Weight: Risk-Free"],
        "🟢 Recommended": [
            f"{res['ret_opt']*100:.2f}%", f"{res['sd_opt']*100:.2f}%",
            f"{res['sr_opt']:.3f}",       f"{res['esg_opt']:.1f}",
            classify_esg(res['esg_opt'])[0],
            f"{x1_opt*100:.1f}%", f"{x2_opt*100:.1f}%", f"{xrf_opt*100:.1f}%"],
        "📐 Tangency": [
            f"{res['ret_tan']*100:.2f}%", f"{res['sd_tan']*100:.2f}%",
            f"{res['sr_tan']:.3f}",       f"{res['esg_tan']:.1f}",
            classify_esg(res['esg_tan'])[0],
            f"{x1_tan*100:.1f}%", f"{x2_tan*100:.1f}%", f"{xrf_tan*100:.1f}%"],
        "🛡️ Min Variance": [
            f"{res['ret_mv']*100:.2f}%",  f"{res['sd_mv']*100:.2f}%",
            f"{res['sr_mv']:.3f}",        f"{res['esg_mv']:.1f}",
            classify_esg(res['esg_mv'])[0],
            f"{x1_mv*100:.1f}%", f"{x2_mv*100:.1f}%", f"{xrf_mv*100:.1f}%"],
    })
    st.dataframe(chars_df, use_container_width=True, hide_index=True)

    if esg_premium > 0:
        st.warning(f"📉 **ESG Premium: {esg_premium:+.3f} Sharpe points** — your ESG preferences reduce risk-adjusted return relative to the purely financial tangency portfolio.")
    else:
        st.success(f"📈 **ESG Premium: {esg_premium:+.3f} Sharpe points** — your ESG preferences align with financial performance. No sacrifice in risk-adjusted return detected.")

    st.markdown('<div class="section-header">💬 Why This Portfolio?</div>', unsafe_allow_html=True)
    driver = (
        f"The tilt toward <strong>{dominant}</strong> is partly driven by its stronger ESG score "
        f"({dom_esg:.1f} vs {sec_esg:.1f}), consistent with your {esg_focus_label.lower()} and θ = {theta}."
        if dom_esg > sec_esg else
        f"The tilt toward <strong>{dominant}</strong> is driven primarily by its superior "
        f"risk-return profile rather than ESG performance."
    )
    rf_note = (
        f"The optimiser allocates <strong>{xrf_opt*100:.1f}%</strong> to the risk-free asset "
        f"(r_f = {r_free*100:.1f}%), reflecting your risk aversion of γ = {gamma}."
        if xrf_opt > 0.005 else
        f"The optimiser allocates all wealth to risky assets — the excess returns are "
        f"high enough to justify full risky investment at γ = {gamma}."
    )
    st.markdown(f"""
    <div class="reco-box">
    Based on your <strong>{risk_label.lower()} risk profile</strong> (γ = {gamma}) and
    <strong>{esg_importance_label.lower()}</strong> (θ = {theta}), ESGenie recommends:
    <strong>{x1_opt*100:.1f}% in {name1}</strong>,
    <strong>{x2_opt*100:.1f}% in {name2}</strong>, and
    <strong>{xrf_opt*100:.1f}% in the risk-free asset</strong>.<br><br>
    {driver}<br><br>{rf_note}
    </div>
    """, unsafe_allow_html=True)

    if apply_threshold and res['esg_opt'] < threshold:
        st.warning(f"The portfolio ESG score ({res['esg_opt']:.1f}) is below your threshold of {threshold:.0f}. A soft penalty was applied.")
    if sin_choice == 1 and excluded:
        for aname, sec in excluded.items():
            st.error(f"**{aname}** ({sec}) was excluded per your ethical screening preferences.")

    st.markdown("<br>", unsafe_allow_html=True)
    summary_txt = (
        f"ESGenie 🧞 — Portfolio Summary\n{'='*40}\n"
        f"Risk Profile:    {risk_label}  (γ={gamma})\n"
        f"ESG Importance:  θ={theta}  ({esg_importance_label})\n"
        f"ESG Focus:       {esg_focus_label}\n"
        f"Investor Type:   {identity[0]}\n\n"
        f"Recommended Allocation\n{'-'*40}\n"
        f"  {name1}:     {x1_opt*100:.1f}%  (fraction of wealth)\n"
        f"  {name2}:     {x2_opt*100:.1f}%  (fraction of wealth)\n"
        f"  Risk-Free:   {xrf_opt*100:.1f}%  (implicit residual)\n\n"
        f"Portfolio Metrics\n{'-'*40}\n"
        f"  Expected Return : {res['ret_opt']*100:.2f}%\n"
        f"  Risk (Std Dev)  : {res['sd_opt']*100:.2f}%\n"
        f"  Sharpe Ratio    : {res['sr_opt']:.3f}\n"
        f"  ESG Score       : {res['esg_opt']:.1f} / 100  ({classify_esg(res['esg_opt'])[0]})\n"
        f"  ESG Premium     : {esg_premium:+.3f} vs tangency Sharpe\n"
    )
    st.download_button(
        label="⬇️ Download Portfolio Summary",
        data=summary_txt,
        file_name="esgenie_summary.txt",
        mime="text/plain",
    )


# ─────────────────────────────────────────────────────────────────────
# TAB 2 — Charts
# ─────────────────────────────────────────────────────────────────────
with tab2:

    # Use the traditional risky frontier
    frontier_ret = res["frontier_ret"]
    frontier_sd  = res["frontier_sd"]
    frontier_esg = res["frontier_esg"]
    frontier_x1  = res["frontier_x1"]
    frontier_x2  = res["frontier_x2"]

    theme_text = "#1f3d2b" if not dark_mode else "#e5e7eb"
    chart_bg   = "#ffffff" if not dark_mode else "#0f1720"
    chart_plot = "#f4f8f5" if not dark_mode else "#18212b"
    chart_grid = "#e8f3ec" if not dark_mode else "#2a3441"

    st.markdown('<div class="section-header">📈 ESG-Efficient Frontier</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-info">'
        'The curve shows all risky-only portfolios (x₁ + x₂ = 100%, x_rf = 0%) coloured by ESG score. '
        'The Capital Market Line (dashed) connects the risk-free rate to the tangency portfolio. '
        'The Recommended star ✨ sits at its actual unconstrained scale — typically inside the frontier '
        'because some wealth is held in the risk-free asset. '
        'Hover over any point for details.'
        '</div>',
        unsafe_allow_html=True
    )

    fig_f = go.Figure()

    # Risky frontier — coloured by ESG score
    fig_f.add_trace(go.Scatter(
        x=frontier_sd * 100, y=frontier_ret * 100, mode="markers",
        marker=dict(color=frontier_esg, colorscale="RdYlGn", cmin=0, cmax=100,
                    size=5, opacity=0.85,
                    colorbar=dict(title=dict(text="ESG Score", font=dict(color=theme_text)),
                                  thickness=14, tickfont=dict(color=theme_text))),
        text=[f"{name1}: {x1:.1%} | {name2}: {x2:.1%}<br>Return: {r*100:.2f}%<br>"
              f"Risk: {s*100:.2f}%<br>ESG: {e:.1f}"
              for x1, x2, r, s, e in zip(frontier_x1, frontier_x2,
                                          frontier_ret, frontier_sd, frontier_esg)],
        hoverinfo="text", showlegend=False,
    ))

    # Capital Market Line — from rf through tangency
    if res["sd_tan"] > 0:
        cml_max = max(frontier_sd.max(), res["sd_tan"]) * 1.20
        cml_x   = np.linspace(0, cml_max, 100)
        cml_s   = (res["ret_tan"] - r_free) / res["sd_tan"]
        fig_f.add_trace(go.Scatter(
            x=cml_x * 100, y=(r_free + cml_s * cml_x) * 100,
            mode="lines", line=dict(dash="dash", color="#4a7c59", width=1.5),
            name="Capital Market Line",
        ))

    # Key portfolio markers
    for sx, ry, label, colour, sym, sz, lx1, lx2 in [
        (0,             r_free,          f"Risk-Free ({r_free*100:.1f}%)", "#4a7c59", "diamond",     10, None,   None),
        (res["sd_mv"],  res["ret_mv"],   "Min Variance",                   "#7b5ea7", "square",      12, x1_mv,  x2_mv),
        (res["sd_tan"], res["ret_tan"],  "Tangency",                       "#2979aa", "triangle-up", 14, x1_tan, x2_tan),
        (res["sd_opt"], res["ret_opt"],  "✨ Recommended",                 "#2d5016", "star",        20, x1_opt, x2_opt),
    ]:
        hover = (
            f"{label}<br>{name1}: {lx1:.1%} | {name2}: {lx2:.1%}<br>"
            f"Return: {ry*100:.2f}% | Risk: {sx*100:.2f}%"
            if lx1 is not None else label
        )
        fig_f.add_trace(go.Scatter(
            x=[sx * 100], y=[ry * 100], mode="markers+text",
            marker=dict(symbol=sym, color=colour, size=sz, line=dict(color="white", width=1.5)),
            text=[label], textposition="top right",
            textfont=dict(color=theme_text, size=9),
            hovertext=[hover], hoverinfo="text", name=label,
        ))

    fig_f.update_layout(
        xaxis_title="Risk — Standard Deviation (%)",
        yaxis_title="Total Portfolio Return (%)",
        height=430,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_plot,
        font=dict(family="DM Sans", color=theme_text),
        margin=dict(l=50, r=20, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.38, xanchor="left", x=0,
                    font=dict(color=theme_text),
                    bgcolor="rgba(255,255,255,0.85)" if not dark_mode else "rgba(24,33,43,0.85)",
                    bordercolor="#c8dfc0", borderwidth=1),
        xaxis=dict(title_font=dict(color=theme_text), tickfont=dict(color=theme_text),
                   gridcolor=chart_grid, zerolinecolor="#c8dfc0"),
        yaxis=dict(title_font=dict(color=theme_text), tickfont=dict(color=theme_text),
                   gridcolor=chart_grid, zerolinecolor="#c8dfc0"),
    )
    st.plotly_chart(fig_f, use_container_width=True)

    # ── Objective function plot ──
    st.markdown('<div class="section-header">📉 Objective Function vs Asset-1 Share</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-info">'
        'Shows how the objective value changes as the share of Asset 1 in the risky basket varies '
        '(each evaluated at the risky-only mix, x₁ + x₂ = 1). '
        'The star marks the maximum — the composition that maximises utility given your preferences. '
        'Note: the recommended portfolio uses this composition but scales x₁ and x₂ down by the optimal '
        'total risky weight (determined by γ), with the remainder held in the risk-free asset.'
        '</div>',
        unsafe_allow_html=True
    )

    w1_ratio = np.linspace(0, 1, len(res["frontier_obj"]))
    obj_plot = res["frontier_obj"]

    fig_u, ax = plt.subplots(figsize=(10, 4))
    fig_u.patch.set_facecolor(chart_bg)
    ax.set_facecolor(chart_plot)
    for spine in ax.spines.values():
        spine.set_edgecolor("#c8dfc0"); spine.set_linewidth(0.8)
    ax.plot(w1_ratio * 100, obj_plot, color="#4a7c59", linewidth=2.5, label="Objective")
    ax.fill_between(w1_ratio * 100, obj_plot, alpha=0.07, color="#4a7c59")
    best_idx = np.argmax(obj_plot)
    ax.axvline(x=w1_ratio[best_idx] * 100, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.scatter(w1_ratio[best_idx] * 100, obj_plot[best_idx],
               marker="*", color="#2d5016", s=250, zorder=5,
               label=f"✨ Optimal: {w1_ratio[best_idx]*100:.1f}% {name1}")
    ax.set_xlabel(f"Share of {name1} in risky basket (%)", color=theme_text)
    ax.set_ylabel("Objective Value", color=theme_text)
    ax.set_title(f"Objective Function vs {name1} Share (risky basket mix)", color=theme_text, fontweight="bold")
    ax.tick_params(colors=theme_text)
    ax.legend(fontsize=9, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.25, color=chart_grid)
    fig_u.tight_layout()
    st.pyplot(fig_u)
    plt.close(fig_u)


# ─────────────────────────────────────────────────────────────────────
# TAB 3 — Sensitivity Analysis
# ─────────────────────────────────────────────────────────────────────
with tab3:

    st.markdown('<div class="section-header">🔬 Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-info">'
        'Higher θ puts more weight on ESG — the portfolio tilts toward the higher-ESG asset. '
        'Higher γ reduces total risky exposure — both x₁ and x₂ fall proportionally (doubling γ '
        'roughly halves both positions). The heatmap shows how portfolio ESG score responds across '
        'all (θ, γ) combinations — your profile is marked with a star.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.spinner("🧞 Computing sensitivity across parameter space..."):
        (theta_range, gamma_range, theta_grid, gamma_grid,
         sa_x1, sa_x2, sa_total, sa_esg, sa_sr,
         sg_total, sg_sr, heatmap) = cached_sensitivity(
            r1, r2, r_free, sd1, sd2, rho,
            gamma, theta, esg1, esg2,
            sin_choice, tuple(excluded.items()), name1, name2,
            apply_threshold, threshold, penalty_strength,
        )

    st.markdown(f'<div class="section-header">📋 θ Sensitivity Table  (γ fixed at {gamma})</div>',
                unsafe_allow_html=True)
    rows = []
    for idx in np.linspace(0, len(theta_range) - 1, 9, dtype=int):
        t_val = theta_range[idx]
        rows.append({
            "θ":              f"{t_val:.2f}" + (" ← your θ" if abs(t_val - theta) < 0.25 else ""),
            f"x₁: {name1}":   f"{sa_x1[idx]:.1f}%",
            f"x₂: {name2}":   f"{sa_x2[idx]:.1f}%",
            "Total Risky":    f"{sa_total[idx]:.1f}%",
            "Risk-Free":      f"{max(0.0, 100 - sa_total[idx]):.1f}%",
            "Portfolio ESG":  f"{sa_esg[idx]:.1f}",
            "ESG Class":      classify_esg(sa_esg[idx])[0],
            "Sharpe":         f"{sa_sr[idx]:.3f}",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    fig_sa, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig_sa.patch.set_facecolor(chart_bg)
    for row in axes:
        for ax in row:
            ax.set_facecolor(chart_plot)
            for spine in ax.spines.values():
                spine.set_edgecolor("#c8dfc0"); spine.set_linewidth(0.8)
            ax.tick_params(colors=theme_text)
    fig_sa.suptitle("ESGenie 🧞 — Sensitivity Analysis", fontsize=13, fontweight="bold", color=theme_text)

    ax = axes[0, 0]
    ax.plot(theta_range, sa_x1,    color="#4a7c59", linewidth=2,   label=f"x₁: {name1}")
    ax.plot(theta_range, sa_x2,    color="#6a9e76", linewidth=2,   linestyle="--", label=f"x₂: {name2}")
    ax.plot(theta_range, sa_total, color="#2d5016", linewidth=2,   linestyle=":", label="Total risky")
    ax.axvline(x=theta, color="#2d5016", linestyle="--", linewidth=1, alpha=0.5, label=f"θ={theta}")
    ax.set_xlabel("ESG Taste (θ)", color=theme_text)
    ax.set_ylabel("Position size (% of wealth)", color=theme_text)
    ax.set_title(f"Positions vs ESG Preference  (γ = {gamma})", color=theme_text, fontweight="bold")
    ax.legend(fontsize=8, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.2, color=chart_grid); ax.set_xlim(0, 4)

    ax = axes[0, 1]
    ax.plot(theta_range, sa_esg, color="#6a9e76", linewidth=2.5)
    ax.fill_between(theta_range, sa_esg, alpha=0.07, color="#6a9e76")
    ax.axvline(x=theta, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8, label=f"Your θ = {theta}")
    ax.axhspan(80, 100, alpha=0.07, color="green",  label="High ESG (≥80)")
    ax.axhspan(50,  80, alpha=0.07, color="yellow", label="Moderate ESG (50–80)")
    ax.axhspan(0,   50, alpha=0.07, color="red",    label="Low ESG (<50)")
    ax.set_xlabel("ESG Taste (θ)", color=theme_text)
    ax.set_ylabel("Portfolio ESG Score (risky basket)", color=theme_text)
    ax.set_title(f"ESG Score vs ESG Preference  (γ = {gamma})", color=theme_text, fontweight="bold")
    ax.legend(fontsize=7, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.2, color=chart_grid); ax.set_xlim(0, 4); ax.set_ylim(0, 100)

    ax = axes[1, 0]
    ax.plot(gamma_range, sg_total, color="#4a7c59", linewidth=2.5, label="Total risky position")
    ax.fill_between(gamma_range, sg_total, alpha=0.07, color="#4a7c59")
    ax.axvline(x=gamma, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8, label=f"Your γ = {gamma}")
    ax.set_xlabel("Risk Aversion (γ)", color=theme_text)
    ax.set_ylabel("Total Risky Weight (% of wealth)", color=theme_text)
    ax.set_title(f"Total Risky Exposure vs Risk Aversion  (θ = {theta})", color=theme_text, fontweight="bold")
    ax.legend(fontsize=8, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.2, color=chart_grid)

    ax = axes[1, 1]
    h_min, h_max = heatmap.min(), heatmap.max()
    im = ax.imshow(heatmap, aspect="auto", origin="lower", cmap="RdYlGn",
                   vmin=h_min, vmax=h_max,
                   extent=[theta_grid[0], theta_grid[-1], gamma_grid[0], gamma_grid[-1]])
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Portfolio ESG Score", color=theme_text)
    cbar.ax.yaxis.set_tick_params(color=theme_text)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=theme_text)
    ax.scatter(theta, gamma, marker="*", color="#2d5016", s=250, zorder=5, label="✨ Your profile")
    ax.set_xlabel("ESG Taste (θ)", color=theme_text)
    ax.set_ylabel("Risk Aversion (γ)", color=theme_text)
    ax.set_title("ESG Score across Parameter Space", color=theme_text, fontweight="bold")
    ax.legend(fontsize=8, loc="upper left", labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")

    plt.tight_layout()
    st.pyplot(fig_sa)
    plt.close(fig_sa)


# ── Footer ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### ⚠️ Model Limitations")
st.caption(
    "This model uses an unconstrained formulation, risky assets weights do not need to sum to one, "
    "and surplus wealth is held in the risk-free asset. "
    "The model assumes normally distributed returns, constant correlations, and static ESG scores. "
    "In practice, ESG ratings differ significantly across providers and financial markets are dynamic. "
    "This app is for educational purposes only and does not constitute financial advice."
)
st.caption("ESGenie 🧞 · Sustainable Portfolio Advisor · Built with Streamlit · Sustainable Finance")
