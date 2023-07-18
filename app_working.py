import streamlit as st
import requests
import json

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
        "model": "claude-v1.3-100k",
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




# Load documents

# Function to present general options
def transversal_options():
    #st.title('Transversal Options')

    # LLM Model
    llm_model = st.selectbox(
        'LLM Model',
        ['ChatGPT', 'Claude'],
        key='model_selectbox'
    )

    # If the user chooses 'ChatGPT', provide options for version
    if llm_model == 'ChatGPT':
        chatgpt_version = st.selectbox(
            'ChatGPT Version',
            ['3.5', '4'], 
            key='gptversion_type_selectbox'
        )

    # Intention
    intention = st.text_area('What is the intention? What do you want to happen? Ex: Prospect Customer books a call, Click on a link, etc.')
    
    # Language
    language = st.selectbox(
        'Which Language?',
        ['English', 'Spanish', 'Portuguese'],
        key='language_selectbox'
    )

    # Audience
    audience = st.selectbox(
        'Who is the audience?',
        ['Exchange', 'Trader', 'Partner', 'Investor', 'Kravata Team', 'Traditional financer', 'Other'],
        key='audience_selectbox'
    )

    # If the user chooses 'Other', provide a text box for them to specify
    if audience == 'Other':
        other_audience = st.text_input('Please specify the audience:')

    # Tone
    tone = st.selectbox(
        'What is the tone?',
        ['Formal', 'Informal', 'Urgent'],
        key='tone_selectbox'
    )

    # Creativity level
    creativity_level = st.number_input('Creativity level', min_value=0.0, max_value=1.0, step=0.1, format="%.1f")

    # Length in words
    length_in_words = st.number_input('How long in words?', min_value=1, value=500, format="%i")


    # Context
    context = st.text_area('Context. Paste any relevant information like previous communications or specific information it is important to take into account')

    return intention, language, audience, tone, length_in_words, context, creativity_level

    

# Function to create the prompt for the content generation
def prompt_creator_content(content_type, social_network, other_social_network, intention, language, audience, tone, word_count, context):
    prompts = f'''Role: You are an AI assistant expert in crafting {content_type} {social_network} {other_social_network} for Kravata and your answers needs to be always in {language}. 
                Your audience is {audience} and your tone should be {tone}, limit your response to a maximum of {word_count} words. No need to write what you are doing or writting anything diferent than your answer. 
                The purpose is {intention}
                Here is some context: {context}
                Task: Craft the content'''

    return prompts

# Function to create the prompt for the communications generation
def prompt_creator_comms(communication_piece_type, other_communication_piece, name_receiver, language, audience, tone, word_count, intention, context):
    prompts = f'''Role: You are an AI assistant expert in crafting {communication_piece_type} {other_communication_piece} for Kravata and your answers needs to be always in {language}. 
                Your audience is {audience} and your tone should be {tone}, limit your response to {word_count} words. No need to write what you are doing or writting anything diferent than your answer. 
                The purpose is {intention} and you are writting to {name_receiver}
                Here is some context: {context}
                Task: Craft the communications piece'''

    return prompts

# Define the pages
def home_page():
    st.title('Home')
    st.write('Welcome to our tool! Here you can create content or create a communications piece. Use the sidebar to navigate between the pages.')


def create_content_page():
    st.title('Create Content')

    # Ask the user what type of content they want to create
    content_type = st.selectbox(
        'What type of content do you want to create?',
        ['Post for Social Networks', 'Post for Newsletter', 'Article', 'Course', 'Deck', 'Brochure', 'Press release'],
        key='content_type_selectbox'
    )

    # If the user chooses 'Post for Social Networks', ask which social network
    social_network = None
    other_social_network = None
    if content_type == 'Post for Social Networks':
        social_network = st.selectbox(
            'Which Social Network?',
            ['Twitter', 'Instagram', 'LinkedIn', 'Facebook', 'TikTok', 'SnapChat', 'Telegram', 'Discord', 'Other'],
            key='social_network_selectbox'
        )

        # If the user chooses 'Other', provide a text box for them to specify
        if social_network == 'Other':
            other_social_network = st.text_input('Which one:')

    intention, language, audience, tone, length_in_words, context, creativity_level = transversal_options()

    if st.button('Create'):
        with st.spinner('Writting...'):
        
            # Create the 'prompts' variable
            prompts = prompt_creator_content(content_type, social_network, other_social_network, intention, language, audience, tone, length_in_words, context)

            # Call the 'send_message()' function with the 'prompts' variable
            result = create_text(prompts, creativity_level)

            # Display the prompt
            st.write(prompts)
            # Display the result
            st.write(result)


def create_communications_piece_page():
    st.title('Create a Communications Piece')

    # Ask the user what type of communication piece they want to create
    communication_piece_type = st.selectbox(
        'What piece of communication do you want to create?',
        ['Email', 'Presentation Letter', 'Instant Message', 'SMS', 'Other'],
        key='communication_piece_type_selectbox'
    )

    # If the user chooses 'Other', provide a text box for them to specify
    other_communication_piece = None
    if communication_piece_type == 'Other':
        other_communication_piece = st.text_input('Which other communications piece:')

    name_receiver = st.text_input('To whom are you writting for?')
    
    intention, language, audience, tone, length_in_words, context, creativity_level = transversal_options()

    if st.button('Create'):
        with st.spinner('Writting...'):
            # Create the 'prompts' variable
            prompts = prompt_creator_comms(communication_piece_type, other_communication_piece, name_receiver, language, audience, tone, length_in_words, intention, context)

            # Call the 'send_message()' function with the 'prompts' variable
            result = create_text(prompts, creativity_level)

            # Display the prompt
            st.write(prompts)
            # Display the result
            st.write(result)

        


# Create a dictionary of pages
pages = {
    'Home': home_page,
    'Create Content': create_content_page,
    'Create a Communications Piece': create_communications_piece_page
}

# Use the sidebar to select the page
page = st.sidebar.selectbox('Choose a page', options=list(pages.keys()))

# Display the selected page with the help of dictionary
pages[page]()
