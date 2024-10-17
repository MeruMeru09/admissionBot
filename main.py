import csv
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv # comment out

# load the API KEY
load_dotenv()

# Access the API_KEY environment variable
api_key = os.getenv('API_KEY')

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=api_key)


# Extract data from a CSV file
def extract_text_from_csv(csv_path):
    csv_content = ""
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert each row to a string and append to the content
            csv_content += ' '.join(row) + "\n"
    return csv_content

# Use the Gemini API to generate a response based on the CSV content and user input
def query_gemini_api(csv_path, user_input):
    csv_content = extract_text_from_csv(csv_path)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Send the CSV content and user query to the Gemini API for content generation
    response = model.generate_content([f"Give me an answer based on this data and the query: {user_input}", csv_content])
    
    return response.text  # Assuming the API returns the text in this field

# Handle conversation using CSV file content
def handle_conversation(csv_path):
    print("Hello, how may I help you? (Type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Pass the CSV content and user's query to the Gemini API
        result = query_gemini_api(csv_path, user_input)
        
        print("Bot: ", result)

if __name__ == "__main__":
    # Provide the path to your CSV file here
    csv_path = "scrapped_data1.csv"
    handle_conversation(csv_path)