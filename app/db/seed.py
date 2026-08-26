from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project


def seed():
    db = SessionLocal()

    try:
        admin = User(
            firstname="admin",
            lastname="User",
            email="admin@example.com",
            password_hash="admin123",
            role="admin",
            is_active=True
        )

        manager = User(
            firstname="Manager",
            lastname="User",
            email="manager@example.com",
            password_hash="manager123",
            role="manager",
            is_active=True
        )

        project1 = Project(
            name="website Development",
            client_name="ABC Company",
            description="Company website development project",
            status="active"
        )

        project2 = Project(
            name="Mobile App",
            client_name="XYZ Company",
            description="Mobile application development project",
            status="active"
        )

        db.add_all(
            [
                admin,
                manager,
                project1,
                project2
            ]
        )
        db.commit()

        print("Admin , Manager and Projects created successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed()