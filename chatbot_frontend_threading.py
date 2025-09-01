import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
# from chatbot_backend import HumanMessage
from chatbot_backend import chatbot,retrieve_all_thread
import uuid

# =========================== Utilities ===========================
#**********************************************************************************************************
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_chat_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_chat_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def get_chat_thread(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    values = state.values   # already a dict
    return values.get("message", [])

# ======================= Session Initialization ===================
#**********************************************************************************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_thread()
add_chat_thread(st.session_state['thread_id'])


# ============================ Sidebar ============================
#**********************************************************************************************************

st.sidebar.title("Chatbot")
if st.sidebar.button(" New Chat"):
    reset_chat()
st.sidebar.header("Chat History")

for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id'] = thread
        messages = get_chat_thread(thread)
        
        temp_message=[]
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_message.append({'role': role, 'content': message.content})
        st.session_state['message_history'] = temp_message

    # st.sidebar.write(f"Thread ID: {thread}")

# ============================ Main UI ============================
#**********************************************************************************************************
for message in st.session_state['message_history']:
    with st.chat_message('role'):
        st.text(message['content'])

#**********************************************************************************************************
user_input=st.chat_input("Type your message here...")
if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    CONFIG={'configurable':{'thread_id':st.session_state['thread_id']},
            "metadata":{"thread_id":st.session_state["thread_id"]},
            "run_name":"chat_turn",
            }
    
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})