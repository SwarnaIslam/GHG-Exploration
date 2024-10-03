import streamlit as st
import json
google_earth_engine_credentials={"type": st.secrets["google_earth_engine"]["type"],
    "project_id": st.secrets["google_earth_engine"]["project_id"],
    "private_key_id": st.secrets["google_earth_engine"]["private_key_id"],
    "private_key": st.secrets["google_earth_engine"]["private_key"],
    "client_email": st.secrets["google_earth_engine"]["client_email"],
    "client_id": st.secrets["google_earth_engine"]["client_id"],
    "auth_uri": st.secrets["google_earth_engine"]["auth_uri"],
    "token_uri": st.secrets["google_earth_engine"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google_earth_engine"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google_earth_engine"]["client_x509_cert_url"],
    "universe_domain": st.secrets["google_earth_engine"]["universe_domain"]
}
credentials_json = json.dumps(google_earth_engine_credentials)