import streamlit as st
import requests

# Backend URL (update to your deployed backend)
BACKEND_URL = "https://abcdefg.free.beeceptor.com/ask"

st.title("Firm Q&A Assistant")

# Initialize session state
if "service_account_verified" not in st.session_state:
    st.session_state.service_account_verified = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step 1: Verify service account
if not st.session_state.service_account_verified:
    service_account = st.text_input("Enter your Service Account")

    if st.button("Verify Account"):
        try:
            # Call backend for verification (you can implement /verify endpoint separately)
            response = requests.post(
                BACKEND_URL,
                json={"serviceAccount": service_account, "question": "__verify__"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                st.success(data.get("answer", "Service account verified."))
                st.session_state.service_account_verified = True
                st.session_state.service_account = service_account
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to server: {e}")

# Step 2: Ask questions once service account is verified
else:
    st.subheader(f"Welcome, {st.session_state.service_account}")

    # Chat history display
    for entry in st.session_state.chat_history:
        st.markdown(f"**You:** {entry['question']}")
        st.markdown(f"**Server:** {entry['answer']}")

    # Input for new question
    question = st.text_input("Ask a question:")

    if st.button("Send"):
        if question.strip():
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"serviceAccount": st.session_state.service_account, "question": question},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received")

                    # Save to chat history
                    st.session_state.chat_history.append({"question": question, "answer": answer})

                    # Force refresh to show updated chat
                    st.rerun()
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to server: {e}")
