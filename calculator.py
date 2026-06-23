from fastapi import FastAPI
import uvicorn

# 1. We build the building
app = FastAPI()

# 2. We open a specific window (the URL path)
@app.get("/calculate")
def calculate_revenue(price: float, customers: int):
    total = price * customers
    
    # Notice we use curly brackets here. This formats the answer 
    # into a language that other computers (and APIs) easily understand.
    return {"price": price, "customers": customers, "total_revenue": total}

# 3. We turn on the "Open" sign so the server starts
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
