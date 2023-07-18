import streamlit as st
import requests
import json

# Function to create text using the Claude API
def create_text(prompt, temperature):
    api_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": st.secrets["API_KEY"]  # Use the API key from Streamlit's secrets
    }

    # Prepare the prompt for Claude
    conversation = f"Human: {prompt}\n\nAssistant:"

    # Define the body of the request
    body = {
        "prompt": conversation,
        "model": "claude-2",
        "temperature": temperature,
        "max_tokens_to_sample": 10000,
        "stop_sequences": ["\n\nHuman:"]
    }

    # Make a POST request to the Claude API
    response = requests.post(api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()

    # Extract Claude's response from the JSON response
    result = response.json()

    # Return Claude's response as a string
    return result['completion']

# Chat page
def chat_page():
    st.title('Chat with Claude')

    # Initialize chat history in the session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ""

    # User input field and 'Send' button
    user_input = st.text_input('Type your message:')
    if st.button('Send'):
        # Append user input to chat history
        st.session_state.chat_history += f"You: {user_input}\n"

        # Creativity level
        creativity_level = 0

        # Generate Claude's response
        response = create_text(user_input, creativity_level)

        # Append Claude's response to chat history
        st.session_state.chat_history += f"Claude: {response}\n"

    # Display the chat history
    st.text_area("Chat History:", value=st.session_state.chat_history, height=200, max_chars=None, key=None)

# Running the chat_page function
chat_page()
