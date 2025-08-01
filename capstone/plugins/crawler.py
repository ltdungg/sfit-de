import requests
import datetime

class TikiCrawler:
    def __init__(self):
        self.base_url = "https://tiki.vn/"
        self.headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    @staticmethod
    def transform_product_data(product, category):
        try:
            quantity_sold = product['quantity_sold']['value']
        except Exception as e:
            quantity_sold = 0

        product_data = {
            'product_id': product['id'] if 'id' in product else None,
            'sku': product['sku'] if 'sku' in product else None,
            'name': product['name'] if 'name' in product else None,
            'url_path': product['url_path'] if 'url_path' in product else None,
            'thumbnail_url': product['thumbnail_url'] if 'thumbnail_url' in product else None,
            'price': product['price'] if 'price' in product else None,
            'discount': product['discount'] if 'discount' in product else None,
            'discount_rate': product['discount_rate'] if 'discount_rate' in product else None,
            'original_price': product['original_price'] if 'original_price' in product else None,
            'rating_average': product['rating_average'] if 'rating_average' in product else None,
            'review_count': product['review_count'] if 'review_count' in product else None,
            'quantity_sold': quantity_sold,
            'prime_category_name': category['text'],
            'crawled_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'source': 'tiki.vn',
        }

        return product_data

    def get_product_categories(self):
        url = f"https://api.tiki.vn/raiden/v2/menu-config"

        response = requests.get(url, headers=self.headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            categories = data['menu_block']['items']

            for category in categories:
                category['category_code'] = category['link'].split('/')[-1].replace('c', '')
                category['category_name'] = category['link'].split('/')[-2]

        else:
            raise Exception(f"Failed to fetch categories: {response.status_code}")

        return categories

    def get_product_list_by_category(self, category: dict):
        print(f"Fetching products for category: {category['text']}")
        url = f"{self.base_url}api/api/personalish/v1/blocks/listings"
        params = {
            "limit": 40,
            "page": 1,
            "category": category['category_code'],
            "urlKey": category['category_name']
        }
        response = requests.get(url, headers=self.headers, params=params)
        print(f"Fetching URL: {response.url} (Page 1)")

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()['data']
            paging = response.json()['paging']

            products = [self.transform_product_data(product, category) for product in data]


        for page in range(2, paging['last_page'] + 1):
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            print(f"Fetching URL: {response.url} (Page {page})")
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()['data']
                products.extend([self.transform_product_data(product, category) for product in data])
            else:
                print(f"Failed to fetch page {page}: {response.status_code}")
                break

        return products

    def get_all_products(self):
        categories = self.get_product_categories()[:1]
        all_products = []

        for category in categories:
            products = self.get_product_list_by_category(category)
            all_products.extend(products)

        return all_products

if __name__ == "__main__":
    crawler = TikiCrawler()
    products = crawler.get_product_categories()
    print(f"Total products fetched: {products}")