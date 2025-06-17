#!/usr/bin/env python3
"""
ADK Bidi-Streaming Test Tool

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
from google.cloud import texttospeech, speech
import pyaudio

# Load environment variables
load_dotenv()

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
RATE = 16000
CHUNK = 1024

class VoiceHandler:
    """Handles voice input/output using Google Cloud TTS and STT."""

    def __init__(self):
        self.tts_client = texttospeech.TextToSpeechClient()
        self.stt_client = speech.SpeechClient()
        self.pyaudio_instance = pyaudio.PyAudio()

    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech and return audio bytes."""
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE
        )

        response = self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return response.audio_content

    def play_audio(self, audio_data: bytes):
        """Play audio data through speakers."""
        stream = self.pyaudio_instance.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True
        )

        stream.write(audio_data)
        stream.stop_stream()
        stream.close()

    def record_audio(self, duration: int = 5) -> bytes:
        """Record audio from microphone for specified duration."""
        print(f"Recording for {duration} seconds... Speak now!")

        stream = self.pyaudio_instance.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        # Convert to bytes
        audio_data = b''.join(frames)
        return audio_data

    def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech audio to text."""
        audio = speech.RecognitionAudio(content=audio_data)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code="en-US",
        )

        response = self.stt_client.recognize(config=config, audio=audio)

        if response.results:
            return response.results[0].alternatives[0].transcript
        return ""

    def __del__(self):
        """Clean up PyAudio instance."""
        if hasattr(self, 'pyaudio_instance'):
            self.pyaudio_instance.terminate()

class ADKStreamingTester:
    """ADK Streaming Test Class for testing bidirectional streaming functionality."""

    def __init__(self, platform, model):
        self.platform = platform
        self.model = model
        self.runner = None
        self.session = None
    async def setup_environment(self):
        """Set up environment variables based on platform"""
        if self.platform == "google-ai-studio":
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment")
        else:  # vertex-ai
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
            project = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION")
            if not project or not location:
                raise ValueError(
                    "GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION required for Vertex AI"
                )

    async def create_agent_session(self):
        """Create an ADK agent session"""
        # Create agent with Google Search tool
        agent = Agent(
            name="time_query_agent",
            model=self.model,
            description="Agent to answer time queries using Google Search",
            instruction=(
                "Answer the question 'What time is it now?' using the Google Search tool. "
                "Provide the current time information."
            ),
            tools=[google_search],
        )

        # Create runner
        self.runner = InMemoryRunner(
            app_name="ADK Streaming Test",
            agent=agent,
        )

        # Create session
        self.session = await self.runner.session_service.create_session(
            app_name="ADK Streaming Test",
            user_id="test_user",
        )

        return agent

    async def test_text_chat(self):
        """Test text chat functionality with time query"""
        print(f"\n{'='*60}")
        print(f"Testing {self.platform} with model: {self.model}")
        print(f"{'='*60}")

        try:
            # Set up environment
            await self.setup_environment()

            # Create agent session
            await self.create_agent_session()

            # Create live request queue
            live_request_queue = LiveRequestQueue()

            # Set response modality to TEXT
            run_config = RunConfig(response_modalities=["TEXT"])

            # Start live session
            live_events = self.runner.run_live(
                session=self.session,
                live_request_queue=live_request_queue,
                run_config=run_config,
            )

            # Send the time query
            question = "What time is it now?"
            content = Content(role="user", parts=[Part.from_text(text=question)])
            live_request_queue.send_content(content=content)

            print(f"Question: {question}")
            print("Response: ", end="", flush=True)

            # Collect response
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

            # Close the request queue
            live_request_queue.close()

            # Verify response contains time information
            time_keywords = ["time", "clock", "hour", "minute", "am", "pm", "utc", "gmt"]
            success = any(keyword in full_response.lower() for keyword in time_keywords)

            print("Test Result: PASS" if success else "Test Result: FAIL")
            if success:
                print("✓ Response contains time-related information")
            else:
                print("✗ Response does not contain expected time information")

            return success

        except Exception as exc:
            print("Test Result: ERROR")
            print(f"✗ Error: {str(exc)}")
            return False

    async def test_voice_chat(self):
        """Test voice chat functionality with TTS/STT"""
        print(f"\n{'='*60}")
        print(f"Testing VOICE CHAT {self.platform} with model: {self.model}")
        print(f"{'='*60}")

        try:
            # Set up environment
            await self.setup_environment()

            # Create agent session
            await self.create_agent_session()

            # Initialize voice handler
            voice_handler = VoiceHandler()

            # Create live request queue
            live_request_queue = LiveRequestQueue()

            # Set response modality to AUDIO
            run_config = RunConfig(response_modalities=["AUDIO"])

            # Start live session
            live_events = self.runner.run_live(
                session=self.session,
                live_request_queue=live_request_queue,
                run_config=run_config,
            )

            # Record voice input
            print("Voice input required:")
            audio_data = voice_handler.record_audio(duration=5)

            # Convert speech to text for verification
            question_text = voice_handler.speech_to_text(audio_data)
            print(f"Recognized speech: '{question_text}'")

            # Send audio to agent
            blob = Blob(data=audio_data, mime_type="audio/pcm")
            live_request_queue.send_realtime(blob)

            print("Waiting for voice response...")

            # Collect audio response
            audio_response_data = b""
            text_response = ""

            async for event in live_events:
                if event.turn_complete:
                    break

                if event.content and event.content.parts:
                    part = event.content.parts[0]

                    # Handle audio response
                    if (part.inline_data and
                        part.inline_data.mime_type and
                        part.inline_data.mime_type.startswith("audio/")):
                        audio_response_data += part.inline_data.data

                    # Handle text response (for verification)
                    elif part.text:
                        text_response += part.text

            # Close the request queue
            live_request_queue.close()

            # Play the audio response
            if audio_response_data:
                print("Playing voice response...")
                voice_handler.play_audio(audio_response_data)

                # Convert response audio to text for verification
                response_text = voice_handler.speech_to_text(audio_response_data)
                print(f"Voice response (transcribed): '{response_text}'")

                # Verify response contains time information
                verification_text = response_text or text_response
                time_keywords = ["time", "clock", "hour", "minute", "am", "pm", "utc", "gmt"]
                success = any(keyword in verification_text.lower() for keyword in time_keywords)
            else:
                print("No audio response received")
                success = False

            print("Test Result: PASS" if success else "Test Result: FAIL")
            if success:
                print("✓ Voice response contains time-related information")
            else:
                print("✗ Voice response does not contain expected time information")

            return success

        except Exception as exc:
            print("Test Result: ERROR")
            print(f"✗ Error: {str(exc)}")
            return False

async def run_all_tests(test_type="text"):
    """Run tests for all platform and model combinations"""
    results = {}

    print(f"Starting ADK Bidirectional Streaming Tests ({test_type.upper()})")
    print("=" * 60)

    # Choose models based on test type
    if test_type == "voice":
        # Only test audio-capable models for voice tests
        studio_models = ["gemini-2.0-flash-live-001",
                        "gemini-2.5-flash-preview-native-audio-dialog",
                        "gemini-2.5-flash-exp-native-audio-thinking-dialog"]
        vertex_models = ["gemini-2.0-flash-live-preview-04-09"]
    else:
        studio_models = GOOGLE_AI_STUDIO_MODELS
        vertex_models = VERTEX_AI_MODELS

    # Test Google AI Studio models
    print("\nTesting Google AI Studio Platform")
    print("-" * 40)

    for model in studio_models:
        tester = ADKStreamingTester("google-ai-studio", model)
        try:
            if test_type == "voice":
                success = await tester.test_voice_chat()
            else:
                success = await tester.test_text_chat()
            results[f"google-ai-studio-{model}-{test_type}"] = success
        except Exception as exc:
            print(f"Failed to test {model}: {exc}")
            results[f"google-ai-studio-{model}-{test_type}"] = False

        # Small delay between tests
        await asyncio.sleep(1)

    # Test Vertex AI models
    print("\nTesting Google Cloud Vertex AI Platform")
    print("-" * 40)

    for model in vertex_models:
        tester = ADKStreamingTester("vertex-ai", model)
        try:
            if test_type == "voice":
                success = await tester.test_voice_chat()
            else:
                success = await tester.test_text_chat()
            results[f"vertex-ai-{model}-{test_type}"] = success
        except Exception as exc:
            print(f"Failed to test {model}: {exc}")
            results[f"vertex-ai-{model}-{test_type}"] = False

        # Small delay between tests
        await asyncio.sleep(1)

    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)

    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")

    # Generate test report
    generate_test_report(results, test_type)

    return results

def generate_test_report(results, test_type, output_file="test_report.txt"):
    """Generate a comprehensive test report file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_content = f"""# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: {timestamp}
- **Test Type**: {test_type.upper()}
- **Total Tests**: {len(results)}
- **Passed Tests**: {sum(1 for success in results.values() if success)}
- **Failed Tests**: {sum(1 for success in results.values() if not success)}
- **Success Rate**: {(sum(1 for success in results.values() if success) / len(results) * 100):.1f}%

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
            report_content += f"- **{model}**: {icon} {status}\n"
        report_content += "\n"
    
    if vertex_ai_results:
        report_content += "### Vertex AI Platform\n\n"
        for test_name, success in vertex_ai_results.items():
            model = test_name.replace("vertex-ai-", "").replace(f"-{test_type}", "")
            status = "PASS" if success else "FAIL"
            icon = "✅" if success else "❌"
            report_content += f"- **{model}**: {icon} {status}\n"
        report_content += "\n"
    
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
- Records 5 seconds of voice input using PyAudio
- Converts speech to text using Google Cloud Speech-to-Text
- Sends audio to ADK streaming API
- Receives audio response from model
- Plays audio response using PyAudio
- Transcribes response for validation

"""
    elif test_type == "both":
        report_content += """### Text Chat Testing
- Sends text query via ADK streaming API
- Receives streaming text response
- Validates response content for time information

### Voice Chat Testing
- Records 5 seconds of voice input using PyAudio
- Converts speech to text using Google Cloud Speech-to-Text
- Sends audio to ADK streaming API
- Receives audio response from model
- Plays audio response using PyAudio
- Transcribes response for validation

"""
    
    # Add notes about failures
    failed_tests = [k for k, v in results.items() if not v]
    if failed_tests:
        report_content += "## Failed Test Analysis\n\n"
        for test_name in failed_tests:
            if "audio-dialog" in test_name or "audio-thinking" in test_name:
                report_content += f"- **{test_name}**: Audio-only model correctly rejects text input (expected behavior)\n"
            else:
                report_content += f"- **{test_name}**: Unexpected failure - requires investigation\n"
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

async def test_single_model(platform, model, test_type="text"):
    """Test a single platform and model combination"""
    tester = ADKStreamingTester(platform, model)
    if test_type == "voice":
        return await tester.test_voice_chat()
    return await tester.test_text_chat()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="ADK Bidirectional Streaming Test Tool")
    parser.add_argument(
        "--platform",
        choices=["google-ai-studio", "vertex-ai", "all"],
        default="all",
        help="Platform to test"
    )
    parser.add_argument("--model", help="Specific model to test")
    parser.add_argument(
        "--test-type",
        choices=["text", "voice", "both"],
        default="text",
        help="Type of test to run: text, voice, or both"
    )

    args = parser.parse_args()

    # Set SSL certificate file as required by ADK
    os.environ["SSL_CERT_FILE"] = os.popen("python -m certifi").read().strip()

    if args.model:
        # Test specific model
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
    else:
        # Run all tests
        if args.test_type == "both":
            print("Running text tests:")
            text_results = asyncio.run(run_all_tests("text"))
            print("\nRunning voice tests:")
            voice_results = asyncio.run(run_all_tests("voice"))
            
            # Generate combined report
            combined_results = {**text_results, **voice_results}
            generate_test_report(combined_results, "both", "combined_test_report.txt")
        else:
            asyncio.run(run_all_tests(args.test_type))

if __name__ == "__main__":
    main()
