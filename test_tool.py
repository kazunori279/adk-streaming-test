#!/usr/bin/env python3
"""
ADK Bidirectional Streaming Test Tool

Tests bidirectional streaming functionality with Google ADK using both
Google AI Studio and Google Cloud Vertex AI platforms. Runs combined 
text and voice tests for comprehensive evaluation.
"""

import os
import asyncio
import argparse
import warnings
from datetime import datetime
from dotenv import load_dotenv
from google.genai.types import Content, Part, Blob
from google.genai import types
from google.adk.runners import InMemoryRunner
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.tools import google_search
from google.cloud import speech
import pyaudio
from pydub import AudioSegment
import google.adk

# Suppress Pydantic serialization warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Load environment variables
load_dotenv()

# Configuration
class Config:
    """Application configuration"""
    # Model configurations

    # Google AI Studio models: https://ai.google.dev/gemini-api/docs/models#live-api
    GOOGLE_AI_STUDIO_MODELS = [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-live-001",
        "gemini-live-2.5-flash-preview",
        "gemini-2.5-flash-native-audio-preview-09-2025",
        "gemini-2.5-flash-preview-native-audio-dialog",
        "gemini-2.5-flash-exp-native-audio-thinking-dialog"
    ]
    
    # Vertex AI models: https://cloud.google.com/vertex-ai/generative-ai/docs/live-api
    VERTEX_AI_MODELS = [
        "gemini-2.0-flash-exp",
        "gemini-live-2.5-flash-preview-native-audio",
        "gemini-live-2.5-flash-preview-native-audio-09-17",
    ]
    
    # Audio configuration
    AUDIO_FORMAT = pyaudio.paInt16
    CHANNELS = 1
    INPUT_RATE = 16000   # Input audio rate for Live API
    OUTPUT_RATE = 24000  # Output audio rate from Live API
    CHUNK_SIZE = 1024    # Audio chunk size for streaming
    TIMEOUT = 60         # Test timeout in seconds
    
    # Test configuration
    TEST_QUESTION = "What time is it now?"
    AUDIO_FILE = "whattime.m4a"
    TIME_KEYWORDS = ["time", "clock", "hour", "minute", "am", "pm", "a.m", "p.m", "utc", "gmt", "o'clock"]

class VoiceHandler:
    """Handles voice input/output for testing."""

    def __init__(self):
        self.stt_client = speech.SpeechClient()
        self.pyaudio_instance = pyaudio.PyAudio()

    def load_audio_as_pcm(self, audio_path: str) -> bytes:
        """Load audio file and convert to PCM format for Live API."""
        audio = AudioSegment.from_file(audio_path)
        
        # Convert to Live API format: 16kHz, mono, 16-bit
        audio = audio.set_frame_rate(Config.INPUT_RATE)
        audio = audio.set_channels(Config.CHANNELS)
        audio = audio.set_sample_width(2)  # 16-bit = 2 bytes
        
        print(f"Audio converted - {audio.channels} channel, {audio.frame_rate}Hz, "
              f"{audio.sample_width * 8}-bit, {len(audio)}ms duration")
        
        # Return raw PCM data (little-endian)
        pcm_data = audio.raw_data
        print(f"PCM data: {len(pcm_data)} bytes")
        return pcm_data

    def play_audio(self, audio_data: bytes):
        """Play audio data through speakers."""
        stream = self.pyaudio_instance.open(
            format=Config.AUDIO_FORMAT,
            channels=Config.CHANNELS,
            rate=Config.OUTPUT_RATE,  # Live API outputs at 24kHz
            output=True
        )
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()

    def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech audio to text for verification."""
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=Config.OUTPUT_RATE,  # Use output rate for STT
            language_code="en-US",
        )
        
        response = self.stt_client.recognize(config=config, audio=audio)
        return response.results[0].alternatives[0].transcript if response.results else ""

    def __del__(self):
        """Clean up PyAudio instance."""
        if hasattr(self, 'pyaudio_instance'):
            self.pyaudio_instance.terminate()

class ADKStreamingTester:
    """Tests ADK bidirectional streaming functionality."""

    def __init__(self, platform: str, model: str, region: str = None):
        self.platform = platform
        self.model = model
        self.region = region
        self.runner = None
        self.session = None
        self.transcription_result = ""  # Store transcription for reporting
        self.error_trace = ""  # Store error details for reporting
        self.failure_reason = ""  # Store failure reason for reporting

    def _is_native_audio_model(self) -> bool:
        """Check if the model is a native-audio model."""
        return "native-audio" in self.model.lower()

    async def setup_environment(self):
        """Configure environment variables for the platform."""
        if self.platform == "google-ai-studio":
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
            if not os.getenv("GOOGLE_API_KEY"):
                raise ValueError("GOOGLE_API_KEY not found in environment")
        else:  # vertex-ai
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
            if not os.getenv("GOOGLE_CLOUD_PROJECT"):
                raise ValueError("GOOGLE_CLOUD_PROJECT required for Vertex AI")

            # Use provided region or fall back to environment variable or default
            if self.region:
                os.environ["GOOGLE_CLOUD_LOCATION"] = self.region
                print(f"Using region: {self.region}")
            elif os.getenv("GOOGLE_CLOUD_LOCATION"):
                print(f"Using region from environment: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
            else:
                os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
                print("Using default region: us-central1")

    async def create_agent_session(self):
        """Create ADK agent and session."""
        agent = Agent(
            name="time_query_agent",
            model=self.model,
            description="Agent to answer time queries using Google Search",
            instruction=f"Answer the question '{Config.TEST_QUESTION}' using the Google Search tool. "
                       "Provide the current time information.",
            tools=[google_search],
        )

        self.runner = InMemoryRunner(app_name="agents", agent=agent)
        self.session = await self.runner.session_service.create_session(
            app_name="agents", user_id="test_user"
        )
        return agent

    async def test_text_chat(self) -> bool:
        """Test text chat functionality."""
        self._print_test_header("TEXT CHAT")

        try:
            await self.setup_environment()
            await self.create_agent_session()

            # Setup live streaming based on model type
            live_request_queue = LiveRequestQueue()

            # Native-audio models require AUDIO modality with transcription
            if self._is_native_audio_model():
                print("Native-audio model detected - using AUDIO modality with transcription")
                run_config = RunConfig(
                    response_modalities=["AUDIO"],
                    output_audio_transcription=types.AudioTranscriptionConfig()
                )
            else:
                run_config = RunConfig(response_modalities=["TEXT"])

            live_events = self.runner.run_live(
                user_id="test_user",
                session_id=self.session.id,
                live_request_queue=live_request_queue,
                run_config=run_config,
            )

            # Send question and collect response
            content = Content(role="user", parts=[Part.from_text(text=Config.TEST_QUESTION)])
            live_request_queue.send_content(content=content)

            print(f"Question: {Config.TEST_QUESTION}")
            print("Response: ", end="", flush=True)

            # Collect response based on model type
            if self._is_native_audio_model():
                full_response = await self._collect_audio_transcription_response(live_events)
            else:
                full_response = await self._collect_text_response(live_events)

            live_request_queue.close()

            # Verify response
            success = self._verify_time_response(full_response)
            if not success:
                if not full_response or full_response.strip() == "":
                    self.failure_reason = "Empty response received"
                else:
                    self.failure_reason = "Response does not contain time-related keywords"
            self._print_test_result(success, "Response contains time-related information")
            return success

        except Exception as exc:
            return self._handle_test_exception(exc)
    
    def _print_test_header(self, test_type: str):
        """Print test header."""
        print(f"\n{'='*60}")
        print(f"Testing {test_type} {self.platform} with model: {self.model}")
        print(f"{'='*60}")
    
    def _print_test_result(self, success: bool, message: str):
        """Print test result."""
        status = "PASS" if success else "FAIL"
        icon = "✓" if success else "✗"
        print(f"Test Result: {status}")
        print(f"{icon} {message}")
    
    def _print_test_error(self, error_msg: str):
        """Print test error."""
        print("Test Result: ERROR")
        print(f"✗ Error: {error_msg}")
    
    def _verify_time_response(self, response: str) -> bool:
        """Verify if response contains time-related information."""
        return any(keyword in response.lower() for keyword in Config.TIME_KEYWORDS)
    
    def _handle_test_exception(self, exc: Exception) -> bool:
        """Handle test exceptions consistently."""
        import traceback
        self.error_trace = traceback.format_exc()
        self.failure_reason = f"Exception: {str(exc)}"
        self._print_test_error(str(exc))
        return False
    
    async def _collect_text_response(self, live_events) -> str:
        """Collect text response from live events."""
        full_response = ""
        async for event in live_events:
            if event.turn_complete:
                break
            if event.content and event.content.parts:
                part = event.content.parts[0]
                if part.text and event.partial:
                    print(part.text, end="", flush=True)
                    full_response += part.text
        print("\n")
        return full_response

    async def _collect_audio_transcription_response(self, live_events) -> str:
        """Collect audio transcription response from live events."""
        full_response = ""
        async for event in live_events:
            if event.turn_complete:
                break
            if event.output_transcription and event.output_transcription.text:
                transcript_text = event.output_transcription.text
                print(transcript_text, end="", flush=True)
                full_response += transcript_text
        print("\n")
        return full_response

    async def _send_audio_chunks(self, pcm_data: bytes, live_request_queue, label: str):
        """Send audio data in chunks for streaming."""
        total_chunks = (len(pcm_data) + Config.CHUNK_SIZE - 1) // Config.CHUNK_SIZE
        print(f"Sending {label} audio in {total_chunks} chunks ({len(pcm_data)} bytes)")
        
        for i in range(0, len(pcm_data), Config.CHUNK_SIZE):
            chunk = pcm_data[i:i+Config.CHUNK_SIZE]
            blob = Blob(data=chunk, mime_type="audio/pcm;rate=16000")
            live_request_queue.send_realtime(blob)
            await asyncio.sleep(0.01)  # Small delay for streaming
        
        print(f"Sent all {total_chunks} {label} chunks")

    async def test_voice_chat(self) -> bool:
        """Test voice chat functionality."""
        self._print_test_header("VOICE CHAT")
        
        try:
            await self.setup_environment()
            await self.create_agent_session()
            
            voice_handler = VoiceHandler()
            
            # Setup live streaming for audio
            live_request_queue = LiveRequestQueue()
            run_config = RunConfig(response_modalities=["AUDIO"])
            live_events = self.runner.run_live(
                user_id="test_user",
                session_id=self.session.id,
                live_request_queue=live_request_queue,
                run_config=run_config,
            )
            
            # Load and send audio question
            print(f"Loading audio file: {Config.AUDIO_FILE}")
            question_pcm = voice_handler.load_audio_as_pcm(Config.AUDIO_FILE)
            await self._send_audio_chunks(question_pcm, live_request_queue, "question")
            
            # Collect audio response
            audio_response, text_response = await self._collect_audio_response(live_events)
            live_request_queue.close()
            
            # Process and verify response
            success = await self._process_voice_response(voice_handler, audio_response, text_response)
            self._print_test_result(success, "Voice response contains time-related information")
            return success
            
        except Exception as exc:
            return self._handle_test_exception(exc)
    
    async def _collect_audio_response(self, live_events):
        """Collect audio response from live events."""
        print("Waiting for voice response...")
        audio_data = b""
        text_data = ""
        event_count = 0
        
        try:
            async with asyncio.timeout(Config.TIMEOUT):
                async for event in live_events:
                    event_count += 1
                    
                    if event.turn_complete:
                        print(f"Turn complete after {event_count} events")
                        break
                    
                    if event.content and event.content.parts:
                        part = event.content.parts[0]
                        
                        # Handle audio response
                        if (part.inline_data and part.inline_data.mime_type and 
                            part.inline_data.mime_type.startswith("audio/")):
                            audio_data += part.inline_data.data
                            print(f"Received {len(part.inline_data.data)} bytes of audio")
                        
                        # Handle text response (for verification)
                        elif part.text:
                            text_data += part.text
                            print(f"Received text: {part.text}")
                    
                    # Progress indicator
                    if event_count % 10 == 0:
                        print(f"Processed {event_count} events...")
                        
        except asyncio.TimeoutError:
            print(f"Audio test timed out after {Config.TIMEOUT} seconds")
        
        return audio_data, text_data
    
    async def _process_voice_response(self, voice_handler: VoiceHandler, audio_data: bytes, text_data: str) -> bool:
        """Process voice response and verify it contains time information."""
        if not audio_data:
            print("No audio response received")
            self.transcription_result = "No audio response received"
            self.failure_reason = "No audio response received"
            return False

        print("Playing voice response...")
        voice_handler.play_audio(audio_data)

        # Transcribe for verification
        response_text = voice_handler.speech_to_text(audio_data)
        self.transcription_result = response_text or text_data or "No transcription available"
        print(f"Voice response (transcribed): '{response_text}'")

        # Verify response contains time information
        verification_text = response_text or text_data
        success = self._verify_time_response(verification_text)
        if not success:
            if not verification_text or verification_text.strip() == "":
                self.failure_reason = "No transcribable content in audio response"
            else:
                self.failure_reason = "Voice response does not contain time-related keywords"
        return success

async def run_all_tests(region: str = None) -> tuple[dict, dict, dict, dict, dict]:
    """Run combined text and voice tests for all platform and model combinations."""
    print("Starting ADK Bidirectional Streaming Tests (COMBINED)")
    print("=" * 60)

    results = {}
    transcriptions = {}
    error_traces = {}
    retry_counts = {}
    failure_reasons = {}

    # Test Google AI Studio
    print("\nTesting Google AI Studio Platform")
    print("-" * 40)

    # Run both text and voice tests for Google AI Studio
    studio_text_results, studio_text_transcriptions, studio_text_errors, studio_text_retries, studio_text_failures = await _test_platform(
        "google-ai-studio", Config.GOOGLE_AI_STUDIO_MODELS, "text", region
    )
    studio_voice_results, studio_voice_transcriptions, studio_voice_errors, studio_voice_retries, studio_voice_failures = await _test_platform(
        "google-ai-studio", Config.GOOGLE_AI_STUDIO_MODELS, "voice", region
    )

    results.update(studio_text_results)
    results.update(studio_voice_results)
    transcriptions.update(studio_text_transcriptions)
    transcriptions.update(studio_voice_transcriptions)
    error_traces.update(studio_text_errors)
    error_traces.update(studio_voice_errors)
    retry_counts.update(studio_text_retries)
    retry_counts.update(studio_voice_retries)
    failure_reasons.update(studio_text_failures)
    failure_reasons.update(studio_voice_failures)

    # Test Vertex AI
    print("\nTesting Google Cloud Vertex AI Platform")
    print("-" * 40)

    # Run both text and voice tests for Vertex AI
    vertex_text_results, vertex_text_transcriptions, vertex_text_errors, vertex_text_retries, vertex_text_failures = await _test_platform(
        "vertex-ai", Config.VERTEX_AI_MODELS, "text", region
    )
    vertex_voice_results, vertex_voice_transcriptions, vertex_voice_errors, vertex_voice_retries, vertex_voice_failures = await _test_platform(
        "vertex-ai", Config.VERTEX_AI_MODELS, "voice", region
    )

    results.update(vertex_text_results)
    results.update(vertex_voice_results)
    transcriptions.update(vertex_text_transcriptions)
    transcriptions.update(vertex_voice_transcriptions)
    error_traces.update(vertex_text_errors)
    error_traces.update(vertex_voice_errors)
    retry_counts.update(vertex_text_retries)
    retry_counts.update(vertex_voice_retries)
    failure_reasons.update(vertex_text_failures)
    failure_reasons.update(vertex_voice_failures)

    # Print summary and generate report
    _print_test_summary(results)
    report_filename = _generate_report_filename(region)
    generate_test_report(results, "both", output_file=report_filename, transcriptions=transcriptions, error_traces=error_traces, retry_counts=retry_counts, failure_reasons=failure_reasons)
    print(f"\nTest report generated: {report_filename}")

    return results, transcriptions, error_traces, retry_counts, failure_reasons

def _handle_test_error(exc: Exception, platform: str, model: str, test_type: str) -> tuple[bool, str, str]:
    """Handle test errors consistently."""
    import traceback
    print(f"Failed to test {model}: {exc}")
    error_trace = traceback.format_exc()
    transcription = f"Error: {str(exc)}" if test_type == "voice" else ""
    return False, error_trace, transcription

async def _run_single_test(tester: ADKStreamingTester, test_type: str) -> tuple[bool, str, str]:
    """Run a single test and return success status, transcription, and failure reason."""
    if test_type == "voice":
        success = await tester.test_voice_chat()
        return success, tester.transcription_result, tester.failure_reason
    else:
        success = await tester.test_text_chat()
        return success, "", tester.failure_reason

async def _run_single_test_with_retry(tester: ADKStreamingTester, test_type: str, max_retries: int = 3) -> tuple[bool, str, int, str]:
    """Run a single test with retry logic.

    Args:
        tester: The ADKStreamingTester instance
        test_type: Type of test ("text" or "voice")
        max_retries: Maximum number of retry attempts (default: 3)

    Returns:
        Tuple of (success, transcription, retry_count, failure_reason)
        retry_count is 0 for first attempt success, 1+ for retries
    """
    failure_reason = ""
    transcription = ""

    for attempt in range(max_retries):
        if attempt > 0:
            print(f"\nRetrying test (attempt {attempt + 1}/{max_retries})...")
            await asyncio.sleep(2)  # Brief delay before retry

        success, transcription, failure_reason = await _run_single_test(tester, test_type)

        if success:
            return success, transcription, attempt, ""

    # All retries exhausted
    return False, transcription, max_retries - 1, failure_reason

async def _test_platform(platform: str, models: list, test_type: str, region: str = None) -> tuple[dict, dict, dict, dict, dict]:
    """Test all models for a specific platform."""
    results = {}
    transcriptions = {}
    error_traces = {}
    retry_counts = {}
    failure_reasons = {}

    for model in models:
        test_key = f"{platform}-{model}-{test_type}"
        tester = ADKStreamingTester(platform, model, region)

        try:
            success, transcription, retry_count, failure_reason = await _run_single_test_with_retry(tester, test_type)
            results[test_key] = success
            retry_counts[test_key] = retry_count

            if test_type == "voice":
                transcriptions[test_key] = transcription

            # Store failure reason if test failed
            if not success and failure_reason:
                failure_reasons[test_key] = failure_reason

            # Store error trace if there was an error during testing
            if tester.error_trace:
                error_traces[test_key] = tester.error_trace

        except Exception as exc:
            success, error_trace, transcription = _handle_test_error(exc, platform, model, test_type)
            results[test_key] = success
            retry_counts[test_key] = 2  # Mark as max retries on exception
            error_traces[test_key] = error_trace
            failure_reasons[test_key] = f"Exception: {str(exc)}"
            if test_type == "voice":
                transcriptions[test_key] = transcription

        await asyncio.sleep(1)  # Brief delay between tests

    return results, transcriptions, error_traces, retry_counts, failure_reasons

def _parse_test_name(test_name: str) -> tuple[str, str, str]:
    """Parse test name into platform, model, and test type.
    
    Args:
        test_name: Format like "google-ai-studio-gemini-2.0-flash-live-001-text"
        
    Returns:
        Tuple of (platform, model, test_type)
    """
    if "google-ai-studio" in test_name:
        platform = "google-ai-studio"
        model_and_type = test_name.replace("google-ai-studio-", "")
    elif "vertex-ai" in test_name:
        platform = "vertex-ai"
        model_and_type = test_name.replace("vertex-ai-", "")
    else:
        return "", "", ""
        
    # Extract test type from the end
    if model_and_type.endswith("-text"):
        model = model_and_type.replace("-text", "")
        test_type = "text"
    elif model_and_type.endswith("-voice"):
        model = model_and_type.replace("-voice", "")
        test_type = "voice"
    else:
        model = model_and_type
        test_type = ""
        
    return platform, model, test_type

def _get_platform_display_name(platform: str) -> str:
    """Get display name for platform."""
    return "Google AI Studio" if platform == "google-ai-studio" else "Vertex AI"

def _format_test_result(success: bool) -> tuple[str, str]:
    """Format test result into icon and status."""
    return ("✅", "PASS") if success else ("❌", "FAIL")

def _print_test_summary(results: dict):
    """Print test summary."""
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    
    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")

def _generate_report_header(results: dict, retry_counts: dict = None) -> str:
    """Generate the header section of the test report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    google_project = os.getenv("GOOGLE_CLOUD_PROJECT", "Not configured")
    google_location = os.getenv("GOOGLE_CLOUD_LOCATION", "Not configured")
    adk_version = google.adk.__version__

    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    text_results = {k: v for k, v in results.items() if k.endswith("-text")}
    voice_results = {k: v for k, v in results.items() if k.endswith("-voice")}
    text_passed = sum(1 for success in text_results.values() if success)
    voice_passed = sum(1 for success in voice_results.values() if success)
    text_rate = (text_passed / len(text_results) * 100) if text_results else 0
    voice_rate = (voice_passed / len(voice_results) * 100) if voice_results else 0

    # Calculate retry statistics
    retry_stats = ""
    if retry_counts:
        tests_with_retries = sum(1 for count in retry_counts.values() if count > 0)
        total_retries = sum(retry_counts.values())
        retry_stats = f"""
### Retry Statistics
- **Tests requiring retries**: {tests_with_retries}/{total_tests}
- **Total retry attempts**: {total_retries}
"""

    return f"""# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: {timestamp}
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: {adk_version}
- **Total Tests**: {total_tests}
- **Passed Tests**: {passed_tests}
- **Failed Tests**: {total_tests - passed_tests}
- **Success Rate**: {success_rate:.1f}%

### Test Type Breakdown
- **Text Tests**: {text_passed}/{len(text_results)} passed ({text_rate:.1f}%)
- **Voice Tests**: {voice_passed}/{len(voice_results)} passed ({voice_rate:.1f}%)
{retry_stats}
## Environment Configuration
- **Google Cloud Project**: {google_project}
- **Google Cloud Location**: {google_location}

## Detailed Results

"""

def _generate_detailed_results(results: dict, retry_counts: dict = None, failure_reasons: dict = None) -> str:
    """Generate the detailed results section for combined tests."""
    content = """
**Note**: The following model list includes both officially supported models and deprecated models. To see a list of the currently supported models, see:
- **Gemini Live API**: Check the [Get started with Live API](https://ai.google.dev/gemini-api/docs/live#audio-generation)
- **Vertex AI Live API**: Check the [official Vertex AI Live API documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/live-api)

"""

    # Group by platform and model for combined tests
    platforms = {}
    for test_name, success in results.items():
        platform, model, current_test_type = _parse_test_name(test_name)
        if not platform or not current_test_type:
            continue

        if platform not in platforms:
            platforms[platform] = {}
        if model not in platforms[platform]:
            platforms[platform][model] = {}

        retry_count = retry_counts.get(test_name, 0) if retry_counts else 0
        failure_reason = failure_reasons.get(test_name, "") if failure_reasons else ""
        platforms[platform][model][current_test_type] = (success, retry_count, failure_reason)

    # Generate platform sections
    for platform, models in platforms.items():
        platform_name = _get_platform_display_name(platform)
        content += f"### {platform_name}\n\n"
        for model, tests in models.items():
            content += f"**{model}**:\n"
            for test_t in ["text", "voice"]:
                if test_t in tests:
                    success, retry_count, failure_reason = tests[test_t]
                    icon, status = _format_test_result(success)
                    # Check if model is native-audio and this is a text test
                    if test_t == "text" and "native-audio" in model.lower():
                        label = "Text (audio transcript)"
                    else:
                        label = test_t.title()

                    # Add retry information if there were retries
                    retry_info = f" (retries: {retry_count})" if retry_count > 0 else ""

                    # Add failure reason if test failed
                    failure_info = f" - Reason: {failure_reason}" if not success and failure_reason else ""

                    content += f"  - {label}: {icon} {status}{retry_info}{failure_info}\n"
            content += "\n"
        content += "\n"

    return content

def _generate_transcription_results(transcriptions: dict) -> str:
    """Generate voice transcription results section."""
    if not transcriptions:
        return ""
        
    content = "## Voice Transcription Results\n\n"
    
    # Group transcriptions by platform
    platforms = {}
    for test_name, transcription in transcriptions.items():
        platform, model, _ = _parse_test_name(test_name)
        if not platform:
            continue
            
        if platform not in platforms:
            platforms[platform] = []
        platforms[platform].append((model, transcription))
    
    for platform, model_transcriptions in platforms.items():
        platform_name = _get_platform_display_name(platform)
        content += f"### {platform_name}\n\n"
        for model, transcription in model_transcriptions:
            content += f"**{model}**: \"{transcription}\"\n\n"
    
    return content

def _generate_error_traces(error_traces: dict) -> str:
    """Generate error traces section."""
    if not error_traces:
        return ""
        
    content = "## Error Traces\n\n"
    
    # Group errors by platform
    platforms = {}
    for test_name, error_trace in error_traces.items():
        platform, model, test_type = _parse_test_name(test_name)
        if not platform:
            continue
            
        if platform not in platforms:
            platforms[platform] = []
        platforms[platform].append((model, test_type, error_trace))
    
    for platform, model_errors in platforms.items():
        platform_name = _get_platform_display_name(platform)
        content += f"### {platform_name}\n\n"
        for model, test_type, error_trace in model_errors:
            content += f"#### {model} ({test_type})\n\n"
            content += "```\n"
            content += error_trace
            content += "```\n\n"
    
    return content

def _generate_methodology_section() -> str:
    """Generate test methodology section."""
    return """## Test Methodology

### Test Question
- **Query**: "What time is it now?"
- **Expected Response**: Agent responds with current time information using Google Search tool

### Success Criteria
- Response contains time-related keywords (time, clock, hour, minute, am, pm, utc, gmt)
- Agent successfully uses Google Search tool for real-time information
- Bidirectional streaming communication works correctly

### Retry Logic
- Each test is automatically retried up to 3 times if it fails
- A 2-second delay is applied between retry attempts
- Tests succeed on first attempt show 0 retries
- Failed tests show the number of retry attempts made

### Platform Configuration
- **Google AI Studio**: Uses GOOGLE_API_KEY with GOOGLE_GENAI_USE_VERTEXAI=FALSE
- **Vertex AI**: Uses GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION with GOOGLE_GENAI_USE_VERTEXAI=TRUE

### Text Chat Testing
- Sends text query via ADK streaming API
- Receives streaming text response
- Validates response content for time information

### Voice Chat Testing
- Uses M4A audio file containing "What time is it now?"
- Converts to 16kHz, mono, 16-bit PCM format
- Sends audio to ADK streaming API in 1KB chunks
- Receives audio response from model at 24kHz
- Plays audio response using PyAudio
- Transcribes response using Google Cloud Speech-to-Text for validation

"""

def _generate_report_filename(region: str = None) -> str:
    """Generate report filename with region and timestamp suffix."""
    from datetime import datetime
    import os
    
    # Get current region from environment if not provided
    if not region:
        region = os.getenv("GOOGLE_CLOUD_LOCATION", "unknown")
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename with region and timestamp
    return f"test_report_{region}_{timestamp}.md"

def generate_test_report(results, test_type, output_file="test_report.md", transcriptions=None, error_traces=None, retry_counts=None, failure_reasons=None):
    """Generate a comprehensive test report file for combined tests."""
    # Build report content using helper functions
    report_content = _generate_report_header(results, retry_counts)
    report_content += _generate_detailed_results(results, retry_counts, failure_reasons)
    report_content += _generate_transcription_results(transcriptions or {})
    report_content += _generate_error_traces(error_traces or {})
    report_content += _generate_methodology_section()

    # Add failed test analysis
    failed_tests = [k for k, v in results.items() if not v]
    if failed_tests:
        report_content += "## Failed Test Analysis\n\n"
        for test_name in failed_tests:
            platform, model, test_type_display = _parse_test_name(test_name)
            formatted_name = f"{model} ({test_type_display})"

            # Get failure reason if available
            failure_reason = failure_reasons.get(test_name, "Unknown") if failure_reasons else "Unknown"

            if "audio-dialog" in test_name or "audio-thinking" in test_name:
                if "text" in test_name:
                    report_content += f"- **{formatted_name}**: Audio-only model correctly rejects text input (expected behavior)\n"
                    report_content += f"  - Failure Reason: {failure_reason}\n"
                else:
                    report_content += f"- **{formatted_name}**: Unexpected failure - requires investigation\n"
                    report_content += f"  - Failure Reason: {failure_reason}\n"
            else:
                report_content += f"- **{formatted_name}**: Unexpected failure - requires investigation\n"
                report_content += f"  - Failure Reason: {failure_reason}\n"
        report_content += "\n"
    
    # Add environment and usage information
    adk_version = google.adk.__version__
    report_content += f"""## Environment Information
- **ADK Version**: {adk_version}
- **Python Dependencies**: google-adk, google-cloud-speech, pyaudio, pydub, python-dotenv
- **Audio Configuration**: Input 16kHz, Output 24kHz, PCM, Mono
- **SSL Configuration**: Automatically configured using certifi

## Test Tool Usage
```bash
# Run all tests (combined text and voice)
python test_tool.py

# Test specific platform only
python test_tool.py --platform google-ai-studio

# Test specific model
python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp

# Test with specific region
python test_tool.py --platform vertex-ai --region us-west1

# Test specific model in specific region
python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp --region europe-west1
```

---
*Report generated by ADK Bidirectional Streaming Test Tool*
"""
    
    # Write report to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n📄 Test report saved to: {output_file}")
    return output_file

async def test_single_model_combined(platform: str, model: str, region: str = None) -> tuple[bool, bool]:
    """Test a single platform and model combination with both text and voice tests."""
    tester = ADKStreamingTester(platform, model, region)
    
    print(f"Testing text chat for {model}:")
    text_success = await tester.test_text_chat()
    
    print(f"\nTesting voice chat for {model}:")
    voice_success = await tester.test_voice_chat()
    
    return text_success, voice_success

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ADK Bidirectional Streaming Test Tool - Combined Text and Voice Testing")
    parser.add_argument("--platform", choices=["google-ai-studio", "vertex-ai", "all"], 
                       default="all", help="Platform to test")
    parser.add_argument("--model", help="Specific model to test")
    parser.add_argument("--region", help="Google Cloud region to use (overrides GOOGLE_CLOUD_LOCATION env var)")
    
    args = parser.parse_args()
    
    # Set SSL certificate file as required by ADK
    os.environ["SSL_CERT_FILE"] = os.popen("python -m certifi").read().strip()
    
    if args.model:
        _run_single_model_tests(args)
    else:
        _run_all_model_tests(args)

def _run_single_model_tests(args):
    """Run combined tests for a single model."""
    if args.platform == "all":
        print("Error: Must specify platform when testing specific model")
        return
    
    print("Running combined text and voice tests:")
    asyncio.run(test_single_model_combined(args.platform, args.model, args.region))

def _run_all_model_tests(args):
    """Run combined tests for all models."""
    results, transcriptions, error_traces, retry_counts, failure_reasons = asyncio.run(run_all_tests(args.region))


if __name__ == "__main__":
    main()
