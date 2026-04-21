import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="NFT PULSE — Live Market Intel",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# GLOBAL CSS — Cyberpunk Terminal Aesthetic
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #020408 !important;
    color: #c8f5e0 !important;
}
.stApp {
    background: radial-gradient(ellipse at 20% 50%, #001a0e 0%, #020408 60%),
                radial-gradient(ellipse at 80% 20%, #00100a 0%, transparent 50%);
    background-color: #020408;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #030d08 !important;
    border-right: 1px solid #00ff7733 !important;
}
section[data-testid="stSidebar"] * {
    color: #a0ffcc !important;
}

/* ── Hero Banner ── */
.hero-wrap {
    position: relative;
    padding: 40px 32px 32px;
    margin-bottom: 8px;
    border: 1px solid #00ff7722;
    border-radius: 4px;
    overflow: hidden;
    background: linear-gradient(135deg, #001208 0%, #000c06 100%);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00ff77, #00ffaa, transparent);
}
.hero-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #00ff77;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 52px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 6px;
}
.hero-title span { color: #00ff77; }
.hero-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: #4d9966;
    letter-spacing: 1px;
}
.hero-stat-row {
    display: flex;
    gap: 40px;
    margin-top: 24px;
}
.hero-stat {
    text-align: left;
}
.hero-stat-val {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #00ff77;
}
.hero-stat-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #4d7a5e;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Section Headers ── */
.sec-header {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 700;
    color: #00ff77;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-left: 3px solid #00ff77;
    padding-left: 12px;
    margin: 28px 0 16px;
}

/* ── NFT Cards ── */
.card-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}
.nft-card {
    background: #050f09;
    border: 1px solid #1a3d28;
    border-radius: 6px;
    padding: 16px 14px;
    position: relative;
    transition: all 0.2s;
    cursor: pointer;
}
.nft-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 6px 6px;
    background: linear-gradient(90deg, #00ff77, transparent);
    opacity: 0;
    transition: opacity 0.2s;
}
.nft-card:hover {
    border-color: #00ff7755;
    background: #071407;
}
.nft-card:hover::after { opacity: 1; }
.card-rank {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #2d6645;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.card-name {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 700;
    color: #e0fff0;
    margin-bottom: 10px;
    line-height: 1.2;
}
.card-cat {
    font-size: 10px;
    color: #00ff7799;
    background: #00ff7711;
    padding: 2px 7px;
    border-radius: 2px;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 1px;
    display: inline-block;
    margin-bottom: 10px;
}
.card-metric {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
}
.card-metric-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: #3d6650;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.card-metric-val {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    color: #a0ffd0;
    font-weight: 700;
}

/* ── Score Bar ── */
.score-bar-wrap { margin-top: 10px; }
.score-bar-bg {
    height: 3px;
    background: #0d2416;
    border-radius: 2px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ff77, #00ffaa);
    border-radius: 2px;
}

/* ── Stat Strip ── */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #0a1f10;
    border: 1px solid #1a3d28;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 24px;
}
.stat-cell {
    background: #050f09;
    padding: 20px 18px;
    text-align: center;
}
.stat-cell-val {
    font-family: 'Orbitron', monospace;
    font-size: 26px;
    font-weight: 900;
    color: #00ff77;
}
.stat-cell-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #3d6650;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Alert Box ── */
.alert-box {
    border: 1px solid #00ff7733;
    background: #00ff770a;
    border-radius: 4px;
    padding: 14px 18px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: #00ff99;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}
.alert-box b { color: #ffffff; }

/* ── Tables ── */
.stDataFrame { border: 1px solid #1a3d28 !important; }
div[data-testid="stDataFrame"] * { font-family: 'Share Tech Mono', monospace !important; font-size: 12px !important; }

/* ── Widgets ── */
.stMultiSelect span, .stSelectbox div { font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important; }
label { font-family: 'Share Tech Mono', monospace !important; font-size: 12px !important; letter-spacing: 1px !important; color: #4d9966 !important; }
.stSlider > div > div { background: #00ff7722 !important; }

/* ── Plotly Charts ── */
.js-plotly-plot { border: 1px solid #0d2416; border-radius: 4px; }

/* ── Hide streamlit branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────
raw = [
    ["CryptoPunks",    "ETH", 40.0, 1_200_000, 3700,  "Historical Art",    10, 5, "OG 10K generative collection. The genesis of NFT culture."],
    ["Bored Ape YC",   "ETH", 12.0, 1_500_000, 5500,  "Exclusive Club",     9, 10, "Membership club with real-world events and celebrity owners."],
    ["Pudgy Penguins",  "ETH", 10.5,   350_000, 4800,  "IP & Brand",        10, 9,  "Expanding into toys, media, and global consumer products."],
    ["Azuki",          "ETH",  4.5,   400_000, 4300,  "Anime PFP",          8, 7,  "Anime-aesthetic collection backed by a strong manga lore."],
    ["Doodles",        "ETH",  1.5,   300_000, 4500,  "Animation/Music",    7, 6,  "Colorful characters expanding into animation and music."],
    ["Mutant Ape YC",  "ETH",  2.0,   550_000, 11500, "BAYC Expansion",     8, 7,  "Serum-mutated BAYC spinoff with the largest holder count."],
    ["CloneX",         "ETH",  0.8,   320_000, 9500,  "3D / Nike Collab",   6, 8,  "RTFKT x Nike 3D avatars built for the digital metaverse."],
    ["DeGods",         "ETH",  1.2,   200_000, 3300,  "Community DAO",      7, 7,  "Culture-first DAO with a deflationary tokenomics model."],
    ["Milady",         "ETH",  3.5,   150_000, 3500,  "Meme / Culture",     8, 4,  "Hyperstition-fuelled cult favourite with extreme meme power."],
    ["Moonbirds",      "ETH",  0.5,   280_000, 5000,  "PFP / Art DAO",      5, 5,  "Pixel owl PFPs with on-chain governance by PROOF Collective."],
]

df = pd.DataFrame(raw, columns=[
    "Collection", "Network", "Floor_ETH", "Volume_ETH",
    "Holders", "Category", "HypeScore", "UtilityScore", "Description"
])
df["Score"] = ((df["HypeScore"] + df["UtilityScore"]) / 2).round(1)
df["Rank"] = df["Score"].rank(ascending=False).astype(int)
df = df.sort_values("Score", ascending=False).reset_index(drop=True)


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Orbitron,monospace;font-size:18px;font-weight:900;color:#00ff77;
                margin-bottom:4px;letter-spacing:2px;'>⬡ NFT PULSE</div>
    <div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#2d6645;
                letter-spacing:3px;margin-bottom:24px;'>MARKET INTELLIGENCE</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#4d9966;letter-spacing:2px;'>FILTER NETWORK</div>", unsafe_allow_html=True)
    net_filter = st.multiselect("", ["ETH"], default=["ETH"], label_visibility="collapsed")

    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#4d9966;letter-spacing:2px;margin-top:16px;'>MIN FLOOR (ETH)</div>", unsafe_allow_html=True)
    min_floor = st.slider("", 0.0, 40.0, 0.0, 0.5, label_visibility="collapsed")

    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#4d9966;letter-spacing:2px;margin-top:16px;'>MIN UTILITY SCORE</div>", unsafe_allow_html=True)
    min_utility = st.slider(" ", 0, 10, 0, 1, label_visibility="collapsed")

    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#4d9966;letter-spacing:2px;margin-top:16px;'>SORT BY</div>", unsafe_allow_html=True)
    sort_col = st.selectbox("  ", ["Score", "Volume_ETH", "Floor_ETH", "Holders", "HypeScore", "UtilityScore"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace;font-size:9px;color:#1d4428;
                letter-spacing:1px;line-height:1.8;'>
    DATA UPDATED MANUALLY<br>
    PRICES IN ETH<br>
    NOT FINANCIAL ADVICE
    </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# APPLY FILTERS
# ──────────────────────────────────────────────
df_f = df[
    (df["Network"].isin(net_filter)) &
    (df["Floor_ETH"] >= min_floor) &
    (df["UtilityScore"] >= min_utility)
].sort_values(sort_col, ascending=False).reset_index(drop=True)


# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
total_vol = df_f["Volume_ETH"].sum()
avg_floor = df_f["Floor_ETH"].mean()
total_holders = df_f["Holders"].sum()
best_score = df_f.iloc[0]["Collection"] if not df_f.empty else "—"

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-tag">⬡ On-Chain Intelligence Dashboard</div>
  <div class="hero-title">NFT <span>PULSE</span></div>
  <div class="hero-sub">// Blue-chip market scanner · {len(df_f)} collections tracked</div>
  <div class="hero-stat-row">
    <div class="hero-stat">
      <div class="hero-stat-val">{total_vol:,.0f}</div>
      <div class="hero-stat-lbl">Total Volume (ETH)</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-val">{avg_floor:.1f}</div>
      <div class="hero-stat-lbl">Avg Floor (ETH)</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-val">{total_holders:,}</div>
      <div class="hero-stat-lbl">Total Holders</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-val">{best_score}</div>
      <div class="hero-stat-lbl">Top Rated</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# COLLECTION CARDS
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Collection Index</div>', unsafe_allow_html=True)

cols = st.columns(5)
for i, (_, row) in enumerate(df_f.head(10).iterrows()):
    score_pct = int(row["Score"] * 10)
    col = cols[i % 5]
    with col:
        st.markdown(f"""
        <div class="nft-card">
          <div class="card-rank">RANK #{i+1}</div>
          <div class="card-name">{row['Collection']}</div>
          <div class="card-cat">{row['Category']}</div>
          <div class="card-metric">
            <span class="card-metric-lbl">Floor</span>
            <span class="card-metric-val">{row['Floor_ETH']} Ξ</span>
          </div>
          <div class="card-metric">
            <span class="card-metric-lbl">Holders</span>
            <span class="card-metric-val">{row['Holders']:,}</span>
          </div>
          <div class="card-metric">
            <span class="card-metric-lbl">Score</span>
            <span class="card-metric-val">{row['Score']}</span>
          </div>
          <div class="score-bar-wrap">
            <div class="score-bar-bg">
              <div class="score-bar-fill" style="width:{score_pct}%"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# STAT STRIP
# ──────────────────────────────────────────────
st.markdown("")
top = df_f.iloc[0] if not df_f.empty else None
avg_hype = df_f["HypeScore"].mean() if not df_f.empty else 0
max_holders = df_f["Holders"].max() if not df_f.empty else 0

st.markdown(f"""
<div class="stat-strip">
  <div class="stat-cell">
    <div class="stat-cell-val">{df_f.shape[0]}</div>
    <div class="stat-cell-lbl">Collections</div>
  </div>
  <div class="stat-cell">
    <div class="stat-cell-val">{avg_hype:.1f}</div>
    <div class="stat-cell-lbl">Avg Hype Score</div>
  </div>
  <div class="stat-cell">
    <div class="stat-cell-val">{max_holders:,}</div>
    <div class="stat-cell-lbl">Peak Holders</div>
  </div>
  <div class="stat-cell">
    <div class="stat-cell-val">{df_f['Volume_ETH'].max():,.0f}</div>
    <div class="stat-cell-lbl">Top Volume (ETH)</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# CHART ROW 1
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Market Breakdown</div>', unsafe_allow_html=True)

CHART_THEME = dict(
    plot_bgcolor="#050f09",
    paper_bgcolor="#050f09",
    font_color="#4d9966",
    font_family="Share Tech Mono",
    gridcolor="#0d2416",
)

c1, c2 = st.columns([3, 2])

with c1:
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(
        x=df_f["Collection"],
        y=df_f["Volume_ETH"],
        marker=dict(
            color=df_f["Volume_ETH"],
            colorscale=[[0, "#003319"], [0.5, "#00994d"], [1, "#00ff77"]],
            showscale=False,
            line=dict(color="#00ff7733", width=1)
        ),
        text=df_f["Volume_ETH"].apply(lambda x: f"{x:,.0f}"),
        textfont=dict(color="#00ff77", size=10, family="Share Tech Mono"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Volume: %{y:,.0f} ETH<extra></extra>"
    ))
    fig_vol.update_layout(
        title=dict(text="TOTAL VOLUME (ETH)", font=dict(size=11, color="#2d6645", family="Share Tech Mono"), x=0.01),
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#2d6645"), tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor="#0d2416", tickfont=dict(size=9, color="#2d6645"), zeroline=False),
        margin=dict(l=10, r=10, t=40, b=60),
        height=300,
        **CHART_THEME
    )
    st.plotly_chart(fig_vol, use_container_width=True, config={"displayModeBar": False})

with c2:
    fig_pie = go.Figure(go.Pie(
        labels=df_f["Collection"],
        values=df_f["Holders"],
        hole=0.6,
        marker=dict(
            colors=px.colors.sequential.Greens[2:],
            line=dict(color="#020408", width=2)
        ),
        textfont=dict(size=9, color="#a0ffd0", family="Share Tech Mono"),
        hovertemplate="<b>%{label}</b><br>Holders: %{value:,}<extra></extra>"
    ))
    fig_pie.add_annotation(
        text=f"<b>{df_f['Holders'].sum():,}</b><br>TOTAL",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=13, color="#00ff77", family="Orbitron")
    )
    fig_pie.update_layout(
        title=dict(text="HOLDER DISTRIBUTION", font=dict(size=11, color="#2d6645", family="Share Tech Mono"), x=0.01),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        height=300,
        **CHART_THEME
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────
# CHART ROW 2 — Radar + Scatter
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Score Intelligence</div>', unsafe_allow_html=True)

c3, c4 = st.columns([2, 3])

with c3:
    # Radar chart for top 5
    top5 = df_f.head(5)
    categories = ["HypeScore", "UtilityScore", "Floor_ETH_norm", "Volume_norm", "Holder_norm"]

    df_radar = top5.copy()
    df_radar["Floor_ETH_norm"]  = (df_radar["Floor_ETH"] / df["Floor_ETH"].max() * 10).round(1)
    df_radar["Volume_norm"]     = (df_radar["Volume_ETH"] / df["Volume_ETH"].max() * 10).round(1)
    df_radar["Holder_norm"]     = (df_radar["Holders"] / df["Holders"].max() * 10).round(1)

    cat_labels = ["Hype", "Utility", "Floor", "Volume", "Community"]
    greens = ["#00ff77", "#00cc55", "#009933", "#006622", "#003311"]

    fig_radar = go.Figure()
    for j, (_, r) in enumerate(df_radar.iterrows()):
        vals = [r["HypeScore"], r["UtilityScore"], r["Floor_ETH_norm"], r["Volume_norm"], r["Holder_norm"]]
        vals += [vals[0]]  # close polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=vals,
            theta=cat_labels + [cat_labels[0]],
            name=r["Collection"],
            line=dict(color=greens[j % len(greens)], width=1.5),
            fill="toself",
            fillcolor=greens[j % len(greens)].replace("ff", "22").replace("cc", "11").replace("99", "0a"),
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="#050f09",
            radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, gridcolor="#0d2416", linecolor="#0d2416"),
            angularaxis=dict(tickfont=dict(size=10, color="#4d9966", family="Share Tech Mono"), gridcolor="#0d2416", linecolor="#0d2416"),
        ),
        showlegend=True,
        legend=dict(font=dict(size=9, color="#4d9966", family="Share Tech Mono"), bgcolor="#00000000"),
        title=dict(text="TOP 5 RADAR", font=dict(size=11, color="#2d6645", family="Share Tech Mono"), x=0.01),
        margin=dict(l=30, r=30, t=40, b=10),
        height=320,
        **CHART_THEME
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

with c4:
    fig_scatter = go.Figure()
    for _, r in df_f.iterrows():
        fig_scatter.add_trace(go.Scatter(
            x=[r["HypeScore"]],
            y=[r["UtilityScore"]],
            mode="markers+text",
            name=r["Collection"],
            text=[r["Collection"]],
            textposition="top center",
            textfont=dict(size=9, color="#4d9966", family="Share Tech Mono"),
            marker=dict(
                size=r["Volume_ETH"] / 50000,
                color="#00ff77",
                opacity=0.7,
                line=dict(color="#00ff7733", width=1)
            ),
            hovertemplate=f"<b>{r['Collection']}</b><br>Hype: {r['HypeScore']}<br>Utility: {r['UtilityScore']}<br>Vol: {r['Volume_ETH']:,} ETH<extra></extra>"
        ))

    fig_scatter.add_shape(type="line", x0=5, x1=5, y0=0, y1=10, line=dict(color="#00ff7722", dash="dot", width=1))
    fig_scatter.add_shape(type="line", x0=0, x1=10, y0=5, y1=5, line=dict(color="#00ff7722", dash="dot", width=1))
    fig_scatter.add_annotation(x=7.5, y=8, text="ELITE ZONE", showarrow=False,
        font=dict(size=9, color="#00ff7744", family="Share Tech Mono"))

    fig_scatter.update_layout(
        title=dict(text="HYPE vs UTILITY  (bubble = volume)", font=dict(size=11, color="#2d6645", family="Share Tech Mono"), x=0.01),
        xaxis=dict(title="Hype Score", range=[0, 11], showgrid=True, gridcolor="#0d2416",
                   tickfont=dict(size=9, color="#2d6645"), titlefont=dict(size=10, color="#2d6645", family="Share Tech Mono")),
        yaxis=dict(title="Utility Score", range=[0, 11], showgrid=True, gridcolor="#0d2416",
                   tickfont=dict(size=9, color="#2d6645"), titlefont=dict(size=10, color="#2d6645", family="Share Tech Mono")),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=40),
        height=320,
        **CHART_THEME
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────
# DETAILED TABLE
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Full Data Table</div>', unsafe_allow_html=True)

display_df = df_f[["Collection", "Category", "Floor_ETH", "Volume_ETH", "Holders", "HypeScore", "UtilityScore", "Score"]].copy()
display_df.columns = ["Collection", "Category", "Floor Ξ", "Volume Ξ", "Holders", "Hype", "Utility", "Score"]
st.dataframe(
    display_df.style
        .format({"Floor Ξ": "{:.1f}", "Volume Ξ": "{:,.0f}", "Holders": "{:,}", "Score": "{:.1f}"})
        .background_gradient(subset=["Score"], cmap="Greens")
        .background_gradient(subset=["Volume Ξ"], cmap="Greens"),
    use_container_width=True,
    hide_index=True
)


# ──────────────────────────────────────────────
# RECOMMENDER TOOL
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Collector Profiler</div>', unsafe_allow_html=True)

r1, r2 = st.columns(2)

with r1:
    profile = st.selectbox("What type of collector are you?", [
        "🏛️  Digital Historian — I want legacy assets",
        "🤝  Social Capital — I want VIP access & clout",
        "📦  Product Builder — I want real-world IP",
        "🎨  Aesthete — I want art I believe in",
        "🌐  Metaverse Native — I want 3D-ready avatars",
        "📈  Speculator — I want maximum hype upside",
        "🛠️  Utility Hunter — I want real product value",
    ])

    profile_map = {
        "🏛️  Digital Historian — I want legacy assets":     ("CryptoPunks",   "Oldest and most historically significant NFT collection."),
        "🤝  Social Capital — I want VIP access & clout":   ("Bored Ape YC",  "Globally recognised status symbol with real member events."),
        "📦  Product Builder — I want real-world IP":       ("Pudgy Penguins","Physical toy lines and active IP licensing program."),
        "🎨  Aesthete — I want art I believe in":           ("Azuki",         "Strong visual identity with expanding manga universe."),
        "🌐  Metaverse Native — I want 3D-ready avatars":   ("CloneX",        "RTFKT x Nike 3D avatars designed for digital worlds."),
        "📈  Speculator — I want maximum hype upside":      ("Milady",        "Peak cultural cachet with meme virality and cult energy."),
        "🛠️  Utility Hunter — I want real product value":   ("Bored Ape YC",  "Highest utility score — token, events, MAYC airdrops."),
    }

    rec_name, rec_reason = profile_map[profile]
    rec_row = df[df["Collection"] == rec_name].iloc[0]

with r2:
    st.markdown(f"""
    <div class="alert-box">
    <b>⬡ RECOMMENDATION</b><br><br>
    <span style="font-size:16px;color:#ffffff;font-family:Orbitron,monospace;">{rec_name}</span><br><br>
    {rec_reason}<br><br>
    Floor: <b>{rec_row['Floor_ETH']} ETH</b> &nbsp;|&nbsp;
    Score: <b>{rec_row['Score']}</b> &nbsp;|&nbsp;
    Category: <b>{rec_row['Category']}</b><br><br>
    <span style="color:#2d6645;font-size:10px;">{rec_row['Description']}</span>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FLOOR PRICE RANKING CHART
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Floor Price Ladder</div>', unsafe_allow_html=True)

df_floor = df_f.sort_values("Floor_ETH", ascending=True)
fig_floor = go.Figure(go.Bar(
    x=df_floor["Floor_ETH"],
    y=df_floor["Collection"],
    orientation="h",
    marker=dict(
        color=df_floor["Floor_ETH"],
        colorscale=[[0, "#001a0e"], [0.5, "#00663d"], [1, "#00ff77"]],
        line=dict(color="#00ff7722", width=1)
    ),
    text=df_floor["Floor_ETH"].apply(lambda x: f"Ξ {x:.1f}"),
    textfont=dict(color="#a0ffd0", size=10, family="Share Tech Mono"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Floor: Ξ %{x:.1f}<extra></extra>"
))
fig_floor.update_layout(
    xaxis=dict(showgrid=True, gridcolor="#0d2416", tickfont=dict(size=9, color="#2d6645"),
               title="Floor Price (ETH)", titlefont=dict(size=10, color="#2d6645", family="Share Tech Mono")),
    yaxis=dict(showgrid=False, tickfont=dict(size=10, color="#a0ffd0", family="Orbitron")),
    margin=dict(l=10, r=80, t=20, b=30),
    height=320,
    **CHART_THEME
)
st.plotly_chart(fig_floor, use_container_width=True, config={"displayModeBar": False})


# ──────────────────────────────────────────────
# GLOSSARY
# ──────────────────────────────────────────────
with st.expander("⬡  GLOSSARY — Key Terms Explained"):
    glossary = {
        "Floor Price": "The lowest listed price for any NFT in a collection. Indicates minimum entry cost.",
        "Volume (ETH)": "Cumulative ETH traded across all secondary sales. Shows market liquidity.",
        "Holders": "Unique wallet addresses that own at least one NFT from the collection.",
        "Hype Score": "Editorial score (1–10) reflecting cultural momentum, social media presence & virality.",
        "Utility Score": "Editorial score (1–10) reflecting real-world benefits: events, tokens, IP rights, etc.",
        "Score": "Simple average of Hype + Utility scores — a quick comparative metric.",
    }
    for term, definition in glossary.items():
        st.markdown(f"""
        <div style='margin-bottom:10px;'>
        <span style='font-family:Orbitron,monospace;font-size:12px;color:#00ff77;'>{term}</span>
        <span style='font-family:Share Tech Mono,monospace;font-size:11px;color:#4d9966;'> — {definition}</span>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div style='margin-top:48px;padding:24px 0;border-top:1px solid #0d2416;
            text-align:center;font-family:Share Tech Mono,monospace;
            font-size:10px;color:#1d4428;letter-spacing:2px;'>
⬡ NFT PULSE — FOR INFORMATIONAL USE ONLY · NOT FINANCIAL ADVICE · DATA IS INDICATIVE
</div>
""", unsafe_allow_html=True)
