from fastapi import FastAPI, Header, HTTPException
import urllib.request
import json
import uvicorn

app = FastAPI()

# 1. We define our VIP Pass
VALID_API_KEY = "sk_live_super_secret_123"

# 2. The new endpoint: A News Scraper
@app.get("/news")
def get_top_news(api_key: str = Header(None)):
    
    # 3. THE BOUNCER: If the key doesn't match, kick them out!
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key")
    
    # 4. THE VALUABLE TASK: Fetching real-time tech news
    try:
        # Step A: Ask Hacker News for the IDs of the top trending stories
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.urlopen(url)
        top_ids = json.loads(req.read())[:5] # Just grab the top 5
        
        headlines = []
        
        # Step B: Look up the title for each of those 5 stories
        for story_id in top_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_req = urllib.request.urlopen(story_url)
            story_data = json.loads(story_req.read())
            headlines.append(story_data.get("title"))
            
        # Step C: Hand the final list out the drive-thru window
        return {
            "status": "success", 
            "message": "Here is your live data. You have been charged $0.05.",
            "top_headlines": headlines
        }
        
    except Exception as e:
        # If the internet is down, let the customer know cleanly
        return {"error": "Could not fetch news right now."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
