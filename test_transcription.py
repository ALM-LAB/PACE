import requests

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
  "audio_url": "https://www.podtrac.com/pts/redirect.mp3/chrt.fm/track/4655F8/pdcn.co/e/pdst.fm/e/api.spreaker.com/download/episode/51529383/3_martini_lunch_10_10_22.mp3"
}

headers = {
  "Authorization": "76611a11d857415d9fe20a4d41b77bf0",
  "Content-Type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)

print(response)


# python test_transcription.py https://www.podtrac.com/pts/redirect.mp3/chrt.fm/track/4655F8/pdcn.co/e/pdst.fm/e/api.spreaker.com/download/episode/51529383/3_martini_lunch_10_10_22.mp3 --api_key 76611a11d857415d9fe20a4d41b77bf0 

'''
curl --request GET \
  --url https://api.assemblyai.com/v2/transcript?limit=200&status=completed \
  --header 'authorization: "76611a11d857415d9fe20a4d41b77bf0"' \
  --header 'content-type: application/json'
'''