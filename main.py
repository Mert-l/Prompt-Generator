from core.services import fetch_hashtag_data, process_item, generate_prompts_from_summary
import json

if __name__ == "__main__":
    hashtags = ["aimade", "aigenerated", "ai", "aivideo"]
    raw_items = fetch_hashtag_data(hashtags)
    processed = [process_item(it) for it in raw_items]

    # save if you like
    with open("processed.json", "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2)

    summary = json.dumps(processed, indent=2)
    prompts = generate_prompts_from_summary(summary)
    print(prompts)
