from google.cloud import speech_v1p1beta1 as speech
import os
# Imports the google.auth.transport.requests transport
from google.auth.transport import requests
# Imports a module to allow authentication using a service account
from google.oauth2 import service_account

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="SA.json"

credentials = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
)
scoped_credentials = credentials.with_scopes(
    ["https://www.googleapis.com/auth/cloud-platform"]
)
# Creates a requests Session object with the credentials.
session = requests.AuthorizedSession(scoped_credentials)
client = speech.SpeechClient()

speech_file = "videoplayback.mp3"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

gcs_uri="gs://test-speech-igngar/videoplayback.mp3"

audio = speech.RecognitionAudio(uri=gcs_uri)

diarization_config = speech.SpeakerDiarizationConfig(
  enable_speaker_diarization=True,
  min_speaker_count=2,
  max_speaker_count=10,
)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=8000,
    language_code="es-ES",
    diarization_config=diarization_config,
)

print("Waiting for operation to complete...")
operation = client.long_running_recognize(config=config, audio=audio)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
print("Waiting for operation to complete...")
response = operation.result(timeout=90)
result = response.results[-1]

words_info = result.alternatives[0].words

# Printing out the output:
for word_info in words_info:
    print(
        u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
    )
