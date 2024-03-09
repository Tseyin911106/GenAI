# Audio-To-Text sample codes

* `post_audio.py` : HTTP Post audio file to a http-server
* `whisper_server.py` : HTTP server to receive audio file and transcribe to text
* `whisper_llm_server.py` : HTTP server to transcribe audio file to text, and text-to-text by calling a LLM model
  
## Installaltion
`pip install requests flask`<br>
`pip install git+https://github.com/openai/whisper.git`<br>

---
## ASR

* Speech Recognition with **OpenAI/Whisper**:
`python asr.py`<br>

* Speech Recognition with **Faster-Whisper**:
`python faster_asr.py`<br>

---
### HTTP Servers

* To test **Whisper** server:
`python whisper_server.py` - running Whiserp http-server<br>
`python post_audio.py` - running http-post audio file to server<br>

* To test **Whisper+LLM** server:
`python whisper_llm_server.py` - running Whiserp+LLM http-server<br>
`python post_audio.py` - running http-post audio file to server<br>

