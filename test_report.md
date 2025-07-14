# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: 2025-07-14 11:26:06
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: 1.6.1
- **Total Tests**: 10
- **Passed Tests**: 9
- **Failed Tests**: 1
- **Success Rate**: 90.0%

### Test Type Breakdown
- **Text Tests**: 4/5 passed (80.0%)
- **Voice Tests**: 5/5 passed (100.0%)

## Environment Configuration
- **Google Cloud Project**: gcp-samples-ic0
- **Google Cloud Location**: us-central1

## Detailed Results

### Google AI Studio

**gemini-live-2.5-flash-preview**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-2.0-flash-live-001**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-2.0-flash-exp**:
  - Text: ✅ PASS
  - Voice: ✅ PASS


### Vertex AI

**gemini-live-2.5-flash-preview-native-audio**:
  - Text: ❌ FAIL
  - Voice: ✅ PASS

**gemini-2.0-flash-exp**:
  - Text: ✅ PASS
  - Voice: ✅ PASS


## Voice Transcription Results

### Google AI Studio

**gemini-live-2.5-flash-preview**: "the current time in Tokyo Japan is 11:24 a.m. on Monday July 14th 2025 Tokyo observes Japan Standard time jst which is UTC GMT + 9 hours"

**gemini-2.0-flash-live-001**: "it is currently 11:25 a.m. in Tokyo Japan"

**gemini-2.0-flash-exp**: "it is 11:25 a.m. in Tokyo Japan"

### Vertex AI

**gemini-live-2.5-flash-preview-native-audio**: "it is 11:25 a.m. in Tokyo right now"

**gemini-2.0-flash-exp**: "it is 11:25 a.m. in Tokyo Japan"

## Error Traces

### Vertex AI

#### gemini-live-2.5-flash-preview-native-audio (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 176, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 219, in _collect_text_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 348, in run_live
    async for event in invocation_context.agent.run_live(invocation_context):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 228, in run_live
    async for event in self._run_live_impl(ctx):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 283, in _run_live_impl
    async for event in self._llm_flow.run_live(ctx):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 88, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 260, in connect
    async with self._live_api_client.aio.live.connect(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/genai/live.py", line 1056, in connect
    logger.info(await ws.recv(decode=False))
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) Request contains an invalid argument.; then sent 1007 (invalid frame payload data) Request contains an invalid argument.
```

## Test Methodology

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

## Failed Test Analysis

- **gemini-live-2.5-flash-preview-native-audio (text)**: Unexpected failure - requires investigation

## Environment Information
- **ADK Version**: 1.6.1
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
```

---
*Report generated by ADK Bidirectional Streaming Test Tool*
