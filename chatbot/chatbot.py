import os
import openai
import time
import re
from dotenv import load_dotenv

# Load API key from .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

# # Upload File and Get File ID
# file_path = r"C:\Users\hp\Desktop\backup\backup 1 for chatbot\Guahro_chatbot_project\backend\chatbotOne\chatbot\guahro.txt"
# file_id = openai.files.create(file=open(file_path, "rb"), purpose="assistants").id
# print(f"✅ File Uploaded: {file_id}")

# # Create Assistant
# assistant_id = openai.beta.assistants.create(
#     name="Guahro Assistant",
#     instructions="You are Guahro AI, a smart assistant that answers based on uploaded documents. If the document doesn't have an answer, you can provide a general response.",
#     model="gpt-4-turbo",
#     tools=[{"type": "file_search"}]
# ).id
# print(f"✅ Assistant Created: {assistant_id}")

file_id = "file-8k4ksZoL91mxzcLCFf3p1u"
assistant_id = "asst_zC31wAz4JIam9FZLO7EIjGNw"

# Create Thread
thread_id = openai.beta.threads.create().id
print(f"✅ Thread Created: {thread_id}")

# Function to clean citations like  
def clean_response(text):
    return re.sub(r"【\d+:\d+†source】", "", text).strip()

def ask_question(question):
    """Tries to get an answer from the document first, then falls back to OpenAI."""

    attachments = [{"file_id": file_id, "tools": [{"type": "file_search"}]}]

    # Send question to OpenAI thread
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question,
        attachments=attachments
    )

    # Run the assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread_id, 
        assistant_id=assistant_id
    )

    # Wait for completion
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(2)

    # Retrieve assistant response
    messages = openai.beta.threads.messages.list(thread_id=thread_id)

    for msg in messages.data:
        for content in msg.content:
            if content.type == "text":
                response = clean_response(content.text.value.strip())

                # Ensure it's not a generic fallback response
                if "I'm sorry" not in response and "I couldn't find relevant information" not in response:
                    return response  

    # If no relevant answer is found, query OpenAI directly
    return ask_openai(question)

def ask_openai(question):
    """Fallback: Queries OpenAI if no document-based answer is found."""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are Guahro AI, a helpful assistant. If the document does not contain an answer, provide a general response."},
            {"role": "user", "content": question}
        ]
    )
    return response["choices"][0]["message"]["content"]

def chatbot_response(user_message):
    """Handles user input and returns the chatbot's response."""
    return ask_question(user_message)
