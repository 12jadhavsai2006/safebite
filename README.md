

# 🛡️ SafeBite: Cloud Allergy Guard

An open-source, mobile-optimized AI web application designed to help people instantly check food product labels and menus for allergens while grocery shopping.

## 🚀 Features
* **Cloud Vision AI:** Powered by Groq and open-source models for lightning-fast analysis.
* **Mobile-Friendly Camera Support:** Snap live photos of ingredient labels directly from your mobile browser.
* **Custom Dietary Profiles:** Pre-loaded presets for severe allergies, gluten restrictions, and vegan diets, plus custom inputs.
* **Recent Scans History:** Keep track of recent product verdicts during your shopping trip.

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit
* **AI Engine:** Groq API (`qwen/qwen3.8-27b`)
* **Image Processing:** Pillow, Base64
* **Deployment:** Render & GitHub

## 🏃‍♂️ Local Setup
1. Clone the repository:
   git clone [https://github.com/12jadhavsai2006/safebite.git](https://github.com/12jadhavsai2006/safebite.git)
   cd safebite
   
3. Install dependencies:
pip install -r requirements.txt

3. Run the app:
python -m streamlit run app.py
