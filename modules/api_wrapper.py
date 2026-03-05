from modules.requests_wrapper import RequestsWrapper
from modules.rate_limiter import RateLimiter

class ApiWrapper:
    def __init__(self):
        rate_limiter = RateLimiter(25, 25, 10)
        self.requests_wrapper = RequestsWrapper(rate_limiter)

    def get_tables(self, query_dict):
        query_string_list = [f"{key}={query_dict[key]}" for key in query_dict]
        query_string = "&".join(query_string_list)
        response = self.requests_wrapper.get_json(
            f"https://statistikdatabasen.scb.se/api/v2/tables?{query_string}")
        return response
    
    def get_table_metadata(self, table_id):
        response = self.requests_wrapper.get_json(
            f"https://statistikdatabasen.scb.se/api/v2/tables/{table_id}/metadata")
        return response

    def get_tables_by_page(self, page_number):
        response = self.get_tables({"pageNumber": page_number})
        is_last_page = response["page"]["pageNumber"] == response["page"]["totalPages"]
        return response, is_last_page

    def get_tables_by_query(self, query):
        response = self.get_tables({"query": query})
        return response

    def iterate_over_tables(self, handle_table):
        page_number = 1
        while True:
            response, is_last_page = api_wrapper.get_table_page(page_number)

            handle_table(response)

            if is_last_page:
                break
            page_number += 1
