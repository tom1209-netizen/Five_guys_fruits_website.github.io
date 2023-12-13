from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from functions import *

app = Flask(__name__, static_folder="static")

# Init client
client = OpenAI(
    api_key="your_api_key_here")

# Create new assistant or load existing
assistant_id = create_assistant(client)


# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
    print("Starting a new conversation...")  # Debugging line
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")  # Debugging line
    return jsonify({"thread_id": thread.id})


# Generate response
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    if not thread_id:
        print("Error: Missing thread_id")  # Debugging line
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")  # Debugging line

    thread, run = create_thread_and_run(client, user_input, assistant_id)
    run = wait_on_run(client, run, thread)
    response = get_response(client, thread)

    assistant_response = None
    for message in response:
        if message.role == 'assistant':
            assistant_response = message.content[0].text.value
            break

    print(f"Assistant response: {assistant_response}")  # Debugging line
    return jsonify({"response": assistant_response})


# Chatbot route
@app.route("/chatbot")
def chatbot_page():
    return render_template('chatbot.html')


# Main page route
@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/fruits')
def fruits_page():
    return render_template('fruits.html')


# Fruits route
@app.route('/dragon_fruits')
def dragon_fruits_page():
    return render_template('dragon_fruit.html')


@app.route('/durian_fruits')
def durian_page():
    return render_template('durian.html')


@app.route('/lychee_fruits')
def lychee_page():
    return render_template('lychee.html')


@app.route('/mangosteen_fruits')
def mangosteen_page():
    return render_template('mangosteen.html')


@app.route('/rambutan_fruits')
def rambutan_page():
    return render_template('rambutan.html')


@app.route('/longan_fruits')
def longan_page():
    return render_template('longan.html')


@app.route('/pomelo_fruits')
def pomelo_page():
    return render_template('pomelo.html')


@app.route('/sapodilla_fruits')
def sapodilla_page():
    return render_template('sapodilla.html')


@app.route('/starapple_fruits')
def starapple_page():
    return render_template("starapple.html")


@app.route('/passion_fruits')
def passion_page():
    return render_template('passion.html')


if __name__ == '__main__':
    app.run()
