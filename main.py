'''import streamlit as st
from dotenv import load_dotenv
import os
import requests  # For interacting with Gemini API
from streamlit_chat import message

def init():
    load_dotenv()
    if os.getenv("GEMINI_API_KEY") is None or os.getenv("GEMINI_API_KEY") == "":
        print("GEMINI_API_KEY is not set")
        exit(1)
    else:
        print("GEMINI_API_KEY is set")

def get_gemini_response(prompt, api_key):
    """Send user input to Gemini API and get response"""
    # Placeholder URL, replace with the actual Gemini API endpoint
    url = "https://your-gemini-api-endpoint/v1/chat"  
    
    # Request headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Request data format (update based on Gemini's API specs)
    data = {
        "model": "gemini-model",  # Specify the model if required
        "messages": [{"role": "user", "content": prompt}]
    }

    # Simulate API request (Replace with real API call when endpoint is available)
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            # Adjust the structure based on Gemini's response format
            return response_data['choices'][0]['message']['content']
        else:
            return "Error: Unable to get a response from Gemini API"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    init()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]

    st.set_page_config(page_title="Your Gemini-Powered Chatbot")
    st.header("Your Chatbot with Gemini")

    with st.sidebar:
        user_input = st.text_input("Your message", key="user_input")
    
    if user_input:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            # Get response from Gemini API
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            response = get_gemini_response(user_input, gemini_api_key)

        # Add AI response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat messages
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg['content'], is_user=True, key=str(i) + '_user')
        else:
            message(msg['content'], is_user=False, key=str(i) + '_ai')

# Run the main function
main()


'''











import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import hashlib
st.set_page_config(page_title="Multi-Function AI Bot", layout="centered")
# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB Setup
client = MongoClient(MONGO_URI)
db = client["chatbot"]
user_collection = db["user_details"]

# Hashing password for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check for duplicate user
def user_exists(email):
    return user_collection.find_one({"email": email}) is not None

# Signup Function
def signup(name, email, password):
    if user_exists(email):
        st.warning("User already exists. Please login.")
        return False
    user_collection.insert_one({"name": name, "email": email, "password": hash_password(password)})
    st.success("Signup successful. Please login.")
    return True

# Login Function
def login(email, password):
    user = user_collection.find_one({"email": email, "password": hash_password(password)})
    if user:
        st.session_state["user"] = user
        return True
    else:
        st.warning("Incorrect email or password.")
        return False

# Sidebar for Account Management
st.sidebar.title("Account")
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    action = st.sidebar.radio("Choose Action", ["Signup", "Login"])
    if action == "Signup":
        name = st.sidebar.text_input("Name")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Signup"):
            signup(name, email, password)
    elif action == "Login":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if login(email, password):
                st.sidebar.success("Login successful.")
else:
    st.sidebar.write(f"Welcome, {st.session_state['user']['name']}")
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None

# Home Page after login
st.title("Multi-Function AI Bot")
if st.session_state["user"]:
    module = st.selectbox("Choose a Module", [
        "PDF Question Answering Bot",
        "CSV Bot",
        "Link Summarizer",
        "Text Summarizer",
        "Code Summarizer"
    ])

    # Import and run the chosen module
    if module == "PDF Question Answering Bot":
        import pdfchat
        pdfchat.main()
        
    elif module == "CSV Bot":
        import csvchat
        csvchat.main()

    elif module == "Link Summarizer":
        import link_summ
        link_summ.main()

    elif module == "Text Summarizer":
        import summ_para
        summ_para.main()

    elif module == "Code Summarizer":
        import codechat
        codechat.main()
