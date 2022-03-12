from flask import render_template, url_for, flash, redirect, request, abort
from STORE import app, db, bcrypt
from STORE.forms import RegistrationForm, LoginForm
from STORE.models import User, Products, Cart
from flask_login import login_user, current_user, logout_user, login_required
import requests
import random
from werkzeug.utils import secure_filename
import os
from werkzeug.utils import secure_filename




@app.route("/", methods=['GET'])
def home():
    products = Products.query.all()
    return render_template('home.html', products=products)

@app.route("/sell", methods=['GET', 'POST'])
def sell():
    if request.method == "POST":
        uploaded_file = request.files['photo']                  #Save the file that user uploaded
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flash("Please use one of the following extensions: png, jpg, gif", 'danger')
                return render_template("sell.html")
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #Insert into products filename, name of product, price, description
        product = Products(name=request.form.get("name") ,price=request.form.get("price") ,description=request.form.get("description"), img=filename)
        db.session.add(product)
        db.session.commit()
        flash('Your product has been added','success')
        return redirect(url_for('home'))
    return render_template('sell.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))    #After login either take user to the account page or to the home page
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/addToCart/<int:product_id>")
@login_required
def addToCart(product_id):
    # check if product is already in cart
    row = Cart.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if row:
        # if in cart update quantity : +1
        row.quantity += 1
        db.session.commit()
        flash('This item is already in your cart, 1 quantity added!', 'success')

        # if not, add item to cart
    else:
        add_to_cart = Cart(product_id=product_id, user_id=current_user.id)
        db.session.add(add_to_cart)
        db.session.commit()
        flash('Item added to the cart!', 'success')
    return redirect(url_for('home'))


@app.route("/cart")
@login_required
def cart():
    cart = Products.query.join(Cart).add_columns(Cart.quantity, Products.price, Products.name,Products.img, Products.id).filter_by(user_id=current_user.id).all()
    return render_template("cart.html", cart=cart)

@app.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):
    remove_from_cart = Cart.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    db.session.delete(remove_from_cart)
    db.session.commit()
    flash('Your item has been removed from your cart!', 'success')
    return redirect(url_for('cart'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

