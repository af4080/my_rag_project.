import streamlit as st
from agent_system import agent # מייבא את הסוכן שהגדרנו קודם

st.set_page_config(page_title="Project AI Assistant", page_icon="🤖")

st.title("🤖 עוזר הפרויקט החכם")
st.markdown("שאל אותי שאלות על תיעוד הפרויקט, החלטות טכניות או נתונים מובנים.")

# אתחול היסטוריית הצ'אט
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת הודעות קודמות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# קלט מהמשתמש
if prompt := st.chat_input("מה תרצה לדעת?"):
    # הוספת הודעת משתמש להיסטוריה
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # יצירת תשובה מהסוכן
    with st.chat_message("assistant"):
        with st.spinner("הסוכן חושב..."):
            # שימוש ב-agent.query כפי שעשינו ב-agent_system
            response = agent.query(prompt)
            st.markdown(response)
    
    # שמירת תשובת הסוכן
    st.session_state.messages.append({"role": "assistant", "content": str(response)})