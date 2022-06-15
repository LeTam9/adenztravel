from flask import Blueprint, render_template
from website.models import load_products, load_toutravel
auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    cates = load_toutravel()
    products = load_products()
    return render_template('text.html', cates=cates, products=products)

