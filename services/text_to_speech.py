class TextToSpeechService:
    def __init__(self, voice_preference: str = "auto") -> None:
        """
        Initialize TTS with voice preference.
        voice_preference: 'auto', 'male', 'female', or specific voice name
        """
        self.engine = None
        self.gtts_engine = None
        self.voice_preference = voice_preference
        self.use_gtts = False  # Flag to use Google TTS for more natural voice

        try:
            # Try to initialize Google TTS first for more natural voice
            from gtts import gTTS
            self.gtts_engine = gTTS
            self.use_gtts = True
            print("Using Google TTS for natural voice")
        except Exception as e:
            print(f"Google TTS not available: {e}")
            # Fallback to pyttsx3
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                
                # Optimize voice settings for more natural speech
                self.engine.setProperty("rate", 140)  # Natural speaking rate
                self.engine.setProperty("volume", 0.85)  # Slightly lower volume for naturalness
                
                # Try to set voice properties for better quality
                voices = self.engine.getProperty('voices')
                if voices:
                    # Prefer Microsoft voices or high-quality system voices
                    for voice in voices:
                        voice_name = voice.name.lower()
                        if any(quality in voice_name for quality in ['microsoft', 'david', 'zira', 'hazel', 'mark']):
                            self.engine.setProperty('voice', voice.id)
                            break
                
                # Set voice based on preference
                self._set_voice()
                print("Using system TTS as fallback")
            except Exception:
                self.engine = None

    def _set_voice(self) -> None:
        """Set the appropriate voice based on preference."""
        if self.engine is None:
            return
            
        try:
            voices = self.engine.getProperty('voices')
            if not voices:
                return
                
            selected_voice = None
            
            if self.voice_preference == "female":
                # Try to find female voices
                female_voices = [v for v in voices if 'female' in v.name.lower() or 'woman' in v.name.lower() or 'zira' in v.name.lower()]
                if female_voices:
                    selected_voice = female_voices[0]
            elif self.voice_preference == "male":
                # Try to find male voices
                male_voices = [v for v in voices if 'male' in v.name.lower() or 'man' in v.name.lower() or 'david' in v.name.lower()]
                if male_voices:
                    selected_voice = male_voices[0]
            else:  # auto
                # Prefer female voices for clarity, fallback to first available
                female_voices = [v for v in voices if 'female' in v.name.lower() or 'woman' in v.name.lower() or 'zira' in v.name.lower()]
                if female_voices:
                    selected_voice = female_voices[0]
                else:
                    selected_voice = voices[0]
            
            if selected_voice:
                self.engine.setProperty('voice', selected_voice.id)
                
        except Exception:
            # If voice setting fails, continue with default
            pass

    def speak(self, text: str) -> None:
        """
        Convert text into speech and play it using the best available TTS engine.
        """
        if not text.strip():
            return

        # Try Google TTS first for more natural voice
        if self.use_gtts and self.gtts_engine:
            try:
                import tempfile
                import os
                import subprocess
                import time
                
                # Create temporary file for audio
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    temp_path = tmp_file.name
                
                # Generate speech with Google TTS
                tts = self.gtts_engine(text=text, lang='en', slow=False)
                tts.save(temp_path)
                
                # Play the audio using Windows media player
                try:
                    # Try using Windows built-in media player
                    subprocess.run(['powershell', '-c', f'(New-Object -comObject WMPlayer.OCX).openPlayer("{temp_path}")'], 
                                 check=True, capture_output=True)
                    # Wait a bit for the media to start playing
                    time.sleep(len(text.split()) * 0.15)  # Rough estimate of playback time
                except:
                    # Fallback to start command
                    subprocess.run(['start', temp_path], shell=True, check=True)
                    time.sleep(len(text.split()) * 0.15)
                
                # Clean up temporary file after a delay
                import threading
                def cleanup():
                    time.sleep(2)  # Wait 2 seconds before cleanup
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                
                threading.Thread(target=cleanup, daemon=True).start()
                return
                
            except Exception as e:
                print(f"Google TTS failed: {e}, falling back to system TTS")
                self.use_gtts = False  # Disable GTTS for future calls

        # Fallback to pyttsx3
        if self.engine is not None:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"System TTS failed: {e}")
