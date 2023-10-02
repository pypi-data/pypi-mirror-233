# ChatGPT-TTS Integration Library!
 The **ChatGPT-TTS Integration Library** is a powerful open-source tool that seamlessly combines the capabilities of ChatGPT and Text-to-Speech (TTS) technology. With this library, developers can effortlessly **create** conversational AI applications that **not only understand text input** but also **generate natural-sounding spoken responses**. This integration allows for a more immersive and interactive user experience, making it ideal for chatbots, virtual assistants, and other AI-driven applications.

## Table of Contents
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Models](#models)
* [Integrate with Telegram](#integrate-with-telegram)
* [Parameters](#parameters)

## Getting Started

### Installation
#### Install using pypi
```bash
pip install chatgpt-tts
```
or
* Clone the GitHub repository:
	```bash
	git clone https://github.com/soyll/chatgpt-tts.git	
	```
* Navigate to directory:
	```bash
	cd chatgpt-tts 
	```
* (Recommended) Create a virtual environment to manage Python packages for your project:
	```bash
	python3 -m venv venv
	```
* Activate the virtual enviropment
	* On windows:
		```bash
		.\venv\Scripts\activate
		```  
	* On linux or macOs:
		```
		source venv/bin/activate
		```
* Install the required Python packages from  `requirements.txt`:
	```bash
	pip install -r requirments.txt
	```
## Usage

```python
import chatgpt-tts

# init ChatGPT-TTS
chat_tts = ChatGpt_TTS(speaker, model_id, language, folder_to_save)

# use ChatGPT-TTS
chat_tts.create_tts(text, prompt, user_id)
```
## Models
#### All *support* modeles check in [Silero Models](https://github.com/snakers4/silero-models#models-and-speakers)

## Integrate with Telegram
```python
# code by bruhmnm
import telebot  
from chatgptTTS import chat  
  
TOKEN = "TELEGRAM_TOKEN"  

# init ChatGPT-TTS 
chat_tts = chat.ChatGpt_TTS("en_0", "v3_en", "en", folder="usr/audio/")  
  
bot = telebot.TeleBot(TOKEN)  
  
@bot.message_handler(content_types=['text'])  
def integrate(message):  
	audio = chat_tts.create_tts(text=message.text, prompt="prompt", id=message.from_user.id)  
	# read wav
	with open(audio[1], 'rb') as fd:  
		audio = fd.read()  
	# send voice
	bot.send_voice(message.from_user.id, audio)  
  
bot.polling(none_stop=True)
```
## Parameters
|   name	|								description										      |   example  |
|----------|----------------------------------------------------------------|-
| speaker | A trained vocal pattern with gender, accent, and tone |en_0, en_1|
| model_id| Unique id of the language, indicating its version     | en_v3, v3_ru|
|   lang  | Language indicating available model_id and speaker    | ru, en
|  folder | Absolute path to the folder where Chat-GPT responses will be saved | C:/Example/Path/
|  prompt | A set of words denoting a task or dialog scenario | _Act as an editor and correct the mistakes in this text_|
|   text  | Text indicating a request to Chat-Gpt to which it will later respond | AI help for your creativty, no mstakes, great wrting!
| 	id	| A unique number that, when integrated with social media, can be linked to an individual user for logs | self.chat_id, self.user_id, id355367865, 34567653479
