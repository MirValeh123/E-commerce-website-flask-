from app import app
from flask import render_template, request, flash, redirect
from models import Product, Size, Color, Category, User, Contact, Comments, Favorites, Subcategory
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user
from forms import RegisterForm, LoginForm, ContactForm, CommentForm
from extensions import db

# Shop
@app.route('/')
def shop():
    products = Product.query.all()
    sub_category = Subcategory.query.all()
    categories = Category.query.all()
    sizes = Size.query.all()
    colors = Color.query.all()
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    color = request.args.get('color')
    size = request.args.get('size')
    min_price = request.args.get('min')
    max_price = request.args.get('max')
    name = request.args.get('test')
    product_count = Color.count_color()
    product_count = Size.count_size()
    
    if category:

        products = Category.query.filter_by(id=category).first().product
    if subcategory:
        products = Subcategory.query.filter_by(id=subcategory).first().product
    if color:
        products = Color.query.filter_by(id=color).first().product
    if size:
        products = Size.query.filter_by(id=size).first().product
    if min_price and max_price:
        products = Product.query.filter(
            Product.price.between(min_price, max_price)).all()
    if name:
        products = Product.query.filter(Product.name.contains(name)).all()

    return render_template('shop.html', products=products, categories=categories, sub_category=sub_category, sizes=sizes, colors=colors, product_count=product_count)



# Start Favorities
@app.route('/add-favorite/<int:product_id>', methods=['POST', 'GET'])
def add_favorite(product_id):
    product = Product.query.get_or_404(product_id)
    favorite = Favorites(
        product_id=product_id,
        user_id=current_user.id
    )
    db.session.add(favorite)
    db.session.commit()
    redirect('favorites')
    return favorites()


@app.route('/favorites', methods=['GET'])
def favorites():
    favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()

    favorites = Favorites.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites, fav_count=favorites_count)


@app.route('/products/<int:id>',methods=['POST'])
def delete_product(id):
    
    fav = Favorites.query.filter_by(product_id=id,
                                 user_id=current_user.id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return favorites()
    return render_template('favorites.html')

# End Favorities


# Start Login&Register

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=generate_password_hash(form.confirm_password.data)

            )

            user.save()
            flash('Registered!', 'success')
            return shop()
        flash('Please register!', 'danger')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request.form)
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):

            login_user(user)
            flash(f'{current_user} login!','success')

            return shop()

        flash('Login Failed!User is false!', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logout!', 'success')
    return shop()

# End Login&Register


# Start Contact
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    favorites_count = Favorites.query.filter_by(
        user_id=current_user.id).count()
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate_on_submit():
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                messages=form.messages.data
            )
            contact.save()
            flash(f'{contact.name} take messages!', 'success')
            return shop()
        flash('Please fill area!','danger')
    return render_template('contact.html', form=form,fav_count=favorites_count)

# End Contact

# Start Detail
@app.route('/detail', methods=['POST', 'GET'])
def detail():
    id = request.args.get('id')
    

    if id:

        comment_count = Comments.query.filter_by(product_id=id).count()
        products = Product.query.filter_by(id=id).first()
        product_comments = Comments.query.filter_by(product_id=id).all()
        name = Product.query.filter(Product.id != id, Product.category_id.ilike(f'%{products.id}%')).all()
    form = CommentForm(formdata=None)
    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate_on_submit():
            comment = Comments(
                comments=form.comment.data,
                user_id=current_user.id,
                product_id=id
            )
            comment.save()
            return redirect(request.url)
        form = CommentForm(formdata=None)
    return render_template('detail.html', product_info=products, form=form, comments=product_comments, com_count=comment_count, name=name)
# End Detail


# Start Search
@app.route('/search')
def search():
    query = request.args.get('test')

    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', query=query, products=products)
# End Search



# Start Error
@app.errorhandler(Exception)          
def basic_error(e): 

    return render_template('includes/error.html',error=e)
# End Error