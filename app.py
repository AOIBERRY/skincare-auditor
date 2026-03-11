import streamlit as st
from openai import OpenAI

# This line tells the app to look for the key in your secrets.toml file
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

st.title("✨ SkinSafe Ingredient Auditor")
st.write("Auditing products based on your skin type and conditions.")

# --- USER PROFILE SELECTION ---
# This part creates the interactive UI elements for different skin types
st.subheader("Personalize Your Profile")
skin_type = st.selectbox(
    "What is your skin type?", 
    options=["Oily", "Dry", "Sensitive", "Combination"],
    index=None, 
    placeholder="Select your skin type..."
)
concerns = st.multiselect("Select your concerns:", ["Sensitive", "Acne-prone", "Rosacea", "Eczema", "Hyperpigmentation"])

# --- INGREDIENT INPUT ---
st.subheader("Ingredient List")
ingredients = st.text_area("Enter or Paste the ingredient list here:")

if st.button("Audit Ingredients"):
    if ingredients:
        # Update THIS specific section below
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": f"""
                    ROLE: You are a friendly but highly knowledgeable Skin Consultant. 
                    PROFILE: {skin_type} skin with {', '.join(concerns)}.
                    
                    TASK: Conduct a safety audit of the provided ingredients.
                    
                    CRITICAL: Start with a 'Risk Score' (1-10) for the Safety Gauge.
                    
                    FORMAT:
                    Score: [Number]
                    
                    ## ⚖️ VERDICT
                    **[SAFE / USE WITH CAUTION / AVOID]**
                    [1-sentence explanation of why it fits this category for {skin_type} skin.]

                    ### 🚩 TRIGGERS FOUND
                    * List any high-risk ingredients here with their specific flare-up risk.

                    ### ✨ SKIN WINS (In this product)
                    * List the beneficial ingredients found in this specific product.

                    ### 🛍️ WHAT TO LOOK FOR INSTEAD
                    Based on your {skin_type} skin and {', '.join(concerns)}, here are 3 "Gold Standard" ingredients you should look for in your next purchase:
                    * **[Ingredient 1]**: Why it helps your specific profile.
                    * **[Ingredient 2]**: Why it helps your specific profile.
                    * **[Ingredient 3]**: Why it helps your specific profile.
                    """
                },
                {"role": "user", "content": f"Audit these ingredients: {ingredients}"}
            ]
        )
        # ... (keep your logic for parsing the score and displaying the sidebar below this)
        
        
        full_text = response.choices[0].message.content
        
        # Logic to pull the score out for the sidebar
        try:
            score_line = [line for line in full_text.split('\n') if 'Score:' in line][0]
            score = int(''.join(filter(str.isdigit, score_line)))
        except:
            score = 5 # Default if AI fails to give a number
            
        # --- SIDEBAR SAFETY GAUGE ---
        st.sidebar.header("Safety Snapshot")
        if score <= 3:
            st.sidebar.success(f"Risk Score: {score}/10 (Low Risk)")
        elif score <= 7:
            st.sidebar.warning(f"Risk Score: {score}/10 (Moderate Risk)")
        else:
            st.sidebar.error(f"Risk Score: {score}/10 (High Risk)")
        
        st.subheader("Audit Results")
        st.write(full_text)
    else:
        st.error("Please paste some ingredients first!")