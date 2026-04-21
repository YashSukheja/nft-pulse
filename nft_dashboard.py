import streamlit as st
import pandas as pd
import altair as alt

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
section[data-testid="stSidebar"] {
    background: #030d08 !important;
    border-right: 1px solid #00ff7733 !important;
}
section[data-testid="stSidebar"] * { color: #a0ffcc !important; }

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
.hero-stat-row { display: flex; gap: 40px; margin-top: 24px; }
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
.nft-card {
    background: #050f09;
    border: 1px solid #1a3d28;
    border-radius: 6px;
    padding: 16px 14px;
    margin-bottom: 12px;
}
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
    margin-bottom: 8px;
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
.card-metric { display: flex; justify-content: space-between; margin-top: 5px; }
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
.score-bar-bg {
    height: 3px;
    background: #0d2416;
    border-radius: 2px;
    overflow: hidden;
    margin-top: 10px;
}
.score-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ff77, #00ffaa);
    border-radius: 2px;
}
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
.stat-cell { background: #050f09; padding: 20px 18px; text-align: center; }
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
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────
raw = [
    ["CryptoPunks",   "ETH", 40.0, 1_200_000, 3700,  "Historical Art",   10, 5,  "OG 10K generative collection. The genesis of NFT culture."],
    ["Bored Ape YC",  "ETH", 12.0, 1_500_000, 5500,  "Exclusive Club",    9, 10, "Membership club with real-world events and celebrity owners."],
    ["Pudgy Penguins","ETH", 10.5,   350_000, 4800,  "IP & Brand",        10, 9,  "Expanding into toys, media, and global consumer products."],
    ["Azuki",         "ETH",  4.5,   400_000, 4300,  "Anime PFP",          8, 7,  "Anime-aesthetic collection backed by a strong manga lore."],
    ["Doodles",       "ETH",  1.5,   300_000, 4500,  "Animation/Music",    7, 6,  "Colorful characters expanding into animation and music."],
    ["Mutant Ape YC", "ETH",  2.0,   550_000, 11500, "BAYC Expansion",     8, 7,  "Serum-mutated BAYC spinoff with the largest holder count."],
    ["CloneX",        "ETH",  0.8,   320_000, 9500,  "3D / Nike Collab",   6, 8,  "RTFKT x Nike 3D avatars built for the digital metaverse."],
    ["DeGods",        "ETH",  1.2,   200_000, 3300,  "Community DAO",      7, 7,  "Culture-first DAO with a deflationary tokenomics model."],
    ["Milady",        "ETH",  3.5,   150_000, 3500,  "Meme / Culture",     8, 4,  "Hyperstition-fuelled cult favourite with extreme meme power."],
    ["Moonbirds",     "ETH",  0.5,   280_000, 5000,  "PFP / Art DAO",      5, 5,  "Pixel owl PFPs with on-chain governance by PROOF Collective."],
]

df = pd.DataFrame(raw, columns=[
    "Collection", "Network", "Floor_ETH", "Volume_ETH",
    "Holders", "Category", "HypeScore", "UtilityScore", "Description"
])
df["Score"] = ((df["HypeScore"] + df["UtilityScore"]) / 2).round(1)
df = df.sort_values("Score", ascending=False).reset_index(drop=True)

# ──────────────────────────────────────────────
# SIDEBAR FILTERS
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Orbitron,monospace;font-size:18px;font-weight:900;
                color:#00ff77;margin-bottom:4px;letter-spacing:2px;'>⬡ NFT PULSE</div>
    <div style='font-family:Share Tech Mono,monospace;font-size:10px;color:#2d6645;
                letter-spacing:3px;margin-bottom:24px;'>MARKET INTELLIGENCE</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    min_floor = st.slider("Min Floor Price (ETH)", 0.0, 40.0, 0.0, 0.5)
    min_utility = st.slider("Min Utility Score", 0, 10, 0, 1)
    sort_col = st.selectbox("Sort By", ["Score", "Volume_ETH", "Floor_ETH", "Holders", "HypeScore", "UtilityScore"])

    st.markdown("---")
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace;font-size:9px;color:#1d4428;
                letter-spacing:1px;line-height:1.8;'>
    DATA IS INDICATIVE<br>NOT FINANCIAL ADVICE
    </div>""", unsafe_allow_html=True)

# Apply filters
df_f = df[
    (df["Floor_ETH"] >= min_floor) &
    (df["UtilityScore"] >= min_utility)
].sort_values(sort_col, ascending=False).reset_index(drop=True)

# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
total_vol = df_f["Volume_ETH"].sum()
avg_floor = df_f["Floor_ETH"].mean() if not df_f.empty else 0
total_holders = df_f["Holders"].sum()
best = df_f.iloc[0]["Collection"] if not df_f.empty else "—"

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-tag">⬡ On-Chain Intelligence Dashboard</div>
  <div class="hero-title">NFT <span>PULSE</span></div>
  <div class="hero-sub">// Blue-chip market scanner · {len(df_f)} collections tracked</div>
  <div class="hero-stat-row">
    <div>
      <div class="hero-stat-val">{total_vol:,.0f}</div>
      <div class="hero-stat-lbl">Total Volume (ETH)</div>
    </div>
    <div>
      <div class="hero-stat-val">{avg_floor:.1f}</div>
      <div class="hero-stat-lbl">Avg Floor (ETH)</div>
    </div>
    <div>
      <div class="hero-stat-val">{total_holders:,}</div>
      <div class="hero-stat-lbl">Total Holders</div>
    </div>
    <div>
      <div class="hero-stat-val">{best}</div>
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
    with cols[i % 5]:
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
          <div class="score-bar-bg">
            <div class="score-bar-fill" style="width:{score_pct}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# STAT STRIP
# ──────────────────────────────────────────────
avg_hype = df_f["HypeScore"].mean() if not df_f.empty else 0
max_holders = df_f["Holders"].max() if not df_f.empty else 0
max_vol = df_f["Volume_ETH"].max() if not df_f.empty else 0

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
    <div class="stat-cell-val">{max_vol:,.0f}</div>
    <div class="stat-cell-lbl">Top Volume ETH</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CHARTS — using Altair (built into Streamlit)
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Market Breakdown</div>', unsafe_allow_html=True)

DARK_CONFIG = {
    "background": "#050f09",
    "view": {"stroke": "#0d2416"},
    "axis": {
        "gridColor": "#0d2416",
        "domainColor": "#0d2416",
        "tickColor": "#0d2416",
        "labelColor": "#4d9966",
        "titleColor": "#4d9966",
        "labelFont": "Share Tech Mono",
        "titleFont": "Share Tech Mono",
        "labelFontSize": 10,
        "titleFontSize": 11,
    },
    "legend": {"labelColor": "#4d9966", "titleColor": "#4d9966", "labelFont": "Share Tech Mono"},
    "title": {"color": "#2d6645", "font": "Share Tech Mono", "fontSize": 11, "anchor": "start"},
}

c1, c2 = st.columns([3, 2])

with c1:
    vol_chart = alt.Chart(df_f, title="TOTAL VOLUME (ETH)").mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=alt.X("Collection:N", sort="-y", axis=alt.Axis(labelAngle=-35)),
        y=alt.Y("Volume_ETH:Q", title="Volume (ETH)"),
        color=alt.Color("Volume_ETH:Q",
            scale=alt.Scale(scheme="greens"), legend=None),
        tooltip=["Collection", "Volume_ETH", "Floor_ETH"]
    ).configure(**DARK_CONFIG).properties(height=280)
    st.altair_chart(vol_chart, use_container_width=True)

with c2:
    holder_chart = alt.Chart(df_f, title="HOLDER DISTRIBUTION").mark_arc(
        innerRadius=60, outerRadius=110
    ).encode(
        theta=alt.Theta("Holders:Q"),
        color=alt.Color("Collection:N",
            scale=alt.Scale(scheme="greens"), legend=alt.Legend(orient="bottom", columns=2)),
        tooltip=["Collection", "Holders"]
    ).configure(**DARK_CONFIG).properties(height=280)
    st.altair_chart(holder_chart, use_container_width=True)

# ── Scatter + Bar row ──
st.markdown('<div class="sec-header">Score Intelligence</div>', unsafe_allow_html=True)

c3, c4 = st.columns([2, 3])

with c3:
    scatter = alt.Chart(df_f, title="HYPE vs UTILITY (size = volume)").mark_circle().encode(
        x=alt.X("HypeScore:Q", scale=alt.Scale(domain=[0, 11]), title="Hype Score"),
        y=alt.Y("UtilityScore:Q", scale=alt.Scale(domain=[0, 11]), title="Utility Score"),
        size=alt.Size("Volume_ETH:Q", scale=alt.Scale(range=[100, 1500]), legend=None),
        color=alt.Color("Collection:N", scale=alt.Scale(scheme="greens"), legend=None),
        tooltip=["Collection", "HypeScore", "UtilityScore", "Volume_ETH", "Category"]
    ).configure(**DARK_CONFIG).properties(height=300)
    st.altair_chart(scatter, use_container_width=True)

with c4:
    df_floor_sorted = df_f.sort_values("Floor_ETH", ascending=False)
    floor_chart = alt.Chart(df_floor_sorted, title="FLOOR PRICE LADDER (ETH)").mark_bar(
        cornerRadiusTopRight=3, cornerRadiusBottomRight=3
    ).encode(
        x=alt.X("Floor_ETH:Q", title="Floor Price (ETH)"),
        y=alt.Y("Collection:N", sort="-x"),
        color=alt.Color("Floor_ETH:Q",
            scale=alt.Scale(scheme="greens"), legend=None),
        tooltip=["Collection", "Floor_ETH", "Score"]
    ).configure(**DARK_CONFIG).properties(height=300)
    st.altair_chart(floor_chart, use_container_width=True)

# ──────────────────────────────────────────────
# FULL DATA TABLE
# ──────────────────────────────────────────────
st.markdown('<div class="sec-header">Full Data Table</div>', unsafe_allow_html=True)

display_df = df_f[["Collection", "Category", "Floor_ETH", "Volume_ETH",
                    "Holders", "HypeScore", "UtilityScore", "Score"]].copy()
display_df.columns = ["Collection", "Category", "Floor Ξ", "Volume Ξ",
                       "Holders", "Hype", "Utility", "Score"]
st.dataframe(
    display_df.style
        .format({"Floor Ξ": "{:.1f}", "Volume Ξ": "{:,.0f}", "Holders": "{:,}", "Score": "{:.1f}"})
        .background_gradient(subset=["Score"], cmap="Greens")
        .background_gradient(subset=["Volume Ξ"], cmap="Greens"),
    use_container_width=True,
    hide_index=True
)

# ──────────────────────────────────────────────
# COLLECTOR PROFILER
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
        "🏛️  Digital Historian — I want legacy assets":   ("CryptoPunks",   "Oldest and most historically significant NFT collection."),
        "🤝  Social Capital — I want VIP access & clout": ("Bored Ape YC",  "Globally recognised status symbol with real member events."),
        "📦  Product Builder — I want real-world IP":     ("Pudgy Penguins","Physical toy lines and active IP licensing program."),
        "🎨  Aesthete — I want art I believe in":         ("Azuki",         "Strong visual identity with expanding manga universe."),
        "🌐  Metaverse Native — I want 3D-ready avatars": ("CloneX",        "RTFKT x Nike 3D avatars designed for digital worlds."),
        "📈  Speculator — I want maximum hype upside":    ("Milady",        "Peak cultural cachet with meme virality and cult energy."),
        "🛠️  Utility Hunter — I want real product value": ("Bored Ape YC",  "Highest utility score — token, events, MAYC airdrops."),
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
# GLOSSARY
# ──────────────────────────────────────────────
with st.expander("⬡  GLOSSARY — Key Terms Explained"):
    glossary = {
        "Floor Price": "The lowest listed price for any NFT in a collection.",
        "Volume (ETH)": "Cumulative ETH traded across all secondary sales.",
        "Holders": "Unique wallet addresses owning at least one NFT.",
        "Hype Score": "Editorial score (1–10) for cultural momentum & virality.",
        "Utility Score": "Editorial score (1–10) for real-world benefits & perks.",
        "Score": "Simple average of Hype + Utility scores.",
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
⬡ NFT PULSE — FOR INFORMATIONAL USE ONLY · NOT FINANCIAL ADVICE
</div>
""", unsafe_allow_html=True)
