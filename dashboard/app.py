import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Indian Air Quality Dashboard",
    layout="wide"
)

# ======================================
# LOAD DATA
# ======================================

@st.cache_data
def load_data():
    df = pd.read_csv("../data/cleaned_air_quality.csv")

    df['last_update'] = pd.to_datetime(df['last_update'])

    return df

df = load_data()

# ======================================
# TITLE
# ======================================

st.title("🇮🇳 Indian Air Quality Index Dashboard")

st.markdown(
"""
Interactive dashboard for analyzing air pollution trends
across India.
"""
)

# ======================================
# SIDEBAR
# ======================================

st.sidebar.header("Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df["state"].dropna().unique().tolist())
)

selected_pollutant = st.sidebar.selectbox(
    "Select Pollutant",
    ["All"] + sorted(df["pollutant_id"].dropna().unique().tolist())
)

# ======================================
# FILTER DATA
# ======================================

filtered_df = df.copy()

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["state"] == selected_state
    ]

if selected_pollutant != "All":
    filtered_df = filtered_df[
        filtered_df["pollutant_id"] == selected_pollutant
    ]

# ======================================
# KPI CARDS
# ======================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        len(filtered_df)
    )

with col2:
    st.metric(
        "States Covered",
        filtered_df["state"].nunique()
    )

with col3:
    st.metric(
        "Cities Covered",
        filtered_df["city"].nunique()
    )

with col4:
    st.metric(
        "Average Pollution",
        round(
            filtered_df["pollutant_avg"].mean(),
            2
        )
    )

# ======================================
# CHART 1
# TOP POLLUTED STATES
# ======================================

st.subheader(
    "States Experience Different Average Pollution Levels"
)

state_pollution = (
    filtered_df.groupby("state")["pollutant_avg"]
    .mean()
    .reset_index()
    .sort_values(
        by="pollutant_avg",
        ascending=False
    )
)

fig1 = px.bar(
    state_pollution,
    x="state",
    y="pollutant_avg",
    title="Average Pollution by State"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================
# CHART 2
# POLLUTANT DISTRIBUTION
# ======================================

col5, col6 = st.columns(2)

with col5:

    pollutant_count = (
        filtered_df["pollutant_id"]
        .value_counts()
        .reset_index()
    )

    pollutant_count.columns = [
        "Pollutant",
        "Count"
    ]

    fig2 = px.pie(
        pollutant_count,
        names="Pollutant",
        values="Count",
        title="Pollutant Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col6:

    category_count = (
        filtered_df["pollution_category"]
        .value_counts()
        .reset_index()
    )

    category_count.columns = [
        "Category",
        "Count"
    ]

    fig3 = px.pie(
        category_count,
        names="Category",
        values="Count",
        title="Pollution Category Share"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ======================================
# CHART 3
# POLLUTANT COMPARISON
# ======================================

st.subheader(
    "Pollutants Contribute Differently to Air Quality"
)

pollutant_avg = (
    filtered_df.groupby("pollutant_id")
    ["pollutant_avg"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    pollutant_avg,
    x="pollutant_id",
    y="pollutant_avg",
    color="pollutant_id",
    title="Average Concentration by Pollutant"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================================
# CHART 4
# CORRELATION HEATMAP
# ======================================

st.subheader(
    "Pollution Metrics Show Strong Relationships"
)

corr = filtered_df[
    [
        "pollutant_min",
        "pollutant_max",
        "pollutant_avg",
        "pollution_range"
    ]
].corr()

fig5 = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ======================================
# ANIMATED PLOTLY CHART
# ======================================

st.subheader(
    "Air Pollution Changes Across Locations Over Time"
)

animated_df = filtered_df.copy()

animated_df["date"] = (
    animated_df["last_update"]
    .dt.date
    .astype(str)
)

fig6 = px.scatter(
    animated_df,
    x="longitude",
    y="latitude",
    size="pollutant_avg",
    color="pollutant_id",
    hover_name="city",
    animation_frame="date",
    title="Animated Air Pollution Movement"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ======================================
# DATA TABLE
# ======================================

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df.head(100)
)

# ======================================
# INSIGHTS
# ======================================

st.subheader("Key Insights")

st.markdown(
"""
### Findings

- PM2.5 and PM10 are among the most monitored pollutants.
- Pollution levels vary significantly across states.
- Some pollutants contribute more heavily to poor air quality.
- Pollution indicators show strong correlations.
- Air quality patterns change over time and location.
"""
)