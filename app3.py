import streamlit as st
import datetime
import time

# 1. Page Configuration
st.set_page_config(page_title="Neon Drift | Simulation", page_icon="🕹️", layout="centered")

# ==========================================
# 🚨 EDUCATOR BANNER (MUST REMAIN VISIBLE)
# ==========================================
st.error("### ⚠️ CYBERSECURITY SIMULATION ⚠️\n**This is an educational phishing and social engineering demo.** Do not enter real personal information. Any files downloaded from this page are part of a controlled classroom exercise.")
st.markdown("---")

# 2. The "Polished" UI (The Lure)
st.title("🕹️ Neon Drift: Custom Level Generator")
st.write("Welcome to the *Neon Drift* early access portal! Our procedural engine builds a custom, retro-wave cyber level tailored specifically to your astrological alignment and age.")
st.write("Verify your birth date below to compile your personalized executable.")

# 3. The Social Engineering Hook (Manufactured Personalization)
user_dob = st.date_input(
    "Enter your Date of Birth:", 
    value=datetime.date(2000, 1, 1),
    min_value=datetime.date(1920, 1, 1),
    max_value=datetime.date.today()
)

st.markdown("---")

# 4. The Trap (Building false legitimacy with fake loading screens)
if st.button("Generate My Custom Game 🚀"):
    with st.spinner('Accessing procedural engine...'):
        time.sleep(1)
    with st.spinner('Weaving chronological data into level design...'):
        time.sleep(1.5)
    with st.spinner('Bypassing standard compiler for custom executable...'):
        time.sleep(1)
        
    st.success(f"🎉 Success! Unique payload generated for a user born on {user_dob.strftime('%B %d, %Y')}.")
    
    # 5. Payload Delivery
    try:
        # In a real classroom demo, you can link your harmless 'birthday_surprise.exe' here
        with open("birthday_surprise.exe", "rb") as file:
            st.download_button(
                label="🎁 Download Neon_Drift_Custom.exe",
                data=file,
                file_name="Neon_Drift_Custom.exe",
                mime="application/octet-stream"
            )
        
        # 6. The "Bypass Security" Red Flag
        st.warning("💡 **Developer Note:** Because this game is uniquely compiled for you just now, Windows Defender SmartScreen won't recognize it yet. If prompted, click **'More info'** and **'Run anyway'** to launch your game!")
        
    except FileNotFoundError:
        st.error("🚨 Simulation Error: Place your compiled .exe in the same folder as this script to demonstrate the download.")

# ==========================================
# 🧠 EDUCATOR DEBRIEF SECTION
# ==========================================
st.markdown("---")
with st.expander("📚 Educator Debrief: Spot the Red Flags"):
    st.write("""
    **What social engineering tactics were used here?**
    1. **Manufactured Personalization:** By asking for a Date of Birth, the attacker makes the victim feel like the file is special and meant *only* for them, lowering suspicion.
    2. **Fake Processing (The Spinner):** Adding a fake delay makes the "generation" process feel legitimate and technically complex.
    3. **Pre-empting Security (The Developer Note):** The attacker knows Windows Defender will flag the file. By warning the victim *first* and framing it as an "indie developer" quirk, the victim is manipulated into ignoring their operating system's warnings.
    """)
