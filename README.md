# ADK Bidirectional Streaming Test Tool

A comprehensive testing framework for Google Agent Development Kit (ADK) bidirectional streaming functionality. This tool tests both text and voice interactions across Google AI Studio and Vertex AI platforms with multiple Gemini models.

## Features

### Core Functionality
- **Bidirectional Streaming**: Tests real-time streaming communication with ADK agents
- **Multi-Platform Support**: Tests both Google AI Studio and Google Cloud Vertex AI
- **Dual Test Modes**: Comprehensive text chat and voice chat testing
- **Automated Test Reports**: Generates detailed test reports with success metrics and error analysis
- **Voice Processing**: Real-time audio conversion, playback, and transcription capabilities
- **Model Validation**: Tests multiple Gemini models with different capabilities

### Test Coverage

#### Google AI Studio Models
- `gemini-live-2.5-flash-preview`: Latest live preview with enhanced streaming
- `gemini-2.0-flash-live-001`: Production-ready live model
- `gemini-2.0-flash-exp`: Experimental flash model

#### Vertex AI Models
- `gemini-live-2.5-flash-preview-native-audio`: Native audio processing model
- `gemini-2.0-flash-exp`: Experimental model on Vertex AI

### Audio Processing Pipeline
- **Input Processing**: Converts M4A audio files to 16kHz, mono, 16-bit PCM format
- **Streaming Upload**: Sends audio in 1KB chunks for real-time processing
- **Response Handling**: Receives 24kHz audio responses from models
- **Audio Playback**: Plays responses through system speakers using PyAudio
- **Speech Transcription**: Uses Google Cloud Speech-to-Text for response validation

## Requirements

### Platform Dependencies (macOS)

This tool is optimized for macOS and requires:

- **Homebrew**: Package manager for installing system dependencies
- **PortAudio**: Audio I/O library for PyAudio
  ```bash
  brew install portaudio
  ```
- **FFmpeg**: Audio/video processing for format conversion
  ```bash
  brew install ffmpeg
  ```

### Python Dependencies

Install from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Key dependencies:
- `google-adk==1.6.1`: Google Agent Development Kit
- `google-cloud-speech`: Google Cloud Speech-to-Text API
- `pyaudio`: Audio I/O (requires PortAudio)
- `pydub`: Audio manipulation (requires FFmpeg)
- `python-dotenv`: Environment variable management

### Environment Setup

1. **Create Environment File**:
   Create a `.env` file in the project root with:
   ```env
   # For Google AI Studio
   GOOGLE_API_KEY=your_api_key_here
   
   # For Vertex AI
   GOOGLE_CLOUD_PROJECT=your_project_id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

2. **SSL Configuration**:
   The tool automatically configures SSL certificates using `certifi`

3. **Audio File**:
   Ensure `whattime.m4a` is present in the project root for voice testing

## Usage

### Run All Tests (Recommended)
```bash
# Run comprehensive test suite across all platforms and models
python test_tool.py
```

### Platform-Specific Testing
```bash
# Test Google AI Studio only
python test_tool.py --platform google-ai-studio

# Test Vertex AI only
python test_tool.py --platform vertex-ai
```

### Single Model Testing
```bash
# Test specific model on specific platform
python test_tool.py --platform google-ai-studio --model gemini-2.0-flash-live-001
python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp
```

## Test Methodology

### Test Question
All tests use the standardized question: **"What time is it now?"**

### Success Criteria
- Response contains time-related keywords (time, clock, hour, minute, am, pm, utc, gmt)
- Agent successfully uses Google Search tool for real-time information
- Bidirectional streaming communication works correctly
- Voice responses are successfully transcribed and validated

### Text Chat Testing
1. Establishes ADK agent session with Google Search tool
2. Sends text query via streaming API
3. Receives and validates streaming text response
4. Verifies response contains time information

### Voice Chat Testing
1. Loads and converts M4A audio file to Live API format (16kHz, mono, 16-bit PCM)
2. Streams audio in chunks to ADK agent
3. Receives audio response at 24kHz
4. Plays audio response through speakers
5. Transcribes response using Google Cloud Speech-to-Text
6. Validates transcribed content for time information

## Test Reports

The tool automatically generates comprehensive test reports (`test_report.txt`) including:

- **Test Summary**: Overall success rates and statistics
- **Platform Breakdown**: Results by Google AI Studio vs Vertex AI
- **Model-Specific Results**: Individual pass/fail status for each model
- **Voice Transcriptions**: Full transcripts of voice responses
- **Error Analysis**: Detailed error traces for failed tests
- **Environment Information**: ADK version, dependencies, and configuration
- **Methodology Documentation**: Complete testing procedures

### Sample Report Metrics
- Total tests run and success rate
- Text vs voice test breakdown
- Platform-specific performance
- Model compatibility analysis
- Failed test investigation

## Architecture

### Core Components

1. **ADKStreamingTester**: Main test orchestrator
   - Manages platform configuration
   - Handles agent session creation
   - Executes test workflows
   - Collects results and metrics

2. **VoiceHandler**: Audio processing engine
   - Audio format conversion
   - Real-time audio streaming
   - Speech-to-text transcription
   - Audio playback management

3. **Config**: Centralized configuration
   - Model definitions for each platform
   - Audio processing parameters
   - Test criteria and validation rules

### Technical Details

- **Audio Configuration**: Input 16kHz, Output 24kHz, PCM format, Mono channel
- **Streaming**: 1KB chunks with minimal latency
- **Timeout Handling**: 60-second timeout for voice tests
- **Error Recovery**: Comprehensive exception handling with detailed traces
- **Platform Switching**: Dynamic environment configuration for each platform

## Development

### Adding New Models
1. Update model lists in `Config` class
2. Ensure model compatibility with chosen platform
3. Test with both text and voice modes

### Extending Test Cases
1. Modify test questions in `Config.TEST_QUESTION`
2. Update validation keywords in `Config.TIME_KEYWORDS`
3. Adjust success criteria in `_verify_time_response()`

### Customizing Reports
1. Modify report generation functions in `generate_test_report()`
2. Add new metrics or analysis sections
3. Customize output format and content

## Troubleshooting

### Common Issues

1. **Audio Dependencies**: Ensure PortAudio and FFmpeg are installed via Homebrew
2. **Environment Variables**: Verify `.env` file contains correct API keys and project settings
3. **Model Access**: Ensure you have access to all tested models on both platforms
4. **Network Connectivity**: Stable internet required for streaming tests
5. **SSL Certificates**: Tool automatically configures certificates using certifi

### Error Analysis

The test tool provides detailed error traces in reports, including:
- WebSocket connection errors
- Model availability issues
- Authentication problems
- Audio processing failures
- Transcription service errors

## Resources

- [Google ADK Documentation](https://github.com/google/adk-docs)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/docs/speech-to-text-client-libraries)
- [Gemini Live API Models](https://ai.google.dev/gemini-api/docs/models#live-api)
- [Vertex AI Live API](https://cloud.google.com/vertex-ai/generative-ai/docs/live-api)
