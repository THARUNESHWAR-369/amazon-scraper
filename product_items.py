"""
    The ProductItem class represents an item in a product inventory.
"""
class ProductItem:
    """
    A class representing product information scraped from a website.

    Attributes:
        product_url (str): URL of the product.
        product_name (str): Name of the product.
        product_price (str): Price of the product.
        rating (str): Rating of the product.
        reviews (str): Number of reviews for the product.
    """
    def __init__(self, product_url, product_name, product_price, rating, reviews) -> None:
        self.product_url = product_url
        self.product_name = product_name
        self.product_price = product_price
        self.rating = rating
        self.reviews = reviews

    def __str__(self) -> str:
        return (
            f"Product: {self.product_name}\n"
            f"URL: {self.product_url}\n"
            f"Price: {self.product_price}\n"
            f"Rating: {self.rating}\n"
            f"Number of Reviews: {self.reviews}\n"
        )
        
    def toList(self) -> list:
        return [self.product_url, self.product_name, self.product_price, self.rating, self.reviews]

class IndividualProduct:
    def __init__(self, description, asin, product_description, manufacturer):
        self.description = description
        self.asin = asin
        self.product_description = product_description
        self.manufacturer = manufacturer

    def toList(self):
        return [self.description, self.asin, self.product_description, self.manufacturer]

class ProductListing:
    def __init__(self, product_item, individual_product):
        self.product_item = product_item
        self.individual_product = individual_product

    def to_list(self):
        return (
            self.product_item.toList() + self.individual_product.toList()
        )