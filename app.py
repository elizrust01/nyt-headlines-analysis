import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NYT Headlines Analysis 2024-2025",
    page_icon="📰",
    layout="wide"
)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("nyt_clusters_sentiment.csv")
    df["date"] = pd.to_datetime(df["date"])
    cluster_labels = {
        0: "World News & Conflict",
        1: "Lifestyle & Culture",
        2: "Arts & Reviews",
        3: "Trump & Politics",
        4: "Breaking News & Disasters",
        5: "Business & Tech",
        6: "Election Results"
    }
    if "cluster_label" not in df.columns:
        df["cluster_label"] = df["cluster"].map(cluster_labels)
    return df

df = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.title("📰 NYT Headlines 2024-2025")
page = st.sidebar.radio("Navigate", [
    "Overview",
    "Cluster Explorer",
    "Sentiment Over Time",
    "Sentiment by Cluster",
    "Headline Browser"
])

colours = {
    "Positive": "#2ecc71",
    "Negative": "#e74c3c",
    "Neutral":  "#f39c12"
}

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("📰 NYT Headlines Analysis 2024-2025")
    st.markdown("Analysing **96,510 New York Times headlines** using K-Means clustering and VADER sentiment analysis.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Headlines", f"{len(df):,}")
    col2.metric("Clusters", "7")
    col3.metric("Date Range", "2024-2025")
    col4.metric("Avg Sentiment", f"{df['sentiment_score_headline'].mean():.3f}")

    st.subheader("Headlines per Cluster")
    cluster_counts = df["cluster_label"].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(cluster_counts.index, cluster_counts.values, color="#3498db")
    ax.set_xlabel("Number of Headlines")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    st.pyplot(fig)

    st.subheader("Overall Sentiment Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Headline Only**")
        st.dataframe(df["sentiment_label_headline"].value_counts().reset_index())
    with col2:
        st.markdown("**Headline + Abstract**")
        st.dataframe(df["sentiment_label_combined"].value_counts().reset_index())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CLUSTER EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Cluster Explorer":
    st.title("🗂️ Cluster Explorer")

    selected_cluster = st.selectbox("Select a cluster", sorted(df["cluster_label"].unique()))
    cluster_df = df[df["cluster_label"] == selected_cluster]

    col1, col2, col3 = st.columns(3)
    col1.metric("Headlines", f"{len(cluster_df):,}")
    col2.metric("Avg Sentiment (Headline)", f"{cluster_df['sentiment_score_headline'].mean():.3f}")
    col3.metric("Avg Sentiment (Combined)", f"{cluster_df['sentiment_score_combined'].mean():.3f}")

    st.subheader("Sample Headlines")
    sample = cluster_df["headline"].sample(min(10, len(cluster_df)), random_state=42).tolist()
    for h in sample:
        st.markdown(f"• {h}")

    st.subheader("Sentiment Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sentiment_counts = cluster_df["sentiment_label_headline"].value_counts()
    ax.bar(sentiment_counts.index,
           sentiment_counts.values,
           color=[colours.get(l, "gray") for l in sentiment_counts.index])
    ax.set_ylabel("Number of Headlines")
    st.pyplot(fig)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SENTIMENT OVER TIME
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Sentiment Over Time":
    st.title("📈 Sentiment Over Time")

    mode = st.radio("Select sentiment measure",
                    ["Headline Only", "Headline + Abstract"],
                    horizontal=True)

    if mode == "Headline Only":
        score_col = "sentiment_score_headline"
        label_col = "sentiment_label_headline"
    else:
        score_col = "sentiment_score_combined"
        label_col = "sentiment_label_combined"

    monthly = df.groupby([pd.Grouper(key="date", freq="ME"), label_col])[score_col].mean().reset_index()
    monthly.columns = ["month_period", "sentiment_label", "sentiment_score"]

    fig, ax = plt.subplots(figsize=(14, 6))
    for label, group in monthly.groupby("sentiment_label"):
        ax.plot(group["month_period"], group["sentiment_score"],
                label=label, color=colours.get(label, "gray"),
                linewidth=2, marker="o", markersize=3)

    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvspan(pd.Timestamp("2024-10-01"), pd.Timestamp("2024-11-30"),
               alpha=0.1, color="purple", label="US Election Period")
    ax.axvspan(pd.Timestamp("2025-01-01"), pd.Timestamp("2025-02-01"),
               alpha=0.1, color="blue", label="US Inauguration Period")
    ax.set_title(f"NYT Sentiment Over Time — {mode}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Sentiment Score")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SENTIMENT BY CLUSTER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Sentiment by Cluster":
    st.title("📉 Sentiment by Cluster")

    st.subheader("Average Sentiment Score by Cluster")
    sentiment_by_cluster = df.groupby("cluster_label")["sentiment_score_headline"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(sentiment_by_cluster.index, sentiment_by_cluster.values,
                   color=["#e74c3c" if v < 0 else "#2ecc71" for v in sentiment_by_cluster.values])
    ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Average Sentiment Score")
    st.pyplot(fig)

    st.subheader("Sentiment Over Time — Select a Cluster")
    selected = st.selectbox("Select a cluster", sorted(df["cluster_label"].unique()))
    cluster_df = df[df["cluster_label"] == selected].copy()

    monthly_c = cluster_df.groupby([pd.Grouper(key="date", freq="ME"),
                                    "sentiment_label_headline"])["sentiment_score_headline"].mean().reset_index()
    monthly_c.columns = ["month_period", "sentiment_label", "sentiment_score"]

    fig, ax = plt.subplots(figsize=(14, 5))
    for label, group in monthly_c.groupby("sentiment_label"):
        ax.plot(group["month_period"], group["sentiment_score"],
                label=label, color=colours.get(label, "gray"),
                linewidth=2, marker="o", markersize=3)

    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvspan(pd.Timestamp("2024-10-01"), pd.Timestamp("2024-11-30"),
               alpha=0.1, color="purple", label="US Election Period")
    ax.axvspan(pd.Timestamp("2025-01-01"), pd.Timestamp("2025-02-01"),
               alpha=0.1, color="blue", label="US Inauguration Period")
    ax.set_title(f"{selected} — Sentiment Over Time", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Sentiment Score")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — HEADLINE BROWSER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Headline Browser":
    st.title("🔍 Headline Browser")

    col1, col2, col3 = st.columns(3)
    with col1:
        cluster_filter = st.multiselect("Filter by cluster",
                                         sorted(df["cluster_label"].unique()),
                                         default=sorted(df["cluster_label"].unique()))
    with col2:
        sentiment_filter = st.multiselect("Filter by sentiment",
                                           ["Positive", "Neutral", "Negative"],
                                           default=["Positive", "Neutral", "Negative"])
    with col3:
        search = st.text_input("Search headlines", "")

    filtered = df[
        (df["cluster_label"].isin(cluster_filter)) &
        (df["sentiment_label_headline"].isin(sentiment_filter))
    ]

    if search:
        filtered = filtered[filtered["headline"].str.contains(search, case=False, na=False)]

    st.markdown(f"**Showing {len(filtered):,} headlines**")
    st.dataframe(
        filtered[["date", "headline", "cluster_label",
                  "sentiment_label_headline", "sentiment_score_headline"]].sort_values("date", ascending=False),
        use_container_width=True
    )