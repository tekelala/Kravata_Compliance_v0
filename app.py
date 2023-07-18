import streamlit as st
import requests
import json
import pandas as pd

# Initialize session state variables
if "result" not in st.session_state:
    st.session_state.result = ""

# Claude functions
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
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Something went wrong: {err}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    # Extract Claude's response from the JSON response
    result = response.json()

    # Return Claude's response as a string
    return result['completion']

# Define the pages

def chat_page():
    st.image("Kravata.png", width=400)
    st.title('Chat with Claude')

    # Initialize session state variables if not already done
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ""

    # Creativity level
    creativity_level = st.number_input('Creativity level', min_value=0.0, max_value=1.0, step=0.1, value=0.7, format="%.1f")

    # Display the chat history
    st.write(st.session_state.chat_history)

    # User input field and 'Send' button
    with st.form(key='chat_form'):
        user_input = st.text_input('Type your message:')
        submit_button = st.form_submit_button('Send')

        if submit_button and user_input:
            with st.spinner('Chatting...'):
                # Append user input to chat history
                st.session_state.chat_history += f"Human: {user_input}\n\n"
                # Generate Claude's response
                response = create_text(st.session_state.chat_history + "Assistant:", creativity_level)
                # Append Claude's response to chat history
                st.session_state.chat_history += f"Assistant: {response}\n\n"
                # Rerun the script to update the chat history display
                st.experimental_rerun()

