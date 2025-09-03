from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import List
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

csv_file = 'data.csv'  
df = pd.read_csv(csv_file)

class WalletRequest(BaseModel):
    wallets: List[str]

@app.post("/check_wallets")
async def check_wallets(request: WalletRequest):
    wallets = request.wallets

    if not wallets:
        return JSONResponse(content={"success": False, "message": "No wallets provided"}, status_code=400)

    results = []
    for wallet in wallets:
        found = df[df['wallet_address'] == wallet].shape[0] > 0  
        results.append({'wallet': wallet, 'found': found})

    return JSONResponse(content={"success": True, "results": results}, status_code=200)

# To run the FastAPI app with Uvicorn, use the following command:
# uvicorn app:app --reload
