Purpose
=======

This repo is an idea to semi automate doctor's letter using chatgpd.

The user can insert patient information and notes and his api key.\
This infomations enables the tool to communicate with ChatGPD and ask for a doctors letter.\
The generated doctors letter will also saved as a word file since this is most likely the commonly used format.

Everything is written in german, feel free to use chatgpd to translate it to english.

Limitation
==========

- you need to create an API token and pay per request
- some general information about the patient and the doctor are still missing


Installation
============

install python3\
install python packages on windows:
```
py -m pip install openai
py -m pip install python-docx 
```
install python packages on linux:
```
pip install openai
pip install python-docx 
```

Start Tool
==========
```
python3 frontend.py
```
