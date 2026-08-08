# Pipeline-Infrastructure

Backend: OpenAIAPIkey -> analyse images -> outputs a specific format (Line from xxx to xxx is incorrect.) 

Frontend : Analyse images -> returns txt. 

>[!NOTE]
>When fully developed. Change backend.py -> allow_origins = ["Your actual website"]

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
Install Vscode live server extension and open frontend/index.html

bot_gem.py and bot_gpt.py does the same thing but uses different AI models. Switch between the two in backend.py
