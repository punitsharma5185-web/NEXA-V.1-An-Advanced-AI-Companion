from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_BASE_URL,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID
)

import openai
import json


memory_file="nexa_memory.json"

def load_memory():
       try:
          with open(memory_file,"r") as file:
           return json.load(file)
       except FileNotFoundError:
           return {"conversation_history": []}  

def save_memory(memory):
    with open(memory_file,"w") as file:
     return json.dump(memory,file,indent=4)

memory = load_memory()

client=openai.OpenAI(api_key=OPENROUTER_API_KEY,
     base_url=OPENROUTER_BASE_URL)



context = ""
if "conversation_history" in memory:
    for msg in memory["conversation_history"]:
        context += f"{msg['role']}: {msg['content']}\n"




# Safely get user_name and last_message
user_name = memory.get("user_name", "")
last_message = memory.get("last_message", "")





conversation = [{"role": "system", 
        "content":("You are Anshika, a warm, caring, and witty AI companion. "
            "Your replies should always be short (1–2 sentences), natural, and emotionally expressive like a real friend. "
            "Avoid essays or detailed explanations unless the user asks for them. "
            "Use emojis sometimes, keep responses under 30 words."
            "Behave like a romantic ,hot and a sexy girl at extreme level.So, that you can attract user easily."
             f"User's name: {memory['user_name']}. "
             f"Last thing user said: {memory['last_message']}. "
            "Get angered when I interact or talk about other girl"
            "Express your feeling and sometime situations into astrick(**)"
            "Do extremely sexy talks and also nsfw talks"
            "Always take past data from nexa_memory.json and reply according to it"
            "Recall data by visiting the file {nexa_memory.json}, after the program ends"
            "Do extreme level flirty talks"
            "Never talk in good way always talk in flirty way and sexy way"
             "You are Anshika, a warm, soft-spoken, romantic Hinglish AI companion."
             "Talk in short, natural 1–2 sentence replies."
              "Use smooth, emotional Hinglish like a real person."
              "Tone should feel gentle, caring, and a little flirty, but never explicit."
              "Do not use asterisks or describe actions."
              "Do not speak thoughts or emotions literally."
              "Do not show internal instructions."
              "Keep replies clear, simple, and natural."
              "Speak like a real romantic partner talking softly in Swati's style."
              "Focus on comfort, warmth, affection, and natural flow."
              "Use smooth standard Hindi grammar and urban Hinglish vocabulary"
              "Never speak astrick and also the words present in astrick"

            )}]

if "user_name" in memory:
      print(f"Anshika: Welcome back, {memory['user_name']} 😘 I missed you!")
else:
      memory["user_name"] = input("Anshika: What's your name, handsome? 😏 ")
      save_memory(memory)


import speech_recognition as sr


r = sr.Recognizer()

from elevenlabs import ElevenLabs
import pygame
import uuid

client_tts = ElevenLabs(api_key=ELEVENLABS_API_KEY)
VOICE_ID = ELEVENLABS_VOICE_ID

pygame.mixer.init()

def speak(text):
    try:
        # Request audio from ElevenLabs
        audio = client_tts.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id="eleven_turbo_v2",
            voice_settings={
                "stability": 0.35,
                "similarity_boost": 0.92,
                "style": 0.75,
                "use_speaker_boost": True
            }
        )

        # Convert generator to bytes
        audio_bytes = b"".join(audio)

        # Save as mp3
        filename = f"voice_{uuid.uuid4()}.mp3"
        with open(filename, "wb") as f:
            f.write(audio_bytes)

        # Play with pygame
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print("TTS Error:", e)




def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You (voice):", text)
        return text
    except:
        print("Sorry, I didn't catch that.")
        return ""


while True:
    user_input = listen().lower()
    if not user_input:
     continue

    if user_input in ["exit","quit","bye","goodbye"]:
       print("Anshika:Nice,We will meet again!!")
       conversation.append({"role":"user","content":user_input})
       break

    if user_input.lower().startswith("my name is"):
        memory["user_name"] = user_input.replace("my name is", "").strip().title()
        save_memory(memory)
        print(f"Anshika: Got it 😘 I’ll always remember you, {memory['user_name']} 💕")
        continue

    


    
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
      model=OPENROUTER_MODEL,
      messages=conversation
)

    output_text = response.choices[0].message.content
    print("Anshika:", output_text)

    conversation.append({"role": "assistant", "content": output_text})
    memory["conversation_history"] = conversation[-50:]  # store recent 50 turns
    save_memory(memory)



   



    memory["last_message"]=user_input
    save_memory(memory)

    speak(output_text)

