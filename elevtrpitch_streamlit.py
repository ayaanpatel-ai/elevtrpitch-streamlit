st.markdown("""
<style>
/* Pale Turquoise color */
:root {
    --accent-color: #AFEEEE;
}

/* Style sliders track and handles */
input[type="range"] {
    accent-color: var(--accent-color);
}

/* Style buttons */
.stButton > button {
    background-color: var(--accent-color);
    color: black;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    padding: 0.4em 1em;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #90e0d0;
}

/* Style text inputs and textareas */
input[type="text"], textarea {
    background-color: white;
    color: black;
    border: 2px solid var(--accent-color);
    border-radius: 5px;
    padding: 0.4em;
    font-weight: bold;
}

input[type="text"]:focus, textarea:focus {
    outline: none;
    border-color: #66cdaa;
    box-shadow: 0 0 5px var(--accent-color);
}
</style>
""", unsafe_allow_html=True)

