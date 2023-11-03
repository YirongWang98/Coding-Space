import json
import requests
import streamlit as st
import datetime

# Read the following for reference:
# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
# https://docs.streamlit.io/library/api-reference/chat

def run_prompt(model, prompt):
    r = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': prompt
        }
    )
    return [json.loads(row) for row in r.text.splitlines()]

# Using object notation for model selection in the Streamlit sidebar
model_selection = st.sidebar.selectbox(
    'Model',
    (
        'llama2:latest'
    )
)

# Define the function to get documents from the UN Search API
def get_un_documents(search_query):
    API_URL_SEARCH = "https://search.un.org/api/search?"
    params = {
        "sort": "relevance",
        "collection": 'ods',
        "currentPageNumber": 1,
        "languageCode": 'en',
        "q": search_query.replace(' ', '+'),
        "row": 10,  # For example, let's fetch 10 documents per search
    }
    response = requests.get(API_URL_SEARCH, params=params)
    if response.status_code == 200:
        return response.json()['docs']
    else:
        return []

if model_selection:
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history when the app reruns
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Handle user input
    if prompt := st.chat_input(''):
        # Display user message in chat container
        st.chat_message('user').text(f'''
        user@{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}:

        {prompt}
        ''')
        
        # Add user message to chat history
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        
        # Determine if the input is a search query for UN documents
        if prompt.lower().startswith('search:'):  # Assuming the input starts with 'search:' to indicate a search query
            search_query = prompt[len('search:'):].strip()
            # Call the UN Search API function to get documents
            documents = get_un_documents(search_query)
            # Format the documents information for display
            document_list = "\n".join([f"Title: {doc['title']} - URL: {doc['url']}" for doc in documents])
            chat_response = f"Here are the documents related to your search:\n{document_list}"
        else:
            # If not a search query, call the chat API to get a response
            with st.spinner(f'Querying {model_selection}...'):
                response = run_prompt(model_selection, prompt)
            chat_response = ""
            for line in response:
                if not line.get('done', True) and 'response' in line:
                    chat_response += line['response']
        
        # Display the chatbot response in the chat container
        with st.chat_message('chatbot'):
            st.markdown(chat_response)
        
        # Add chatbot response to chat history
        st.session_state.messages.append({'role': 'chatbot', 'content': chat_response})
