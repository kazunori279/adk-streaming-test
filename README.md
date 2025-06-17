# Project: ADK Bidi-Streaming test

This is an instruction for Claude Code to build a test tool. Works only with macOS.

## Goal

Build a test tool for bidirectional streamping functionality with Google ADK (Agent Development Kit)

## Tech Stack

- Google ADK
  - A simple agent with a Google Search built-in tool
  - Bidi-streaming API for communicating with the agent

## Requirements

### Platform Dependencies (macOS)

This test tool is currently designed for macOS and uses the following Mac-specific dependencies:

- **Homebrew**: Package manager for installing system dependencies
- **PortAudio**: Audio I/O library for PyAudio (installed via `brew install portaudio`)
- **FFmpeg**: Audio/video processing library for M4A file conversion (installed via `brew install ffmpeg`)

### Python Dependencies

Install Python dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Dependencies include:
- `google-adk==1.3.0`: Google Agent Development Kit
- `pyaudio`: Audio playback/recording (requires PortAudio system library)
- `pydub`: Audio file format conversion (requires FFmpeg)
- `google-cloud-texttospeech`: Google Cloud TTS API
- `google-cloud-speech`: Google Cloud STT API
- `python-dotenv`: Environment variable management

### Resources

- GitHub resources: Use the GitHub MCP server to read the following resources on GitHub to learn how to use ADK and Bidi-streaming API:
  - examples/python/snippets/streaming/adk-streaming/ from the google/adk-docs repository
  - docs/streaming/custom-streaming.md from the google/adk-docs repository
- Text to speech: refer to the following page:
  - https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python
- Speech to text: refer to the following page:
  - https://cloud.google.com/speech-to-text/docs/speech-to-text-client-libraries

### Environment Setup

- Check if .env exists. If not, create one
- Set SSL_CERT_FILE variable before running the server, as explained in the doc
- For voice tests, ensure `whattime.m4a` audio file is present in the project root

## Test specification

For each `Test cases` below, test the `Test functionality`:

- Test cases:

  - Google AI Studio test:
    - Environment variables setting:
      - set GOOGLE_GENAI_USE_VERTEXAI=FALSE
      - Use GOOGLE_API_KEY in .env file
    - Models to test:
      - gemini-2.0-flash-live-001
      - gemini-2.5-flash-preview-native-audio-dialog
      - gemini-2.5-flash-exp-native-audio-thinking-dialog
      - gemini-2.0-flash-exp

  - Vertex AI test:
    - Environment variables setting:
      - set GOOGLE_GENAI_USE_VERTEXAI=TRUE
      - Use GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION in .env file
    - Models to test:
      - gemini-2.0-flash-live-preview-04-09
      - gemini-2.0-flash-exp

- Test functionality:
  - Text chat: ask "What time is it now?" and verify the agent responds with the time
  - Voice chat: ask "What time is it now?" with voice, and verify the agent responds with the time in voice.

- Test report:
  - Output a text file that summarizes the result of all test cases.
