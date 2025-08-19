from django.shortcuts import render
from core.services import fetch_hashtag_data, process_item, generate_prompts_from_summary
import json

def home(request):
    raw = request.GET.get("hashtags", "aimade,aigenerated,ai,aivideo")
    hashtags = [h.strip() for h in raw.split(",") if h.strip()]

    raw_items = fetch_hashtag_data(hashtags)
    processed = [process_item(it) for it in raw_items]

    summary = json.dumps(processed, indent=2)
    prompts = generate_prompts_from_summary(summary)

    return render(request, "dashboard/home.html", {
        "hashtags": hashtags,
        "data": processed,
        "prompts": prompts,
    })

