from flask import Flask, render_template, jsonify
import speech_recognition as sr
import requests

app = Flask(__name__)

# Function to capture voice input and convert to text
def voice_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None

    except sr.RequestError as e:
        print(f"Error with the request: {e}")
        return None

# Function to send SMS using Vonage API
def send_sms_via_vonage(message, to_number):
    if message:
        try:
            # Your Vonage API credentials
            api_key = "934533ad"  # Replace with your API Key
            api_secret = "P2B6EAWCtNolwqE3"  # Replace with your API Secret
            vonage_number = "918509690758"  # Replace with your Vonage number

            # Vonage SMS API endpoint
            url = "https://rest.nexmo.com/sms/json"

            # Payload for sending SMS
            payload = {
                'api_key': "934533ad",
                'api_secret': "P2B6EAWCtNolwqE3",
                'to': 918509690758,
                'from': 918509690758,
                'text': message
            }

            # Send the request
            response = requests.post(url, data=payload)
            response_data = response.json()

            if response_data.get('messages')[0].get('status') == '0':
                print(f"Message sent to {to_number} via Vonage")
                return True
            else:
                print(f"Failed to send SMS: {response_data.get('messages')[0].get('error-text')}")
                return False

        except Exception as e:
            print(f"Failed to send SMS via Vonage: {e}")
            return False
    else:
        print("No message to send.")
        return False

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the voice to text and send SMS
@app.route('/process_voice', methods=['POST'])
def process_voice():
    # Capture voice and convert to text
    message_text = voice_to_text()

    if message_text:
        # Define the recipient's phone number
        recipient_number = "919334232663"  # Replace with the recipient's phone number

        # Send the text as an SMS using Vonage
        success = send_sms_via_vonage(message_text, recipient_number)

        if success:
            return jsonify({"status": "success", "message": "SMS sent successfully!"})
        else:
            return jsonify({"status": "failure", "message": "Failed to send SMS."})
    else:
        return jsonify({"status": "failure", "message": "Failed to recognize voice."})

if __name__ == "__main__":
    app.run(debug=True)
