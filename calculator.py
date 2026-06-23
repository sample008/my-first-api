from fastapi import FastAPI, Header, HTTPException
import urllib.request
import re
import uvicorn

app = FastAPI()

# 1. We define our VIP Pass
VALID_API_KEY = "sk_live_super_secret_123"

# 2. The New Commercial Endpoint: SEO Extractor
@app.get("/extract")
def extract_seo_data(target_url: str, api_key: str = Header(None)):
    
    # 3. THE BOUNCER
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key")
    
    # 4. THE VALUABLE TASK
    try:
        # We pretend to be a normal web browser so websites don't block us
        req = urllib.request.Request(
            target_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        # Download the raw website code
        response = urllib.request.urlopen(req)
        html_content = response.read().decode('utf-8', errors='ignore')
        
        # Hunt down the Title tag
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        title = title_match.group(1) if title_match else "No title found"
        
        # Hunt down the Description tag
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
        description = desc_match.group(1) if desc_match else "No description found"
        
        # Hand the packaged data back to the customer
        return {
            "target_url": target_url,
            "title": title,
            "description": description,
            "status": "Success. Billed $0.05."
        }
        
    except Exception as e:
        return {"error": f"Could not extract data. Details: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
