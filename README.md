# ADK Bidirectional Streaming Test Tool

A comprehensive testing framework for Google Agent Development Kit (ADK) bidirectional streaming functionality. This tool tests both text and voice interactions across Google AI Studio and Gemini Enterprise platforms with multiple Gemini models.

## Latest Test Report:

See [the latest test report](test_report.md)

## Features

### Core Functionality
- **Bidirectional Streaming**: Tests real-time streaming communication with ADK agents
- **Multi-Platform Support**: Tests both Google AI Studio and Gemini Enterprise (formerly Vertex AI). Select Gemini Enterprise with `--platform ge`. The SDK environment variable keeps its old name: `GOOGLE_GENAI_USE_VERTEXAI`.
- **Dual Test Modes**: Comprehensive text chat and voice chat testing
- **Automated Test Reports**: Generates detailed test reports with success metrics and error analysis
- **Voice Processing**: Real-time audio conversion, playback, and transcription capabilities
- **Model Validation**: Tests multiple Gemini models with different capabilities

### Test Coverage

#### Google AI Studio Models
- `gemini-2.5-flash-native-audio-preview-09-2025`: Native audio model (audio-only, uses transcription for text tests)
- `gemini-2.5-flash-native-audio-preview-12-2025`: Native audio model (December 2025 version)
- `gemini-3.1-flash-live-preview`: Gemini 3.1 Flash live preview model (legacy preview)
- `gemini-3.8-live`: Gemini 3.8 Live (stable)
- `gemini-3.8-live-extended-thinking`: Gemini 3.8 Live with background reasoning (stable)

#### Gemini Enterprise Models
- `gemini-live-2.5-flash-native-audio`: Native audio model
- `gemini-3.8-live`: Gemini 3.8 Live (GA)

### Audio Processing Pipeline
- **Input Processing**: Converts M4A audio files to 16kHz, mono, 16-bit PCM format
- **Streaming Upload**: Sends audio in 1KB chunks for real-time processing
- **Response Handling**: Receives 24kHz audio responses from models
- **Audio Playback**: Plays responses through system speakers using PyAudio
- **Speech Transcription**: Uses Google Cloud Speech-to-Text for response validation

### Audio-Only Model Support
Models with "native-audio" or "-live" in their names (e.g., `gemini-2.5-flash-native-audio-preview-09-2025`, `gemini-3.8-live`) are audio-only models that require special handling:

- **Text Chat Tests**: Instead of using TEXT modality, these models:
  - Use AUDIO response modality with `output_audio_transcription` enabled
  - Receive audio responses that are automatically transcribed by the API
  - Extract text from `event.output_transcription.text` in the response stream
  - Display as "Text (audio transcript)" in test reports

- **Voice Chat Tests**: Work the same as standard models with direct audio input/output

This allows comprehensive testing of audio-only models across both text and voice interaction modes.

## Requirements

### Platform Dependencies

#### macOS

- **Homebrew**: Package manager for installing system dependencies
- **PortAudio**: Audio I/O library for PyAudio
  ```bash
  brew install portaudio
  ```
- **FFmpeg**: Audio/video processing for format conversion
  ```bash
  brew install ffmpeg
  ```

#### Linux (Debian/Ubuntu)

- **PortAudio**: Audio I/O library for PyAudio (development headers required)
  ```bash
  sudo apt-get install portaudio19-dev
  ```
- **FFmpeg**: Audio/video processing for format conversion
  ```bash
  sudo apt-get install ffmpeg
  ```

### Python Dependencies

This project uses [uv](https://docs.astral.sh/uv/) for Python and dependency management. Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create .venv and install the locked dependencies
uv sync
```

To test a different ADK version locally, re-pin it in the lock file:

```bash
uv lock --upgrade-package "google-adk==2.10.0"
uv sync
```

Key dependencies:
- `google-adk`: Google Agent Development Kit (version in current_adk_version.txt)
- `google-cloud-speech`: Google Cloud Speech-to-Text API
- `pyaudio`: Audio I/O (requires PortAudio)
- `pydub`: Audio manipulation (requires FFmpeg)
- `python-dotenv`: Environment variable management
- `audioop-lts`: Audio operations compatibility for Python 3.13+

### Environment Setup

1. **Create Environment File**:
   Create a `.env` file in the project root with:
   ```env
   # For Google AI Studio
   GOOGLE_API_KEY=your_api_key_here
   
   # For Gemini Enterprise
   GOOGLE_CLOUD_PROJECT=your_project_id
   GOOGLE_CLOUD_LOCATION=us-central1  # Optional: defaults to us-central1 if not set
   ```

2. **SSL Configuration**:
   The tool automatically configures SSL certificates using `certifi`

3. **Audio File**:
   Ensure `whattime.m4a` is present in the project root for voice testing

## Usage

### Quick Start
```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Run tests
uv run python test_tool.py
```

### Run All Tests (Recommended)
```bash
# Run comprehensive test suite across all platforms and models
uv run python test_tool.py
```

### Platform-Specific Testing
```bash
# Test Google AI Studio only
uv run python test_tool.py --platform google-ai-studio

# Test Gemini Enterprise only
uv run python test_tool.py --platform ge
```

### Single Model Testing
```bash
# Test specific model on specific platform
uv run python test_tool.py --platform google-ai-studio --model gemini-3.8-live
uv run python test_tool.py --platform ge --model gemini-live-2.5-flash-native-audio
```

### Region-Specific Testing
```bash
# Test with specific region (overrides GOOGLE_CLOUD_LOCATION env var)
uv run python test_tool.py --platform ge --region europe-west1

# Test specific model in specific region
uv run python test_tool.py --platform ge --model gemini-live-2.5-flash-native-audio --region us-west1

# Region priority: --region parameter > GOOGLE_CLOUD_LOCATION env var > us-central1 default
```

### Headless Mode (CI/GitHub Actions)
```bash
# Run tests without audio playback (for CI environments)
uv run python test_tool.py --headless

# Headless mode:
# - Skips audio playback to speakers
# - Preserves all validation functionality
# - Generates complete test reports
# - Compatible with GitHub Actions and other CI systems
```

## Automated Testing (GitHub Actions)

This repository includes an automated workflow that monitors PyPI for new Google ADK releases and automatically runs comprehensive tests.

### Workflow Features

- **Automatic Version Detection**: Checks PyPI every 12 hours for new `google-adk` releases
- **Smart Testing**: Runs tests only when a new version is detected
- **Comprehensive Coverage**: Tests all platforms (Google AI Studio + Gemini Enterprise) and models
- **Automated Reporting**: Commits test reports with detailed results and analytics
- **Failure Notifications**: Creates GitHub issues when tests fail
- **Manual Triggers**: Supports manual workflow runs with force option

### Workflow Configuration

The workflow is defined in `.github/workflows/adk-version-monitor.yml` and runs:
- **Scheduled**: Every 12 hours (midnight and noon UTC)
- **Manual**: Via GitHub Actions UI or `gh workflow run` command

### Required GitHub Secrets

Configure these secrets in your repository settings (Settings > Secrets and variables > Actions):

| Secret Name | Description | Required For |
|-------------|-------------|--------------|
| `GOOGLE_API_KEY` | Google AI Studio API key | Google AI Studio tests |
| `GOOGLE_CLOUD_PROJECT` | Google Cloud project ID | Gemini Enterprise tests |
| `WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider resource name | Gemini Enterprise authentication |
| `SERVICE_ACCOUNT_EMAIL` | Service account email address | Gemini Enterprise authentication |
| `GOOGLE_CLOUD_LOCATION` | Default region (e.g., `us-central1`) | Gemini Enterprise tests (optional) |

### Setting Up Secrets

#### 1. Google AI Studio API Key
```bash
# Get your API key from https://aistudio.google.com/app/apikey
gh secret set GOOGLE_API_KEY
# Paste your API key when prompted
```

#### 2. Google Cloud Project
```bash
gh secret set GOOGLE_CLOUD_PROJECT
# Enter your project ID (e.g., my-project-12345)
```

#### 3. Workload Identity Federation Setup

This uses Workload Identity Federation (recommended by Google) instead of service account keys, which is more secure and doesn't require managing keys.

**Step 3a: Create Service Account**
```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Create service account
gcloud iam service-accounts create adk-tester \
  --project="${PROJECT_ID}" \
  --display-name="ADK Test Runner"

# Grant required permissions for Gemini Enterprise
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:adk-tester@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

**Step 3b: Create Workload Identity Pool**
```bash
# Create Workload Identity Pool
gcloud iam workload-identity-pools create "github-actions-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Get the pool ID (save this for later)
gcloud iam workload-identity-pools describe "github-actions-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"
```

**Step 3c: Create Workload Identity Provider**
```bash
# Replace YOUR_GITHUB_ORG and YOUR_REPO_NAME with your values
export GITHUB_REPO="YOUR_GITHUB_ORG/YOUR_REPO_NAME"

gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '$(echo ${GITHUB_REPO} | cut -d'/' -f1)'" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

**Step 3d: Allow GitHub Actions to Impersonate Service Account**
```bash
gcloud iam service-accounts add-iam-policy-binding "adk-tester@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/${GITHUB_REPO}"
```

**Step 3e: Get Values for GitHub Secrets**
```bash
# Get Workload Identity Provider (save this value)
gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --format="value(name)"

# This will output something like:
# projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider

# Service account email is:
# adk-tester@${PROJECT_ID}.iam.gserviceaccount.com
```

**Step 3f: Set GitHub Secrets**
```bash
# Set Workload Identity Provider (paste the full resource name from step 3e)
gh secret set WORKLOAD_IDENTITY_PROVIDER
# Example: projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider

# Set Service Account Email
gh secret set SERVICE_ACCOUNT_EMAIL
# Example: adk-tester@your-project-id.iam.gserviceaccount.com
```

#### 4. Cloud Location (Optional)
```bash
gh secret set GOOGLE_CLOUD_LOCATION
# Enter region (e.g., us-central1, europe-west1)
```

### Workflow Behavior

#### When New Version Detected

1. **Version Check**: Compares PyPI version with `current_adk_version.txt`
2. **Test Execution**: Pins the new version in `uv.lock` with `uv lock --upgrade-package`, then runs `uv run python test_tool.py --headless`
3. **Report Generation**: Creates timestamped test report (e.g., `test_report_us-central1_20251030_123456.md`)
4. **Auto-Commit**: Commits the report, version file, and `uv.lock` with message:
   ```
   Test results for google-adk v1.18.0

   - Tested on: 2025-10-30 12:34:56 UTC
   - Platform: GitHub Actions (headless mode)
   - Success Rate: 85%
   - Tests Passed: 17/20
   - Report: test_report_us-central1_20251030_123456.md
   ```
5. **Issue Creation**: If tests fail, creates issue with failure summary and links

#### When No New Version

- Workflow exits early with "No new version detected"
- No tests run, no commits made
- Minimal resource usage

### Manual Workflow Triggers

```bash
# Run workflow manually (tests only if new version available)
gh workflow run adk-version-monitor.yml

# Force test run even if version unchanged
gh workflow run adk-version-monitor.yml -f force_run=true

# View workflow runs
gh run list --workflow=adk-version-monitor.yml

# View specific run logs
gh run view <run-id> --log
```

### Version Tracking

The file `current_adk_version.txt` tracks the last tested ADK version:
- Updated automatically after successful test runs
- Used to detect new releases and as the version source for test reports
- Current version is read from this file by test_tool.py for all reporting

### Benefits

- **Zero Maintenance**: Automatic testing without manual intervention
- **Early Detection**: Catch breaking changes immediately after release
- **Historical Tracking**: All test reports committed to repository
- **Version Audit Trail**: Clear record of tested versions
- **Multi-Platform Coverage**: Tests both Google AI Studio and Gemini Enterprise
- **Comprehensive Reports**: Full analytics, transcriptions, and error traces

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
2. Detects model type and configures appropriate response modality:
   - **Standard models**: Uses TEXT modality for text responses
   - **Audio-only models**: Uses AUDIO modality with `AudioTranscriptionConfig` for audio responses with automatic transcription
3. Sends text query via streaming API
4. Receives and validates streaming response (text or audio transcript)
5. Verifies response contains time information

### Voice Chat Testing
1. Loads and converts M4A audio file to Live API format (16kHz, mono, 16-bit PCM)
2. Streams audio in chunks to ADK agent
3. Receives audio response at 24kHz
4. Plays audio response through speakers
5. Transcribes response using Google Cloud Speech-to-Text
6. Validates transcribed content for time information

### ADK Evaluation for Live Models (Not Adopted)

ADK evaluation supports Live models through `EvalConfig.live_model_config`. We checked it against google-adk 2.10.0 in September 2026 and decided not to use it in this tool for now. It can grade answer quality, but it cannot replace the streaming checks above.

What it would add:
- **Correctness grading.** The keyword check passes a wrong time as long as the answer mentions one (for example, `gemini-3.1-flash-live-preview` has answered with a wrong time). A rubric-based judge (`rubric_based_final_response_quality_v1`) could fail wrong answers if the rubric included the current time at run time.
- **Test cases as data.** Eval sets and the audio user simulator (`LlmAudioUserSimulator`) would allow more questions and multi-turn conversations without code changes.

Why it cannot replace the current tests:
- **It grades the output transcription, not the output audio.** `final_response` is built from `output_transcription`, and the judge only reads text parts. Broken, silent, or truncated audio passes as long as the transcript looks right. The voice test here transcribes the actual audio bytes with Google Cloud Speech-to-Text and fails when no audio arrives.
- **It does not exercise automatic VAD.** Eval wraps each user turn in `send_activity_start()` / `send_activity_end()`. The voice test streams audio the way an app does and relies on server-side voice activity detection, which is how we found that `gemini-3.8-live` needs trailing silence before it responds.
- **google_search is not visible as a tool call.** The search does run in live eval on both platforms and returns correct answers. It runs server-side, though, so `get_all_tool_calls()` is empty and `tool_trajectory_avg_score` cannot check it. Only `rubric_based_final_response_quality_v1` passes grounding metadata to the judge. Gemini Enterprise fills it with the search queries and sources; Google AI Studio returns empty grounding metadata.
- **Cost.** Judge model calls add API cost and CI time.

If this tool adopts ADK evaluation later, it should run as an extra mode for answer correctness alongside the existing text and voice tests.

## Test Reports

The tool automatically generates comprehensive test reports including:

- **Test Summary**: Overall success rates and statistics
- **Platform Breakdown**: Results by Google AI Studio vs Gemini Enterprise
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
   - Detects and handles audio-only models with automatic transcription
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
- [Gemini Enterprise Live API](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api)
