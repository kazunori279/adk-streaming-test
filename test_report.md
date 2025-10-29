# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: 2025-10-30 02:46:14
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: 1.17.0
- **Total Tests**: 18
- **Passed Tests**: 14
- **Failed Tests**: 4
- **Success Rate**: 77.8%

### Test Type Breakdown
- **Text Tests**: 7/9 passed (77.8%)
- **Voice Tests**: 7/9 passed (77.8%)

### Retry Statistics
- **Tests requiring retries**: 4/18
- **Total retry attempts**: 8

## Environment Configuration
- **Google Cloud Project**: gcp-samples-ic0
- **Google Cloud Location**: us-central1

## Detailed Results

### Google AI Studio

**gemini-2.0-flash-exp**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-2.0-flash-live-001**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-live-2.5-flash-preview**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-2.5-flash-native-audio-preview-09-2025**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS

**gemini-2.5-flash-preview-native-audio-dialog**:
  - Text (audio transcript): ❌ FAIL (retries: 2) - Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener; then sent 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener
  - Voice: ❌ FAIL (retries: 2) - Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener; then sent 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener

**gemini-2.5-flash-exp-native-audio-thinking-dialog**:
  - Text (audio transcript): ❌ FAIL (retries: 2) - Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi; then sent 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi
  - Voice: ❌ FAIL (retries: 2) - Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi; then sent 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi


### Vertex AI

**gemini-2.0-flash-exp**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-live-2.5-flash-preview-native-audio**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS

**gemini-live-2.5-flash-preview-native-audio-09-17**:
  - Text (audio transcript): ✅ PASS
  - Voice: ✅ PASS


## Voice Transcription Results

### Google AI Studio

**gemini-2.0-flash-exp**: "it is 2:42 a.m. in Tokyo Japan"

**gemini-2.0-flash-live-001**: "it is 2:42 a.m. on Thursday October 30th 2025 in Tokyo"

**gemini-live-2.5-flash-preview**: "the current time in Tokyo Japan is 2:43 a.m. on Wednesday October 29th 2025 Tokyo observes Japan Standard time jst which is UTC GMT + 9 hours and does not use daylight saving time"

**gemini-2.5-flash-native-audio-preview-09-2025**: "the current time in Tokyo Japan is 2 244 a.m."

**gemini-2.5-flash-preview-native-audio-dialog**: ""

**gemini-2.5-flash-exp-native-audio-thinking-dialog**: ""

### Vertex AI

**gemini-2.0-flash-exp**: "it's 2:45 a.m. in Tokyo"

**gemini-live-2.5-flash-preview-native-audio**: "the current time in Tokyo Japan is 2:45 a.m. on Thursday October 30 2025"

**gemini-live-2.5-flash-preview-native-audio-09-17**: "the current time in Tokyo Japan is 2:46 a.m."

## Error Traces

### Google AI Studio

#### gemini-2.5-flash-preview-native-audio-dialog (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 213, in test_text_chat
    full_response = await self._collect_audio_transcription_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 279, in _collect_audio_transcription_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 855, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 652, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 844, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 428, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 285, in connect
    async with self._live_api_client.aio.live.connect(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/genai/live.py", line 1075, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener; then sent 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener
```

#### gemini-2.5-flash-exp-native-audio-thinking-dialog (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 213, in test_text_chat
    full_response = await self._collect_audio_transcription_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 279, in _collect_audio_transcription_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 855, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 652, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 844, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 428, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 285, in connect
    async with self._live_api_client.aio.live.connect(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/genai/live.py", line 1075, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi; then sent 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi
```

#### gemini-2.5-flash-preview-native-audio-dialog (voice)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 328, in test_voice_chat
    audio_response, text_response = await self._collect_audio_response(live_events)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 348, in _collect_audio_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 855, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 652, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 844, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 428, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 285, in connect
    async with self._live_api_client.aio.live.connect(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/genai/live.py", line 1075, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener; then sent 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener
```

#### gemini-2.5-flash-exp-native-audio-thinking-dialog (voice)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 328, in test_voice_chat
    audio_response, text_response = await self._collect_audio_response(live_events)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 348, in _collect_audio_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 855, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 652, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 844, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 428, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 285, in connect
    async with self._live_api_client.aio.live.connect(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/genai/live.py", line 1075, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi; then sent 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi
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

- **gemini-2.5-flash-preview-native-audio-dialog (text)**: Audio-only model correctly rejects text input (expected behavior)
  - Failure Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener; then sent 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener
- **gemini-2.5-flash-exp-native-audio-thinking-dialog (text)**: Audio-only model correctly rejects text input (expected behavior)
  - Failure Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi; then sent 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi
- **gemini-2.5-flash-preview-native-audio-dialog (voice)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener; then sent 1008 (policy violation) models/gemini-2.5-flash-preview-native-audio-dialog is not found for API version v1alpha, or is not supported for bidiGener
- **gemini-2.5-flash-exp-native-audio-thinking-dialog (voice)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi; then sent 1008 (policy violation) models/gemini-2.5-flash-exp-native-audio-thinking-dialog is not found for API version v1alpha, or is not supported for bidi

## Environment Information
- **ADK Version**: 1.17.0
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
