import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# Page Configuration
st.set_page_config(
    page_title="SafeBite - Cloud Allergy Guard", 
    page_icon="🛡️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

# Custom CSS for polished UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #4B5563;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-header">🛡️ SafeBite</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Your intelligent, cloud-powered companion for instant food allergy checks.</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🛡️")
    st.header("Settings & Profile")
    
    with st.expander("🔑 Groq API Key Setup", expanded=True):
        api_key = st.text_input("Enter Key:", type="password", help="Your Groq API key is kept secure in your session.")
        st.markdown("[Get a free key here ↗](https://console.groq.com)")
    
    st.divider()
    
    st.subheader("Dietary Profiles")
    preset = st.selectbox(
        "Choose a Preset Profile:",
        ["Custom", "Severe Nut & Gluten Allergy", "Lactose Intolerant & Vegan"]
    )

    default_allergies = "Peanuts\nGluten\nLactose\nShellfish"
    if preset == "Severe Nut & Gluten Allergy":
        default_allergies = "Peanuts\nTree Nuts\nGluten\nWheat"
    elif preset == "Lactose Intolerant & Vegan":
        default_allergies = "Milk\nLactose\nWhey\nEggs\nHoney\nGelatin"

    allergies = st.text_area("Active Restrictions (one per line):", default_allergies, height=120)
    
    # Scan History Sidebar Section
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Recent Scans")
        for idx, item in enumerate(st.session_state.history[-3:]): 
            st.text(f"{idx+1}. {item}")

# Main Section: Choose input method (Upload vs. Camera)
with st.container(border=True):
    st.subheader("📸 Scan Product Label or Menu")
    input_method = st.radio("Choose input mode:", ["Upload Image File", "Take Photo with Camera"], horizontal=True)

    image = None
    if input_method == "Upload Image File":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    else:
        camera_file = st.camera_input("Take a picture of the label")
        if camera_file is not None:
            image = Image.open(camera_file)

if image is not None:
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        with st.container(border=True):
            st.image(image, caption="Captured/Uploaded Label", use_container_width=True)
            
    with col2:
        with st.container(border=True):
            st.markdown("### Ready to Analyze")
            st.markdown("Click below to check ingredients against your restrictions using cloud vision AI.")
            analyze_btn = st.button("Check Safety 🔍", type="primary")

    if analyze_btn:
        if not api_key:
            st.error("⚠️ Please enter your Groq API Key in the sidebar expander first.")
        else:
            with st.spinner("Analyzing ingredients with cloud AI..."):
                try:
                    # Convert image to base64
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    client = Groq(api_key=api_key)
                    
                    prompt = f"""
                    Analyze this image of an ingredient list or food product. 
                    The person eating this has the following strict allergies/restrictions:
                    {allergies}
                    
                    Does this product contain any of these restricted items, potential traces, or hidden derivatives? 
                    Give a clear 'SAFE' or 'DANGER' verdict at the top, followed by a short, bulleted explanation.
                    """
                    
                    completion = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{img_str}"
                                        }
                                    }
                                ]
                            }
                        ],
                        temperature=0.1
                    )
                    
                    verdict_text = completion.choices[0].message.content
                    
                    # Add to session history log
                    status_label = "🔴 DANGER" if "DANGER" in verdict_text.upper() else "🟢 SAFE"
                    st.session_state.history.append(status_label)
                    
                    # Styled Verdict Display Card
                    st.markdown("---")
                    st.subheader("📋 Safety Verdict")
                    
                    with st.container(border=True):
                        if "DANGER" in verdict_text.upper():
                            st.error(verdict_text)
                        else:
                            st.success(verdict_text)
                            
                except Exception as e:
                    st.error(f"Error processing image: {e}")
