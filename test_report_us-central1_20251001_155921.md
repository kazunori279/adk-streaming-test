# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: 2025-10-01 15:59:21
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: 1.15.1
- **Total Tests**: 18
- **Passed Tests**: 13
- **Failed Tests**: 5
- **Success Rate**: 72.2%

### Test Type Breakdown
- **Text Tests**: 4/9 passed (44.4%)
- **Voice Tests**: 9/9 passed (100.0%)

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
  - Text: ❌ FAIL
  - Voice: ✅ PASS

**gemini-2.5-flash-preview-native-audio-dialog**:
  - Text: ❌ FAIL
  - Voice: ✅ PASS

**gemini-2.5-flash-exp-native-audio-thinking-dialog**:
  - Text: ❌ FAIL
  - Voice: ✅ PASS


### Vertex AI

**gemini-2.0-flash-exp**:
  - Text: ✅ PASS
  - Voice: ✅ PASS

**gemini-live-2.5-flash-preview-native-audio**:
  - Text: ❌ FAIL
  - Voice: ✅ PASS

**gemini-live-2.5-flash-preview-native-audio-09-17**:
  - Text: ❌ FAIL
  - Voice: ✅ PASS


## Voice Transcription Results

### Google AI Studio

**gemini-2.0-flash-exp**: "it is currently 3:56 p.m. in Tokyo Japan"

**gemini-2.0-flash-live-001**: "it is 356 p.m. in Tokyo Japan"

**gemini-live-2.5-flash-preview**: "the current time in Tokyo Japan is 356 p.m. on Wednesday October 1 2025 Tokyo observes Japan Standard time jst which is UTC +9 and does not currently use daylight saving time"

**gemini-2.5-flash-native-audio-preview-09-2025**: "the current time and Tokyo Japan is 3:57 p.m."

**gemini-2.5-flash-preview-native-audio-dialog**: "the current time in Tokyo Japan is 357 p.m."

**gemini-2.5-flash-exp-native-audio-thinking-dialog**: "the current time in Tokyo Japan is 358 p.m."

### Vertex AI

**gemini-2.0-flash-exp**: "it is 358 p.m. in Tokyo"

**gemini-live-2.5-flash-preview-native-audio**: "it's currently 3:58 p.m. in Tokyo Japan they are in the Asia Tokyo time zone and do not currently observe Daylight Saving Time"

**gemini-live-2.5-flash-preview-native-audio-09-17**: "it is currently 3:59 p.m. in Tokyo Japan Tokyo is in the Asia Tokyo time zone"

## Error Traces

### Google AI Studio

#### gemini-2.5-flash-native-audio-preview-09-2025 (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 191, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 234, in _collect_text_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 575, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 383, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 564, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 283, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 276, in _run_with_trace
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 350, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 271, in connect
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
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) Cannot extract voices from a non-audio request.; then sent 1007 (invalid frame payload data) Cannot extract voices from a non-audio request.
```

#### gemini-2.5-flash-preview-native-audio-dialog (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 191, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 234, in _collect_text_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 575, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 383, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 564, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 283, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 276, in _run_with_trace
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 350, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 271, in connect
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
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) Cannot extract voices from a non-audio request.; then sent 1007 (invalid frame payload data) Cannot extract voices from a non-audio request.
```

#### gemini-2.5-flash-exp-native-audio-thinking-dialog (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 191, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 234, in _collect_text_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 575, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 383, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 564, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 283, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 276, in _run_with_trace
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 350, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 271, in connect
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
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) Cannot extract voices from a non-audio request.; then sent 1007 (invalid frame payload data) Cannot extract voices from a non-audio request.
```

### Vertex AI

#### gemini-live-2.5-flash-preview-native-audio (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 191, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 234, in _collect_text_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 575, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 383, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 564, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 283, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 276, in _run_with_trace
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 350, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 271, in connect
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

#### gemini-live-2.5-flash-preview-native-audio-09-17 (text)

```
Traceback (most recent call last):
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 191, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/test_tool.py", line 234, in _collect_text_response
    async for event in live_events:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 575, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 383, in _exec_with_plugin
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/runners.py", line 564, in execute
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 283, in run_live
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/base_agent.py", line 276, in _run_with_trace
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/agents/llm_agent.py", line 350, in _run_live_impl
    async for event in agen:
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 128, in run_live
    async with llm.connect(llm_request) as llm_connection:
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kazsato/Documents/GitHub/adk-streaming-test/.venv/lib/python3.12/site-packages/google/adk/models/google_llm.py", line 271, in connect
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

- **gemini-2.5-flash-native-audio-preview-09-2025 (text)**: Unexpected failure - requires investigation
- **gemini-2.5-flash-preview-native-audio-dialog (text)**: Audio-only model correctly rejects text input (expected behavior)
- **gemini-2.5-flash-exp-native-audio-thinking-dialog (text)**: Audio-only model correctly rejects text input (expected behavior)
- **gemini-live-2.5-flash-preview-native-audio (text)**: Unexpected failure - requires investigation
- **gemini-live-2.5-flash-preview-native-audio-09-17 (text)**: Unexpected failure - requires investigation

## Environment Information
- **ADK Version**: 1.15.1
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
