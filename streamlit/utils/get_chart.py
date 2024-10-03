import pandas as pd
import plotly.express as px
import streamlit as st


def draw_line_chart(df, x_column, y_column, title, x_label, y_label, color="red"):

    # Convert the x_column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df[x_column]):
        df[x_column] = pd.to_datetime(df[x_column])

    # Create the plot
    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        title=title,
        labels={x_column: x_label, y_column: y_label},
        markers=True,
    )

    fig.update_traces(marker=dict(color=color))

    # Show the plot in Streamlit
    st.plotly_chart(fig)
