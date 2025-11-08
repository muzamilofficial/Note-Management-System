import streamlit as st
import pandas as pd
import os

USER_DATA_FILE = "users.xlsx"
NOTES_DIR = "notes"

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "menu_option" not in st.session_state:
    st.session_state.menu_option = None

# Ensure user file exists
def initialize_user_file():
    if not os.path.exists(USER_DATA_FILE):
        df = pd.DataFrame(columns=["email", "password"])
        df.to_excel(USER_DATA_FILE, index=False)

# Signup
def signup_user(email, password):
    df = pd.read_excel(USER_DATA_FILE)
    if email in df["email"].values:
        return False, "User already exists"
    new_user = pd.DataFrame([[email, password]], columns=["email", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USER_DATA_FILE, index=False)
    return True, "Signup successful"

# Login
def login_user(email, password):
    df = pd.read_excel(USER_DATA_FILE)
    return ((df["email"] == email) & (df["password"] == password)).any()

# Logout
def logout_user():
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.menu_option = None
    st.rerun()

# Notes directory
os.makedirs(NOTES_DIR, exist_ok=True)

# Note functions
def save_note(title, content):
    with open(os.path.join(NOTES_DIR, f"{title}.txt"), "w", encoding="utf-8") as f:
        f.write(content)

def load_note(title):
    with open(os.path.join(NOTES_DIR, f"{title}.txt"), "r", encoding="utf-8") as f:
        return f.read()

def delete_note(title):
    try:
        os.remove(os.path.join(NOTES_DIR, f"{title}.txt"))
        return True
    except FileNotFoundError:
        return False

def list_notes():
    return [f[:-4] for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]

# ------------------- UI -------------------
st.set_page_config(page_title="Notes Manager", layout="wide")
st.title("📝 Personal Notes Manager")
initialize_user_file()

if not st.session_state.logged_in:
    menu = st.sidebar.radio("Choose Option", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    elif menu == "Signup":
        if st.button("Signup"):
            success, message = signup_user(email, password)
            if success:
                st.success(message)
            else:
                st.warning(message)

else:
    st.sidebar.markdown(f"👤 **{st.session_state.user_email}**")
    if st.sidebar.button("🚪 Logout"):
        logout_user()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📂 Notes Menu")

    if st.sidebar.button("📝 Create Note"):
        st.session_state.menu_option = "Create"
    if st.sidebar.button("📖 Read Note"):
        st.session_state.menu_option = "Read"
    if st.sidebar.button("🗑️ Delete Note"):
        st.session_state.menu_option = "Delete"
    if st.sidebar.button("📋 List Notes"):
        st.session_state.menu_option = "List"

    # ----------------- Main Area -----------------
    if st.session_state.menu_option == "Create":
        st.subheader("✍️ Create a New Note")
        title = st.text_input("Note Title")
        content = st.text_area("Note Content")
        if st.button("💾 Save Note"):
            if title and content:
                save_note(title, content)
                st.success(f"Note '{title}' saved!")
            else:
                st.error("Please enter both title and content.")

    elif st.session_state.menu_option == "Read":
        st.subheader("📖 Read Note")
        notes = list_notes()
        if notes:
            selected_note = st.selectbox("Select a note to read", notes)
            if selected_note:
                content = load_note(selected_note)
                st.text_area("Content", content, height=300)
        else:
            st.warning("No notes available.")

    elif st.session_state.menu_option == "Delete":
        st.subheader("🗑️ Delete Note")
        notes = list_notes()
        if notes:
            selected_note = st.selectbox("Select a note to delete", notes)
            if st.button("Delete"):
                if delete_note(selected_note):
                    st.success(f"Note '{selected_note}' deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete note.")
        else:
            st.warning("No notes available to delete.")

    elif st.session_state.menu_option == "List":
        st.subheader("📋 All Notes")
        notes = list_notes()
        if notes:
            st.write(notes)
        else:
            st.info("No notes found.")
