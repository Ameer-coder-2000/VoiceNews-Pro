class SpeechToTextService:
    def __init__(self) -> None:
        try:
            import speech_recognition as sr
        except ImportError as error:
            raise RuntimeError(
                "SpeechRecognition is not installed. You can still use text input mode."
            ) from error

        try:
            import numpy as np
            import sounddevice as sd
        except ImportError as error:
            raise RuntimeError(
                "Microphone dependencies are missing. Install the packages from requirements.txt."
            ) from error

        self.sr = sr
        self.np = np
        self.sd = sd
        self.recognizer = sr.Recognizer()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> str:
        """
        Capture audio from the microphone and convert it to text.
        Audio is recorded with sounddevice and recognized with SpeechRecognition.
        """
        duration = max(1, min(timeout + phrase_time_limit, 15))
        sample_rate = 16000

        try:
            input_device = self.sd.default.device[0]
            if input_device is None or input_device < 0:
                raise RuntimeError("No microphone input device is configured on this system.")
        except Exception as error:
            raise RuntimeError(
                "Microphone not found or not accessible. Check your audio settings."
            ) from error

        try:
            print("Listening... Please ask your news question.")
            recording = self.sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
            )
            self.sd.wait()
        except OSError as error:
            raise RuntimeError(
                "Microphone recording failed. Check whether another app is using the microphone."
            ) from error
        except Exception as error:
            raise RuntimeError(f"Could not capture audio: {error}") from error

        try:
            print("Converting speech to text...")
            audio_bytes = recording.astype(self.np.int16).tobytes()
            audio = self.sr.AudioData(audio_bytes, sample_rate, 2)
            return self.recognizer.recognize_google(audio)
        except self.sr.UnknownValueError as error:
            raise RuntimeError(
                "Speech was unclear. Please try speaking slowly and clearly."
            ) from error
        except self.sr.RequestError as error:
            raise RuntimeError(
                "Speech recognition service is unavailable. Check your internet connection."
            ) from error
