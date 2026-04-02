import json
from backend.scorer import score_and_rank_hotels

with open('data/hotels.json', 'r') as f:
    data = json.load(f)

print("--- Testing HONEYMOON persona ---")
res = score_and_rank_hotels(data, 'honeymoon')
for item in res:
    print(item["hotel_name"], "-> Score:", item["score"], "->", item["highlights"])

print("\n--- Testing FAMILY persona ---")
res2 = score_and_rank_hotels(data, 'family')
for item in res2:
    print(item["hotel_name"], "-> Score:", item["score"], "->", item["highlights"])

print("\n--- Testing BUDGET persona ---")
res3 = score_and_rank_hotels(data, 'budget')
for item in res3:
    print(item["hotel_name"], "-> Score:", item["score"], "->", item["highlights"])
