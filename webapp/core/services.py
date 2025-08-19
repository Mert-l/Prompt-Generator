# core/services.py
from apify_client import ApifyClient
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import os, json

load_dotenv()
APIFY_KEY = os.getenv("APIFY_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

#getting data from Apify
def fetch_hashtag_data(hashtags):
    client = ApifyClient(APIFY_KEY)
    run_input = {
        "hashtags": hashtags,
        "adsTimeRange": "",
        "adsCountryCode": "",
    }
    run = client.actor("IDzg0vK5q8Gyhhteg").call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    return items

def _format_date(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')

#cleaning up, processing data
def process_item(item):
    
    return {
        "hashtag": item.get("hashtagName", "N/A"),
        "country": item.get("countryInfo", {}).get("value", "N/A"),
        "publish_count": item.get("publishCnt", 0),
        "video_views": item.get("videoViews", 0),
        "trend": [
            {"date": _format_date(t["time"]), "value": t["value"]}
            for t in item.get("trend", [])
        ],
        "audience_ages": item.get("audienceAges", []),
        "audience_interests": [
            {
                "label": i.get("interestInfo", {}).get("value", "Unknown"),
                "score": i.get("score", 0),
            }
            for i in item.get("audienceInterests", [])
        ],
        "related_hashtags": [
            {"name": t.get("hashtagName", ""), "url": t.get("videoUrl", "")}
            for t in item.get("relatedHashtags", [])
        ],
    }

#using open ai api to generate prompts
def generate_prompts_from_summary(summary_json_str):
    client = Groq(api_key=GROQ_KEY)
    prompt = f"""
Here is trending TikTok hashtag data:
{summary_json_str}

Based on that data, generate 5 short, viral video prompts that can be pasted directly into a video generator.
Do NOT focus on AI. Make them creative, attention-grabbing, and optimized for TikTok.
Include a short caption and suggested hashtags for each prompt.
"""
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
