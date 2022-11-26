
from django.shortcuts import render, redirect, HttpResponse
import string
import random
import os
import shutil
import azure.cognitiveservices.speech as speechsdk
from django.http import JsonResponse

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription='22b8bd86359c4d26ab83e9bb5db787e6', region='southeastasia')
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.endpoint_id = "6b861b34-9a47-496b-a13f-2011814e6b47"
speech_config.speech_synthesis_voice_name = "New Test Voice"
# speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def index(request):


    return render(request, 'index.html')


def speak(request):
    # request should be ajax and method should be POST.
    if is_ajax(request=request) and request.method == "POST":
        print('ddd')
        letters = string.ascii_lowercase
        file_name = f"{''.join(random.choice(letters) for i in range(10))}.mp3"
        text = request.POST['text']

        speech_synthesis_result = speech_synthesizer.speak_text(text)
        audio = speechsdk.AudioDataStream(speech_synthesis_result)

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

        #
        # tts = gTTS(text, lang=lang, tld=tdl)
        audio.save_to_wav_file(file_name)
        #
        dir = os.getcwd()
        full_dir = os.path.join(dir, file_name)
        print(dir)
        print(full_dir)

        dest = shutil.move(full_dir, os.path.join(
            dir, "tts/static/sound_file"))


        return JsonResponse({"loc": file_name, "text": text}, status=200)


    # some error occured
    return JsonResponse({"error": ""}, status=400)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

