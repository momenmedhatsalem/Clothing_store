
from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from frontend.models import Product, ProductColor, ProductImage, ProductSize


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the product data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from products.csv"

    def handle(self, *args, **options):
    



        #Code to load the data into database
        for row in DictReader(open('./Products.csv')):
            product=Product(product_name=row['product_name'], category=row['category'], label=row['label'], subcategory=['subcategory'], price=row['price'], discount_price=row['discount_price'], pub_date=row['pub_date'])  
            product.save()

            # Get size data for this product from the file
            sizes = row['sizes'].split(';')
            for size in sizes:
                size_data = size.split(':')
                size_name = size_data[0]
                size_quantity = int(size_data[1])
                size_instance = ProductSize(product=product, size=size_name, quantity=size_quantity)
                size_instance.save()

            # Get color data for this product from the file
            colors = row['colors'].split(';')
            for color in colors:
                color_data = color.split(':')
                color_name = color_data[0]
                color_id = color_data[1]
                color_quantity = int(color_data[2])
                color_instance = ProductColor(product=product, color=color_name, color_id=color_id, quantity=color_quantity)
                color_instance.save()


