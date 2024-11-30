# Khadijah AI (in-progress)

Khadijah is a voice-controlled digital assistant designed to perform various tasks such as opening and closing applications, responding to greetings, and interacting with the user via voice commands. This project leverages Python libraries for text-to-speech, speech recognition, and keyboard shortcuts to deliver a dynamic and interactive experience.

---

## Features

- **Voice-Controlled Commands**: 
  - Open or close common applications like Terminal, Safari, Notes, and more.
  - Respond to user greetings and basic queries.
  
- **Customizable Hotkeys**:
  - `j` to start listening.
  - `k` to pause listening.

- **Dynamic Application Mapping**:
  - Easily add or modify supported applications in the global `APP_MAP`.

---

## Technologies Used

- **Python Libraries**:
  - `pyttsx3`: For text-to-speech functionality.
  - `SpeechRecognition`: To recognize and process user voice commands.
  - `keyboard`: To add hotkey functionality for starting and pausing the assistant.
  - `python-decouple`: For managing user and bot configuration variables.

- **macOS-Specific Utilities**:
  - `osascript`: Used to execute AppleScript for closing applications.
  - `open`: The native macOS command to launch applications.

---

## Installation

### Prerequisites
- Python 3.7 or higher installed on your system.

### Step 1: Clone the Repository
```bash
$ git clone https://github.com/shahbajsingh/khadijah-ai.git
$ cd khadijah-ai
```

### Step 2: 
#### (Option 1) Set up Dependencies
```bash
$ pip install -r requirements.txt
```
#### (Option 2) Use Setup Script
```bash
$ chmod +x setup.sh
$ ./setup.sh
```

### Step 3: Configure User Information
Create a `.env` file in the project directory with the following content:
```env
USER=YourName
```

### Usage

###### 1. Start Khadijah

Run the script
```bash
$ python khadijah-ai.py
```
###### 2. Voice Commands

* Say `open [application]` to open an application
* Say `quit [application]` to close an application
* Example:
    * `open terminal`
    * `quit safari`

###### 3. Exit Khadijah
Say `stop` or `exit` to gracefully shut down Khadijah
