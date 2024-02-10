# Vosmos - Clothing Store Django Project

Welcome to Vosmos, a Django-based Clothing Store project that offers a delightful shopping experience with a range of features designed to enhance user convenience and satisfaction.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Models](#models)
4. [Features](#features)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction

Vosmos is a web application built using Django, featuring a tailored and streamlined user experience. Below are some key aspects that set Vosmos apart:

- **Anonymous Shopping:** Customers can seamlessly place orders without the need to create an account. The use of sessions and cookies ensures a smooth and efficient shopping process.

- **Persistent Cart:** The shopping cart retains added items even if the user chooses not to create an account. This allows users to continue their shopping experience seamlessly across sessions.

- **Email Notifications:** Vosmos sends email confirmations to users after a purchase, providing a transparent and professional communication channel. Users can track their orders and access order history through the application.

- **Contact Us Page:** Vosmos includes a dedicated "Contact Us" page, offering users a straightforward way to reach out for support or inquiries.

- **Favorite Items:** Users can create and manage a list of favorite items, allowing them to curate their preferences and easily revisit items of interest.

- **Return Policy Page:** Vosmos is committed to transparency, and the Return Policy page outlines the procedures and guidelines for returns, ensuring a clear understanding for customers.

- **Product Details Page:** Each product is presented with detailed information, providing users with comprehensive insights into the item they are considering.

- **Product Customization:** Vosmos empowers users to personalize their clothing items by offering a product customization page. Users can upload their designs and see them applied to their customized t-shirts.

- **Frontend Template:** The project utilizes a frontend template from Colorlib, which has been carefully modified and integrated to harmonize with the backend functionalities.

## Installation

## Clothing Store Project Installation Guide

Thank you for your interest in Vosmos Store project! This guide will walk you through the installation process step by step.

### Prerequisites
- Python 3.x installed on your system
- Git installed on your system

### Installation Steps

1. **Fork the Repository**

   Fork the repository from [GitHub](https://github.com/momenmedhatsalem/Clothing_store) to your own GitHub account.

2. **Clone the Repository**

   Clone the forked repository to your local machine using the following command:
   ```bash
   git clone https://github.com/momenmedhatsalem/Clothing_store.git
   ```

3. **Navigate to the Project Directory**

   Change your current directory to the project directory:
   ```bash
   cd clothing
   ```

4. **Install Requirements**

   Install the required Python packages using pip. It's recommended to use a virtual environment to manage dependencies.
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Server**

   Once the requirements are installed, you can start the Django development server using the following command:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:8000/` or `http://localhost:8000/` to access the Clothing Store application.

### Notes
- If you encounter any issues during the installation process, please refer to the [Django documentation](https://docs.djangoproject.com/en/stable/) or feel free to open an issue in the GitHub repository.
- Remember to set up your database configurations in `settings.py` before running the server in a production environment.

Thank you for installing our Clothing Store project! If you have any questions or feedback, please don't hesitate to contact us. Happy coding!
## Models

### Product
- Represents a clothing product with various attributes such as name, category, label, price, and images.
- Allows customization with front and back canvas designs.

### FrontCanva and BackCanva
- Store properties and images for the front and back canvas designs associated with a product.

### Category and ProductCategory
- Define product categories and associate them with products.

### ProductImage
- Represents additional images associated with a product, including color and path information.

### MyUser
- Extends the default Django `AbstractUser` model to include additional user information such as country, city, phone, and favorites.

### ProductSize and ProductColor
- Manage product sizes and colors, including quantity information.

### PromoCode
- Represents promotional codes with discount information.

### Cart and CartItem
- Implement a shopping cart system with the ability to apply promo codes and calculate total prices.

### Address
- Represents user addresses with details like country, street, building, city, etc.

### Order and OrderItem
- Handle user orders, including items, payment information, and order status.

## Contributing

We welcome contributions from the community. To contribute to Vosmos, please refer to our [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE), providing users with the freedom to use, modify, and distribute the code for their projects.

Thank you for choosing Vosmos! We look forward to providing you with an exceptional shopping experience. Happy shopping!




