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

To run the Vosmos project locally, follow the installation steps outlined in the [Installation](#installation) section of the README.

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




