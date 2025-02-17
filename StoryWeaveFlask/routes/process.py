from flask import flash, redirect, url_for, render_template, session, request
import requests
from app import app, mongodb
from datetime import datetime
from WTForms.prompt import PromptForm
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
import os


genai.configure(api_key=os.getenv("FIREBASE_API_KEY"))
FIREBASE_URL = os.getenv("FIREBASE_URL")


def get_gemini_story_script_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    full_prompt = f"Generate a detailed and engaging story based on: '{prompt}'. Ensure the story lasts at least 50-60 seconds when read aloud, which means it should be around 180 - 220 words. Make it immersive and written as a paragraph."
    response = model.generate_content(full_prompt)
    return response.text


def get_gemini_prompts_for_image_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    full_prompt = f"{prompt} :I need you to give appropriate number of prompts for images with a minimum 10 simple image generation prompts at least, they should be of the format, img_1= your first response: img_2= your second response: img_3= your third response in a long continuous string with a colon as a separator for each image prompt"
    response = model.generate_content(full_prompt)
    if not response:
        return False
    return response.text


def store_history(emailID, user_prompt):
    mongodb.history.insert_one(
        {"EmailID": emailID, "UserPrompt": user_prompt, "DateTime": str(datetime.now())}
    )


def send_to_firebase(prompts, script, email, voice_model):
    data = {
        "Prompt": prompts,
        "Script": script,
        "EmailID": email,
        "VoiceModel": voice_model,
    }
    try:
        response = requests.put(f"{FIREBASE_URL}/Process.json", json=data, timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Firebase Error: {e}")
        return False


def translate(prompt, lang):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"{prompt} translate this to {lang}"
    response = model.generate_content(prompt)
    return response.text


def translater(lang, script):
    list = []
    model = None
    tran_script = None
    match lang:
        case "eng":
            model = "en-US-AriaNeural"
            tran_script = script
        case "hin":
            tran_script = translate(script, "hindi")
            model = "hi-IN-MadhurNeural"
        case "kan":
            tran_script = translate(script, "kannada")
            model = "kn-IN-SapnaNeural"
        case "tam":
            tran_script = translate(script, "tamil")
            model = "ta-IN-PallaviNeural"
        case "mal":
            tran_script = translate(script, "malayalam")
            model = "ml-IN-MidhunNeural"
        case "tel":
            tran_script = translate(script, "telugu")
            model = "te-IN-MohanNeural"
        case "fre":
            tran_script = translate(script, "french")
            model = "fr-FR-DeniseNeural"
        case "spa":
            tran_script = translate(script, "spainish")
            model = "es-ES-AlvaroNeural"

    list.append(tran_script)
    list.append(model)
    return list


@app.route("/processing", methods=["POST", "GET"])
def processingPrompt():
    promptForm = PromptForm()

    if promptForm.validate_on_submit():
        userPrompt = promptForm.prompt.data
        ai_response = get_gemini_story_script_response(userPrompt)
        if ai_response:
            prompts = get_gemini_prompts_for_image_response(ai_response)
            if prompts is False:
                flash(
                    f"Some error occurred while generating image. Please try again :)."
                )
            else:
                param = translater(promptForm.language.data, ai_response)
                if send_to_firebase(
                    prompts, param[0], session.get("emailID"), param[1]
                ):
                    thankingMsg = "Thank you! Your video link will be sent to your registered email shortly. Stay tuned!"
                    store_history(session.get("emailID"), userPrompt)
                    return render_template("finalPage.html", thankingMsg=thankingMsg)
        else:
            flash(f"Some error occurred while generating script. Please try again :).")

    return redirect(url_for("promptIndex"))
