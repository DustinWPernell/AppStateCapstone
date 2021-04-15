import requests

from Management.models import Settings


class APIAccess():
    Relevance = "Relevance"

    @staticmethod
    def build_body(sort, filter, limit, offset):
        filter_list = []
        for item in filter:
            filter_list.append({
                "values": item["value"],
                "name": item["name"]
            })

        return {
            "filters": filter_list,
            "limit": limit,
            "offset": offset,
            "sort": sort
        }

    @staticmethod
    def build_header():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Nenniltoz",
            "Authorization": "bearer " + Settings.get_tcg_bearer()
        }

    @staticmethod
    def build_url(productID):
        url = APIAccess.run_details(productID).json()["results"]
        return url[0]["url"] # add affiliate here

    @staticmethod
    def run_get(url):
        return requests.get("https://api.tcgplayer.com/v1.39.0/catalog/categories/1/" + url,
                            headers=APIAccess.build_header())

    @staticmethod
    def run_post(sort, filter, limit, offset):
        return requests.request("POST", "https://api.tcgplayer.com/v1.39.0/catalog/categories/1/search",
                                json=APIAccess.build_body(sort, filter, limit, offset),
                                headers=APIAccess.build_header()
                                )

    @staticmethod
    def run_details(result_list):
        formatted_list = str(result_list)
        formatted_list = formatted_list.strip("[").strip("]")
        return requests.get("https://api.tcgplayer.com/catalog/products/" + formatted_list,
                            headers=APIAccess.build_header())

    @staticmethod
    def run_pricing(result_list):
        formatted_list = str(result_list)
        formatted_list = formatted_list.strip("[").strip("]")
        return requests.get("https://api.tcgplayer.com/pricing/product/" + formatted_list,
                            headers=APIAccess.build_header())