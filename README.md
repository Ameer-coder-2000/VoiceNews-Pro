# Voice-Based AI News Assistant

A beginner-friendly Python project that listens to a spoken question like "What is the news today?", fetches the latest headlines, summarizes them, and reads the result aloud. Now available as both a command-line tool and a web application!

## Features

- Capture voice from the microphone (command-line) or browser (web app)
- Convert speech to text
- Fetch the latest global news from GNews
- Detect simple categories such as sports, technology, business, and health
- Summarize the top headlines into a short spoken response
- **Voice Selection**: Choose between male, female, or auto-selected voices for clear, high-quality speech
- Read the result aloud using text-to-speech
- Handle common errors such as no internet, missing API key, and unclear speech
- Web interface for easy deployment and browser-based access

## Project Structure

```text
.
|-- main.py                 # Command-line application
|-- app.py                  # Web application
|-- config.py
|-- requirements.txt
|-- .env.example
|-- templates/
|   `-- index.html          # Web interface
|-- services/
|   |-- speech_to_text.py
|   |-- news_service.py
|   |-- summarizer.py
|   `-- text_to_speech.py
`-- README.md
```

## Setup

1. Create a virtual environment:

```powershell
python -m venv venv
```

2. Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install the dependencies:

```powershell
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add your API key:

```env
NEWS_API_KEY=your_api_key_here
NEWS_API_PROVIDER=gnews
DEFAULT_CATEGORY=general
DEFAULT_COUNTRY=in
MAX_HEADLINES=5
LANGUAGE=en
```

## Run the Project

### Command-Line Version

```powershell
python main.py
```

If microphone support is not working yet, the app will automatically switch to text input mode.

You can also test it directly in text mode:

```powershell
python main.py --text
```

Or run one command with a question:

```powershell
python main.py --query "What is the latest technology news?" --voice female
```

### Voice Options

Choose your preferred voice for text-to-speech:

```powershell
# Auto-select best voice (default)
python main.py --voice auto

# Female voice (usually clearer)
python main.py --voice female

# Male voice
python main.py --voice male
```

### Web Application Version

```powershell
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000/` to access the web interface.

The web app provides:
- Voice input using your browser's microphone
- Text input as an alternative
- Category selection
- **Voice selection** with test button for different male/female voices
- Visual display of news articles
- Text-to-speech output through your browser

Then speak a question like:

- "What is the news today?"
- "Tell me the latest technology news."
- "Give me sports headlines."

## How It Works

### Command-Line Version

1. The app records your voice through the microphone using `sounddevice`.
2. It converts your voice into text using `SpeechRecognition`.
3. It detects the requested category from your sentence.
4. It calls the GNews API to fetch the latest headlines.
5. It creates a short summary from the top headlines.
6. It reads the answer aloud using `pyttsx3`.

### Web Version

1. The web interface uses your browser's Web Speech API for voice input.
2. It sends the transcribed text to the Flask backend.
3. The backend detects the category and fetches news from GNews API.
4. It summarizes the headlines and returns the data.
5. The frontend displays the results and uses Web Speech API for text-to-speech output.

## Deployment

The web application can be deployed to various platforms:

### Local Development
```powershell
python app.py
```
Access at: `http://127.0.0.1:5000/`

### Production Deployment Options

1. **Heroku**: Create a `Procfile` with `web: python run.py` and deploy
2. **Railway**: Connect your GitHub repo and deploy automatically
3. **Render**: Use their free tier for web services
4. **PythonAnywhere**: Upload your code and run `python run.py`
5. **Vercel/Netlify**: For static frontend with serverless functions

Make sure to set your `NEWS_API_KEY` in the environment variables on your deployment platform.

## Notes

- Speech recognition uses Google's free recognizer and usually needs internet access.
- The text-to-speech part works offline with `pyttsx3` in command-line mode, or uses browser TTS in web mode.
- The web app requires a modern browser with Web Speech API support (Chrome, Edge, Safari).
- For deployment, make sure your hosting platform supports Python and has the required packages installed.
- The web interface provides a more user-friendly experience and is suitable for deployment on cloud platforms.
- This version does not require `PyAudio`, which helps a lot on Windows and newer Python versions.
- You can change the default category, country, and number of headlines in the `.env` file.

## Next Improvements

- Add a text input fallback when the microphone is unavailable
- Use a real LLM for smarter summarization
- Add support for multiple countries
- Save the news summary to a file
- Build a GUI with Tkinter or Streamlit



D:\DATA\PythonProject1\python.exe app.py                       