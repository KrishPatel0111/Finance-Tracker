import requests
import PyPDF2

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Define the endpoint URL
url = "https://api.openai.com/v1/chat/completions"

# Set your API key here
api_key = "key"

# Define the headers, including your API key
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Path to the PDF file
pdf_file_path = "/Users/gp/Desktop/statement.pdf"

# Extract text from the PDF file
pdf_text = extract_text_from_pdf(pdf_file_path)

#Define the data (prompt and model) for the API request
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "the firts column is the name of expenditure, 2nd column is type of expenditure such as food, biills, education, others,etc. and then their the credit, which is non negative, and a column called debit which is non negative, and with date as fourth column with just data in YYYY-MM-DD format with no time"},
        {"role": "user", "content": f"Make summary of statement of account attached as a json file: {pdf_text}"}
    ]
}

# Make the request
response = requests.post(url, headers=headers, json=data)

# Print only the assistant's message content
if response.status_code == 200:
    response_data = response.json()
    message_content = response_data['choices'][0]['message']['content']
    print(message_content)
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
