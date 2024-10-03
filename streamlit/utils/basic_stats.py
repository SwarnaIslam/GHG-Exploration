from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def generate_basic_stats(
    dataset_name, title, type, unit="g CO₂/m²/yr", gas="CO2", df=None
):

    # Read the CSV file
    if df is None:
        df = pd.read_csv(dataset_name)

    # Convert date to pandas date
    df["date"] = pd.to_datetime(df["date"])

    st.title(title)

    # Add date pickers
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input(
            "Start Date",
            min_value=df["date"].min().date(),
            max_value=df["date"].max().date(),
            value=df["date"].min().date(),
            key=f"time_granularity_{title}_1",
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            min_value=df["date"].min().date(),
            max_value=df["date"].max().date(),
            value=df["date"].max().date(),
            key=f"time_granularity_{title}_2",
        )
    with col3:
        # Add a selectbox for time granularity
        time_granularity = st.selectbox(
            "Select time granularity",
            ["Year", "Month"],
            index=min(len(dataset_name) % 2, 1),
            key=f"time_granularity_{title}_3",  # Add a unique key
        )

    # Filter dataframe based on selected date range
    mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
    filtered_df = df.loc[mask]

    # Calculate statistics based on filtered data
    mean = filtered_df["mean"].mean()
    stddev = filtered_df["std"].mean()
    minimum = filtered_df["min"].min()
    maximum = filtered_df["max"].max()
    total = filtered_df["mean"].sum()

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Average {type}", f"{mean:.5f} {unit}")
    col2.metric(f"Max {type}", f"{maximum:.5f} {unit}")
    col3.metric(f"Total {type}", f"{total:.5f} {unit}")

    # Group by year or month based on user selection
    if time_granularity == "Year":
        yearly_avg = (
            filtered_df.groupby(filtered_df["date"].dt.year)["max"].mean().reset_index()
        )
        yearly_avg.columns = ["date", "max"]
    else:
        yearly_avg = (
            filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["max"]
            .mean()
            .reset_index()
        )
        yearly_avg["date"] = yearly_avg["date"].dt.to_timestamp()

    fig_trend = px.line(
        yearly_avg,
        x="date",
        y="max",
        title=f"{gas} {type} Trend Over Selected Period ({time_granularity}ly)",
    )

    st.plotly_chart(fig_trend)


# # Create normal distribution plot (using filtered data)
# x = np.linspace(minimum, maximum, 1000)
# y = (1 / (stddev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / stddev) ** 2)

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Normal Distribution", line=dict(color="blue")))

# # Add vertical lines for statistics
# for value, color, label in [
#     (mean, "green", "Mean"),
#     (mean + stddev, "orange", "Stddev"),
#     (minimum, "red", "Min"),
#     (maximum, "purple", "Max")
# ]:
#     fig.add_vline(x=value, line_dash="dash", line_color=color, annotation_text=f"{label}: {value:.2f}")

# fig.update_layout(
#     title="Normal Distribution of CO2 Emission Data (Selected Period)",
#     xaxis_title="Emission (g CO₂/m²/yr)",
#     yaxis_title="Density",
#     height=500,
# )

# st.plotly_chart(fig)
