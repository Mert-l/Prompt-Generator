from apify_client import ApifyClient
import json
from datetime import datetime
from groq import Groq
import os
from dotenv import load_dotenv


#handling api keys
load_dotenv()
apify_key = os.getenv("APIFY_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

#processing data from apify
def process_data(data):
    def format_date(timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

    # basic info
    hashtag_name = data.get('hashtagName', 'N/A')
    country = data.get('countryInfo', {}).get('value', 'N/A')
    publish_count = data.get('publishCnt', 0)
    video_views = data.get('videoViews', 0)

    print(f"Hashtag: {hashtag_name}")
    print(f"Country: {country}")
    print(f"Published Videos: {publish_count}")
    print(f"Total Video Views: {video_views}\n")

    # trend data
    print("Trend over time:")
    for entry in data.get('trend', []):
        date = format_date(entry['time'])
        value = entry['value']
        print(f"{date}: {value}")

    #  age distribution
    print("\nAudience Ages:")
    for age_group in data.get('audienceAges', []):
        print(f"Age Level {age_group['ageLevel']}: {age_group['score']}%")

    # interests
    print("\nAudience Interests:")
    for interest in data.get('audienceInterests', []):
        label = interest['interestInfo']['value']
        score = interest['score']
        print(f"{label}: {score}%")

    # related hashtags
    print("\nRelated Hashtags:")
    for tag in data.get('relatedHashtags', []):
        print(f"{tag['hashtagName']} - {tag['videoUrl']}")



    if "relatedVideos" in data:
        del data["relatedVideos"]


    with open('processed.json', 'w') as f:
        json.dump(data, f, indent=4)



# getting data from apify
client = ApifyClient(apify_key)

run_input = {
    "hashtags": ["aimade", "aigenerated", "ai", "aivideo"],
    "adsTimeRange": "",
    "adsCountryCode": "",
}

run = client.actor("IDzg0vK5q8Gyhhteg").call(run_input=run_input)

items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
for item in items:
    process_data(item)

with open("processed.json", "r", encoding="utf-8") as f:
    summary = f.read()



#video prompts 
prompt = f"""
Here is trending TikTok hashtag data:
{summary}

Based on that data, generate 5 short, viral video prompts that can be pasted directly into a video generator.
Do NOT focus on AI. Make them creative, attention-grabbing, and optimized for TikTok. 
Ideas can include animals, comedy, pranks, food, or any trending theme that has potential to go viral.
Include a short caption and suggested hashtags for each prompt.
"""

client = Groq(api_key=groq_key)

response = client.chat.completions.create(
    model="llama3-8b-8192",  
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
