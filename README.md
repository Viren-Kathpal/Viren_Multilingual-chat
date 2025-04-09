# Multilingual Chat App

A Streamlit-based real-time multilingual chat app where users can send and receive messages in their preferred languages. Messages are translated automatically using preloaded language models from HuggingFace's Helsinki-NLP collection.

---

## Features

- Multilingual chat with real-time translation

- Stores and displays both sent and received messages per user

- Supports 7 languages with auto-translation using HuggingFace MarianMT models

- Unicode-safe chat storage (chat.json) — no weird character codes

- Translation fallback using English as an intermediate language when direct path fails


---

## How It Works

- Each user enters a unique username and selects:
  - Preferred language
  - Known languages (multi-select)
- Chat UI starts immediately after entering settings
- All previous messages are visible
- New messages are translated if needed
- All chat sessions are saved in JSON files per run

---


## *Supported Languages (7 Total)*
The following languages are fully supported (either directly or via fallback using English):

| Language  | Code |
|-----------|------|
| English   | en   |
| French    | fr   |
| Spanish   | es   |
| Arabic    | ar   |
| Russian   | ru   |
| German    | de   |
| Japanese  | ja   |

> Example: If ru → ja is not directly available, the app will try ru → en → ja instead.




## *Example Users*

| Username | Language  | Code |
|----------|-----------|------|
| Alice    | English   | en   |
| Bob      | French    | fr   |
| Carlos   | Spanish   | es   |
| Diana    | Arabic    | ar   |
| Eva      | Russian   | ru   |
| George   | German    | de   |
| Hiro     | Japanese  | ja   |



