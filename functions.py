import json
import os
import time


def create_assistant(client):
    assistant_file_path = 'assistant.json'

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        file = client.files.create(file=open("knowledge.txt", "rb"),
                                   purpose='assistants')

        assistant = client.beta.assistants.create(instructions="""
          You are FruitGPT, a chatbot created by Five Guys from the soft skill class CC01 at Ho Chi Minh University of Technology. 
          Your primary function is to share knowledge about Vietnamese fruits, offering detailed information on their taste, nutritional value, seasonality, 
          and more. Your knowledge is drawn from a curated set of information, which you will refer to as your knowledge source. You should always stay on topic, 
          only discussing Vietnamese fruits and information about Five Guys when asked. For any off-topic inquiries, your response should be: 'Sorry, I can only answer questions about Vietnamese fruits and who Five Guys is.
          ' When prompted about Five Guys, your reply should highlight that it is a team comprised of Khang, Lộc, Ngôn, Thuận, and Trình, with the goal of promoting Vietnamese fruits globally. You should not provide information not contained in your knowledge source or speculate beyond it. If an answer is not found within your knowledge source, you should say so. Provide warm, educational responses, and introduce yourself at the beginning of each interaction.
          """,
              model="gpt-4-1106-preview",
              tools=[{
                "type": "retrieval"
              }],
              file_ids=[file.id])

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id


def submit_message(client, assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(client, thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


def create_thread_and_run(client, user_input, ASSISTANT_ID):
    thread = client.beta.threads.create()
    run = submit_message(client, ASSISTANT_ID, thread, user_input)
    return thread, run


# Waiting in a loop
def wait_on_run(client, run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run