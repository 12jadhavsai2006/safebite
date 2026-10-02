import streamlit as st
from groq import Groq
from PIL import Image
import os

# Page Configuration
st.set_page_config(page_title="SafeBite - Cloud Allergy Guard", page_icon="🛡️", layout="centered")

st.title("🛡️ SafeBite: Cloud Allergy Guard")
st.markdown("An open-source AI assistant deployed in the cloud to check food labels anywhere.")

# Sidebar for Groq API Key & Profile
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
st.sidebar.markdown("[Get a free Groq API key here](https://console.groq.com)")

preset = st.sidebar.selectbox(
    "Choose a Preset Profile:",
    ["Custom", "Severe Nut & Gluten Allergy", "Lactose Intolerant & Vegan"]
)

default_allergies = "Peanuts\nGluten\nLactose\nShellfish"
if preset == "Severe Nut & Gluten Allergy":
    default_allergies = "Peanuts\nTree Nuts\nGluten\nWheat"
elif preset == "Lactose Intolerant & Vegan":
    default_allergies = "Milk\nLactose\nWhey\nEggs\nHoney\nGelatin"

allergies = st.sidebar.text_area("Restrictions (one per line):", default_allergies)

# Main Section: Image Upload
st.subheader("📸 Scan Ingredient List or Menu")
uploaded_file = st.file_uploader("Upload an image of the ingredient label", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Product Label", use_container_width=True)
    
    if st.button("Check Safety 🔍", type="primary"):
        if not api_key:
            st.error("Please enter your Groq API Key in the sidebar.")
        else:
            with st.spinner("Analyzing ingredients via open-source cloud AI..."):
                try:
                    import base64
                    import io
                    
                    # Convert image to base64 for Groq API
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
                    
                    st.subheader("📋 Safety Verdict")
                    if "DANGER" in verdict_text.upper():
                        st.error(verdict_text)
                    else:
                        st.success(verdict_text)
                        
                except Exception as e:
                    st.error(f"Error processing image: {e}")