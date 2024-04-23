# streamlit_app.py
import streamlit as st
import requests

def main():
    st.title("Retrosynthesis Pharma LLM")

    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        # Call the backend API to authenticate
        response = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.sidebar.success("Logged In as: {}".format(username))
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.sidebar.error("Invalid Username or Password")
            st.session_state.logged_in = False

    st.sidebar.title("Register")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")

    if st.sidebar.button("Register"):
        # Call the backend API to register
        response = requests.post("http://localhost:8000/register", json={"username": new_username, "password": new_password})
        if response.status_code == 200:
            st.sidebar.success("Registration Successful. You can now login.")
        else:
            st.sidebar.error("Registration Failed. Please try a different username.")

    if st.session_state.get("logged_in"):
        st.subheader("Predict Reactants from Products")

        product = st.text_input("Enter Product SMILES (e.g., C1=CC=CC=C1)")
        reaction_class = st.text_input("Enter Reaction Class (e.g., Hydrogenation)")

        if st.button("Predict"):
            if not product or not reaction_class:
                st.warning("Please enter both Product SMILES and Reaction Class.")
            else:
                # Call the backend API for prediction
                response = requests.post("http://localhost:8000/predict", json={"product": product, "reaction_class": reaction_class})
                if response.status_code == 200:
                    reactants = response.json()["reactants"]
                    st.success("Predicted Reactants:")
                    for i, reactant in enumerate(reactants[:-1], 1):
                        st.write(f"Reactant {i}: {reactant}")
                    st.write(f"Reactant {len(reactants)}: {reactants[-1]}")
                else:
                    st.error("Failed to predict reactants.")

    else:
        st.warning("Please login to use the app.")

if __name__ == "__main__":
    main()
