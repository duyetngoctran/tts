
from django.shortcuts import render, redirect, HttpResponse, reverse
import string
import random
import os
import shutil
import azure.cognitiveservices.speech as speechsdk
from django.http import JsonResponse

import requests
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from log.models import Speak



# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription='22b8bd86359c4d26ab83e9bb5db787e6', region='southeastasia')
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.endpoint_id = "6b861b34-9a47-496b-a13f-2011814e6b47"
speech_config.speech_synthesis_voice_name = "New Test Voice"
# speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

@login_required
def index(request):

    return render(request, 'index.html')


def speak(request):
    # request should be ajax and method should be POST.
    if is_ajax(request=request) and request.method == "POST":
        # print('ddd')
        letters = string.ascii_lowercase
        file_name = f"{''.join(random.choice(letters) for i in range(10))}.mp3"
        text = request.POST['text']
        #
        # speech_synthesis_result = speech_synthesizer.speak_text(text)
        # audio = speechsdk.AudioDataStream(speech_synthesis_result)
        #
        # if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #     print("Speech synthesized for text [{}]".format(text))
        # elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        #     cancellation_details = speech_synthesis_result.cancellation_details
        #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
        #         if cancellation_details.error_details:
        #             print("Error details: {}".format(cancellation_details.error_details))
        #             print("Did you set the speech resource key and region values?")
        #
        # #
        # # tts = gTTS(text, lang=lang, tld=tdl)
        # audio.save_to_wav_file(file_name)
        # #
        # dir = os.getcwd()
        # full_dir = os.path.join(dir, file_name)
        # print(dir)
        # print(full_dir)
        #
        # dest = shutil.move(full_dir, os.path.join(
        #     dir, "tts/static/sound_file"))
        #
        #
        # return JsonResponse({"loc": file_name, "text": text}, status=200)
        print('g')
        url = 'https://southeastasia.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId=6b861b34-9a47-496b-a13f-2011814e6b47'
        data = text
        headers = {'Content-Type': 'text/plain',
                   'Ocp-Apim-Subscription-Key': '22b8bd86359c4d26ab83e9bb5db787e6',
                   'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3',
                   }

        r = requests.post(url, data=data, headers=headers)
        speak = Speak.objects.create(txt=text, username=request.user.get_username())
        speak.save()
        # url = 'http://127.0.0.1:8000/log/speak/'
        # # response = requests.post(url, json={"txt": text, "username": username})
        # try:
        #
        #     rq = requests.post(url, json={"txt": text, "username": request.user.get_username()})
        # except requests.exceptions.RequestException as e:  # This is the correct syntax
        #     print(e)


        with open(file_name, "wb") as file:
            file.write(r.content)
        dir = os.getcwd()
        full_dir = os.path.join(dir, file_name)
        dest = shutil.move(full_dir, os.path.join(
            dir, "tts/static/sound_file"))


        return JsonResponse({"loc": file_name, "text": text}, status=200)


    # some error occured
    return JsonResponse({"error": ""}, status=400)




def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})