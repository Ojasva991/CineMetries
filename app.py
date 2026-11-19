import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="CineMetrics | Movie Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# THEME
# ==========================================================

INDIGO = "#4F46E5"
VIOLET = "#7C3AED"
TEAL = "#0D9488"
AMBER = "#F59E0B"
ROSE = "#E11D48"
GREEN = "#16A34A"
SKY = "#0284C7"
TEXT = "#0F172A"

PROFIT_COLORS = {"Profitable": GREEN, "Loss / break-even": ROSE}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
}

/* ===== GLOBAL ===== */
.stApp { background: #F4F6FB; color: #0F172A; }
.block-container { padding: 1.6rem 2.6rem 2rem 2.6rem; max-width: 1650px; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* ===== SIDEBAR (dark navy) ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1220 0%, #111B33 100%);
    border-right: none;
}
[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.10) !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] [data-testid="stTickBarMin"],
[data-testid="stSidebar"] [data-testid="stTickBarMax"],
[data-testid="stSidebar"] [data-testid="stSliderThumbValue"] {
    color: #E2E8F0 !important;
}

.brand {
    display: flex; align-items: center; gap: 12px;
    padding: 4px 4px 2px 4px;
}
.brand-logo {
    width: 44px; height: 44px; border-radius: 13px;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; box-shadow: 0 6px 16px rgba(79,70,229,0.45);
}
.brand-name { color: #FFFFFF; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; line-height: 1.1; }
.brand-sub  { color: #94A3B8; font-size: 12px; font-weight: 500; }
.side-label {
    color: #64748B; font-size: 11px; font-weight: 700;
    letter-spacing: 1.4px; text-transform: uppercase; margin: 14px 0 4px 2px;
}
.side-foot {
    color: #64748B; font-size: 11.5px; line-height: 1.6;
    border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px; margin-top: 10px;
}
.side-foot b { color: #CBD5E1; }

/* Radio nav as pills */
[data-testid="stSidebar"] .stRadio > div { gap: 6px; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 10px 14px; width: 100%;
    transition: all .15s ease;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(99,102,241,0.18); border-color: rgba(129,140,248,0.4);
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    border-color: transparent; box-shadow: 0 6px 16px rgba(79,70,229,0.35);
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) p { color: #FFFFFF !important; font-weight: 700; }

/* ===== HERO ===== */
.hero {
    background: linear-gradient(120deg, #312E81 0%, #4F46E5 55%, #7C3AED 100%);
    border-radius: 22px; padding: 28px 34px; margin-bottom: 22px;
    box-shadow: 0 14px 34px rgba(79,70,229,0.28);
    position: relative; overflow: hidden;
}
.hero::after {
    content: ""; position: absolute; right: -60px; top: -80px;
    width: 280px; height: 280px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.18), rgba(255,255,255,0));
}
.hero-tag {
    display: inline-block; background: rgba(255,255,255,0.16); color: #E0E7FF;
    font-size: 11px; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase;
    padding: 5px 12px; border-radius: 999px; margin-bottom: 12px;
}
.hero h1 {
    color: #FFFFFF !important; font-size: 34px !important; font-weight: 800 !important;
    letter-spacing: -1px; margin: 0 0 6px 0 !important; padding: 0 !important;
}
.hero p { color: #C7D2FE; font-size: 15px; margin: 0; max-width: 760px; }

/* ===== KPI CARDS ===== */
.kpi {
    background: #FFFFFF; border: 1px solid #E5EAF3; border-radius: 18px;
    padding: 18px 20px; display: flex; align-items: center; gap: 16px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.04); position: relative; overflow: hidden;
    transition: transform .18s ease, box-shadow .18s ease;
}
.kpi::before {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px;
    background: var(--accent);
}
.kpi:hover { transform: translateY(-3px); box-shadow: 0 12px 26px rgba(15,23,42,0.09); }
.kpi-icon {
    width: 50px; height: 50px; border-radius: 14px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 24px;
    background: color-mix(in srgb, var(--accent) 12%, white);
}
.kpi-label { color: #64748B; font-size: 12.5px; font-weight: 600; letter-spacing: .2px; }
.kpi-value { color: #0F172A; font-size: 27px; font-weight: 800; letter-spacing: -0.8px; line-height: 1.15; }

/* ===== SECTION TITLES ===== */
.section-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 19px; font-weight: 800; color: #0F172A; letter-spacing: -0.4px;
    margin: 30px 0 14px 0;
}
.section-title::before {
    content: ""; width: 5px; height: 22px; border-radius: 4px;
    background: linear-gradient(180deg, #4F46E5, #7C3AED);
}

/* ===== CHART & TABLE CARDS ===== */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF; border: 1px solid #E5EAF3; border-radius: 18px;
    padding: 10px; box-shadow: 0 4px 16px rgba(15,23,42,0.04);
}
div[data-testid="stDataFrame"] {
    background: #FFFFFF; border: 1px solid #E5EAF3; border-radius: 14px; overflow: hidden;
}
[data-testid="stCaptionContainer"] { color: #64748B; }

/* ===== INSIGHT CARDS ===== */
.insight {
    background: #FFFFFF; border: 1px solid #E5EAF3; border-radius: 16px;
    padding: 16px 18px; display: flex; gap: 14px; align-items: flex-start;
    box-shadow: 0 4px 14px rgba(15,23,42,0.035); height: 100%;
}
.insight-ico {
    width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0; font-size: 19px;
    display: flex; align-items: center; justify-content: center;
    background: color-mix(in srgb, var(--accent) 13%, white);
}
.insight-title { color: #64748B; font-size: 11.5px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.insight-body  { color: #0F172A; font-size: 15px; font-weight: 600; margin-top: 3px; line-height: 1.4; }

/* ===== MISC ===== */
.stSlider [data-baseweb="slider"] > div > div { background: #4F46E5; }
hr { border-color: #E2E8F0 !important; }
.footer { text-align:center; color:#94A3B8; font-size:12px; padding: 22px 0 6px 0; }
</style>
""", unsafe_allow_html=True)


# ==========================================================
# DATA
# ==========================================================

@st.cache_data
def load_data():
    app_dir = Path(__file__).resolve().parent

    possible_dirs = [app_dir / "dataset" / "processed", app_dir, Path.cwd()]
    possible_dirs.extend(parent / "dataset" / "processed" for parent in app_dir.parents)

    def find(name):
        return next((d / name for d in possible_dirs if (d / name).is_file()), None)

    movies_path = find("movies_cleaned.csv")
    genres_path = find("movie_genres.csv")

    if movies_path is None or genres_path is None:
        return None, None

    movies = pd.read_csv(movies_path)
    genres = pd.read_csv(genres_path)

    movies = (
        movies[movies["status"] == "Released"]
        .dropna(subset=["release_year"])
        .copy()
    )
    movies["release_year"] = movies["release_year"].astype(int)

    movies["profit_status"] = "Unknown"
    has_profit = movies["profit"].notna()
    movies.loc[has_profit & (movies["profit"] > 0), "profit_status"] = "Profitable"
    movies.loc[has_profit & (movies["profit"] <= 0), "profit_status"] = "Loss / break-even"

    genres = genres[genres["id"].isin(movies["id"])]
    return movies, genres


movies, genres = load_data()

if movies is None:
    st.error(
        "Could not find movies_cleaned.csv and movie_genres.csv. "
        "Put them in the same folder as app.py (or in dataset/processed/)."
    )
    st.stop()


# ==========================================================
# HELPERS
# ==========================================================

def money(x):
    if pd.isna(x):
        return "$0"
    if abs(x) >= 1e9:
        return f"${x / 1e9:,.2f}B"
    if abs(x) >= 1e6:
        return f"${x / 1e6:,.1f}M"
    return f"${x:,.0f}"


def chart_layout(fig, height=420):
    fig.update_layout(
        height=height,
        template="plotly_white",
        font=dict(family="Inter, Segoe UI, Arial", color="#334155", size=13),
        title=dict(font=dict(size=18, color=TEXT), x=0.03, xanchor="left"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=30, r=25, t=70, b=40),
        colorway=[INDIGO, TEAL, VIOLET, AMBER, SKY, "#EC4899"],
        legend=dict(bgcolor="rgba(255,255,255,0)", borderwidth=0, font=dict(color="#475569")),
        xaxis=dict(showgrid=True, gridcolor="#EEF2F7", zerolinecolor="#CBD5E1", linecolor="#E2E8F0"),
        yaxis=dict(showgrid=True, gridcolor="#EEF2F7", zerolinecolor="#CBD5E1", linecolor="#E2E8F0"),
        hoverlabel=dict(bgcolor="#0F172A", font_color="#FFFFFF", bordercolor="#0F172A"),
    )
    return fig


def filter_data(use_year=True, use_genre=True):
    df = movies.copy()

    if use_year:
        lo = int(movies["release_year"].min())
        hi = int(movies["release_year"].max())
        years = st.sidebar.slider("Release year", min_value=lo, max_value=hi, value=(lo, hi))
        df = df[df["release_year"].between(*years)]

    if use_genre:
        picked = st.sidebar.multiselect(
            "Genre",
            sorted(genres["genre"].unique()),
            placeholder="All genres",
            key="genre_filter",
        )
        if picked:
            ids = genres[genres["genre"].isin(picked)]["id"].unique()
            df = df[df["id"].isin(ids)]

    if df.empty:
        st.warning("No movies match the selected filters.")
        st.stop()

    return df


def genre_table(df):
    """One row per (movie, genre) for the filtered movies."""
    return genres.merge(df[["id", "rating_clean", "vote_count"]], on="id", how="inner")


def hero(tag, title, subtitle):
    st.markdown(
        f'<div class="hero"><span class="hero-tag">{tag}</span>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def kpi(col, icon, label, value, accent):
    col.markdown(
        f'<div class="kpi" style="--accent:{accent}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def insight(col, icon, title, body, accent=INDIGO):
    col.markdown(
        f'<div class="insight" style="--accent:{accent}">'
        f'<div class="insight-ico">{icon}</div>'
        f'<div><div class="insight-title">{title}</div><div class="insight-body">{body}</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown(
    '<div class="brand"><div class="brand-logo">🎬</div>'
    '<div><div class="brand-name">CineMetrics</div>'
    '<div class="brand-sub">Movie analytics</div></div></div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown('<div class="side-label">Navigate</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigate",
    ["📊  Industry Overview", "🎭  Genre & Audience", "💰  Financial Performance"],
    label_visibility="collapsed",
)

st.sidebar.markdown('<div class="side-label">Filters</div>', unsafe_allow_html=True)


# ==========================================================
# PAGE 1 — INDUSTRY OVERVIEW
# ==========================================================

if "Industry" in page:

    hero("Page 1 of 3", "Movie Industry Overview",
         "Production trends, audience ratings and genre mix across the movie industry.")

    df = filter_data(use_year=True, use_genre=False)

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "🎞️", "Total Movies", f"{df['id'].nunique():,}", INDIGO)
    kpi(c2, "⭐", "Avg Audience Rating", f"{df['rating_clean'].mean():.2f} / 10", AMBER)
    kpi(c3, "⏱️", "Avg Runtime", f"{df['runtime_clean'].mean():.0f} min", TEAL)
    kpi(c4, "💵", "Recorded Revenue", money(df["revenue_clean"].sum()), GREEN)

    section("Trends & Genres")
    left, right = st.columns(2)

    by_year = df.groupby("release_year").size().reset_index(name="movies")

    fig = px.area(
        by_year, x="release_year", y="movies", markers=True,
        title="Movie Releases Over Time",
        labels={"release_year": "Release year", "movies": "Movies"},
    )
    fig.update_traces(line_color=INDIGO, fillcolor="rgba(79,70,229,0.14)")
    left.plotly_chart(chart_layout(fig), width="stretch")
    left.caption("2016-2017 are incomplete in the dataset, so the drop at the end is a data limit, not a real decline.")

    gc = genre_table(df)["genre"].value_counts().reset_index()
    gc.columns = ["genre", "movies"]
    gc = gc.sort_values("movies", ascending=True)

    fig = px.bar(
        gc, x="movies", y="genre", orientation="h", title="Movies by Genre",
        labels={"movies": "Movies", "genre": "Genre"},
        color_discrete_sequence=[INDIGO],
    )
    right.plotly_chart(chart_layout(fig), width="stretch")
    right.caption("A movie with several genres is counted once per genre.")

    section("Industry Snapshot")
    i1, i2, i3 = st.columns(3)

    peak = by_year.loc[by_year["movies"].idxmax()]
    insight(i1, "📈", "Peak release year",
            f"{int(peak['release_year'])} with {int(peak['movies'])} movies", INDIGO)

    top_genre = gc.iloc[-1]
    insight(i2, "🏷️", "Most common genre",
            f"{top_genre['genre']} ({int(top_genre['movies']):,} movies)", TEAL)

    insight(i3, "🗓️", "Dataset coverage",
            f"{df['release_year'].min()} – {df['release_year'].max()}", AMBER)


# ==========================================================
# PAGE 2 — GENRE & AUDIENCE
# ==========================================================

elif "Genre" in page:

    hero("Page 2 of 3", "Genre & Audience Analysis",
         "How audiences rate each genre, which genres dominate, and what movie characteristics matter.")

    df = filter_data(use_year=False, use_genre=True)
    gt = genre_table(df)

    # Show only the selected genres (otherwise co-tagged genres leak in)
    picked = st.session_state.get("genre_filter", [])
    if picked:
        gt = gt[gt["genre"].isin(picked)]

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "🎞️", "Movies Analysed", f"{df['id'].nunique():,}", INDIGO)
    kpi(c2, "⭐", "Avg Rating", f"{df['rating_clean'].mean():.2f} / 10", AMBER)
    kpi(c3, "⏱️", "Avg Runtime", f"{df['runtime_clean'].mean():.0f} min", TEAL)
    kpi(c4, "🗳️", "Avg Votes per Movie", f"{df['vote_count'].mean():,.0f}", VIOLET)

    section("Genre Performance")
    left, right = st.columns(2)

    avg = gt.groupby("genre")["rating_clean"].mean().sort_values().reset_index()

    fig = px.bar(
        avg, x="rating_clean", y="genre", orientation="h",
        title="Average Rating by Genre",
        labels={"rating_clean": "Average rating", "genre": "Genre"},
        color_discrete_sequence=[INDIGO],
    )
    left.plotly_chart(chart_layout(fig), width="stretch")

    cnt = gt.groupby("genre").size().sort_values().reset_index(name="movies")

    fig = px.bar(
        cnt, x="movies", y="genre", orientation="h", title="Movie Count by Genre",
        labels={"movies": "Movies", "genre": "Genre"},
        color_discrete_sequence=[TEAL],
    )
    right.plotly_chart(chart_layout(fig), width="stretch")

    section("Audience Behaviour")
    left, right = st.columns(2)

    fig = px.histogram(
        df.dropna(subset=["rating_clean"]), x="rating_clean", nbins=20,
        title="Audience Rating Distribution",
        color_discrete_sequence=[VIOLET],
        labels={"rating_clean": "Audience rating"},
    )
    fig.update_layout(bargap=0.06, yaxis_title="Movies")
    left.plotly_chart(chart_layout(fig), width="stretch")

    sc = df.dropna(subset=["rating_clean", "runtime_clean"])

    fig = px.scatter(
        sc, x="runtime_clean", y="rating_clean", hover_name="title", opacity=0.5,
        title="Runtime vs Audience Rating",
        labels={"runtime_clean": "Runtime (minutes)", "rating_clean": "Audience rating"},
        color_discrete_sequence=[INDIGO],
    )
    right.plotly_chart(chart_layout(fig), width="stretch")

    section("Audience Insights")

    stats = gt.groupby("genre").agg(avg_rating=("rating_clean", "mean"), movies=("id", "nunique"))
    eligible = stats[stats["movies"] >= 20]
    if eligible.empty:
        eligible = stats

    i1, i2, i3 = st.columns(3)

    best = eligible["avg_rating"].idxmax()
    insight(i1, "🏅", "Highest-rated genre",
            f"{best} (avg {eligible.loc[best, 'avg_rating']:.2f})", AMBER)

    popular = stats["movies"].idxmax()
    insight(i2, "🔥", "Most popular genre",
            f"{popular} ({int(stats.loc[popular, 'movies']):,} movies)", ROSE)

    corr = sc["runtime_clean"].corr(sc["rating_clean"])
    msg = (f"Correlation {corr:.2f}: longer movies tend to be rated slightly higher"
           if corr > 0.1 else f"Correlation {corr:.2f}: runtime has little link to rating")
    insight(i3, "📐", "Runtime vs rating", msg, VIOLET)

    section("Top Rated Movies")

    min_votes = st.slider(
        "Minimum audience votes",
        min_value=0, max_value=5000, value=500, step=50,
        help="Raise the threshold to hide movies with only a few votes.",
    )

    top = (
        df[df["vote_count"] >= min_votes]
        .nlargest(10, "rating_clean")[["title", "rating_clean", "vote_count", "release_year"]]
        .rename(columns={"title": "Movie", "rating_clean": "Rating",
                         "vote_count": "Votes", "release_year": "Year"})
    )
    st.dataframe(top, hide_index=True, width="stretch")


# ==========================================================
# PAGE 3 — FINANCIAL PERFORMANCE
# ==========================================================

else:

    hero("Page 3 of 3", "Financial Performance",
         "Budgets, box-office revenue and profitability for movies with complete financial data.")

    df = filter_data(use_year=True, use_genre=True)

    fin = df[df["financial_data_available"] == "Available"].copy()

    if fin.empty:
        st.warning("No financially complete movies match your filters.")
        st.stop()

    budget = fin["budget_clean"].sum()
    revenue = fin["revenue_clean"].sum()
    profit = fin["profit"].sum()

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "🏗️", "Total Budget", money(budget), AMBER)
    kpi(c2, "💵", "Total Revenue", money(revenue), GREEN)
    kpi(c3, "📈", "Net Profit", money(profit), INDIGO)
    kpi(c4, "🎞️", "Movies Analysed", f"{len(fin):,}", TEAL)

    st.caption(f"Based on {len(fin):,} movies that have both budget and revenue recorded. Net profit = revenue − budget.")

    section("Profitability")
    left, right = st.columns(2)

    ps = fin["profit_status"].value_counts().reset_index()
    ps.columns = ["status", "movies"]

    fig = px.pie(
        ps, names="status", values="movies", hole=0.62,
        title="Profitable vs Loss-making Movies",
        color="status", color_discrete_map=PROFIT_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      marker=dict(line=dict(color="#FFFFFF", width=3)))
    fig.update_layout(showlegend=False)
    left.plotly_chart(chart_layout(fig), width="stretch")

    top = fin.nlargest(10, "revenue_clean").sort_values("revenue_clean", ascending=True)

    fig = px.bar(
        top, x="revenue_clean", y="title", orientation="h",
        title="Top 10 Movies by Revenue",
        labels={"revenue_clean": "Revenue ($)", "title": "Movie"},
        color_discrete_sequence=[INDIGO],
    )
    right.plotly_chart(chart_layout(fig), width="stretch")

    section("Budget vs Revenue")

    scatter_data = fin[(fin["budget_clean"] >= 10_000) & (fin["revenue_clean"] >= 10_000)].copy()

    fig = px.scatter(
        scatter_data, x="budget_clean", y="revenue_clean", color="profit_status",
        hover_name="title", log_x=True, log_y=True, opacity=0.65,
        title="Budget vs Revenue (log scale)",
        labels={"budget_clean": "Budget ($)", "revenue_clean": "Revenue ($)",
                "profit_status": "Result"},
        color_discrete_map=PROFIT_COLORS,
    )
    st.plotly_chart(chart_layout(fig, height=500), width="stretch")
    st.caption("Movies with a recorded budget or revenue under $10,000 are left out of this chart "
               "because they look like data-entry errors.")

    section("Financial Insights")
    i1, i2, i3 = st.columns(3)

    pct = (fin["profit"] > 0).mean() * 100
    insight(i1, "✅", "Profitable movies", f"{pct:.0f}% earned more than their budget", GREEN)

    best_row = fin.loc[fin["profit"].idxmax()]
    insight(i2, "🏆", "Biggest profit", f"{best_row['title']} ({money(best_row['profit'])})", AMBER)

    insight(i3, "💡", "Median budget", f"{money(fin['budget_clean'].median())} per movie", INDIGO)

    section("Highest Profit Movies")

    top_profit = fin.nlargest(10, "profit")[["title", "budget_clean", "revenue_clean", "profit"]].copy()
    for c in ["budget_clean", "revenue_clean", "profit"]:
        top_profit[c] = top_profit[c] / 1e6
    top_profit = top_profit.rename(columns={
        "title": "Movie", "budget_clean": "Budget", "revenue_clean": "Revenue", "profit": "Profit"})

    st.dataframe(
        top_profit, hide_index=True, width="stretch",
        column_config={
            "Budget": st.column_config.NumberColumn("Budget ($M)", format="$%.0fM"),
            "Revenue": st.column_config.NumberColumn("Revenue ($M)", format="$%.0fM"),
            "Profit": st.column_config.NumberColumn("Profit ($M)", format="$%.0fM"),
        },
    )


# ==========================================================
# SIDEBAR FOOTER + PAGE FOOTER
# ==========================================================

st.sidebar.markdown(
    '<div class="side-foot"><b>CineMetrics v2.0</b><br>'
    'Built with Python, Pandas,<br>Plotly &amp; Streamlit</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="footer">🎬 CineMetrics · Movie Industry Analytics Dashboard</div>',
    unsafe_allow_html=True,
)
