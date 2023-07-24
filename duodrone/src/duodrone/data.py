class OuterEvent:
    text: str
    emotion: str
    audio: bytearray

    def __init__(self, text, emotion=None, audio=None):
        self.text = text
        self.emotion = emotion
        self.audio = audio
