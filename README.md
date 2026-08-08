# Pipeline-Infrastructure-for-Chatgpt

Backend: OpenAIAPIkey -> analyse images -> outputs a specific format (Line from xxx to xxx is incorrect.) 
Frontend : Analyse images -> returns txt. 

>[!Change this]
backend.py -> allow_origins = ["Your actual website"]
To init, create a venv
```bash
python3 -m venv .venv
source .venv/bin/activate # Or if using windows .venv\Scripts\Activate.ps1 
pip install -r requirements.txt 
```
To run, type
```bash
python -m uvicorn backend:app --reload
```
Open frontend/index.html in VScode liveserver.

bot_gem.py and bot_gpt.py does the same thing but uses different AI models
