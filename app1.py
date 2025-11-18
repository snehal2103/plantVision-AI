import streamlit as st
from groq import Groq
import base64
import os

# ------------------------------------------------------
# 1. GROQ CLIENT 
# ------------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ------------------------------------------------------
# STREAMLIT PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Plant Species & Disease Detector",
    page_icon="🌿",
    layout="wide"
)

# ------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------
with st.sidebar:
    st.title("🌿 Plant Vision AI")
    st.write("Upload any plant image and get:")
    st.markdown("""
    - ✅ Plant Species  
    - ✅ Scientific Name  
    - ✅ Plant Category  
    - ✅ Key Visual Features  
    - 🌡️ **Health Status**  
    - 🦠 **Disease Name (if infected)**  
    - 💊 **Treatment Suggestions**  
    """)
    


# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>🌱 Plant Species & Disease Identification</h1>", unsafe_allow_html=True)
st.write("Upload a plant image and let AI analyze it for species and health condition.")


# ------------------------------------------------------
# Convert uploaded image → Base64
# ------------------------------------------------------
def file_to_base64(file):
    return base64.b64encode(file.read()).decode("utf-8")


# ------------------------------------------------------
# File Upload Section
# ------------------------------------------------------
uploaded = st.file_uploader("📸 Upload a plant image", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns([1.5, 1])

if uploaded:
    with col1:
        st.image(uploaded, caption="Uploaded Image", use_column_width=True)

    img_b64 = file_to_base64(uploaded)
    image_url = f"data:image/jpeg;base64,{img_b64}"

    with col2:
        st.success("Image uploaded successfully!")
        analyze_btn = st.button("🔍 Analyze Plant")


    if analyze_btn:
        with st.spinner("Analyzing plant with Llama-4-Scout Vision… ⏳"):

            prompt_text = """
Identify the plant in this image and analyze if the plant has any disease.
Provide the result strictly in this format:

### 🌿 Plant Information
1. **Plant Species Name**  
2. **Scientific Name**  
3. **Plant Type** (Tree / Flower / Herb / Shrub / Leaf)  
4. **Key Identifiable Features**

### 🩺 Health & Disease Diagnosis
5. **Is the Plant Healthy?** (Yes/No)  
6. **If unhealthy → Identify the Disease Name**  
7. **Cause of Disease**  
8. **Symptoms Visible in Image**  
9. **Recommended Treatment & Prevention**

Make the response clean, professional, and easy to understand.
"""

            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                temperature=0.2,
                max_completion_tokens=700,
                top_p=1,
                stream=False
            )

        result = response.choices[0].message.content

        # ----------------------------------------------
        # Result Box
        # ----------------------------------------------
        st.markdown("## 🧾 Analysis Report")
        st.markdown(f"""
        <div style="
            background:#F6FFF2;
            padding:20px;
            border-radius:15px;
            border-left:5px solid #4CAF50;
            font-size:17px;
        ">{result}</div>
        """, unsafe_allow_html=True)

        # Download Button
        st.download_button(
            "📄 Download Report",
            data=result,
            file_name="plant_analysis.txt",
            mime="text/plain"
        )

else:
    st.warning("📤 Please upload an image to begin analysis.")


# Footer
st.markdown("---")
st.caption("🌿 Built with ❤️ using Streamlit")

