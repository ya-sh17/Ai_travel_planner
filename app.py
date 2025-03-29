import streamlit as st
import os
import gdown
from llama_cpp import Llama

MODEL_PATH = "model.gguf"
FILE_ID = "your file id"  # Replace with your actual file ID


def download_model():
    if not os.path.exists(MODEL_PATH):
        st.info("Downloading model... (This may take a while)")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)


download_model() 

# Load LLaMA Model
llm = Llama(model_path=MODEL_PATH, n_ctx=4096)

st.title("✈️ AI-Powered Travel Planner")
st.subheader("Get a personalized travel itinerary in seconds!")

name = st.text_input("📛 What is your name?")
destination = st.text_input("🌍 Where are you traveling?")
budget = st.selectbox("💰 Budget", ["Low", "Medium", "High"])
trip_duration = st.slider("📅 Trip Duration (days)", 1, 31, 5)
preferences = st.multiselect(
    "🎭 Interests",
    ["Sightseeing", "Food & Drinks", "Adventure", "Relaxation", "Nightlife", "Shopping"]
)
dietary_prefs = st.text_input("🥗 Dietary Preferences (if any)")
walking_tolerance = st.radio("🚶 Walking Tolerance", ["Low", "Moderate", "High"], index=1)
accommodation = st.selectbox("🏨 Accommodation Preferences", ["Budget", "Mid-range", "Luxury", "Central Location"])

def generate_itinerary(prompt):
    system_prompt = """
    You are a helpful AI travel assistant. Your task is to generate a detailed, personalized travel itinerary for users based on their inputs.
    Consider their budget, interests, dietary preferences, and walking tolerance. Provide specific recommendations, including:
    - Best places to visit
    - Local foods to try
    - Hidden gems
    - Estimated travel times
    - Budget-friendly tips

    Keep your responses concise yet informative. Use a friendly and engaging tone.
    """
    
    full_prompt = system_prompt + "\n\nUser Request:\n" + prompt
    output = llm(full_prompt, max_tokens=1024)
    return output["choices"][0]["text"]

if st.button("Generate Itinerary"):
    if not destination:
        st.warning("Please enter the destination")
    else:
        prompt = f"""
        I am planning a {trip_duration}-day trip to {destination}.
        My budget is {budget}. I am interested in {', '.join(preferences)}.
        My dietary preferences are {dietary_prefs}.
        My walking tolerance is {walking_tolerance}.
        I prefer {accommodation} accommodation.
        Suggest a detailed day-by-day itinerary, including:
        - Best places to visit
        - Local foods to try
        - Hidden gems
        - Estimated travel times
        - Any budget-friendly tips
        """

        st.info(f"Generating travel itinerary for {name}... ⏳")
        itinerary = generate_itinerary(prompt)
        st.success("Here is your personalized itinerary:")
        st.write(itinerary)

st.markdown("---")
