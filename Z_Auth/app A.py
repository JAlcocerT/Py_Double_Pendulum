#Streamlit APP: Adding Authentication
##streamlit run app.py

import streamlit as st
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

import streamlit_authenticator as stauth #pip install streamlit_authenticator==v0.1.5
from pathlib import Path
import pickle

# import yaml
# from yaml.loader import SafeLoader

# with open('./Z_Auth/config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)



# --- USER AUTHENTICATION ---
names = ["demo", "anotheruser"]
usernames = ["demo", "anotheruser"]

# load hashed passwords
file_path = Path(__file__).parent / "./Z_Auth/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

cookie_expiry_days=1

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

name, authentication_status, username = authenticator.login("Login", "main")


###


# Define the layout
def app_layout():
    st.title("Double Pendulum Simulation")
    st.markdown("""<style>div.stButton > button:first-child { width: 100%; }</style>""", unsafe_allow_html=True)

    #authenticator.logout("Loagout", "sidebar")
    st.sidebar.title("Simulation's Parameters")

    L1 = st.sidebar.number_input('Pendulum 1 Length:', value=1.0)
    L2 = st.sidebar.number_input('Pendulum 2 Length:', value=1.0)
    m1 = st.sidebar.number_input('Pendulum 1 Mass:', value=1.0)
    m2 = st.sidebar.number_input('Pendulum 2 Mass:', value=1.0)
    g = st.sidebar.number_input('Acceleration due to Gravity:', value=9.81)
    theta1_0 = st.sidebar.number_input('Pendulum 1 Initial Angle:', value=np.pi/4)
    theta2_0 = st.sidebar.number_input('Pendulum 2 Initial Angle:', value=np.pi/2)
    omega1_0 = st.sidebar.number_input('Pendulum 1 Initial Angular Velocity:', value=0.0)
    omega2_0 = st.sidebar.number_input('Pendulum 2 Initial Angular Velocity:', value=0.0)
    dt = st.sidebar.number_input('Simulation Step:' , value=0.01)
    T = st.sidebar.number_input('Simulation Time:', value=10.0)
    run_button = st.sidebar.button('Run Simulation')

    return L1, L2, m1, m2, g, T, dt, theta1_0, theta2_0, omega1_0, omega2_0, run_button

# Define the simulation function
def simulate_pendulum(L1, L2, m1, m2, g, T, dt, theta1_0, theta2_0, omega1_0, omega2_0):
    # Time grid
    #dt = 0.01  # time step (s)
    N = int(T / dt)  # number of steps

    # Define the equations of motion
    def equations(y, t, L1, L2, m1, m2, g):
        theta1, z1, theta2, z2 = y
        c, s = np.cos(theta1 - theta2), np.sin(theta1 - theta2)
        theta1_dot = z1
        z1_dot = (m2 * g * np.sin(theta2) * c - m2 * s * (L1 * z1 ** 2 * c + L2 * z2 ** 2) - (m1 + m2) * g * np.sin(
            theta1)) / L1 / (m1 + m2 * s ** 2)
        theta2_dot = z2
        z2_dot = ((m1 + m2) * (L1 * z1 ** 2 * s - g * np.sin(theta2) + g * np.sin(theta1) * c) + m2 * L2 * z2 ** 2 * s * c) / L2 / (
                    m1 + m2 * s ** 2)
        return theta1_dot, z1_dot, theta2_dot, z2_dot

    # Initial conditions
    y0 = np.array([theta1_0, omega1_0, theta2_0, omega2_0])

    # Time array
    t = np.linspace(0, T, N)

    # Solve ODE
    sol = odeint(equations, y0, t, args=(L1, L2, m1, m2, g))
    theta1, omega1, theta2, omega2 = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]

    # Convert theta to x, y
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)

   # Create plotly figure for path
    path_fig = go.Figure()
    path_fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines', line=dict(color='#3366CC'), name='Pendulum 1 Path'))
    path_fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', line=dict(color='#DC3912'), name='Pendulum 2 Path'))
    path_fig.update_layout(
    title=dict(
        text='Double Pendulum Path',
        x=0.3,  # Centered title
        y=0.9  # Adjust the y position as needed
    ),
    xaxis_title='x',
    yaxis_title='y',
    xaxis=dict(range=[-3, 3]),  # Set the range for x-axis from -3 to 3
    yaxis=dict(range=[-3, 3], scaleanchor="x", scaleratio=1),  # Set the range for y-axis from -3 to 3 and ensure it maintains the same scale as x-axis 
)

    # Create plotly figure for animation
    anim_fig = go.Figure()
    anim_fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines', line=dict(color='#3366CC'), name='Pendulum 1 Path'))
    anim_fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', line=dict(color='#DC3912'), name='Pendulum 2 Path'))
    anim_fig.add_trace(go.Scatter(x=[0], y=[0], mode='lines+markers', line=dict(color='#00CC96'), name='Double Pendulum'))

    # Frame skipping factor
    SKIP = 5  # this will generate every 5th frame

    # Modify the frame generation in the simulate_pendulum function
    frames = [go.Frame(data=[
        go.Scatter(x=x1[:i+1:SKIP], y=y1[:i+1:SKIP], mode='lines', line=dict(color='#3366CC')),
        go.Scatter(x=x2[:i+1:SKIP], y=y2[:i+1:SKIP], mode='lines', line=dict(color='#DC3912')),
        go.Scatter(x=[0, x1[i], x2[i]], y=[0, y1[i], y2[i]], mode='lines+markers', line=dict(color='#00CC96'), name='Double Pendulum')
    ], name=str(i)) for i in range(0, N, SKIP)]  # Added name attribute



    anim_fig.frames = frames
    anim_fig.update_layout(
    title=dict(
        text='Double Pendulum Animation',
        x=0.3,  # Centered title
        y=0.9  # Adjust the y position as needed
    ),
    xaxis_title='x',
    yaxis_title='y',
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[dict(label='Play',
                      method='animate',
                      args=[None, dict(frame=dict(duration=dt*SKIP, redraw=True), fromcurrent=True, transition=dict(duration=0))])]
    )],

    sliders = [dict(
    steps=[dict(
        method='animate',
        args=[[str(i)], dict(mode='immediate', frame=dict(duration=dt*SKIP, redraw=True), transition=dict(duration=0))],
        label=f"{i*dt*SKIP:.2f}") for i in range(0, N, SKIP)],  # Reference the frame names
    active=0,
    transition=dict(duration=0, easing='cubic-in-out')
    )],
    xaxis=dict(range=[-3, 3]),  # Set the range for x-axis from -3 to 3
    yaxis=dict(range=[-3, 3], scaleanchor="x", scaleratio=1),  # Set the range for y-axis from -3 to 3 and ensure it maintains the same scale as x-axis 
    )


    return path_fig, anim_fig

# Streamlit app
def main():
    L1, L2, m1, m2, g, T, dt, theta1_0, theta2_0, omega1_0, omega2_0, run_button = app_layout()

    if run_button:
        path_fig, anim_fig = simulate_pendulum(L1, L2, m1, m2, g, T, dt, theta1_0, theta2_0, omega1_0, omega2_0)

        # Display the path plot
        st.plotly_chart(path_fig)

        # Display the animation plot
        st.plotly_chart(anim_fig)


###


if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- Show must go on ---- #

    if __name__ == '__main__':
        main()
        #st.set_option('server.port', 8501)