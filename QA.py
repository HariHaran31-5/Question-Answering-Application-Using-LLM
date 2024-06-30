import streamlit as st
import fitz  # PyMuPDF
import openai

# Set your OpenAI API key here
openai.api_key = "sk-proj-AFpXQ0giVBBEigkdxBPqT3BlbkFJHX7w9zXLaT61Yz3N2Etv"

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to ask a question using GPT-3

def ask_gpt3(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Adjust the model name as needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context},
            {"role": "user", "content": question},
        ],
        max_tokens=150,
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit application
def main():
    st.title("PDF Question & Answer Application")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner('Extracting text from PDF...'):
            pdf_text = extract_text_from_pdf(uploaded_file)
        st.success('Text extracted from PDF!')
        
        question = st.text_input("Ask a question about the PDF:")
        
        if st.button("Get Answer"):
            if question:
                with st.spinner('Generating answer...'):
                    answer = ask_gpt3(question, pdf_text)
                st.success('Answer generated!')
                st.write(f"**Question:** {question}")
                st.write(f"**Answer:** {answer}")
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
