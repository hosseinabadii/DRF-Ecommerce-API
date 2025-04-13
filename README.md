# 🛍️ Django REST Framework E-commerce API

A robust e-commerce API built with [**Django REST Framework**](https://www.django-rest-framework.org/). This API provides endpoints for managing products, orders, and user authentication with JWT.

## 🚀 Features

* User authentication using [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
* Product management with filtering and search capabilities
* Order management with order items
* Advanced filtering using [django-filter](https://django-filter.readthedocs.io/)
* API documentation using [drf-spectacular](https://drf-spectacular.readthedocs.io/)
* Performance monitoring with [django-silk](https://github.com/jazzband/django-silk)

## 💻 Technologies Used

* **Backend**: Django & Django REST Framework
* **Database**: SQLite
* **Authentication**: JWT (JSON Web Tokens)
* **Filtering**: Django Filter
* **API Documentation**: DRF Spectacular
* **Performance Monitoring**: Django Silk
* **Development Tools**: Django Extensions

## 📦 Setup

To set up the project, follow these steps:

1. Clone the repository: `git clone [repository-url]`
2. Navigate to the project root directory
3. Create a virtual environment:
   * On Windows: `python -m venv venv`
   * On Linux: `python3 -m venv venv`
4. Activate the virtual environment:
   * On Windows: `venv\Scripts\activate`
   * On Linux: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Run migrations: `python manage.py migrate`
7. Populate the database with sample data: `python manage.py populate_db`
8. Run the development server: `python manage.py runserver`

## 📚 API Endpoints

### Authentication
* `POST /api/token/` - Obtain JWT token
* `POST /api/token/refresh/` - Refresh JWT token
* `POST /api/token/verify/` - Verify JWT token

### Products
* `GET /api/products/` - List all products
* `POST /api/products/` - Create new product (Admin only)
* `GET /api/products/<id>/` - Get product details
* `PUT /api/products/<id>/` - Update product (Admin only)
* `PATCH /api/products/<id>/` - Partial update product (Admin only)
* `DELETE /api/products/<id>/` - Delete product (Admin only)
* `GET /api/products/info/` - Get product statistics

### Orders
* `GET /api/orders/` - List all orders (User's own orders or all for staff)
* `POST /api/orders/` - Create new order
* `GET /api/orders/<uuid>/` - Get order details
* `PUT /api/orders/<uuid>/` - Update order
* `PATCH /api/orders/<uuid>/` - Partial update order
* `DELETE /api/orders/<uuid>/` - Delete order
* `GET /api/orders/user-orders/` - Get user's orders

## 🔍 Filtering Capabilities

### Product Filters
* **Name Filter**: Search products by name (case-insensitive)
  * `GET /api/products/?name=product_name`
  * Supports exact and partial matches
* **Price Range Filters**:
  * `GET /api/products/?min_price=10` - Products with price >= 10
  * `GET /api/products/?max_price=100` - Products with price <= 100
  * `GET /api/products/?min_price=10&max_price=100` - Products within price range

### Order Filters
* **Date Filters**:
  * `GET /api/orders/?created_at=2024-01-01` - Orders created on specific date
  * `GET /api/orders/?created_before=2024-01-01` - Orders created before date
  * `GET /api/orders/?created_after=2024-01-01` - Orders created after date
* **Status Filter**:
  * `GET /api/orders/?status=pending` - Filter by order status
  * Available statuses: `pending`, `confirmed`, `cancelled`

### Additional Features
* **Search**: Search products by name and description
  * `GET /api/products/?search=keyword`
* **Ordering**: Sort results by various fields
  * `GET /api/products/?ordering=price` - Sort by price ascending
  * `GET /api/products/?ordering=-price` - Sort by price descending
  * Available fields: `name`, `price`
* **Pagination**: Control the number of results per page
  * `GET /api/products/?size=10` - Show 10 items per page
  * Maximum page size: 20 items

## 📊 API Documentation

The API documentation is available at:
* Swagger UI: `/api/schema/swagger-ui/`
* ReDoc: `/api/schema/redoc/`

## 🔍 Performance Monitoring

Django Silk is integrated for performance monitoring:
* Access the Silk interface at `/silk/`

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## 📝 License

This project is licensed under the MIT [License](./LICENSE).

**Note:** This project is based on a YouTube tutorial by **BugBytes**, which can be found at [here](https://www.youtube.com/watch?v=6AEvlNgRPNc&list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t).