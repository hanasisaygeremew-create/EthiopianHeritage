from flask import (
    Flask, render_template, request, abort,
    redirect, url_for, session
)
from database import get_connection
import os
import hmac

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("HERITAGE_SECRET_KEY")
    app.config["ADMIN_PASSWORD"] = os.environ.get("HERITAGE_ADMIN_PASSWORD")

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/sites")
    def sites():
        return render_template("sites.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()

            if not all([name, email, subject, message]):
                return render_template(
                    "contact.html",
                    feedback="Please fill in all fields."
                )
            try:
                with get_connection() as connection:
                    connection.execute(
                        """
                        INSERT INTO contact_messages
                        (name, email, subject, message)
                        VALUES (?, ?, ?, ?)
                        """,
                        (name, email, subject, message)
                    )

                return render_template(
                    "contact.html",
                    feedback="Your message was saved successfully!"
                )

            except Exception:
                app.logger.exception("Could not save contact message")
                return render_template(
                    "contact.html",
                    feedback="Sorry, we couldn't save your message. Please try again."
                ), 500  

        return render_template("contact.html")

    site_data = {
        "lalibela": {
            "name": "Lalibela",
            "image": "lalibela.jpg",
            "location": "Lalibela, Amhara Region, northern Ethiopia",
            "period": "Medieval period, especially the 12th and 13th centuries",
            "short_description": "Discover Ethiopia's remarkable rock-hewn churches.",
            "history": (
                "Lalibela is famous for its eleven medieval churches "
                "carved directly into rock. Their construction is "
                "traditionally associated with King Lalibela of the "
                "Zagwe dynasty. The churches remain important places "
                "of worship and pilgrimage."
            ),
            "fact": (
                "The churches include Biete Ghiorgis, also known as "
                "the Church of Saint George, which has a cross-shaped design."
            )
        },
        "aksum": {
            "name": "Aksum",
            "image": "aksum.jpg",
            "location": "Aksum, Tigray Region, northern Ethiopia",
            "period": "Ancient Aksumite civilization, especially the 1st to 8th centuries CE",
            "short_description": "Explore the legacy of an ancient African kingdom.",
            "history": (
                "Aksum was the center of a powerful ancient kingdom "
                "connected to trade across the Red Sea and beyond. "
                "Its archaeological remains include monumental stone "
                "stelae, royal tombs, and ruins of ancient buildings."
            ),
            "fact": (
                "Aksumite inscriptions in languages including Ge'ez, "
                "Sabaean, and Greek help historians study the kingdom."
            )
        },
        "gondar": {
            "name": "Gondar",
            "image": "gondar.jpg",
            "location": "Gondar, Amhara Region, northwestern Ethiopia",
            "period": "Especially the 17th and 18th centuries",
            "short_description": "Discover Ethiopia's historic royal castles.",
            "history": (
                "Emperor Fasilides established Gondar as a permanent "
                "capital in 1636. Its royal complex, Fasil Ghebbi, "
                "contains castles and other buildings that reflect "
                "Ethiopia's distinctive architectural history."
            ),
            "fact": (
                "Fasil Ghebbi is surrounded by a wall about 900 metres "
                "long and was inscribed on the UNESCO World Heritage "
                "List in 1979."
            )
        },
        "harar": {
            "name": "Harar Jugol",
            "image": "harar.jpg",
            "location": "Harar, Harari Region, eastern Ethiopia",
            "period": "Historic walled city, with walls dating from the medieval period",
            "short_description": "Explore a historic walled city shaped by African and Islamic traditions.",
            "history": (
                "Harar Jugol is a historic fortified town in eastern "
                "Ethiopia. Its walls, mosques, shrines, traditional "
                "houses, and narrow streets reflect centuries of "
                "cultural exchange, trade, and religious learning."
            ),
            "fact": (
                "Harar Jugol was inscribed on the UNESCO World Heritage "
                "List in 2006."
            )
        },
        "tiya": {
            "name": "Tiya",
            "image": "tiya.jpg",
            "location": "Tiya, central Ethiopia",
            "period": "Ancient archaeological site; the exact dates of its monuments are uncertain",
            "short_description": "Discover distinctive carved stone monuments.",
            "history": (
                "Tiya is an archaeological site known for its group of "
                "standing stone monuments, or stelae. Some bear carved "
                "symbols and designs that researchers study to better "
                "understand the region's past cultural traditions."
            ),
            "fact": (
                "Tiya was inscribed on the UNESCO World Heritage "
                "List in 1980."
            )
        }
    }

    @app.route("/sites/<slug>")
    def site_detail(slug):
        site = site_data.get(slug)

        if site is None:
            abort(404)

        return render_template("site_detail.html", site=site)

    @app.route("/map")
    def heritage_map():
        return render_template("map.html")

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            password = request.form.get("password", "")
            admin_password = app.config.get("ADMIN_PASSWORD")

            if not admin_password or not app.config.get("SECRET_KEY"):
                return "Admin login is not configured.", 500

            if hmac.compare_digest(password, admin_password):
                session["is_admin"] = True
                return redirect(url_for("admin_messages"))

            return render_template(
                "admin_login.html",
                error="Incorrect password. Please try again."
            ), 401

        return render_template("admin_login.html")

    @app.route("/admin/messages")
    def admin_messages():
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))

        with get_connection() as connection:
            messages = connection.execute(
                """
                SELECT id, name, email, subject, message, created_at
                FROM contact_messages
                ORDER BY id DESC
                """
            ).fetchall()

        return render_template("messages.html", messages=messages)

    @app.route("/admin/logout", methods=["POST"])
    def admin_logout():
        session.pop("is_admin", None)
        return redirect(url_for("admin_login"))

    return app