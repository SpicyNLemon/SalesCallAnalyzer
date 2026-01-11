from gtts import gTTS
import os

# Create different emotion test files
test_cases = {
    "happy_test.mp3": "Hello! I am so excited and happy today! This is wonderful news and I feel absolutely joyful!",
    "sad_test.mp3": "I am feeling very sad and disappointed today. Things are not going well and I feel down.",
    "angry_test.mp3": "I am extremely angry and frustrated! This is completely unacceptable and makes me furious!",
}

for filename, text in test_cases.items():
    tts = gTTS(text=text, lang='en', slow=False)
    filepath = os.path.join("Audio files", filename)
    tts.save(filepath)
    print(f"Created: {filepath}")

print("\nTest files created successfully! Upload them to test emotion detection.")
