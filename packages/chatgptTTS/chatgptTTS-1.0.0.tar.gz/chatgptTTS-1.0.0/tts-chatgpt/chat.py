#  • ▌ ▄ ·.  ▄▄▄· ·▄▄▄▄  ▄▄▄ .    ▄▄▄▄·  ▄· ▄▌    .▄▄ ·        ▄· ▄▌▄▄▌  ▄▄▌
#  ·██ ▐███▪▐█ ▀█ ██▪ ██ ▀▄.▀·    ▐█ ▀█▪▐█▪██▌    ▐█ ▀. ▪     ▐█▪██▌██•  ██•
#  ▐█ ▌▐▌▐█·▄█▀▀█ ▐█· ▐█▌▐▀▀▪▄    ▐█▀▀█▄▐█▌▐█▪    ▄▀▀▀█▄ ▄█▀▄ ▐█▌▐█▪██▪  ██▪
#  ██ ██▌▐█▌▐█ ▪▐▌██. ██ ▐█▄▄▌    ██▄▪▐█ ▐█▀·.    ▐█▄▪▐█▐█▌.▐▌ ▐█▀·.▐█▌▐▌▐█▌▐▌
#  ▀▀  █▪▀▀▀ ▀  ▀ ▀▀▀▀▀•  ▀▀▀     ·▀▀▀▀   ▀ •      ▀▀▀▀  ▀█▄▀▪  ▀ • .▀▀▀ .▀▀▀

from os import walk
import torch
import torchaudio
import g4f

class ChatGpt_TTS:
    def __init__(self, speaker="en_0", model_id="en_v3", lang="en", folder="/"):
        self.answer = None
        self.audio = None
        self.model = None
        self.prompt = None
        self.text = None
        self.out_path = None
        self.id = None

        self.speaker = speaker
        self.model_id = model_id
        self.lang = lang
        self.device = torch.device("cpu")
        self.folder = folder

    def create_tts(self, prompt, text, id=123):
        self.prompt = prompt
        self.text = text
        self.id = id

        f = next(walk("C:/Users/soyll/PycharmProject/chat-tts-api/audio_folder/"), (None, None, []))[2]
        try:
            filename = f'{self.id}-{int(f[-1].split("-")[1].split(".")[0]) + 1}.wav'
        except:
            filename = f"{self.id}-1.wav"
        self.out_path = self.folder + filename

        try:
            completion = g4f.ChatCompletion.create(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": self.prompt + " " + self.text}],
            )
            self.answer = completion

        except ValueError:
            print("Incorrect text")
        try:
            self.model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                 model='silero_tts',
                                                 language=self.lang,
                                                 speaker=self.model_id)
            self.model.to(self.device)

        except ValueError:
            print("Incorrect lang or model id")

        try:
            self.audio = self.model.apply_tts(text=self.answer,
                                    speaker=self.speaker,
                                    sample_rate=48000,
                                    put_accent=True,
                                    put_yo=True)
        except Exception as e:
            print(f"Incorrect speaker. {e}")

        try:
            torchaudio.save(self.out_path, self.audio.unsqueeze(0), 48000)
        except ValueError:
            print("Incorrect output_path")
        return self.answer, self.out_path