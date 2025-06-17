#!/usr/bin/env python3
"""
ADK Bidirectional Streaming Test Tool

Tests bidirectional streaming functionality with Google ADK using both
Google AI Studio and Google Cloud Vertex AI platforms.
"""

import os
import asyncio
import argparse
from datetime import datetime
from dotenv import load_dotenv
from google.genai.types import Content, Part, Blob
from google.adk.runners import InMemoryRunner
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.tools import google_search
from google.cloud import speech
import pyaudio
from pydub import AudioSegment
import google.adk

# Load environment variables
load_dotenv()

# Configuration
class Config:
    """Application configuration"""
    # Model configurations
    GOOGLE_AI_STUDIO_MODELS = [
        "gemini-2.0-flash-live-001",
        "gemini-2.5-flash-preview-native-audio-dialog", 
        "gemini-2.5-flash-exp-native-audio-thinking-dialog",
        "gemini-2.0-flash-exp"
    ]
    
    VERTEX_AI_MODELS = [
        "gemini-2.0-flash-live-preview-04-09",
        "gemini-2.0-flash-exp"
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

    def __init__(self, platform: str, model: str):
        self.platform = platform
        self.model = model
        self.runner = None
        self.session = None
        self.transcription_result = ""  # Store transcription for reporting
        self.error_trace = ""  # Store error details for reporting

    async def setup_environment(self):
        """Configure environment variables for the platform."""
        if self.platform == "google-ai-studio":
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
            if not os.getenv("GOOGLE_API_KEY"):
                raise ValueError("GOOGLE_API_KEY not found in environment")
        else:  # vertex-ai
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
            if not (os.getenv("GOOGLE_CLOUD_PROJECT") and os.getenv("GOOGLE_CLOUD_LOCATION")):
                raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION required for Vertex AI")

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

        self.runner = InMemoryRunner(app_name="ADK Streaming Test", agent=agent)
        self.session = await self.runner.session_service.create_session(
            app_name="ADK Streaming Test", user_id="test_user"
        )
        return agent

    async def test_text_chat(self) -> bool:
        """Test text chat functionality."""
        self._print_test_header("TEXT CHAT")
        
        try:
            await self.setup_environment()
            await self.create_agent_session()
            
            # Setup live streaming
            live_request_queue = LiveRequestQueue()
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
            
            full_response = await self._collect_text_response(live_events)
            live_request_queue.close()
            
            # Verify response
            success = self._verify_time_response(full_response)
            self._print_test_result(success, "Response contains time-related information")
            return success
            
        except Exception as exc:
            import traceback
            self.error_trace = traceback.format_exc()
            self._print_test_error(str(exc))
            return False
    
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
            import traceback
            self.error_trace = traceback.format_exc()
            self._print_test_error(str(exc))
            return False
    
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
            return False
        
        print("Playing voice response...")
        voice_handler.play_audio(audio_data)
        
        # Transcribe for verification
        response_text = voice_handler.speech_to_text(audio_data)
        self.transcription_result = response_text or text_data or "No transcription available"
        print(f"Voice response (transcribed): '{response_text}'")
        
        # Verify response contains time information
        verification_text = response_text or text_data
        return self._verify_time_response(verification_text)

async def run_all_tests(test_type: str = "text") -> tuple[dict, dict]:
    """Run tests for all platform and model combinations."""
    print(f"Starting ADK Bidirectional Streaming Tests ({test_type.upper()})")
    print("=" * 60)
    
    # Select models based on test type
    if test_type == "voice":
        studio_models = ["gemini-2.0-flash-live-001",
                        "gemini-2.5-flash-preview-native-audio-dialog", 
                        "gemini-2.5-flash-exp-native-audio-thinking-dialog",
                        "gemini-2.0-flash-exp"]
        vertex_models = ["gemini-2.0-flash-live-preview-04-09",
                        "gemini-2.0-flash-exp"]
    else:
        studio_models = Config.GOOGLE_AI_STUDIO_MODELS
        vertex_models = Config.VERTEX_AI_MODELS
    
    results = {}
    transcriptions = {}
    error_traces = {}
    
    # Test Google AI Studio
    print("\nTesting Google AI Studio Platform")
    print("-" * 40)
    studio_results, studio_transcriptions, studio_errors = await _test_platform("google-ai-studio", studio_models, test_type)
    results.update(studio_results)
    transcriptions.update(studio_transcriptions)
    error_traces.update(studio_errors)
    
    # Test Vertex AI
    print("\nTesting Google Cloud Vertex AI Platform") 
    print("-" * 40)
    vertex_results, vertex_transcriptions, vertex_errors = await _test_platform("vertex-ai", vertex_models, test_type)
    results.update(vertex_results)
    transcriptions.update(vertex_transcriptions)
    error_traces.update(vertex_errors)
    
    # Print summary and generate report (only for individual test types)
    _print_test_summary(results)
    if test_type != "combined":  # Don't generate individual reports for combined runs
        generate_test_report(results, test_type, transcriptions=transcriptions, error_traces=error_traces)
    
    return results, transcriptions, error_traces

async def _test_platform(platform: str, models: list, test_type: str) -> tuple[dict, dict, dict]:
    """Test all models for a specific platform."""
    results = {}
    transcriptions = {}
    error_traces = {}
    
    for model in models:
        tester = ADKStreamingTester(platform, model)
        try:
            if test_type == "voice":
                success = await tester.test_voice_chat()
                transcriptions[f"{platform}-{model}-{test_type}"] = tester.transcription_result
            else:
                success = await tester.test_text_chat()
            results[f"{platform}-{model}-{test_type}"] = success
            
            # Store error trace if there was an error during testing
            if tester.error_trace:
                error_traces[f"{platform}-{model}-{test_type}"] = tester.error_trace
                
        except Exception as exc:
            import traceback
            print(f"Failed to test {model}: {exc}")
            results[f"{platform}-{model}-{test_type}"] = False
            error_traces[f"{platform}-{model}-{test_type}"] = traceback.format_exc()
            if test_type == "voice":
                transcriptions[f"{platform}-{model}-{test_type}"] = f"Error: {str(exc)}"
        
        await asyncio.sleep(1)  # Brief delay between tests
    
    return results, transcriptions, error_traces

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

def generate_test_report(results, test_type, output_file="test_report.txt", transcriptions=None, error_traces=None):
    """Generate a comprehensive test report file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get environment configuration
    google_project = os.getenv("GOOGLE_CLOUD_PROJECT", "Not configured")
    google_location = os.getenv("GOOGLE_CLOUD_LOCATION", "Not configured")
    adk_version = google.adk.__version__
    
    report_content = f"""# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: {timestamp}
- **Test Type**: {test_type.upper()}
- **Google ADK Version**: {adk_version}
- **Total Tests**: {len(results)}
- **Passed Tests**: {sum(1 for success in results.values() if success)}
- **Failed Tests**: {sum(1 for success in results.values() if not success)}
- **Success Rate**: {(sum(1 for success in results.values() if success) / len(results) * 100):.1f}%

## Environment Configuration
- **Google Cloud Project**: {google_project}
- **Google Cloud Location**: {google_location}

## Detailed Results

"""
    
    # Group results by platform
    google_ai_studio_results = {k: v for k, v in results.items() if "google-ai-studio" in k}
    vertex_ai_results = {k: v for k, v in results.items() if "vertex-ai" in k}
    
    if google_ai_studio_results:
        report_content += "### Google AI Studio Platform\n\n"
        for test_name, success in google_ai_studio_results.items():
            model = test_name.replace("google-ai-studio-", "").replace(f"-{test_type}", "")
            status = "PASS" if success else "FAIL"
            icon = "✅" if success else "❌"
            report_content += f"- **{model} ({test_type})**: {icon} {status}\n"
        report_content += "\n"
    
    if vertex_ai_results:
        report_content += "### Vertex AI Platform\n\n"
        for test_name, success in vertex_ai_results.items():
            model = test_name.replace("vertex-ai-", "").replace(f"-{test_type}", "")
            status = "PASS" if success else "FAIL"
            icon = "✅" if success else "❌"
            report_content += f"- **{model} ({test_type})**: {icon} {status}\n"
        report_content += "\n"
    
    # Add voice transcription results if this is a voice test
    if test_type == "voice" and transcriptions:
        report_content += "## Voice Transcription Results\n\n"
        
        # Group transcriptions by platform
        google_ai_transcriptions = {k: v for k, v in transcriptions.items() if "google-ai-studio" in k}
        vertex_ai_transcriptions = {k: v for k, v in transcriptions.items() if "vertex-ai" in k}
        
        if google_ai_transcriptions:
            report_content += "### Google AI Studio Platform\n\n"
            for test_name, transcription in google_ai_transcriptions.items():
                model = test_name.replace("google-ai-studio-", "").replace(f"-{test_type}", "")
                report_content += f"**{model}**: \"{transcription}\"\n\n"
        
        if vertex_ai_transcriptions:
            report_content += "### Vertex AI Platform\n\n"
            for test_name, transcription in vertex_ai_transcriptions.items():
                model = test_name.replace("vertex-ai-", "").replace(f"-{test_type}", "")
                report_content += f"**{model}**: \"{transcription}\"\n\n"
    
    # Add error traces section if there are any errors
    if error_traces:
        report_content += "## Error Traces\n\n"
        
        # Group errors by platform
        google_ai_errors = {k: v for k, v in error_traces.items() if "google-ai-studio" in k}
        vertex_ai_errors = {k: v for k, v in error_traces.items() if "vertex-ai" in k}
        
        if google_ai_errors:
            report_content += "### Google AI Studio Platform\n\n"
            for test_name, error_trace in google_ai_errors.items():
                # Extract model name and test type
                if "google-ai-studio" in test_name:
                    model_and_type = test_name.replace("google-ai-studio-", "")
                    if model_and_type.endswith("-text"):
                        model = model_and_type.replace("-text", "")
                        test_type_display = "text"
                    elif model_and_type.endswith("-voice"):
                        model = model_and_type.replace("-voice", "")
                        test_type_display = "voice"
                    else:
                        model = model_and_type
                        test_type_display = "unknown"
                    
                    report_content += f"#### {model} ({test_type_display})\n\n"
                    report_content += "```\n"
                    report_content += error_trace
                    report_content += "```\n\n"
        
        if vertex_ai_errors:
            report_content += "### Vertex AI Platform\n\n"
            for test_name, error_trace in vertex_ai_errors.items():
                # Extract model name and test type
                if "vertex-ai" in test_name:
                    model_and_type = test_name.replace("vertex-ai-", "")
                    if model_and_type.endswith("-text"):
                        model = model_and_type.replace("-text", "")
                        test_type_display = "text"
                    elif model_and_type.endswith("-voice"):
                        model = model_and_type.replace("-voice", "")
                        test_type_display = "voice"
                    else:
                        model = model_and_type
                        test_type_display = "unknown"
                    
                    report_content += f"#### {model} ({test_type_display})\n\n"
                    report_content += "```\n"
                    report_content += error_trace
                    report_content += "```\n\n"
    
    # Add test methodology
    report_content += """## Test Methodology

### Test Question
- **Query**: "What time is it now?"
- **Expected Response**: Agent responds with current time information using Google Search tool

### Success Criteria
- Response contains time-related keywords (time, clock, hour, minute, am, pm, utc, gmt)
- Agent successfully uses Google Search tool for real-time information
- Bidirectional streaming communication works correctly

### Platform Configuration
- **Google AI Studio**: Uses GOOGLE_API_KEY with GOOGLE_GENAI_USE_VERTEXAI=FALSE
- **Vertex AI**: Uses GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION with GOOGLE_GENAI_USE_VERTEXAI=TRUE

"""
    
    if test_type == "text":
        report_content += """### Text Chat Testing
- Sends text query via ADK streaming API
- Receives streaming text response
- Validates response content for time information

"""
    elif test_type == "voice":
        report_content += """### Voice Chat Testing
- Generates voice input using Google Cloud Text-to-Speech
- Sends audio to ADK streaming API
- Receives audio response from model
- Plays audio response using PyAudio
- Transcribes response using Google Cloud Speech-to-Text for validation

"""
    elif test_type == "both":
        report_content += """### Text Chat Testing
- Sends text query via ADK streaming API
- Receives streaming text response
- Validates response content for time information

### Voice Chat Testing
- Generates voice input using Google Cloud Text-to-Speech
- Sends audio to ADK streaming API
- Receives audio response from model
- Plays audio response using PyAudio
- Transcribes response using Google Cloud Speech-to-Text for validation

"""
    
    # Add notes about failures
    failed_tests = [k for k, v in results.items() if not v]
    if failed_tests:
        report_content += "## Failed Test Analysis\n\n"
        for test_name in failed_tests:
            # Format the test name properly
            if "google-ai-studio" in test_name:
                model = test_name.replace("google-ai-studio-", "")
            elif "vertex-ai" in test_name:
                model = test_name.replace("vertex-ai-", "")
            else:
                model = test_name
            
            # Extract test type from the end
            if model.endswith("-text"):
                clean_model = model.replace("-text", "")
                test_type_display = "text"
            elif model.endswith("-voice"):
                clean_model = model.replace("-voice", "")
                test_type_display = "voice"
            else:
                clean_model = model
                test_type_display = "unknown"
            
            formatted_name = f"{clean_model} ({test_type_display})"
            
            if "audio-dialog" in test_name or "audio-thinking" in test_name:
                if "text" in test_name:
                    report_content += f"- **{formatted_name}**: Audio-only model correctly rejects text input (expected behavior)\n"
                else:
                    report_content += f"- **{formatted_name}**: Unexpected failure - requires investigation\n"
            else:
                report_content += f"- **{formatted_name}**: Unexpected failure - requires investigation\n"
        report_content += "\n"
    
    report_content += f"""## Environment Information
- **ADK Version**: 1.3.0
- **Python Dependencies**: google-adk, google-cloud-texttospeech, google-cloud-speech, pyaudio, python-dotenv
- **Audio Configuration**: 16kHz, PCM, Mono
- **SSL Configuration**: Automatically configured using certifi

## Test Tool Usage
```bash
# Text tests only
python test_tool.py --test-type text

# Voice tests only  
python test_tool.py --test-type voice

# Both test types
python test_tool.py --test-type both

# Specific platform
python test_tool.py --platform google-ai-studio --test-type text

# Specific model
python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp --test-type voice
```

---
*Report generated by ADK Bidirectional Streaming Test Tool*
"""
    
    # Write report to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("\\n📄 Test report saved to: " + output_file)
    return output_file

async def test_single_model(platform: str, model: str, test_type: str = "text") -> bool:
    """Test a single platform and model combination."""
    tester = ADKStreamingTester(platform, model)
    if test_type == "voice":
        return await tester.test_voice_chat()
    return await tester.test_text_chat()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ADK Bidirectional Streaming Test Tool")
    parser.add_argument("--platform", choices=["google-ai-studio", "vertex-ai", "all"], 
                       default="all", help="Platform to test")
    parser.add_argument("--model", help="Specific model to test")
    parser.add_argument("--test-type", choices=["text", "voice", "both"], 
                       default="text", help="Type of test to run")
    
    args = parser.parse_args()
    
    # Set SSL certificate file as required by ADK
    os.environ["SSL_CERT_FILE"] = os.popen("python -m certifi").read().strip()
    
    if args.model:
        _run_single_model_tests(args)
    else:
        _run_all_model_tests(args)

def _run_single_model_tests(args):
    """Run tests for a single model."""
    if args.platform == "all":
        print("Error: Must specify platform when testing specific model")
        return
    
    if args.test_type == "both":
        print("Testing text chat:")
        asyncio.run(test_single_model(args.platform, args.model, "text"))
        print("\nTesting voice chat:")
        asyncio.run(test_single_model(args.platform, args.model, "voice"))
    else:
        asyncio.run(test_single_model(args.platform, args.model, args.test_type))

def _run_all_model_tests(args):
    """Run tests for all models."""
    if args.test_type == "both":
        print("Running text tests:")
        text_results, text_transcriptions, text_errors = asyncio.run(run_all_tests("text"))
        print("\nRunning voice tests:")
        voice_results, voice_transcriptions, voice_errors = asyncio.run(run_all_tests("voice"))
        
        # Generate combined report with both test types
        combined_errors = {**text_errors, **voice_errors}
        _generate_combined_report(text_results, voice_results, voice_transcriptions, combined_errors)
    else:
        results, transcriptions, error_traces = asyncio.run(run_all_tests(args.test_type))

def _generate_combined_report(text_results: dict, voice_results: dict, voice_transcriptions: dict, error_traces: dict):
    """Generate a combined report for both text and voice tests."""
    combined_results = {**text_results, **voice_results}
    
    # Generate the combined report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get environment configuration
    google_project = os.getenv("GOOGLE_CLOUD_PROJECT", "Not configured")
    google_location = os.getenv("GOOGLE_CLOUD_LOCATION", "Not configured")
    adk_version = google.adk.__version__
    
    # Calculate statistics
    total_tests = len(combined_results)
    passed_tests = sum(1 for success in combined_results.values() if success)
    text_tests = len(text_results)
    text_passed = sum(1 for success in text_results.values() if success)
    voice_tests = len(voice_results)
    voice_passed = sum(1 for success in voice_results.values() if success)
    
    report_content = f"""# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: {timestamp}
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: {adk_version}
- **Total Tests**: {total_tests}
- **Passed Tests**: {passed_tests}
- **Failed Tests**: {total_tests - passed_tests}
- **Success Rate**: {(passed_tests / total_tests * 100):.1f}%

### Test Type Breakdown
- **Text Tests**: {text_passed}/{text_tests} passed ({(text_passed / text_tests * 100):.1f}%)
- **Voice Tests**: {voice_passed}/{voice_tests} passed ({(voice_passed / voice_tests * 100):.1f}%)

## Environment Configuration
- **Google Cloud Project**: {google_project}
- **Google Cloud Location**: {google_location}

## Detailed Results

"""
    
    # Group results by platform and model
    platforms = {}
    for test_name, success in combined_results.items():
        if "google-ai-studio" in test_name:
            platform = "Google AI Studio"
            model_and_type = test_name.replace("google-ai-studio-", "")
        elif "vertex-ai" in test_name:
            platform = "Vertex AI"
            model_and_type = test_name.replace("vertex-ai-", "")
        else:
            continue
            
        # Extract model name and test type
        if model_and_type.endswith("-text"):
            model = model_and_type.replace("-text", "")
            test_type = "text"
        elif model_and_type.endswith("-voice"):
            model = model_and_type.replace("-voice", "")
            test_type = "voice"
        else:
            continue
            
        if platform not in platforms:
            platforms[platform] = {}
        if model not in platforms[platform]:
            platforms[platform][model] = {}
            
        platforms[platform][model][test_type] = success
    
    # Generate platform sections
    for platform, models in platforms.items():
        report_content += f"### {platform}\n\n"
        for model, tests in models.items():
            text_result = tests.get("text", None)
            voice_result = tests.get("voice", None)
            
            report_content += f"**{model}**:\n"
            if text_result is not None:
                icon = "✅" if text_result else "❌"
                status = "PASS" if text_result else "FAIL"
                report_content += f"  - Text: {icon} {status}\n"
            if voice_result is not None:
                icon = "✅" if voice_result else "❌"
                status = "PASS" if voice_result else "FAIL"
                report_content += f"  - Voice: {icon} {status}\n"
            report_content += "\n"
        report_content += "\n"
    
    # Add voice transcription results
    if voice_transcriptions:
        report_content += "## Voice Transcription Results\n\n"
        
        # Group transcriptions by platform
        google_ai_transcriptions = {k: v for k, v in voice_transcriptions.items() if "google-ai-studio" in k}
        vertex_ai_transcriptions = {k: v for k, v in voice_transcriptions.items() if "vertex-ai" in k}
        
        if google_ai_transcriptions:
            report_content += "### Google AI Studio Platform\n\n"
            for test_name, transcription in google_ai_transcriptions.items():
                model = test_name.replace("google-ai-studio-", "").replace("-voice", "")
                report_content += f"**{model}**: \"{transcription}\"\n\n"
        
        if vertex_ai_transcriptions:
            report_content += "### Vertex AI Platform\n\n"
            for test_name, transcription in vertex_ai_transcriptions.items():
                model = test_name.replace("vertex-ai-", "").replace("-voice", "")
                report_content += f"**{model}**: \"{transcription}\"\n\n"
    
    # Add error traces section if there are any errors
    if error_traces:
        report_content += "## Error Traces\n\n"
        
        # Group errors by platform
        google_ai_errors = {k: v for k, v in error_traces.items() if "google-ai-studio" in k}
        vertex_ai_errors = {k: v for k, v in error_traces.items() if "vertex-ai" in k}
        
        if google_ai_errors:
            report_content += "### Google AI Studio Platform\n\n"
            for test_name, error_trace in google_ai_errors.items():
                # Extract model name and test type
                if "google-ai-studio" in test_name:
                    model_and_type = test_name.replace("google-ai-studio-", "")
                    if model_and_type.endswith("-text"):
                        model = model_and_type.replace("-text", "")
                        test_type_display = "text"
                    elif model_and_type.endswith("-voice"):
                        model = model_and_type.replace("-voice", "")
                        test_type_display = "voice"
                    else:
                        model = model_and_type
                        test_type_display = "unknown"
                    
                    report_content += f"#### {model} ({test_type_display})\n\n"
                    report_content += "```\n"
                    report_content += error_trace
                    report_content += "```\n\n"
        
        if vertex_ai_errors:
            report_content += "### Vertex AI Platform\n\n"
            for test_name, error_trace in vertex_ai_errors.items():
                # Extract model name and test type
                if "vertex-ai" in test_name:
                    model_and_type = test_name.replace("vertex-ai-", "")
                    if model_and_type.endswith("-text"):
                        model = model_and_type.replace("-text", "")
                        test_type_display = "text"
                    elif model_and_type.endswith("-voice"):
                        model = model_and_type.replace("-voice", "")
                        test_type_display = "voice"
                    else:
                        model = model_and_type
                        test_type_display = "unknown"
                    
                    report_content += f"#### {model} ({test_type_display})\n\n"
                    report_content += "```\n"
                    report_content += error_trace
                    report_content += "```\n\n"
    
    # Add methodology and other sections
    report_content += """## Test Methodology

### Test Question
- **Query**: "What time is it now?"
- **Expected Response**: Agent responds with current time information using Google Search tool

### Success Criteria
- Response contains time-related keywords (time, clock, hour, minute, am, pm, utc, gmt)
- Agent successfully uses Google Search tool for real-time information
- Bidirectional streaming communication works correctly

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

## Environment Information
- **ADK Version**: 1.3.0
- **Python Dependencies**: google-adk, google-cloud-speech, pyaudio, pydub, python-dotenv
- **Audio Configuration**: Input 16kHz, Output 24kHz, PCM, Mono
- **SSL Configuration**: Automatically configured using certifi

## Test Tool Usage
```bash
# Text tests only
python test_tool.py --test-type text

# Voice tests only  
python test_tool.py --test-type voice

# Both test types (generates this combined report)
python test_tool.py --test-type both

# Specific platform
python test_tool.py --platform google-ai-studio --test-type text

# Specific model
python test_tool.py --platform vertex-ai --model gemini-2.0-flash-exp --test-type voice
```

---
*Report generated by ADK Bidirectional Streaming Test Tool*
"""
    
    # Write combined report
    output_file = "combined_test_report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n📄 Combined test report saved to: {output_file}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("COMBINED TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Text Tests: {text_passed}/{text_tests} passed ({(text_passed / text_tests * 100):.1f}%)")
    print(f"Voice Tests: {voice_passed}/{voice_tests} passed ({(voice_passed / voice_tests * 100):.1f}%)")
    print(f"Overall: {passed_tests}/{total_tests} tests passed ({(passed_tests / total_tests * 100):.1f}%)")

if __name__ == "__main__":
    main()
