import streamlit as st
import time
from rag.recommendation_engine import get_recommendations
from rag.llm import generate_response

st.set_page_config(layout="wide")

# ---------------------------------------------------
# LUXURY SAFARI STYLING
# ---------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(160deg, #0a0f1f 0%, #0f1a33 100%);
    color: white;
}

/* Floating Kenya Map Background */
body::before {
    content: "";
    position: fixed;
    top: 20%;
    left: 50%;
    width: 600px;
    height: 600px;
    background: url('https://upload.wikimedia.org/wikipedia/commons/4/49/Kenya_location_map.svg') no-repeat center;
    background-size: contain;
    opacity: 0.03;
    transform: translateX(-50%);
    z-index: -1;
}

/* HERO */
.hero {
    text-align: center;
    padding: 80px 0 40px 0;
}

.hero h1 {
    font-size: 56px;
    font-weight: 800;
    background: linear-gradient(90deg, #facc15, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #cbd5e1;
    font-size: 20px;
    margin-top: 15px;
}

/* Search Bar */
.search-bar {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    margin-bottom: 50px;
}

/* Glowing Button */
.glow-btn {
    background: linear-gradient(90deg, #facc15, #f97316);
    border: none;
    padding: 12px 24px;
    border-radius: 30px;
    font-weight: 600;
    color: black;
    transition: 0.3s ease;
}

.glow-btn:hover {
    box-shadow: 0 0 25px rgba(249,115,22,0.7);
}

/* Trending Strip */
.trending-strip {
    display: flex;
    gap: 20px;
    overflow-x: auto;
    margin-bottom: 40px;
}

.trending-card {
    background: rgba(255,255,255,0.05);
    padding: 15px 25px;
    border-radius: 30px;
    white-space: nowrap;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Listing Cards */
.listing-card {
    background: rgba(255,255,255,0.05);
    border-radius: 25px;
    overflow: hidden;
    transition: 0.3s ease;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

.listing-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 70px rgba(249,115,22,0.4);
}

.listing-card img {
    width: 100%;
    height: 240px;
    object-fit: cover;
}

.card-body {
    padding: 20px;
}

.price {
    color: #facc15;
    font-weight: 700;
    font-size: 20px;
}

.carousel {
    display: flex;
    gap: 20px;
    overflow-x: auto;
    padding-bottom: 20px;
}

.carousel-item {
    min-width: 300px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO
# ---------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>Luxury Safaris. Curated by AI.</h1>
    <p>Experience Kenya’s finest destinations with intelligent personalization.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TRENDING STRIP
# ---------------------------------------------------

st.markdown("### 🔥 Trending Destinations")
st.markdown('<div class="trending-strip">', unsafe_allow_html=True)

trending_list = ["Maasai Mara", "Diani Beach", "Nakuru", "Amboseli", "Nairobi"]

for place in trending_list:
    st.markdown(f'<div class="trending-card">{place}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

with st.container():
    st.markdown('<div class="search-bar">', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,0.7])

    with col1:
        budget = st.number_input("Budget ($)", value=3000)

    with col2:
        days = st.number_input("Days", value=5)

    with col3:
        style = st.selectbox("Travel Style",
                             ["luxury","adventure","relaxing","family","honeymoon","budget"])

    with col4:
        location = st.text_input("Destination")

    with col5:
        search = st.button("Search", key="search")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# RESULTS
# ---------------------------------------------------

if search:

    with st.spinner("Curating premium experiences..."):
        time.sleep(1)
        results = get_recommendations(budget, days, style, location)

    if not results:
        st.warning("No luxury experiences found.")
    else:
        st.markdown("## Top Picks For You")

        st.markdown('<div class="carousel">', unsafe_allow_html=True)

        for r in results:
            image_path = "assets/hero.jpg"

            if r.destination:
                d = r.destination.lower()

                if "mara" in d:
                    image_path = "assets/safari.jpg"
                elif "diani" in d:
                    image_path = "assets/diani.jpg"
                elif "nakuru" in d:
                    image_path = "assets/nakuru.jpg"
                elif "mombasa" in d:
                    image_path = "assets/mombasa.jpg"

            st.markdown('<div class="carousel-item">', unsafe_allow_html=True)
            st.markdown('<div class="listing-card">', unsafe_allow_html=True)

            st.image(image_path)

            st.markdown(f"""
            <div class="card-body">
                <h3>{r.package_name}</h3>
                <p>{r.destination} • {r.duration}</p>
                <div class="price">${r.price_usd if r.price_usd else "Contact Concierge"}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# AI ASSISTANT
# ---------------------------------------------------

st.markdown("## 🦁 Speak to Our Safari Concierge")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask about luxury safaris, exclusive stays, private tours...")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.spinner("Consulting safari experts..."):
        response = generate_response(user_input)

    st.session_state.messages.append({"role":"assistant","content":response})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])