from pytube import YouTube

def youtube(url, audio=False):
    if url.startswith("https://www.youtube.com/") or url.startswith("https://www.youtu.be/"):
        if audio == False:
            print("Downloading started...")
            YouTube(url).streams.get_highest_resolution().download()
            print("Downloading completed!")
        elif audio == True:
            print("Audio downloading started...")
            YouTube(url).streams.get_audio_only().download()
            print("Audio downloading completed!")
    else:
        print("URL is invalid!")