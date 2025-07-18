import streamlit as st
import subprocess
import time
import ollama

# Calls Ollama

def query_mistral(prompt):
    try:
        response = ollama.chat(
            model='mistral',
            messages=[{"role": "user", "content": prompt}]
        )

        return response['message']['content']
    except Exception as e:
        return f"Error calling Mistral: {e}"

# basic medicine database

medicine_db = {

    "fever": ["paracetamol", "ibuprofen"],
    "cold": ["cetirizine", "levocetirizine"],
    "headache": ["aspirin", "paracetamol"],
    "stomach ache": ["omeprazole", "drotaverine"],
    "cough": ["dextromethorphan", "ambroxol"],

}

st.set_page_config(page_title="MedicBot", layout="centered")
st.title("💊Medic Chatbot🩺")
st.write("Ask about common symptoms, compare medicines, or seek suggestions!")

#User input

user_input = st.text_input("🗣️ You:", "")

if st.button("Send") and user_input:
    last_user_msg=user_input
    # Check for keyword-based response (fallback)
    response = ""
    found = False

    for symptom, meds in medicine_db.items():
        if symptom in user_input.lower():
            found = True
            response = f"For {symptom}, common medicines include: {', '.join(meds)}."
            break

    # Ask Mistral

    if not found:
        with st.spinner("Consulting MedicBot..."):
            time.sleep(1)
            full_prompt = (
                f"You are a helpful medical assistant. "
                f"Answer the following medical query in a friendly and simple way.\n\n"
                f"User: {user_input}\nAssistant:"

            )

            response = query_mistral(full_prompt)
    last_bot_response=response

#Display 
if user_input:
    st.markdown(f"**👤 You:** {last_user_msg}")
    st.markdown(f"**🤖 MedicBot:** {last_bot_response}")