# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: 2026-01-13 00:25:36
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: 1.22.1
- **Total Tests**: 14
- **Passed Tests**: 12
- **Failed Tests**: 2
- **Success Rate**: 85.7%

### Test Type Breakdown
- **Text Tests**: 6/7 passed (85.7%)
- **Voice Tests**: 6/7 passed (85.7%)

### Retry Statistics
- **Tests requiring retries**: 2/14
- **Total retry attempts**: 4

## Environment Configuration
- **Google Cloud Project**: gcp-samples-ic0
- **Google Cloud Location**: us-central1

## Detailed Results


**Note**: The following model list includes both officially supported models and deprecated models. To see a list of the currently supported models, see:
- **Gemini Live API**: Check the [Get started with Live API](https://ai.google.dev/gemini-api/docs/live#audio-generation)
- **Vertex AI Live API**: Check the [official Vertex AI Live API documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/live-api)

### Google AI Studio

**gemini-2.0-flash-exp**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-2.5-flash-native-audio-preview-09-2025**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS

**gemini-2.5-flash-native-audio-preview-12-2025**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS


### Vertex AI

**gemini-2.0-flash-exp**:
  - Text: ❌ FAIL (retries: 2) - Reason: Exception: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.
  - Voice: ❌ FAIL (retries: 2) - Reason: Exception: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.

**gemini-live-2.5-flash-preview-native-audio**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS

**gemini-live-2.5-flash-preview-native-audio-09-17**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS

**gemini-live-2.5-flash-native-audio**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS


## Voice Transcription Results

### Google AI Studio

**gemini-2.0-flash-exp**: "it is 9:24 a.m. in Tokyo Japan"

**gemini-2.5-flash-native-audio-preview-09-2025**: "it is 9:24 a.m. in Tokyo Japan"

**gemini-2.5-flash-native-audio-preview-12-2025**: "the current time in Tokyo Japan is 9:24 a.m."

### Vertex AI

**gemini-2.0-flash-exp**: ""

**gemini-live-2.5-flash-preview-native-audio**: "the current time in Tokyo Japan is 9:25 a.m."

**gemini-live-2.5-flash-preview-native-audio-09-17**: "the current time in Tokyo Japan is 9:25 p.m."

**gemini-live-2.5-flash-native-audio**: "the current time in Tokyo Japan is 9:25 a.m."

## Error Traces

### Vertex AI

#### gemini-2.0-flash-exp (text)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 233, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 283, in _collect_text_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 1027, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 739, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 1016, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 492, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 402, in connect
    async with self._live_api_client.aio.live.connect(
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/genai/live.py", line 1093, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.
```

#### gemini-2.0-flash-exp (voice)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 346, in test_voice_chat
    audio_response, text_response = await self._collect_audio_response(live_events)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 366, in _collect_audio_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 1027, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 739, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 1016, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 492, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 402, in connect
    async with self._live_api_client.aio.live.connect(
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/genai/live.py", line 1093, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.
```

## Test Methodology

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

## Failed Test Analysis

- **gemini-2.0-flash-exp (text)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.
- **gemini-2.0-flash-exp (voice)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.

## Environment Information
- **ADK Version**: 1.22.1
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
