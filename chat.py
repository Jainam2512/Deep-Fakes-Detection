import streamlit as st
import torch
from transformers import pipeline

# Install transformers from source - only needed for versions <= v4.34


# Function to initialize the chatbot pipeline
@st.cache(allow_output_mutation=True)
def initialize_chatbot():
    pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")
    return pipe

# Main function to run the Streamlit app
def main():
    # Title for the app
    st.title("Deepfake and Social Media Fraud Prevention Chatbot")

    # Initialize the chatbot pipeline
    chatbot_pipe = initialize_chatbot()

    # Initial message to display
    st.write("Welcome! You are chatting with a friendly chatbot who helps with understanding deepfakes and social media fraud prevention.")

    # Input box for user messages
    user_input = st.text_input("You:", "")

    # Button to send user message
    if st.button("Send"):
        # Process user message and get response from chatbot
        response = chatbot_pipe(user_input, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)[0]["generated_text"]

        # Display chatbot response
        st.text_area("Chatbot:", value=response, height=200, max_chars=None, key=None)

# Run the app
if __name__ == "__main__":
    main()
