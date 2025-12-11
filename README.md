# ADK Bidirectional Streaming Test Tool

A comprehensive testing framework for Google Agent Development Kit (ADK) bidirectional streaming functionality. This tool tests both text and voice interactions across Google AI Studio and Vertex AI platforms with multiple Gemini models.

## Latest Test Report:

See [the latest test report](test_report.md)

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
- `gemini-2.0-flash-exp`: Experimental flash model
- `gemini-2.5-flash-native-audio-preview-09-2025`: Native audio model (audio-only, uses transcription for text tests)

#### Vertex AI Models
- `gemini-2.0-flash-exp`: Experimental model on Vertex AI
- `gemini-live-2.5-flash-preview-native-audio`: Native audio processing model (audio-only, uses transcription for text tests)
- `gemini-live-2.5-flash-preview-native-audio-09-17`: Native audio model (September 2025 version)

### Audio Processing Pipeline
- **Input Processing**: Converts M4A audio files to 16kHz, mono, 16-bit PCM format
- **Streaming Upload**: Sends audio in 1KB chunks for real-time processing
- **Response Handling**: Receives 24kHz audio responses from models
- **Audio Playback**: Plays responses through system speakers using PyAudio
- **Speech Transcription**: Uses Google Cloud Speech-to-Text for response validation

### Native-Audio Model Support
Models with "native-audio" in their names (e.g., `gemini-2.5-flash-native-audio-preview-09-2025`) are audio-only models that require special handling:

- **Text Chat Tests**: Instead of using TEXT modality, these models:
  - Use AUDIO response modality with `output_audio_transcription` enabled
  - Receive audio responses that are automatically transcribed by the API
  - Extract text from `event.output_transcription.text` in the response stream
  - Display as "Text (audio transcript)" in test reports

- **Voice Chat Tests**: Work the same as standard models with direct audio input/output

This allows comprehensive testing of native-audio models across both text and voice interaction modes.

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
   
   # For Vertex AI
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
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
python test_tool.py
```

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

### Region-Specific Testing
```bash
# Test with specific region (overrides GOOGLE_CLOUD_LOCATION env var)
python test_tool.py --platform vertex-ai --region europe-west1

# Test specific model in specific region
python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp --region us-west1

# Region priority: --region parameter > GOOGLE_CLOUD_LOCATION env var > us-central1 default
```

### Headless Mode (CI/GitHub Actions)
```bash
# Run tests without audio playback (for CI environments)
python test_tool.py --headless

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
- **Comprehensive Coverage**: Tests all platforms (Google AI Studio + Vertex AI) and models
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
| `GOOGLE_CLOUD_PROJECT` | Google Cloud project ID | Vertex AI tests |
| `WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider resource name | Vertex AI authentication |
| `SERVICE_ACCOUNT_EMAIL` | Service account email address | Vertex AI authentication |
| `GOOGLE_CLOUD_LOCATION` | Default region (e.g., `us-central1`) | Vertex AI tests (optional) |

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

# Grant required permissions for Vertex AI
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
2. **Test Execution**: Runs `python test_tool.py --headless` with new version
3. **Report Generation**: Creates timestamped test report (e.g., `test_report_us-central1_20251030_123456.md`)
4. **Auto-Commit**: Commits report and updates version file with message:
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
- **Multi-Platform Coverage**: Tests both Google AI Studio and Vertex AI
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
   - **Native-audio models**: Uses AUDIO modality with `AudioTranscriptionConfig` for audio responses with automatic transcription
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

## Test Reports

The tool automatically generates comprehensive test reports including:

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
   - Detects and handles native-audio models with automatic transcription
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
