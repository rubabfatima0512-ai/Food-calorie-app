"""Module 1: User Interface Module (Streamlit web app).

Run:  streamlit run app.py
Then open the URL shown in the terminal (usually http://localhost:8501).
"""
import os
import tempfile
import streamlit as st

from food_classifier import predict
from calorie_estimator import get_nutrition, pretty_name

# Cloud deployment: build the nutrition DB automatically on first run
_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nutrition.db")
if not os.path.exists(_DB_PATH):
    from setup_database import build as _build_db
    _build_db()

st.set_page_config(page_title="Food Recognition & Calorie Estimation", page_icon="🍔")
st.title("🍔 Food Recognition & Calorie Estimation System")
st.write(
    "Upload a food image. The system identifies the dish using a Vision Transformer "
    "trained on the Food-101 dataset and estimates its calories and nutrition."
)

uploaded = st.file_uploader("Choose a food image", type=["jpg", "jpeg", "png", "webp"])
portions = st.slider("Portion size (servings)", 0.5, 3.0, 1.0, 0.5)

if uploaded is not None:
    st.image(uploaded, caption="Uploaded image", use_container_width=True)
    with st.spinner("Analyzing image..."):
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(uploaded.name)[1]
        ) as tmp:
            tmp.write(uploaded.getbuffer())
            tmp_path = tmp.name
        try:
            results = predict(tmp_path, top_k=3)
        finally:
            os.remove(tmp_path)

    st.subheader("🔍 Recognition Results")
    for i, (label, conf) in enumerate(results):
        st.write(f"**{i + 1}. {pretty_name(label)}** — {conf * 100:.1f}% confidence")

    top_label = results[0][0]
    nutrition = get_nutrition(top_label, portions=portions)

    st.subheader("🔥 Calorie Estimation")
    if nutrition:
        col1, col2 = st.columns(2)
        col1.metric("Estimated Calories", f"{nutrition['calories']} kcal")
        col2.metric("Serving", f"{nutrition['serving']} × {portions}")
        st.subheader("📊 Nutritional Information")
        st.write(f"**Protein:** {nutrition['protein_g']} g")
        st.write(f"**Carbohydrates:** {nutrition['carbs_g']} g")
        st.write(f"**Fat:** {nutrition['fat_g']} g")
        st.caption(
            "Note: calorie and nutrition values are estimates per typical serving, "
            "intended for awareness and tracking."
        )
    else:
        st.warning("Nutrition data not available for this food.")
else:
    st.info("👆 Upload an image to get started.")
