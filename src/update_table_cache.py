from modules.requests_wrapper import RequestsWrapper
from modules.rate_limiter import RateLimiter

rate_limiter = RateLimiter(25, 25, 10)
requests_wrapper = RequestsWrapper(rate_limiter)

page_number = 1
complete = False
while not complete:
    response = requests_wrapper.get_json(
        f"https://statistikdatabasen.scb.se/api/v2/tables?pageNumber={page_number}")

    for table in response["tables"]:
        print(table["label"])

    if response["page"]["pageNumber"] == response["page"]["totalPages"]:
        break
    page_number += 1