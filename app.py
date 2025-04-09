# app.py

import streamlit as st
import os
import json
import time
from datetime import datetime
from utils.translation import translate_message
from utils.language_data import SUPPORTED_LANGUAGES, LANG_CODE_MAP

OUTPUT_BASE = "output"
ACTIVE_USERS_FILE = "active_users.json"
USER_PREFS_FILE = "user_prefs.json"

st.set_page_config(page_title="Multilingual Chat")

# Ensure output folder exists
os.makedirs(OUTPUT_BASE, exist_ok=True)

# Initialize user-related JSON files
for file in [ACTIVE_USERS_FILE, USER_PREFS_FILE]:
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False)

def get_next_output_folder():
    existing = [d for d in os.listdir(OUTPUT_BASE) if d.startswith("output")]
    nums = [int(d.replace("output", "")) for d in existing if d.replace("output", "").isdigit()]
    next_num = max(nums) + 1 if nums else 1
    folder = os.path.join(OUTPUT_BASE, f"output{next_num}")
    os.makedirs(folder, exist_ok=True)
    chat_file = os.path.join(folder, "chat.json")
    if not os.path.exists(chat_file):
        with open(chat_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
    return chat_file

@st.cache_resource
class ChatSession:
    def __init__(self):
        self.chat_file = get_next_output_folder()
        self.messages = self.load_messages()

    def save_message(self, msg):
        self.messages.append(msg)
        with open(self.chat_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

    def load_messages(self):
        try:
            with open(self.chat_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

chat_session = ChatSession()

st.sidebar.title("User Settings")
username = st.sidebar.text_input("Username")
preferred_lang = st.sidebar.selectbox("Preferred Language", SUPPORTED_LANGUAGES)
known_langs = st.sidebar.multiselect("Known Languages", SUPPORTED_LANGUAGES, default=[preferred_lang])
entered = st.sidebar.button("Enter Chat")

if entered and username:
    try:
        with open(ACTIVE_USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = {}

    if username not in users:
        users[username] = True
        with open(ACTIVE_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False)

    with open(USER_PREFS_FILE, "r", encoding="utf-8") as f:
        prefs = json.load(f)

    prefs[username] = {
        "preferred_lang": preferred_lang,
        "known_langs": known_langs
    }

    with open(USER_PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)

    st.session_state["username"] = username
    st.session_state["preferred_lang"] = preferred_lang
    st.session_state["known_langs"] = known_langs
    st.session_state["joined"] = True

if "joined" in st.session_state and st.session_state["joined"]:
    st.title(f"Welcome, {st.session_state['username']}!")

    with open(ACTIVE_USERS_FILE, "r", encoding="utf-8") as f:
        all_users_dict = json.load(f)
    with open(USER_PREFS_FILE, "r", encoding="utf-8") as f:
        user_prefs = json.load(f)

    all_users = list(all_users_dict.keys())
    other_users = [u for u in all_users if u != st.session_state["username"]]

    if not other_users:
        st.info("No other users online. Start chatting — others will see your messages when they join.")

    recipient = st.selectbox("Send message to", other_users) if other_users else None
    message = st.text_input("Your message")
    send = st.button("Send")

    if send and message and recipient:
        now = datetime.utcnow().isoformat()
        original_msg = {
            "type": "sent",
            "sender": st.session_state["username"],
            "recipient": recipient,
            "content": message,
            "timestamp": now
        }
        chat_session.save_message(original_msg)

        sender_lang = LANG_CODE_MAP.get(st.session_state["preferred_lang"], "en")
        recipient_lang = LANG_CODE_MAP.get(user_prefs.get(recipient, {}).get("preferred_lang", "English"), "en")
        translated_content = translate_message(message, sender_lang, recipient_lang)

        received_msg = {
            "type": "received",
            "sender": st.session_state["username"],
            "recipient": recipient,
            "content": translated_content,
            "timestamp": now
        }
        chat_session.save_message(received_msg)

    st.subheader("Chat History")
    messages = chat_session.load_messages()

    for m in messages:
        if st.session_state["username"] in [m["sender"], m["recipient"]]:
            if m["type"] == "sent":
                st.markdown(f"**{m['sender']} → {m['recipient']} (sent):** {m['content']}")
            elif m["type"] == "received" and m["recipient"] == st.session_state["username"]:
                st.markdown(f"**{m['sender']} → {m['recipient']} (received):** {m['content']}")

    time.sleep(5)
    st.experimental_rerun()