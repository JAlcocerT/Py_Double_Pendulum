import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016],
    'Sales': [100, 120, 80, 110, 90, 95, 115]
}

df = pd.DataFrame(data)

# Streamlit app
def main():
    st.title("Sample Streamlit App with Plotly Line Chart")
    st.write("This app demonstrates a simple line chart using Plotly.")

    # Display the data table
    st.subheader("Data Table")
    st.dataframe(df)
    

    # Create a line chart using Plotly
    fig = px.line(df, x='Year', y='Sales', title='Sales Trend')
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()