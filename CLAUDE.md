# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python testing framework for Google Agent Development Kit (ADK) bidirectional streaming functionality. The project provides automated testing across multiple platforms and models with both text and voice interaction capabilities.

### Key Features
- **Multi-Platform Testing**: Google AI Studio and Google Cloud Vertex AI
- **Dual Test Modes**: Text chat and voice chat testing
- **Model Coverage**: Tests multiple Gemini models including live, experimental, and native-audio variants
- **Voice Processing Pipeline**: Complete audio conversion, streaming, playback, and transcription
- **Automated Reporting**: Comprehensive test reports with metrics, transcriptions, and error analysis
- **Real-time Streaming**: Bidirectional streaming with chunked audio processing
- **Validation Framework**: Automated response verification with configurable success criteria

### Technical Components
- Python virtual environment in `.venv/`
- Google ADK v1.17.0 for AI agent development
- Audio processing capabilities (PyAudio for I/O, pydub for conversion)
- Google Cloud Speech-to-Text integration for voice validation
- MCP (Model Context Protocol) configuration with GitHub server access
- SSL certificate management with certifi
- Environment-based platform configuration

## Development Environment

### Virtual Environment
The project uses a Python virtual environment located in `.venv/`. Activate it with:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Dependencies
Dependencies are managed through `requirements.txt`. Key dependencies include:
- **google-adk==1.17.0**: Google Agent Development Kit with streaming support
- **google-cloud-speech**: Google Cloud Speech-to-Text API for voice transcription
- **PyAudio**: Audio I/O library for real-time audio playback (requires PortAudio)
- **pydub**: Audio format conversion and manipulation (requires FFmpeg)
- **python-dotenv**: Environment variable management for platform configuration

**System Dependencies (macOS)**:
```bash
# Install via Homebrew
brew install portaudio ffmpeg
```

**Python Dependencies**:
```bash
pip install -r requirements.txt
```

## Common Commands

Development and testing commands for this ADK streaming test project:

### Environment Setup
- **Activate virtual environment**: `source .venv/bin/activate`
- **Install dependencies**: `pip install -r requirements.txt`
- **Update ADK**: `pip install --upgrade google-adk`
- **Generate requirements**: `pip freeze > requirements.txt`

### Testing Commands
- **Run all tests (recommended)**: `python test_tool.py`
- **Test specific platform**: `python test_tool.py --platform google-ai-studio`
- **Test specific model**: `python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp`
- **Test with specific region**: `python test_tool.py --platform vertex-ai --region europe-west1`
- **Test specific model in region**: `python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp --region us-west1`
- **View test results**: Open generated timestamped report files

### Platform Configuration
- **Google AI Studio**: Requires `GOOGLE_API_KEY` in `.env`, sets `GOOGLE_GENAI_USE_VERTEXAI=FALSE`
- **Vertex AI**: Requires `GOOGLE_CLOUD_PROJECT` in `.env`, sets `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
  - **Region Priority**: CLI `--region` parameter > `GOOGLE_CLOUD_LOCATION` env var > `us-central1` default

## MCP Configuration

The project includes MCP (Model Context Protocol) configuration in `.mcp.json` with access to:

- **GitHub MCP Server**: Provides GitHub API functionality including repository management, issues, pull requests, and user information access
- Used for accessing ADK documentation and examples from google/adk-docs repository
- Enables integration with GitHub workflow for issue tracking and documentation updates

## Project Structure

```text
adk-streaming-test/
├── .venv/                 # Python virtual environment
├── .env                   # Environment variables (create manually)
├── .mcp.json             # MCP configuration for GitHub access
├── CLAUDE.md             # Project documentation for Claude Code
├── README.md             # Comprehensive project documentation
├── requirements.txt      # Python dependencies
├── test_tool.py          # Main ADK streaming test tool (755 lines)
├── test_report_*.md      # Generated test reports with region and timestamp
├── whattime.m4a          # Audio test file ("What time is it now?")
└── LICENSE               # Project license
```

### File Details

- **test_tool.py**: Comprehensive test framework with classes for streaming tests, voice handling, and report generation
- **test_report_*.md**: Auto-generated reports with success metrics, transcriptions, error traces, and methodology documentation (format: `test_report_{region}_{timestamp}.md`)
- **.env**: Contains API keys and project configuration (not tracked in git)
- **whattime.m4a**: M4A audio file used for voice testing, converted to PCM format during tests

## Architecture

This project provides a comprehensive testing framework for Google ADK streaming functionality with the following architecture:

### Core Classes

#### ADKStreamingTester

Main test orchestrator that handles:

- Platform environment configuration (Google AI Studio vs Vertex AI)
- ADK agent session creation with Google Search tool integration
- Text chat testing with streaming response collection
- Voice chat testing with audio processing pipeline
- Error handling and result collection
- Test validation using configurable success criteria

#### VoiceHandler

Audio processing engine that manages:

- Audio file loading and format conversion (M4A to 16kHz PCM)
- Real-time audio streaming in 1KB chunks
- Audio playback through system speakers (24kHz output)
- Speech-to-Text transcription for response validation
- PyAudio instance management and cleanup

#### Config

Centralized configuration management:

- Platform-specific model definitions
- Audio processing parameters (sample rates, formats, chunk sizes)
- Test criteria and validation keywords
- Timeout and streaming configuration

### Testing Pipeline

1. **Environment Setup**: Dynamic platform configuration based on test target
2. **Agent Creation**: ADK agent with Google Search tool for time queries
3. **Session Management**: Live session creation and streaming setup
4. **Test Execution**: Parallel text and voice testing across all models
5. **Response Processing**: Audio conversion, playback, and transcription
6. **Validation**: Keyword-based success criteria validation
7. **Report Generation**: Comprehensive analytics and error documentation

### Supported Models

#### Google AI Studio

- `gemini-2.0-flash-exp`: Experimental flash model
- `gemini-2.0-flash-live-001`: Production-ready live model
- `gemini-live-2.5-flash-preview`: Latest live preview with enhanced streaming
- `gemini-2.5-flash-native-audio-preview-09-2025`: Native audio model
- `gemini-2.5-flash-preview-native-audio-dialog`: Dialog-optimized native audio model
- `gemini-2.5-flash-exp-native-audio-thinking-dialog`: Experimental thinking-mode native audio model

#### Vertex AI

- `gemini-2.0-flash-exp`: Experimental model on Vertex AI
- `gemini-live-2.5-flash-preview-native-audio`: Native audio processing model
- `gemini-live-2.5-flash-preview-native-audio-09-17`: Native audio model (September 2025 version)

### Audio Processing Flow

1. **Input**: M4A file → pydub conversion → 16kHz, mono, 16-bit PCM
2. **Streaming**: PCM chunks → ADK Live API → Real-time processing
3. **Output**: 24kHz audio response → PyAudio playback
4. **Validation**: Audio → Google Cloud Speech-to-Text → Content verification

### Report Generation

Automated generation of detailed test reports including:

- Test summary with success rates and platform breakdown
- Model-specific results with pass/fail status
- Voice transcription results for all successful voice tests
- Detailed error traces with full stack traces for debugging
- Test methodology documentation
- Environment and configuration information
- Failed test analysis with categorized failure reasons

## Testing Strategy

### Test Execution Flow

1. **Comprehensive Testing** (`python test_tool.py`):
   - Tests all Google AI Studio models with both text and voice
   - Tests all Vertex AI models with both text and voice
   - Generates combined analytics and success metrics
   - Produces detailed test report with transcriptions and error analysis

2. **Platform-Specific Testing**:
   - Isolates testing to single platform for focused debugging
   - Useful for API key validation and platform-specific issues

3. **Model-Specific Testing**:
   - Tests individual models for detailed analysis
   - Helps identify model-specific capabilities and limitations

### Validation Criteria

- **Response Content**: Must contain time-related keywords (time, clock, hour, minute, am, pm, utc, gmt, o'clock)
- **Tool Usage**: Agent must successfully use Google Search tool for real-time information
- **Streaming**: Bidirectional communication must work without connection errors
- **Audio Quality**: Voice responses must be playable and transcribable

### Error Handling

- **Connection Errors**: WebSocket connection issues with detailed traces
- **Model Availability**: Graceful handling of unavailable models
- **Authentication**: Clear error messages for API key and permission issues
- **Audio Processing**: Comprehensive error handling for audio pipeline failures
- **Timeouts**: Configurable timeout handling with 60-second default for voice tests

## Development Workflows

### Adding New Models

1. Update model lists in `Config.GOOGLE_AI_STUDIO_MODELS` or `Config.VERTEX_AI_MODELS`
2. Ensure model supports required modalities (text/audio)
3. Test with both platforms to verify compatibility
4. Update documentation with model capabilities and limitations

### Modifying Test Criteria

1. Update `Config.TEST_QUESTION` for different test scenarios
2. Modify `Config.TIME_KEYWORDS` for different validation criteria
3. Adjust `_verify_time_response()` method for custom validation logic
4. Update methodology documentation in report generation

### Extending Audio Capabilities

1. Modify `VoiceHandler` class for different audio formats
2. Update audio configuration in `Config` class
3. Ensure compatibility with ADK Live API requirements
4. Test with different audio sample rates and formats

### Report Customization

1. Modify report generation functions for additional metrics
2. Add new analysis sections in `generate_test_report()`
3. Customize output format and content structure
4. Include additional debugging information as needed
