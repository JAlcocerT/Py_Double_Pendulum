import streamlit as st
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

# Define the layout
def app_layout():
    st.label('Pendulum 1 Length:')
    L1 = st.number_input('L1', value=1)
    st.label('Pendulum 2 Length:')
    L2 = st.number_input('L2', value=1)
    st.label('Pendulum 1 Mass:')
    m1 = st.number_input('m1', value=1)
    st.label('Pendulum 2 Mass:')
    m2 = st.number_input('m2', value=1)
    st.label('Simulation Time:')
    T = st.number_input('T', value=10)
    st.label('Pendulum 1 Initial Angle:')
    theta1_0 = st.number_input('theta1_0', value=np.pi/4)
    st.label('Pendulum 2 Initial Angle:')
    theta2_0 = st.number_input('theta2_0', value=np.pi/2)
    st.label('Pendulum 1 Initial Angular Velocity:')
    omega1_0 = st.number_input('omega1_0', value=0)
    st.label('Pendulum 2 Initial Angular Velocity:')
    omega2_0 = st.number_input('omega2_0', value=0)
    run_button = st.button('Run Simulation')

    return L1, L2, m1, m2, T, theta1_0, theta2_0, omega1_0, omega2_0, run_button

# Define the simulation function
def simulate_pendulum(L1, L2, m1, m2, T, theta1_0, theta2_0, omega1_0, omega2_0):
    # Your code here for solving the ODE and creating the figure
    # ...

    fig = go.Figure()
    # Add your figure creation code here
    # ...

    return fig

# Streamlit app
def main():
    st.title("Double Pendulum Simulation")

    L1, L2, m1, m2, T, theta1_0, theta2_0, omega1_0, omega2_0, run_button = app_layout()

    if run_button:
        fig = simulate_pendulum(L1, L2, m1, m2, T, theta1_0, theta2_0, omega1_0, omega2_0)
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()
