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
    st.title('Una IA para Compliance de Kravata')

    # Initialize chat history in the session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Creativity level
    creativity_level = 0

    # Display the chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input field
    with st.form(key='chat_form'):
        user_input = st.text_input('Type your message:')
        submit_button = st.form_submit_button('Send')

        if submit_button and user_input:
            # Append user input to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner('The Kravata Compliance AI is working...'):
                # Generate Claude's response
                response = create_text(user_input, creativity_level)

                # Append Claude's response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Rerun the script to update the chat history display
            st.experimental_rerun()

# Running the chat_page function
chat_page()
