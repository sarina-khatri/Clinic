#createadmin.py
from Admin import create_app, db
from Admin.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin = User(
        username="admin2",
        email="admin2@gmail.com",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin created successfully!")
