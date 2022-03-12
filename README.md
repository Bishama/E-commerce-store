# E-commerce-store

#### Video Demo: <https://youtu.be/NSWs2E6aDUo>


#### Description:
This is an ecommerce website. Users can register for an account. After registering users are taken to the login page.
Users can go to the sell route and upload the image of the product they want to sell along with the product name, price and a short description
All of the products uploaded by users can be seen on the homepage
Users can add and remove item from their cart.
To go to the cart page login is required

Libraries Used are
flask
flask_sqlalchemy
flask_bcrypt
flask_login
flask_wtf
wtforms
sqlalchemy



Forms and Database
Flask-wtf forms are used for the validation of users. Sqlite and SQLALCHEMY is used for the storage of data. My program implements three tables
Users: Stores username, hashed-password and email entered in the registration form. Hashed passwords are obtained by using bcrypt.
Products: In this table images, name of product, price of product and description of product is saved when the user uploads the product on the sell page.
Cart: It stores user_id, product_id and quantity of products.

How to Run

To install all the packages, run:
pip3 install -r requirements.txt

Then run:

cd project
python app.py


 Resources Used
https://www.youtube.com/
https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g
https://flask.palletsprojects.com/en/2.0.x/
