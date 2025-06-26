import os
import PyPDF2
import google.generativeai as genai

def load_api_key():
    """Loads the Gemini API key from the .env file."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("GEMINI_API_KEY")
    except ImportError:
        return os.environ.get("GEMINI_API_KEY")

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def generate_answer(question, context, api_key):
    """Generates an answer based on the question and context."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    You are a helpful assistant that answers questions based on the given context.
    Context: {context}
    Question: {question}
    Answer:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I'm sorry, I couldn't generate an answer."

def main(pdf_file, question):
    """Main function to orchestrate the chatbot."""
    api_key = load_api_key()
    if not api_key:
        return "API key not found. Please set the GEMINI_API_KEY environment variable."

    context = extract_text_from_pdf(pdf_file)
    if not context:
        return "Could not extract text from the PDF."

    answer = generate_answer(question, context, api_key)
    return answer

if __name__ == "__main__":
    # Example usage (for testing purposes)
    # Replace 'your_pdf_file.pdf' with the actual path to your PDF file
    # and 'your question' with the question you want to ask.
    pdf_file_path = 'your_pdf_file.pdf'
    question = "What is this document about?"
    answer = main(open(pdf_file_path, 'rb'), question)
    print(answer)