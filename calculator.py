from fastapi import FastAPI, Header, HTTPException
import uvicorn

app = FastAPI()

# 1. We define our VIP Pass (In reality, Stripe generates this)
VALID_API_KEY = "sk_live_super_secret_123"

# 2. We tell the function to look for an "api-key" in the hidden Headers
@app.get("/calculate")
def calculate_revenue(price: float, customers: int, api_key: str = Header(None)):
    
    # 3. THE BOUNCER: If the key doesn't match, kick them out!
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key")
    
    # If the bouncer lets them through, do the math:
    total = price * customers
    return {"price": price, "customers": customers, "total_revenue": total}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
