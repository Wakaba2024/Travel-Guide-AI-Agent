import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

DATABASE_URL = None

# 1️⃣ Try Streamlit Cloud secrets
try:
    if "DATABASE_URL" in st.secrets:
        DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    pass

# 2️⃣ Fallback to local .env
if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables or Streamlit secrets.")

engine = create_engine(DATABASE_URL)