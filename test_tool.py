#!/usr/bin/env python3
"""
ADK Bidi-Streaming Test Tool

Tests bidirectional streaming functionality with Google ADK using both
Google AI Studio and Google Cloud Vertex AI platforms.
"""

import os
import asyncio
import argparse
from dotenv import load_dotenv
from google.genai.types import Content, Part
from google.adk.runners import InMemoryRunner
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.tools import google_search

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

async def run_all_tests():
    """Run tests for all platform and model combinations"""
    results = {}

    print("Starting ADK Bidirectional Streaming Tests")
    print("=" * 60)

    # Test Google AI Studio models
    print("\nTesting Google AI Studio Platform")
    print("-" * 40)

    for model in GOOGLE_AI_STUDIO_MODELS:
        tester = ADKStreamingTester("google-ai-studio", model)
        try:
            success = await tester.test_text_chat()
            results[f"google-ai-studio-{model}"] = success
        except Exception as exc:
            print(f"Failed to test {model}: {exc}")
            results[f"google-ai-studio-{model}"] = False

        # Small delay between tests
        await asyncio.sleep(1)

    # Test Vertex AI models
    print("\nTesting Google Cloud Vertex AI Platform")
    print("-" * 40)

    for model in VERTEX_AI_MODELS:
        tester = ADKStreamingTester("vertex-ai", model)
        try:
            success = await tester.test_text_chat()
            results[f"vertex-ai-{model}"] = success
        except Exception as exc:
            print(f"Failed to test {model}: {exc}")
            results[f"vertex-ai-{model}"] = False

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

    return results

async def test_single_model(platform, model):
    """Test a single platform and model combination"""
    tester = ADKStreamingTester(platform, model)
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

    args = parser.parse_args()

    # Set SSL certificate file as required by ADK
    os.environ["SSL_CERT_FILE"] = os.popen("python -m certifi").read().strip()

    if args.model:
        # Test specific model
        if args.platform == "all":
            print("Error: Must specify platform when testing specific model")
            return
        asyncio.run(test_single_model(args.platform, args.model))
    else:
        # Run all tests
        asyncio.run(run_all_tests())

if __name__ == "__main__":
    main()
