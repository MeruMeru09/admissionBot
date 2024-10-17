import csv
import google.generativeai as genai
import os
from pathlib import Path

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=os.environ["API_KEY"])

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
    
    if user_input.lower() in ["hi", "hello", "hey", "greetings"]:
        prompt = "Hello! How can I assist you with admission information today?"
    else:
        prompt = f"Provide an answer based on this data and the query. Make it concise.: '{user_input}'. {csv_content}"

    # Send the user query and the CSV content to the Gemini API for response
    response = model.generate_content([prompt, csv_content])
    
    if "Not found" in response.text or "Unavailable" in response.text or not response.text.strip():
        return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?"
    
    
    
    return response.text  # Assuming the API returns the text in this field

# Handle conversation using CSV file content
def handle_conversation(csv_path):
    print("Hello, I am Margatron. How may I help you? (Type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("")
            break

        # Pass the CSV content and user's query to the Gemini API
        result = query_gemini_api(csv_path, user_input)
        
        print("Margatron: ", result)

if __name__ == "__main__":
    # Provide the path to your CSV file here
    csv_path = "scrapped_scholarship.csv"
    handle_conversation(csv_path)
