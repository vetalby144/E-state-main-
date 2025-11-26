from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from sqlalchemy import or_
import os

# =====================================================
#   APP + DB INIT
# =====================================================

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# =====================================================
#   MODELS
# =====================================================

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    inquiries = db.relationship("Inquiry", backref="user", lazy=True)


class Property(db.Model):
    __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    inquiries = db.relationship("Inquiry", backref="property", lazy=True)


class Inquiry(db.Model):
    __tablename__ = "inquiry"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)

    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


# =====================================================
#   CREATE TABLES + AUTO-SEED
# =====================================================

with app.app_context():
    db.create_all()

    # AUTO-SEED PROPERTIES (runs only if DB is empty)
    try:
        from seed import seed_properties
        seed_properties()
    except Exception as e:
        print("Seed skipped:", e)


# =====================================================
#   ROUTES — MAIN PAGE
# =====================================================

@app.route("/")
def index():
    search = request.args.get("search")
    city = request.args.get("city")
    prop_type = request.args.get("type")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    page = request.args.get("page", 1, type=int)

    query = Property.query

    if search and search.strip():
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Property.title.ilike(pattern),
                Property.city.ilike(pattern),
                Property.description.ilike(pattern)
            )
        )

    if city:
        query = query.filter(Property.city == city)

    if prop_type:
        query = query.filter(Property.property_type == prop_type)

    if min_price and min_price.isdigit():
        query = query.filter(Property.price >= int(min_price))

    if max_price and max_price.isdigit():
        query = query.filter(Property.price <= int(max_price))

    pagination = query.paginate(page=page, per_page=6, error_out=False)
    properties = pagination.items

    return render_template("index.html", properties=properties, pagination=pagination)


# =====================================================
#   REGISTER
# =====================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        if User.query.filter_by(email=email).first():
            flash("Email вже зайнятий!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("Реєстрація успішна!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# =====================================================
#   LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Користувача не знайдено!", "danger")
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash("Невірний пароль!", "danger")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["role"] = user.role

        flash("Вітаємо!", "success")

        if user.role == "admin":
            return redirect(url_for("admin_home"))

        return redirect(url_for("index"))

    return render_template("login.html")


# =====================================================
#   LOGOUT
# =====================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# =====================================================
#   USER HOME
# =====================================================

@app.route("/user_home")
def user_home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") == "admin":
        return redirect(url_for("admin_home"))

    user = User.query.get(session["user_id"])
    inquiries = Inquiry.query.filter_by(user_id=user.id).order_by(Inquiry.created_at.desc()).all()

    return render_template("user_home.html", user=user, inquiries=inquiries)


# =====================================================
#   ADMIN HOME
# =====================================================

@app.route("/admin_home")
def admin_home():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Доступ заборонено!", "danger")
        return redirect(url_for("index"))

    user = User.query.get(session["user_id"])
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()

    return render_template("admin_home.html", user=user, inquiries=inquiries)


# =====================================================
#   PROPERTY DETAILS
# =====================================================

@app.route("/property/<int:property_id>")
def property_details(property_id):
    prop = Property.query.get_or_404(property_id)
    return render_template("property_details.html", property=prop)


# =====================================================
#   CREATE INQUIRY
# =====================================================

@app.route("/property/<int:property_id>/request", methods=["POST"])
def create_inquiry(property_id):
    if "user_id" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("login"))

    message = request.form.get("message")

    if not message or len(message) < 3:
        flash("Повідомлення занадто коротке!", "danger")
        return redirect(url_for("property_details", property_id=property_id))

    inquiry = Inquiry(
        user_id=session["user_id"],
        property_id=property_id,
        message=message
    )

    db.session.add(inquiry)
    db.session.commit()

    flash("Заявку надіслано!", "success")
    return redirect(url_for("property_details", property_id=property_id))


# =====================================================
#   DELETE INQUIRY (ADMIN)
# =====================================================

@app.route("/admin/inquiries/delete/<int:inquiry_id>", methods=["POST"])
def delete_inquiry(inquiry_id):
    if "user_id" not in session or session.get("role") != "admin":
        flash("Доступ заборонено!", "danger")
        return redirect(url_for("index"))

    inquiry = Inquiry.query.get_or_404(inquiry_id)
    db.session.delete(inquiry)
    db.session.commit()

    flash("Заявку видалено!", "success")
    return redirect(url_for("admin_home"))


# =====================================================
#   CRUD: PROPERTIES
# =====================================================

@app.route("/admin/properties")
def admin_properties():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("index"))

    properties = Property.query.all()
    return render_template("admin_properties.html", properties=properties)


@app.route("/admin/properties/add", methods=["GET", "POST"])
def admin_add_property():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("index"))

    if request.method == "POST":
        prop = Property(
            title=request.form["title"],
            city=request.form["city"],
            property_type=request.form["property_type"],
            price=request.form["price"],
            description=request.form["description"],
            image_url=request.form["image_url"]
        )
        db.session.add(prop)
        db.session.commit()

        flash("Оголошення створено!", "success")
        return redirect(url_for("admin_properties"))

    return render_template("admin_add_property.html")


@app.route("/admin/properties/edit/<int:property_id>", methods=["GET", "POST"])
def admin_edit_property(property_id):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("index"))

    prop = Property.query.get_or_404(property_id)

    if request.method == "POST":
        prop.title = request.form["title"]
        prop.city = request.form["city"]
        prop.property_type = request.form["property_type"]
        prop.price = request.form["price"]
        prop.description = request.form["description"]
        prop.image_url = request.form["image_url"]

        db.session.commit()

        flash("Оголошення оновлено!", "success")
        return redirect(url_for("admin_properties"))

    return render_template("admin_edit_property.html", prop=prop)


@app.route("/admin/properties/delete/<int:property_id>", methods=["POST"])
def admin_delete_property(property_id):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("index"))

    prop = Property.query.get_or_404(property_id)
    db.session.delete(prop)
    db.session.commit()

    flash("Оголошення видалено!", "success")
    return redirect(url_for("admin_properties"))


# =====================================================
#   RUN (LOCAL ONLY)
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
