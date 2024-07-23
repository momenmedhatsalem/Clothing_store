
from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from backend.models import Product, ProductColor, ProductImage, ProductSize, ProductCategory, Category


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the product data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from products.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('./Products.csv')):
            # Check if product with this id already exists
            product_id = row['id']
            existing_product = Product.objects.filter(id=product_id).first()
            if existing_product:
                # Product already exists, update its path
                existing_product.path = row['path']
                existing_product.price = row['price']
                existing_product.save()
            else:
                # Product does not exist, create a new one
                categories = row['category'].split(';')
                product = Product(product_name=row['product_name'], label=row['label'], subcategory=['subcategory'], price=row['price'], discount_price=row['discount_price'], pub_date=row['pub_date'], path=row['path'])
                product.save()

                for category_name in categories:
                    category, _ = Category.objects.get_or_create(name=category_name)
                    ProductCategory.objects.create(product=product, category=category)

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

            # Update or create ProductImage instances
            images = row['images'].split(';')
            for image in images:
                image_data = image.split(':')
                image_path = image_data[0]
                image_id = int(image_data[1])
                image_color = image_data[2]
                existing_image = ProductImage.objects.filter(id=image_id, product=existing_product or product).first()
                if existing_image:
                    # Image already exists, update its path
                    existing_image.path = image_path
                    existing_image.color = image_color
                    existing_image.save()
                else:
                    # Image does not exist, create a new one
                    new_image = ProductImage(product=existing_product or product, path=image_path, color=image_color)
                    new_image.save()



