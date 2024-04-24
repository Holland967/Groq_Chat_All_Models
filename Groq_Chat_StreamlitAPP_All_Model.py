import streamlit as st
from groq import Groq
import os

st.title('Chat with Groq')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'], unsafe_allow_html=True)

client = Groq(api_key=os.environ.get('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'))

model_max_tokens = {
    'llama3-70b-8192': 8192,
    'llama3-8b-8192': 8192,
    'llama2-70b-4096': 4096,
    'mixtral-8x7b-32768': 32768,
    'gemma-7b-it': 8192,
}

with st.sidebar:
    model = st.selectbox('Choose a LLM to chat', ('llama3-70b-8192', 'llama3-8b-8192', 'llama2-70b-4096', 'mixtral-8x7b-32768', 'gemma-7b-it'))
    system_prompt = st.text_area('System Prompt', value='You are a helpful assistant.')
    max_tokens = st.slider('Max Tokens', 1, model_max_tokens[model], model_max_tokens[model], step=1)
    temperature = st.slider('Temperature', 0.00, 2.00, 0.75, step=0.01)
    top_p = st.slider('Top P', 0.00, 1.00, 1.00, step=0.01)

    if st.button('New Chat'):
        st.session_state.messages = []
        st.experimental_rerun()

user_input = st.chat_input('Say something...')

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    messages = [{'role': 'system', 'content': system_prompt}] + st.session_state.messages

    with st.chat_message('user'):
        st.markdown(user_input, unsafe_allow_html=True)

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stop=None,
        stream=False
    )
    response = chat_completion.choices[0].message.content

    with st.chat_message('assistant'):
        st.markdown(response, unsafe_allow_html=True)

    st.session_state.messages.append({'role': 'assistant', 'content': response})
