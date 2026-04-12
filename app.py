# app.py
# ESGenie 🧞 — Sustainable Portfolio Optimiser

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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

    dark_mode = st.toggle("🌙 Dark mode", value=st.session_state.get("dark_mode", False))
    st.session_state.dark_mode = dark_mode

    high_contrast = st.toggle("🔲 High contrast", value=st.session_state.get("high_contrast", False))
    st.session_state.high_contrast = high_contrast

    dyslexia_font = st.toggle("🔡 Dyslexia-friendly font", value=st.session_state.get("dyslexia_font", False))
    st.session_state.dyslexia_font = dyslexia_font

    font_size = st.slider("🔠 Font size", 14, 22, st.session_state.get("font_size", 16), step=1)
    st.session_state.font_size = font_size

# ── CSS ───────────────────────────────────────────────────────────────
if high_contrast:
    theme_css = """
    :root {
        --bg: #000000; --card: #111111; --text: #ffffff; --text-muted: #dddddd;
        --forest: #ffffff; --sage: #00ff88; --sage-light: #00cc66;
        --soft-bg: #1a1a1a; --border: #00ff88;
        --green: #00ff88; --amber: #ffcc00; --red: #ff4444;
    }
    """
elif dark_mode:
    theme_css = """
    :root {
        --bg: #0f1720; --card: #18212b; --text: #e5e7eb; --text-muted: #9ca3af;
        --forest: #9be3b0; --sage: #6fa77f; --sage-light: #8fd19e;
        --soft-bg: #1f2a33; --border: #2a3441;
        --green: #4ade80; --amber: #fbbf24; --red: #f87171;
    }
    """
else:
    theme_css = """
    :root {
        --bg: #f4f8f5; --card: #ffffff; --text: #1f3d2b; --text-muted: #5f6f65;
        --forest: #1f3d2b; --sage: #4c7a5a; --sage-light: #6fa77f;
        --soft-bg: #e8f3ec; --border: #cfe3d6;
        --green: #2e7d32; --amber: #b7791f; --red: #c53030;
    }
    """

body_font = "'OpenDyslexic', 'Comic Sans MS', sans-serif" if dyslexia_font else "'DM Sans', sans-serif"
serif_font = "'OpenDyslexic', 'Comic Sans MS', sans-serif" if dyslexia_font else "'DM Serif Display', serif"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
{("@import url('https://fonts.cdnfonts.com/css/opendyslexic');" if dyslexia_font else "")}

{theme_css}

.stApp {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: {body_font} !important;
    font-size: {font_size}px !important;
}}
body, p, div, span, li {{ color: var(--text) !important; font-size: {font_size}px !important; }}
label {{ color: var(--forest) !important; font-weight: 500 !important; }}
.stCaption {{ color: var(--text-muted) !important; }}

h1, h2, h3, h4 {{ font-family: {serif_font} !important; color: var(--forest) !important; }}
.section-header {{ font-family: {serif_font} !important; color: var(--forest) !important;
                   font-size: 1.15rem !important; font-weight: 600; border-left: 4px solid var(--sage);
                   padding-left: 0.65rem; margin: 1.25rem 0 0.7rem; }}

/* HERO */
.hero-banner {{
    background: var(--card); border: 1px solid var(--border); border-radius: 14px;
    padding: 1.6rem 2rem; margin-bottom: 1rem; display: flex; align-items: center;
    gap: 1.25rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}}
.hero-title {{
    font-family: {serif_font}; font-size: 2.4rem; color: var(--forest); margin: 0;
}}
.hero-subtitle {{ font-size: 0.95rem; color: var(--text-muted); margin: 0.1rem 0 0; }}
.hero-badge {{
    background: var(--sage); color: white; font-size: 0.7rem; padding: 0.25rem 0.6rem;
    border-radius: 20px; display: inline-block; margin-top: 0.4rem;
}}

/* HOW TO USE */
.how-to-box {{
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 1.5rem 2rem; margin: 0.5rem 0 1.5rem;
}}
.how-to-steps {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.85rem; margin-top: 1rem;
}}
.how-to-step {{
    background: var(--soft-bg); border: 1px solid var(--border); border-radius: 10px;
    padding: 0.85rem 1rem;
}}
.how-to-step-num {{
    font-family: {serif_font}; font-size: 1.3rem; color: var(--sage); font-weight: 700;
}}
.how-to-step-title {{
    font-weight: 600; color: var(--forest); font-size: 0.88rem; margin: 0.2rem 0;
}}
.how-to-step-desc {{ font-size: 0.8rem; color: var(--text-muted); line-height: 1.5; }}
.utility-formula {{
    background: var(--soft-bg); border-left: 3px solid var(--sage); border-radius: 0 8px 8px 0;
    padding: 0.75rem 1.25rem; margin-top: 1rem; font-size: 0.88rem; color: var(--forest);
    font-family: 'Courier New', monospace;
}}

/* EXPANDERS */
details[data-testid="stExpander"] {{
    border: 1px solid var(--border) !important; border-radius: 10px !important; margin-bottom: 0.75rem !important;
}}
details[data-testid="stExpander"] summary {{
    background: var(--soft-bg) !important; color: var(--forest) !important;
    font-family: {serif_font} !important; font-weight: 600 !important; padding: 0.85rem 1.1rem !important;
}}
details[open] summary {{ background: var(--sage) !important; color: white !important; }}
details[open] summary svg {{ fill: white !important; }}
details[data-testid="stExpander"] > div {{
    background: var(--card) !important; padding: 1rem 1.25rem 1.25rem !important; color: var(--text) !important;
}}
details[data-testid="stExpander"] > div * {{ color: var(--text) !important; }}
details[data-testid="stExpander"] summary * {{ color: var(--forest) !important; }}
details[open] summary * {{ color: white !important; }}

/* SECTION LABEL */
.section-label {{
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.10em; color: var(--text-muted); margin-bottom: 0.4rem; margin-top: 0.6rem;
}}

/* TIPS */
.tip-box {{
    background: var(--soft-bg); border-left: 3px solid var(--sage-light); border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem; margin-top: 0.5rem; font-size: 0.82rem; color: var(--text-muted); line-height: 1.5;
}}

/* METRIC CARDS */
.metric-card {{
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 1rem 1.2rem; text-align: center; height: 100%;
}}
.metric-card-label {{ color: var(--text-muted); font-size: 0.72rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 0.3rem; }}
.metric-card-value {{ color: var(--forest); font-family: {serif_font}; font-size: 1.45rem; line-height: 1.1; }}
.metric-card-delta {{ font-size: 0.75rem; color: var(--sage); margin-top: 0.25rem; }}

/* RECO BOX */
.reco-box {{
    background: var(--soft-bg); border: 1px solid var(--sage); border-left: 5px solid var(--sage);
    border-radius: 0 10px 10px 0; padding: 1.1rem 1.4rem; color: var(--forest);
    font-size: 0.93rem; line-height: 1.65;
}}

/* CHART INFO */
.chart-info {{
    background: var(--soft-bg); border-left: 3px solid var(--sage-light);
    border-radius: 0 8px 8px 0; padding: 0.6rem 1rem; margin-bottom: 0.75rem;
    font-size: 0.83rem; color: var(--text-muted); line-height: 1.5;
}}

/* ESG PILLS */
.esg-high {{ background:rgba(46,125,50,0.15); color:var(--green); border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:600; }}
.esg-mid  {{ background:rgba(183,121,31,0.15); color:var(--amber); border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:600; }}
.esg-low  {{ background:rgba(197,48,48,0.15);  color:var(--red);   border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:600; }}

/* BUTTONS */
.stButton > button {{ background:var(--soft-bg)!important; color:var(--forest)!important; border:1px solid var(--border)!important; border-radius:8px!important; }}
.stButton > button:hover {{ background:var(--sage-light)!important; color:white!important; }}
.stButton > button[kind="primary"] {{ background:var(--sage)!important; color:white!important; border:none!important; font-weight:600!important; }}
.stButton > button[kind="primary"]:hover {{ background:var(--forest)!important; }}
.stDownloadButton > button {{ background:var(--soft-bg)!important; color:var(--forest)!important; border:1px solid var(--border)!important; border-radius:8px!important; }}

/* INPUTS */
input, textarea {{ background-color:var(--soft-bg)!important; color:var(--forest)!important; border:1px solid var(--border)!important; border-radius:6px!important; }}
[data-baseweb="input"] {{ background-color:var(--soft-bg)!important; }}
[data-baseweb="select"] > div {{ background-color:var(--soft-bg)!important; color:var(--forest)!important; border:1px solid var(--border)!important; }}
ul[role="listbox"] {{ background-color:var(--card)!important; border:1px solid var(--border)!important; }}
li[role="option"] {{ color:var(--forest)!important; }}
li[role="option"]:hover {{ background-color:var(--soft-bg)!important; }}

/* TABS */
[data-testid="stTabs"] button {{ color:var(--sage)!important; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color:var(--forest)!important; border-bottom:2px solid var(--sage)!important; }}

/* TABLES */
table {{ color:var(--text)!important; }}
thead tr {{ background:var(--soft-bg)!important; }}
tbody tr {{ background:var(--card)!important; }}
tbody tr:nth-child(even) {{ background:var(--soft-bg)!important; }}
th, td {{ color:var(--text)!important; }}

/* ALERTS */
[data-testid="stInfo"]    {{ border-left:3px solid var(--sage)!important; }}
[data-testid="stWarning"] {{ border-left:3px solid var(--amber)!important; }}
[data-testid="stSuccess"] {{ border-left:3px solid var(--green)!important; }}
[data-testid="stError"]   {{ border-left:3px solid var(--red)!important; }}

/* DATAFRAMES */
[data-testid="stDataFrame"] {{ border:1px solid var(--border)!important; border-radius:10px!important; overflow:hidden; }}

/* SIDEBAR */
[data-testid="stSidebar"] {{ background:var(--soft-bg)!important; border-right:1px solid var(--border)!important; }}
[data-testid="stSidebar"] * {{ color:var(--text)!important; }}

hr {{ border:none!important; border-top:1px solid var(--border)!important; margin:1.25rem 0!important; }}
.stCaption {{ color:var(--text-muted)!important; font-size:0.76rem!important; }}
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
    return w_e * E + w_s * S + w_g * G

# ── Unconstrained portfolio statistics ────────────────────────────────
# x1, x2 are the weights in the two risky assets.
# The remainder (1 - x1 - x2) is held in the risk-free asset.
# There is NO sum-to-one constraint on the risky weights.

def portfolio_ret(x1, x2, r1, r2, r_free):
    """E[rp] = x1·r1 + x2·r2 + (1 - x1 - x2)·rf"""
    return x1 * r1 + x2 * r2 + (1 - x1 - x2) * r_free

def portfolio_sd(x1, x2, sd1, sd2, rho):
    """σp = sqrt(x1²σ1² + x2²σ2² + 2ρx1x2σ1σ2)
    Only risky assets contribute to variance; the risk-free has zero variance."""
    var = (x1**2 * sd1**2
           + x2**2 * sd2**2
           + 2 * rho * x1 * x2 * sd1 * sd2)
    return np.sqrt(np.maximum(var, 0.0))

def portfolio_esg(x1, x2, esg1, esg2):
    """Weighted-average ESG of the risky portion only.
    When total risky weight is zero the score is undefined; return 0."""
    total_risky = x1 + x2
    if np.isscalar(total_risky):
        if abs(total_risky) < 1e-9:
            return 0.0
        return (x1 * esg1 + x2 * esg2) / total_risky
    # vectorised path — avoid NaN by using a safe denominator
    numer      = x1 * esg1 + x2 * esg2
    safe_denom = np.where(np.abs(total_risky) < 1e-9, 1.0, total_risky)
    result     = np.where(np.abs(total_risky) < 1e-9, 0.0, numer / safe_denom)
    return result

def portfolio_ret_excess(x1, x2, r1, r2, r_free):
    """E[rp] - rf = x1·(r1-rf) + x2·(r2-rf)"""
    return x1 * (r1 - r_free) + x2 * (r2 - r_free)

def sharpe_ratio(x1, x2, r1, r2, sd1, sd2, rho, r_free):
    ret = portfolio_ret(x1, x2, r1, r2, r_free)
    sd  = portfolio_sd(x1, x2, sd1, sd2, rho)
    if np.isscalar(sd):
        if sd == 0: return 0.0
    return (ret - r_free) / sd

def utility(x1, x2, r1, r2, sd1, sd2, rho, r_free,
            gamma, theta, esg1, esg2,
            sin_choice, excluded, name1, name2,
            apply_threshold, threshold, penalty_strength):
    """
    ESG-adjusted mean-variance utility (unconstrained):
      U = [E(rp) − rf] − (γ/2)·σ²p + θ·(ESGp / 100)

    x1 and x2 are unconstrained risky weights; (1 - x1 - x2) sits in the risk-free asset.
    """
    excess = portfolio_ret_excess(x1, x2, r1, r2, r_free)
    sd     = portfolio_sd(x1, x2, sd1, sd2, rho)
    esg    = portfolio_esg(x1, x2, esg1, esg2)
    base   = excess - (gamma / 2) * sd**2 + theta * (esg / 100)

    excl = 0.0
    if sin_choice == 1:
        if name1 in excluded and x1 > 0:  excl -= 1e6 * x1
        if name2 in excluded and x2 > 0:  excl -= 1e6 * x2

    thr = 0.0
    if apply_threshold and esg < threshold:
        thr = -penalty_strength * ((threshold - esg) / 100)

    return base + excl + thr


def run_optimisation(r1, r2, sd1, sd2, rho, r_free,
                     gamma, theta, esg1, esg2,
                     sin_choice, excluded, name1, name2,
                     apply_threshold, threshold, penalty_strength, n=80):
    """
    Unconstrained two-asset optimisation.

    Searches x1 and x2 independently over a grid; the remainder sits in the
    risk-free asset. The grid spans [-0.5, 1.5] for each risky weight,
    covering short positions, full investment, and modest leverage.

    Grid size: n × n points (default 80 × 80 = 6 400 evaluations).
    """
    grid = np.linspace(-0.5, 1.5, n)
    X1, X2 = np.meshgrid(grid, grid)   # shape (n, n)

    # Vectorised utility over the full grid
    excess = X1 * (r1 - r_free) + X2 * (r2 - r_free)
    var    = X1**2 * sd1**2 + X2**2 * sd2**2 + 2 * rho * X1 * X2 * sd1 * sd2
    sd_    = np.sqrt(np.maximum(var, 0.0))

    total_risky = X1 + X2
    esg_numer = X1 * esg1 + X2 * esg2
    safe_denom = np.where(np.abs(total_risky) < 1e-9, 1.0, total_risky)
    esg_ = np.where(np.abs(total_risky) < 1e-9, 0.0, esg_numer / safe_denom)

    utils = excess - (gamma / 2) * var + theta * (esg_ / 100)

    # Ethical exclusion penalty (vectorised)
    if sin_choice == 1:
        if name1 in excluded:
            utils = np.where(X1 > 0, utils - 1e6 * X1, utils)
        if name2 in excluded:
            utils = np.where(X2 > 0, utils - 1e6 * X2, utils)

    # ESG threshold penalty (vectorised)
    if apply_threshold and threshold > 0:
        below = esg_ < threshold
        utils = np.where(below,
                         utils - penalty_strength * ((threshold - esg_) / 100),
                         utils)

    # ── Optimal (max utility) ──────────────────────────────────────────
    idx_flat = np.argmax(utils)
    oi, oj   = np.unravel_index(idx_flat, utils.shape)
    x1_opt   = float(X1[oi, oj])
    x2_opt   = float(X2[oi, oj])

    # ── Tangency: max Sharpe ──────────────────────────────────────────
    ret_  = X1 * r1 + X2 * r2 + (1 - X1 - X2) * r_free
    with np.errstate(invalid="ignore", divide="ignore"):
        sharpes = np.where(sd_ > 0, (ret_ - r_free) / sd_, 0.0)
    idx_t = np.argmax(sharpes)
    ti, tj = np.unravel_index(idx_t, sharpes.shape)
    x1_tan = float(X1[ti, tj])
    x2_tan = float(X2[ti, tj])

    # ── Minimum variance ──────────────────────────────────────────────
    idx_m = np.argmin(var)
    mi, mj = np.unravel_index(idx_m, var.shape)
    x1_mv  = float(X1[mi, mj])
    x2_mv  = float(X2[mi, mj])

    def _stats(x1, x2):
        ret = portfolio_ret(x1, x2, r1, r2, r_free)
        sd  = portfolio_sd(x1, x2, sd1, sd2, rho)
        esg = portfolio_esg(x1, x2, esg1, esg2)
        sr  = (ret - r_free) / sd if sd > 0 else 0.0
        return ret, sd, esg, sr

    ret_opt, sd_opt, esg_opt, sr_opt = _stats(x1_opt, x2_opt)
    ret_tan, sd_tan, esg_tan, sr_tan = _stats(x1_tan, x2_tan)
    ret_mv,  sd_mv,  esg_mv,  sr_mv  = _stats(x1_mv,  x2_mv)

    # ── Proper efficient frontier: for each target return, find min variance ──
    # Use the full 2-D grid already computed above and extract the lower envelope.
    # For each distinct (risk, return) point, keep the one with lowest variance
    # at each return level — this traces the true parabolic frontier.
    all_rets = (X1 * r1 + X2 * r2 + (1 - X1 - X2) * r_free).ravel()
    all_vars = var.ravel()
    all_x1   = X1.ravel()
    all_x2   = X2.ravel()

    # Bin returns into 200 buckets and pick min-variance portfolio per bucket
    n_bins = 200
    ret_min_v, ret_max_v = all_rets.min(), all_rets.max()
    bin_edges = np.linspace(ret_min_v, ret_max_v, n_bins + 1)
    frontier_x1_list, frontier_x2_list = [], []
    for i in range(n_bins):
        mask = (all_rets >= bin_edges[i]) & (all_rets < bin_edges[i + 1])
        if mask.sum() == 0:
            continue
        best = np.argmin(all_vars[mask])
        idx  = np.where(mask)[0][best]
        frontier_x1_list.append(float(all_x1[idx]))
        frontier_x2_list.append(float(all_x2[idx]))

    frontier_x1 = np.array(frontier_x1_list)
    frontier_x2 = np.array(frontier_x2_list)

    f_ret  = frontier_x1 * r1 + frontier_x2 * r2 + (1 - frontier_x1 - frontier_x2) * r_free
    f_var  = (frontier_x1**2 * sd1**2 + frontier_x2**2 * sd2**2
              + 2 * rho * frontier_x1 * frontier_x2 * sd1 * sd2)
    f_sd   = np.sqrt(np.maximum(f_var, 0.0))
    f_total = frontier_x1 + frontier_x2
    f_esg_numer  = frontier_x1 * esg1 + frontier_x2 * esg2
    f_safe_denom = np.where(np.abs(f_total) < 1e-9, 1.0, f_total)
    f_esg   = np.where(np.abs(f_total) < 1e-9, 0.0, f_esg_numer / f_safe_denom)
    f_utils = (frontier_x1 * (r1 - r_free) + frontier_x2 * (r2 - r_free)
               - (gamma / 2) * f_var + theta * (f_esg / 100))

    # Sort by risk so the plotted curve reads left-to-right
    sort_idx    = np.argsort(f_sd)
    frontier_x1 = frontier_x1[sort_idx]
    frontier_x2 = frontier_x2[sort_idx]
    f_ret       = f_ret[sort_idx]
    f_sd        = f_sd[sort_idx]
    f_esg       = f_esg[sort_idx]
    f_utils     = f_utils[sort_idx]

    return dict(
        # optimal
        x1_optimal=x1_opt,   x2_optimal=x2_opt,
        ret_optimal=ret_opt,  sd_optimal=sd_opt,
        esg_optimal=esg_opt,  sr_optimal=sr_opt,
        rf_weight_optimal=1 - x1_opt - x2_opt,
        # tangency
        x1_tangency=x1_tan,  x2_tangency=x2_tan,
        ret_tangency=ret_tan, sd_tangency=sd_tan,
        esg_tangency=esg_tan, sr_tangency=sr_tan,
        rf_weight_tangency=1 - x1_tan - x2_tan,
        # min variance
        x1_min_var=x1_mv,   x2_min_var=x2_mv,
        ret_min_var=ret_mv,  sd_min_var=sd_mv,
        esg_min_var=esg_mv,  sr_min_var=sr_mv,
        rf_weight_min_var=1 - x1_mv - x2_mv,
        # frontier curve for charts
        frontier_x1=frontier_x1, frontier_x2=frontier_x2,
        frontier_ret=f_ret,  frontier_sd=f_sd,
        frontier_esg=f_esg,  frontier_utils=f_utils,
    )


@st.cache_data(show_spinner=False)
def cached_sensitivity(r1, r2, sd1, sd2, rho, r_free,
                       gamma, theta, esg1, esg2,
                       sin_choice, excluded_tuple, name1, name2,
                       apply_threshold, threshold, penalty_strength):
    excluded = dict(excluded_tuple)

    theta_range = np.linspace(0, 4, 60)
    gamma_range = np.linspace(1, 15, 60)
    theta_grid  = np.linspace(0, 4, 12)
    gamma_grid  = np.linspace(1, 15, 12)

    def opt(t, g):
        res = run_optimisation(r1, r2, sd1, sd2, rho, r_free, g, t,
                               esg1, esg2, sin_choice, excluded, name1, name2,
                               apply_threshold, threshold, penalty_strength, n=50)
        return res["x1_optimal"], res["x2_optimal"]

    sa_x1, sa_x2, sa_risky, sa_esg, sa_sr = [], [], [], [], []
    for t in theta_range:
        x1, x2 = opt(t, gamma)
        sa_x1.append(x1 * 100)
        sa_x2.append(x2 * 100)
        sa_risky.append((x1 + x2) * 100)
        sa_esg.append(portfolio_esg(x1, x2, esg1, esg2))
        sa_sr.append(sharpe_ratio(x1, x2, r1, r2, sd1, sd2, rho, r_free))

    sg_risky, sg_sr = [], []
    for g in gamma_range:
        x1, x2 = opt(theta, g)
        sg_risky.append((x1 + x2) * 100)
        sg_sr.append(sharpe_ratio(x1, x2, r1, r2, sd1, sd2, rho, r_free))

    heatmap_esg   = np.zeros((len(gamma_grid), len(theta_grid)))
    heatmap_risky = np.zeros((len(gamma_grid), len(theta_grid)))
    for i, g in enumerate(gamma_grid):
        for j, t in enumerate(theta_grid):
            x1, x2 = opt(t, g)
            heatmap_esg[i, j]   = portfolio_esg(x1, x2, esg1, esg2)
            heatmap_risky[i, j] = (x1 + x2) * 100

    return (theta_range, gamma_range, theta_grid, gamma_grid,
            np.array(sa_x1), np.array(sa_x2), np.array(sa_risky),
            np.array(sa_esg), np.array(sa_sr),
            np.array(sg_risky), np.array(sg_sr),
            heatmap_esg, heatmap_risky)


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
  <div style="font-size:3rem;line-height:1;">🧞</div>
  <div>
    <p class="hero-title">ESGenie</p>
    <p class="hero-subtitle">Your personalised sustainable investment portfolio advisor</p>
    <span class="hero-badge">🌿 Sustainable Finance · ESG Optimisation · Retail Investing</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# HOW TO USE — immediately after hero
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
        you care about sustainability.
        <br><br>
        Weights <em>x₁</em> and <em>x₂</em> are <strong>unconstrained</strong>: they do not
        need to sum to one. Any remainder is held in (or borrowed from) the risk-free asset,
        just as in the classic mean-variance framework.
      </p>
      <div class="how-to-steps">
        <div class="how-to-step">
          <div class="how-to-step-num">01</div>
          <div class="how-to-step-title">📈 Enter Financial Data</div>
          <div class="how-to-step-desc">Provide expected returns, standard deviations, the correlation between your assets, and a risk-free rate (e.g. the current government bond yield).</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">02</div>
          <div class="how-to-step-title">🧭 Set Risk Profile</div>
          <div class="how-to-step-desc">Choose Conservative, Balanced, or Aggressive. This sets γ — the risk aversion coefficient. A higher γ penalises volatility more heavily and shrinks all risky positions proportionally.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">03</div>
          <div class="how-to-step-title">🌱 Define ESG Priorities</div>
          <div class="how-to-step-desc">Set θ (how much sustainability influences your recommendation) and choose which ESG pillar — Environmental, Social, or Governance — matters most to you.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">04</div>
          <div class="how-to-step-title">🔍 Score & Screen Assets</div>
          <div class="how-to-step-desc">Rate each asset on E, S, and G from 0–100. ESGenie combines these using your pillar weights to produce a single composite ESG score. Optionally exclude controversial sectors.</div>
        </div>
        <div class="how-to-step">
          <div class="how-to-step-num">05</div>
          <div class="how-to-step-title">✨ Run & Explore</div>
          <div class="how-to-step-desc">Click Run Optimisation. ESGenie searches over unconstrained risky weights and finds the combination that maximises your utility. Results are shown across three tabs.</div>
        </div>
      </div>
      <div class="utility-formula">
        <strong>Utility function:</strong><br>
        U(x₁, x₂) = [x₁(r₁−rᶠ) + x₂(r₂−rᶠ)] − (γ/2) · σ²ₚ + θ · (ESGₚ / 100)<br><br>
        <span style="font-size:0.8rem;">
        x₁, x₂ = risky weights (unconstrained; remainder in risk-free) &nbsp;|&nbsp;
        rᶠ = risk-free rate &nbsp;|&nbsp; γ = risk aversion &nbsp;|&nbsp;
        σₚ = portfolio std dev &nbsp;|&nbsp; θ = ESG weight
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
        if st.button(pname, key=f"pre_{pname}", use_container_width=True):
            st.session_state.preset = pname
            st.rerun()

with preset_cols[-1]:
    if st.button("📋 Apple vs BP", use_container_width=True):
        # FIX: also write directly to the widget state keys so names update immediately
        st.session_state.update(dict(
            _name1="Apple", _name2="BP",
            n1="Apple",     n2="BP",        # widget keys for the text inputs
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

# ── 01 Financial Data ─────────────────────────────────────────────────
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

# ── 02 Risk Profile ───────────────────────────────────────────────────
with st.expander("02  —  Risk Profile", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">Your risk profile determines γ, the risk aversion coefficient in the utility function. A higher γ penalises portfolio volatility more heavily and proportionally shrinks all risky positions — doubling γ roughly halves the total allocation to risky assets.</div>', unsafe_allow_html=True)
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
    st.caption(f"γ = {gamma}  ·  Utility: U = [x₁(r₁−rᶠ) + x₂(r₂−rᶠ)] − ({gamma}/2) · σ²ₚ + θ · ESGₚ")

# ── 03 ESG Preferences ────────────────────────────────────────────────
with st.expander("03  —  ESG Preferences", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">θ controls how strongly sustainability influences your recommendation. A higher θ tilts the optimiser toward the higher-ESG asset even at some financial cost. The ESG threshold is enforced independently of θ — even a purely financial investor (θ = 0) can set a minimum ESG floor.</div>', unsafe_allow_html=True)
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

# ── 04 Asset ESG Scores ───────────────────────────────────────────────
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

# ── 05 Ethical Screening ──────────────────────────────────────────────
with st.expander("05  —  Ethical Screening", expanded=False):
    st.markdown('<div class="tip-box" style="margin-bottom:0.85rem;">ESGenie automatically detects assets in controversial sectors — Tobacco, Weapons & Defence, Gambling, and Fossil Fuels. You can exclude them entirely from the portfolio, apply a utility penalty, or proceed without restriction. You can also set a minimum ESG floor below which a utility penalty is applied — this threshold operates independently of θ.</div>', unsafe_allow_html=True)

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

    apply_threshold = use_thr and threshold > 0

    # FIX: penalty_strength is independent of θ so the threshold is enforced even when θ = 0.
    # A fixed value of 0.01 provides a meaningful but not overwhelming penalty per ESG point below threshold.
    penalty_strength = 0.01

# ── Run button ─────────────────────────────────────────────────────────
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
        r1, r2, sd1, sd2, rho, r_free,
        gamma, theta, esg1, esg2,
        sin_choice, excluded, name1, name2,
        apply_threshold, threshold, penalty_strength,
    )

x1_opt = res["x1_optimal"];  x2_opt = res["x2_optimal"];  xrf_opt = res["rf_weight_optimal"]
x1_tan = res["x1_tangency"]; x2_tan = res["x2_tangency"]; xrf_tan = res["rf_weight_tangency"]
x1_mv  = res["x1_min_var"];  x2_mv  = res["x2_min_var"];  xrf_mv  = res["rf_weight_min_var"]

esg_premium = res["sr_tangency"] - res["sr_optimal"]

if theta <= 1:     esg_importance_label = "Low ESG preference"
elif theta <= 2.5: esg_importance_label = "Moderate ESG preference"
else:              esg_importance_label = "High ESG preference"

# Dominant risky asset by weight
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

    st.markdown('<div class="section-header">📐 Recommended Portfolio</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, label, value, delta in [
        (m1, "Expected Return",  f"{res['ret_optimal']*100:.2f}%",  "annualised"),
        (m2, "Risk (Std Dev)",   f"{res['sd_optimal']*100:.2f}%",   "annualised"),
        (m3, "Sharpe Ratio",     f"{res['sr_optimal']:.3f}",        "risk-adjusted"),
        (m4, "ESG Score",        f"{res['esg_optimal']:.1f} / 100", classify_esg(res['esg_optimal'])[0]),
        (m5, "ESG Premium",      f"{esg_premium:+.3f}",             "vs tangency Sharpe"),
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

    # Asset allocation table — now shows unconstrained weights + risk-free
    st.markdown('<div class="section-header">💼 Asset Allocation</div>', unsafe_allow_html=True)
    _, p1 = classify_esg(esg1)
    _, p2 = classify_esg(esg2)
    _, pp = classify_esg(res["esg_optimal"])
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
        <tr>
          <td style="padding:9px 14px;color:var(--text);">Risk-Free Asset</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">{xrf_opt*100:.1f}%</td>
          <td style="text-align:right;padding:9px 14px;color:var(--text);">—</td>
          <td style="text-align:center;padding:9px 14px;">—</td>
        </tr>
        <tr style="border-top:2px solid var(--border);">
          <td style="padding:9px 14px;font-weight:700;color:var(--forest);">Portfolio (weighted risky ESG)</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">100.0%</td>
          <td style="text-align:right;padding:9px 14px;font-weight:700;color:var(--forest);">{res['esg_optimal']:.1f}</td>
          <td style="text-align:center;padding:9px 14px;">{pp}</td>
        </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)

    if xrf_opt > 0.01:
        st.caption(f"ℹ️ {xrf_opt*100:.1f}% of the portfolio is held in the risk-free asset — a natural consequence of unconstrained mean-variance optimisation when risk aversion is high.")
    elif xrf_opt < -0.01:
        st.caption(f"ℹ️ The portfolio is leveraged: {abs(xrf_opt)*100:.1f}% is borrowed at the risk-free rate to fund additional risky exposure.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Three-portfolio comparison
    st.markdown('<div class="section-header">📋 Portfolio Comparison</div>', unsafe_allow_html=True)
    st.caption("How your ESG-optimal recommendation compares to purely financial alternatives.")
    chars_df = pd.DataFrame({
        "Metric": ["Expected Return","Risk (Std Dev)","Sharpe Ratio","ESG Score","ESG Class",
                   f"{name1} weight", f"{name2} weight","Risk-Free weight"],
        f"🟢 Recommended": [
            f"{res['ret_optimal']*100:.2f}%",  f"{res['sd_optimal']*100:.2f}%",
            f"{res['sr_optimal']:.3f}",         f"{res['esg_optimal']:.1f}",
            classify_esg(res['esg_optimal'])[0],
            f"{x1_opt*100:.1f}%", f"{x2_opt*100:.1f}%", f"{xrf_opt*100:.1f}%"],
        f"📐 Tangency": [
            f"{res['ret_tangency']*100:.2f}%",  f"{res['sd_tangency']*100:.2f}%",
            f"{res['sr_tangency']:.3f}",         f"{res['esg_tangency']:.1f}",
            classify_esg(res['esg_tangency'])[0],
            f"{x1_tan*100:.1f}%", f"{x2_tan*100:.1f}%", f"{xrf_tan*100:.1f}%"],
        f"🛡️ Min Variance": [
            f"{res['ret_min_var']*100:.2f}%",   f"{res['sd_min_var']*100:.2f}%",
            f"{res['sr_min_var']:.3f}",          f"{res['esg_min_var']:.1f}",
            classify_esg(res['esg_min_var'])[0],
            f"{x1_mv*100:.1f}%", f"{x2_mv*100:.1f}%", f"{xrf_mv*100:.1f}%"],
    })
    st.dataframe(chars_df, use_container_width=True, hide_index=True)

    if esg_premium > 0:
        st.warning(f"📉 **ESG Premium: {esg_premium:+.3f} Sharpe points** — your ESG preferences reduce risk-adjusted return relative to the purely financial tangency portfolio.")
    else:
        st.success(f"📈 **ESG Premium: {esg_premium:+.3f} Sharpe points** — your ESG preferences align with financial performance. No sacrifice in risk-adjusted return detected.")

    # Recommendation narrative
    st.markdown('<div class="section-header">💬 Why This Portfolio?</div>', unsafe_allow_html=True)
    driver = (
        f"The tilt toward <strong>{dominant}</strong> is partly driven by its stronger ESG score "
        f"({dom_esg:.1f} vs {sec_esg:.1f}), consistent with your {esg_focus_label.lower()} and θ = {theta}."
        if dom_esg > sec_esg else
        f"The tilt toward <strong>{dominant}</strong> is driven primarily by its superior "
        f"risk-return profile rather than ESG performance."
    )
    rf_note = ""
    if abs(xrf_opt) > 0.01:
        rf_note = (
            f" <strong>{xrf_opt*100:.1f}%</strong> is allocated to the risk-free asset, "
            f"reflecting your risk aversion (γ = {gamma}). "
            f"Doubling γ would roughly halve the total risky allocation."
            if xrf_opt > 0 else
            f" The portfolio is <strong>leveraged by {abs(xrf_opt)*100:.1f}%</strong>, "
            f"funded by borrowing at the risk-free rate."
        )
    st.markdown(f"""
    <div class="reco-box">
    Based on your <strong>{risk_label.lower()} risk profile</strong> (γ = {gamma}) and
    <strong>{esg_importance_label.lower()}</strong> (θ = {theta}), ESGenie recommends allocating
    <strong>{x1_opt*100:.1f}% to {name1}</strong>,
    <strong>{x2_opt*100:.1f}% to {name2}</strong>, and
    <strong>{xrf_opt*100:.1f}% to the risk-free asset</strong>.{rf_note}<br><br>{driver}
    </div>
    """, unsafe_allow_html=True)

    if apply_threshold and (esg1 < threshold or esg2 < threshold):
        st.warning(f"One or more assets fell below your minimum ESG threshold of {threshold:.0f}. A utility penalty was applied.")
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
        f"Recommended Allocation (Unconstrained)\n{'-'*40}\n"
        f"  {name1}:        {x1_opt*100:.1f}%\n"
        f"  {name2}:        {x2_opt*100:.1f}%\n"
        f"  Risk-Free Asset: {xrf_opt*100:.1f}%\n\n"
        f"Portfolio Metrics\n{'-'*40}\n"
        f"  Expected Return : {res['ret_optimal']*100:.2f}%\n"
        f"  Risk (Std Dev)  : {res['sd_optimal']*100:.2f}%\n"
        f"  Sharpe Ratio    : {res['sr_optimal']:.3f}\n"
        f"  ESG Score       : {res['esg_optimal']:.1f} / 100  ({classify_esg(res['esg_optimal'])[0]})\n"
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

    # Use the frontier curve produced by run_optimisation
    risk_plot  = res["frontier_sd"]
    ret_plot   = res["frontier_ret"]
    esg_plot   = res["frontier_esg"]
    util_plot  = res["frontier_utils"]
    fx1_plot   = res["frontier_x1"]
    fx2_plot   = res["frontier_x2"]

    theme_text = "#1f3d2b" if not dark_mode else "#e5e7eb"
    chart_bg   = "#ffffff" if not dark_mode else "#0f1720"
    chart_plot = "#f4f8f5" if not dark_mode else "#18212b"
    chart_grid = "#e8f3ec" if not dark_mode else "#2a3441"

    # Plotly frontier
    st.markdown('<div class="section-header">📈 ESG-Efficient Frontier</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-info">Each point on the curve is the minimum-variance portfolio for a given return level, tracing the true parabolic frontier. Points are coloured by portfolio ESG score (green = high ESG, red = low ESG). The ✨ star marks your recommended portfolio. Hover over any point for details.</div>', unsafe_allow_html=True)

    fig_f = go.Figure()
    fig_f.add_trace(go.Scatter(
        x=risk_plot * 100, y=ret_plot * 100, mode="markers",
        marker=dict(color=esg_plot, colorscale="RdYlGn", cmin=0, cmax=100,
                    size=5, opacity=0.85,
                    colorbar=dict(title=dict(text="ESG Score", font=dict(color=theme_text)),
                                  thickness=14, tickfont=dict(color=theme_text))),
        text=[f"{name1}: {a*100:.1f}%  {name2}: {b*100:.1f}%  RF: {(1-a-b)*100:.1f}%<br>"
              f"Return: {r*100:.2f}%  Risk: {sk*100:.2f}%  ESG: {e:.1f}"
              for a, b, r, sk, e in zip(fx1_plot, fx2_plot, ret_plot, risk_plot, esg_plot)],
        hoverinfo="text", showlegend=False,
    ))
    # Capital Market Line from risk-free through tangency
    cml_x = np.linspace(0, max(risk_plot) * 1.2, 100)
    cml_s = (res["ret_tangency"] - r_free) / res["sd_tangency"] if res["sd_tangency"] > 0 else 0
    fig_f.add_trace(go.Scatter(
        x=cml_x * 100, y=(r_free + cml_s * cml_x) * 100,
        mode="lines", line=dict(dash="dash", color="#4a7c59", width=1.5),
        name="Capital Market Line",
    ))
    for sx, ry, label, colour, sym, sz, x1v, x2v in [
        (0,                   r_free,              f"Risk-Free ({r_free*100:.1f}%)", "#4a7c59", "diamond",     10, 0.0,   0.0),
        (res["sd_min_var"],   res["ret_min_var"],   "Min Variance",                  "#7b5ea7", "square",      12, x1_mv, x2_mv),
        (res["sd_tangency"],  res["ret_tangency"],  "Tangency",                      "#2979aa", "triangle-up", 14, x1_tan,x2_tan),
        (res["sd_optimal"],   res["ret_optimal"],   "✨ Recommended",                "#2d5016", "star",        20, x1_opt,x2_opt),
    ]:
        hover = (f"{label}<br>{name1}: {x1v*100:.1f}% | {name2}: {x2v*100:.1f}% | RF: {(1-x1v-x2v)*100:.1f}%<br>"
                 f"Return: {ry*100:.2f}% | Risk: {sx*100:.2f}%")
        fig_f.add_trace(go.Scatter(
            x=[sx * 100], y=[ry * 100], mode="markers+text",
            marker=dict(symbol=sym, color=colour, size=sz, line=dict(color="white", width=1.5)),
            text=[label], textposition="top right",
            textfont=dict(color=theme_text, size=9),
            hovertext=[hover], hoverinfo="text", name=label,
        ))
    fig_f.update_layout(
        xaxis_title="Risk — Standard Deviation (%)",
        yaxis_title="Expected Return (%)",
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

    # Utility vs weight in Asset 1 (along the frontier)
    st.markdown('<div class="section-header">📉 Utility Function vs Portfolio Risk</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-info">Shows how utility varies across frontier portfolios, plotted against portfolio risk (std dev). The ✨ star marks your recommended portfolio — the one that maximises utility given your risk aversion (γ={gamma}) and ESG preference (θ={theta}).</div>', unsafe_allow_html=True)

    if np.all(util_plot == util_plot[0]):
        st.warning("Utility function is flat — check your inputs.")

    opt_scale_idx = np.argmax(util_plot)

    fig_u, ax = plt.subplots(figsize=(10, 4))
    fig_u.patch.set_facecolor(chart_bg)
    ax.set_facecolor(chart_plot)
    for spine in ax.spines.values():
        spine.set_edgecolor("#c8dfc0"); spine.set_linewidth(0.8)
    ax.plot(risk_plot * 100, util_plot, color="#4a7c59", linewidth=2.5, label="Utility U(w)")
    ax.fill_between(risk_plot * 100, util_plot, alpha=0.07, color="#4a7c59")
    ax.axvline(x=risk_plot[opt_scale_idx] * 100, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.scatter(risk_plot[opt_scale_idx] * 100, util_plot[opt_scale_idx],
               marker="*", color="#2d5016", s=250, zorder=5,
               label=f"✨ Recommended: σ={risk_plot[opt_scale_idx]*100:.1f}%")
    ax.set_xlabel("Portfolio Risk — Standard Deviation (%)", color=theme_text)
    ax.set_ylabel("Utility", color=theme_text)
    ax.set_title("Utility Function vs Portfolio Risk (Frontier)", color=theme_text, fontweight="bold")
    ax.tick_params(colors=theme_text)
    ax.legend(fontsize=9, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.25, color=chart_grid)
    fig_u.tight_layout()
    st.pyplot(fig_u)
    plt.close(fig_u)


# ─────────────────────────────────────────────────────────────────────
# TAB 3 — Sensitivity Analysis (cached)
# ─────────────────────────────────────────────────────────────────────
with tab3:

    st.markdown('<div class="section-header">🔬 Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-info">ℹ️ How to read this: higher θ puts more weight on ESG; higher γ reduces total risky exposure (doubling γ roughly halves the total risky allocation). The plots show how your recommended allocation, portfolio ESG score, Sharpe ratio, and total risky exposure respond to changes in each preference. The heatmap shows ESG score across the full (θ, γ) parameter space — your profile is marked with a ✨ star.</div>', unsafe_allow_html=True)

    with st.spinner("🧞 Computing sensitivity across parameter space..."):
        (theta_range, gamma_range, theta_grid, gamma_grid,
         sa_x1, sa_x2, sa_risky,
         sa_esg, sa_sr,
         sg_risky, sg_sr,
         heatmap_esg, heatmap_risky) = cached_sensitivity(
            r1, r2, sd1, sd2, rho, r_free,
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
            "θ":                     f"{t_val:.2f}" + (" ← your θ" if abs(t_val - theta) < 0.25 else ""),
            f"{name1} weight":       f"{sa_x1[idx]:.1f}%",
            f"{name2} weight":       f"{sa_x2[idx]:.1f}%",
            "Total Risky":           f"{sa_risky[idx]:.1f}%",
            "Risk-Free":             f"{100 - sa_risky[idx]:.1f}%",
            "Portfolio ESG":         f"{sa_esg[idx]:.1f}",
            "ESG Class":             classify_esg(sa_esg[idx])[0],
            "Sharpe":                f"{sa_sr[idx]:.3f}",
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
    fig_sa.suptitle("ESGenie — Sensitivity Analysis", fontsize=13, fontweight="bold", color=theme_text)

    # Top-left: Total risky exposure vs θ
    ax = axes[0, 0]
    ax.plot(theta_range, sa_risky, color="#4a7c59", linewidth=2.5, label=f"Total risky ({name1}+{name2})")
    ax.plot(theta_range, sa_x1,    color="#2979aa", linewidth=1.8, linestyle="--", label=f"{name1}")
    ax.plot(theta_range, sa_x2,    color="#7b5ea7", linewidth=1.8, linestyle=":",  label=f"{name2}")
    ax.fill_between(theta_range, sa_risky, alpha=0.07, color="#4a7c59")
    ax.axvline(x=theta, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8, label=f"Your θ = {theta}")
    ax.set_xlabel("ESG Preference (θ)", color=theme_text)
    ax.set_ylabel("Weight (%)", color=theme_text)
    ax.set_title(f"Risky Allocation vs ESG Preference  (γ = {gamma})", color=theme_text, fontweight="bold")
    ax.legend(fontsize=7, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.2, color=chart_grid); ax.set_xlim(0, 4)

    # Top-right: Portfolio ESG vs θ
    ax = axes[0, 1]
    ax.plot(theta_range, sa_esg, color="#6a9e76", linewidth=2.5)
    ax.fill_between(theta_range, sa_esg, alpha=0.07, color="#6a9e76")
    ax.axvline(x=theta, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8, label=f"Your θ = {theta}")
    ax.axhspan(80, 100, alpha=0.07, color="green",  label="High ESG (≥80)")
    ax.axhspan(50,  80, alpha=0.07, color="yellow", label="Moderate ESG (50–80)")
    ax.axhspan(0,   50, alpha=0.07, color="red",    label="Low ESG (<50)")
    ax.set_xlabel("ESG Preference (θ)", color=theme_text)
    ax.set_ylabel("Portfolio ESG Score", color=theme_text)
    ax.set_title(f"ESG Score vs ESG Preference  (γ = {gamma})", color=theme_text, fontweight="bold")
    ax.legend(fontsize=7, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.2, color=chart_grid); ax.set_xlim(0, 4); ax.set_ylim(0, 100)

    # Bottom-left: Total risky exposure vs γ (key audit check: doubling γ halves risky)
    ax = axes[1, 0]
    ax.plot(gamma_range, sg_risky, color="#4a7c59", linewidth=2.5, label="Total risky allocation (%)")
    ax.fill_between(gamma_range, sg_risky, alpha=0.07, color="#4a7c59")
    ax.axvline(x=gamma, color="#2d5016", linestyle="--", linewidth=1.5, alpha=0.8, label=f"Your γ = {gamma}")
    # Annotation: doubling γ line
    ax.axvline(x=gamma * 2, color="#c8dfc0", linestyle=":", linewidth=1.2, alpha=0.6,
               label=f"2×γ = {gamma*2}")
    ax.set_xlabel("Risk Aversion (γ)", color=theme_text)
    ax.set_ylabel("Total Risky Allocation (%)", color=theme_text)
    ax.set_title(f"Total Risky Exposure vs Risk Aversion  (θ = {theta})", color=theme_text, fontweight="bold")
    ax.legend(fontsize=8, labelcolor=theme_text, facecolor=chart_bg, edgecolor="#c8dfc0")
    ax.grid(True, alpha=0.2, color=chart_grid)

    # Bottom-right: ESG score heatmap over (θ, γ) space
    ax = axes[1, 1]
    h_min, h_max = heatmap_esg.min(), heatmap_esg.max()
    im = ax.imshow(heatmap_esg, aspect="auto", origin="lower", cmap="RdYlGn",
                   vmin=h_min, vmax=h_max,
                   extent=[theta_grid[0], theta_grid[-1], gamma_grid[0], gamma_grid[-1]])
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Portfolio ESG Score", color=theme_text)
    cbar.ax.yaxis.set_tick_params(color=theme_text)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=theme_text)
    ax.scatter(theta, gamma, marker="*", color="#2d5016", s=250, zorder=5, label="✨ Your profile")
    ax.set_xlabel("ESG Preference (θ)", color=theme_text)
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
    "This model assumes normally distributed returns, constant correlations, and static ESG scores. "
    "Risky weights are unconstrained — the model may suggest leveraged or short positions that are "
    "not appropriate for all investors. "
    "In practice, ESG ratings differ across providers and financial markets are dynamic. "
    "This app is for educational purposes and does not constitute financial advice."
)
st.caption("ESGenie 🧞 · Sustainable Portfolio Advisor · Built with Streamlit · Sustainable Finance")
