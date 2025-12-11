# ADK Bidirectional Streaming Test Report

## Test Summary
- **Test Date**: 2025-12-11 05:48:31
- **Test Type**: COMBINED (Text + Voice)
- **Google ADK Version**: 1.20.0
- **Total Tests**: 10
- **Passed Tests**: 4
- **Failed Tests**: 6
- **Success Rate**: 40.0%

### Test Type Breakdown
- **Text Tests**: 2/5 passed (40.0%)
- **Voice Tests**: 2/5 passed (40.0%)

### Retry Statistics
- **Tests requiring retries**: 6/10
- **Total retry attempts**: 12

## Environment Configuration
- **Google Cloud Project**: gcp-samples-ic0
- **Google Cloud Location**: us-central1

## Detailed Results


**Note**: The following model list includes both officially supported models and deprecated models. To see a list of the currently supported models, see:
- **Gemini Live API**: Check the [Get started with Live API](https://ai.google.dev/gemini-api/docs/live#audio-generation)
- **Vertex AI Live API**: Check the [official Vertex AI Live API documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/live-api)

### Google AI Studio

**gemini-2.0-flash-exp**:
  - Text: ❌ FAIL (retries: 2) - Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
  - Voice: ❌ FAIL (retries: 2) - Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.

**gemini-2.5-flash-native-audio-preview-09-2025**:
  - Text (audio transcript): ❌ FAIL (retries: 2) - Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
  - Voice: ❌ FAIL (retries: 2) - Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.


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


## Voice Transcription Results

### Google AI Studio

**gemini-2.0-flash-exp**: ""

**gemini-2.5-flash-native-audio-preview-09-2025**: ""

### Vertex AI

**gemini-2.0-flash-exp**: ""

**gemini-live-2.5-flash-preview-native-audio**: "it's currently 2:48 p.m. in Tokyo Japan"

**gemini-live-2.5-flash-preview-native-audio-09-17**: "it is currently 2:48 p.m. in Tokyo Japan"

## Error Traces

### Google AI Studio

#### gemini-2.0-flash-exp (text)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 231, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 281, in _collect_text_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 967, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 689, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 956, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 487, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 342, in connect
    async with self._live_api_client.aio.live.connect(
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/genai/live.py", line 1093, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
```

#### gemini-2.5-flash-native-audio-preview-09-2025 (text)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 229, in test_text_chat
    full_response = await self._collect_audio_transcription_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 295, in _collect_audio_transcription_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 967, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 689, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 956, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 487, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 342, in connect
    async with self._live_api_client.aio.live.connect(
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/genai/live.py", line 1093, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
```

#### gemini-2.0-flash-exp (voice)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 344, in test_voice_chat
    audio_response, text_response = await self._collect_audio_response(live_events)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 364, in _collect_audio_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 967, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 689, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 956, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 487, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 342, in connect
    async with self._live_api_client.aio.live.connect(
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/genai/live.py", line 1093, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
```

#### gemini-2.5-flash-native-audio-preview-09-2025 (voice)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 344, in test_voice_chat
    audio_response, text_response = await self._collect_audio_response(live_events)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 364, in _collect_audio_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 967, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 689, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 956, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 487, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 342, in connect
    async with self._live_api_client.aio.live.connect(
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/genai/live.py", line 1093, in connect
    raw_response = await ws.recv(decode=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/websockets/asyncio/connection.py", line 322, in recv
    raise self.protocol.close_exc from self.recv_exc
websockets.exceptions.ConnectionClosedError: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
```

### Vertex AI

#### gemini-2.0-flash-exp (text)

```
Traceback (most recent call last):
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 231, in test_text_chat
    full_response = await self._collect_text_response(live_events)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 281, in _collect_text_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 967, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 689, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 956, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 487, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 342, in connect
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
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 344, in test_voice_chat
    audio_response, text_response = await self._collect_audio_response(live_events)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/adk-streaming-test/adk-streaming-test/test_tool.py", line 364, in _collect_audio_response
    async for event in live_events:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 967, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 689, in _exec_with_plugin
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/runners.py", line 956, in execute
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/base_agent.py", line 327, in run_live
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/agents/llm_agent.py", line 487, in _run_live_impl
    async for event in agen:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/flows/llm_flows/base_llm_flow.py", line 129, in run_live
    async with llm.connect(llm_request) as llm_connection:
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.14/x64/lib/python3.11/site-packages/google/adk/models/google_llm.py", line 342, in connect
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
  - Failure Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
- **gemini-2.5-flash-native-audio-preview-09-2025 (text)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
- **gemini-2.0-flash-exp (voice)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
- **gemini-2.5-flash-native-audio-preview-09-2025 (voice)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.; then sent 1007 (invalid frame payload data) API Key not found. Please pass a valid API key.
- **gemini-2.0-flash-exp (text)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.
- **gemini-2.0-flash-exp (voice)**: Unexpected failure - requires investigation
  - Failure Reason: Exception: received 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.; then sent 1007 (invalid frame payload data) gemini-2.0-flash-exp is not supported in the live api.

## Environment Information
- **ADK Version**: 1.20.0
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
