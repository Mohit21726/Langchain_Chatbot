import streamlit as st
from chatbot_backend import HumanMessage
from chatbot_backend import chatbot


CONFIG={'configurable':{'thread_id':"thread1"}}
#session state 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
for message in st.session_state['message_history']:
    if message['role'] == 'user':
        with st.chat_message('user'):
            st.text(message['content'])
    else:
        with st.chat_message('assistant'):
            st.text(message['content'])
    
user_input=st.chat_input("Type your message here...")
if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    # response = chatbot.invoke({'message':[HumanMessage(content=user_input)]},config=CONFIG)
    with st.chat_message('assistant'):
        # st.text(response['message'][-1].content)
        ai_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'message':[HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})