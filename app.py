import streamlit as st
import datetime

# 1. Page Configuration (Makes it look legit)
st.set_page_config(page_title="Custom Birthday Game", page_icon="🎮", layout="centered")

# 2. The Setup / UI
st.title("🎮 The Birthday Game Portal")
st.write("Welcome! Our system generates a completely custom, retro-style mini-game based on your exact age and astrological alignment. 🌟")
st.write("To compile your personalized adventure, please verify your birth date below.")

# 3. The "Verification" Input
# Defaulting to a random date so they have to scroll to their actual 1981/1982 birth year
user_dob = st.date_input(
    "Enter your Date of Birth:", 
    value=datetime.date(2000, 1, 1),
    min_value=datetime.date(1920, 1, 1),
    max_value=datetime.date.today()
)

# 4. The Hook & Download
st.markdown("---")
if st.button("Generate My Custom Game 🚀"):
    # We don't actually care what date they entered, we just pretend to process it
    with st.spinner('Compiling personalized assets...'):
        import time
        time.sleep(2) # Fake loading time to make it feel real
        
    st.success(f"🎉 Success! Algorithms calibrated for someone born on {user_dob.strftime('%B %d, %Y')}.")
    
    # 5. The Payload Delivery
    try:
        with open("Birthday_Game.exe", "rb") as file:
            st.download_button(
                label="🎁 Click Here to Download 'Birthday_Game.exe'",
                data=file,
                file_name="birthday_surprise.exe",
                mime="application/octet-stream"
            )
        
        # A little psychological priming for Windows Defender
        st.info("💡 **Installation Note:** Because this is a custom-generated indie game, Windows Defender might show a 'SmartScreen' warning. Just click **'More info'** and **'Run anyway'** to start your adventure!")
        
    except FileNotFoundError:
        st.error("🚨 System Error: The game payload (`Birthday_Game.exe`) is missing from the server directory.")
