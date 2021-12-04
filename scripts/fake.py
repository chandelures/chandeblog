from flask import Flask
import faker
from app import create_app
from app.models import db
from app.models.auth import User
from app.models.blog import Category

en_fake = faker.Faker("en_US")
zh_fake = faker.Faker("zh_CN")


def word() -> str:
    return en_fake.word()


def name() -> str:
    return en_fake.name().replace(" ", "")


def title() -> str:
    return zh_fake.sentence().rstrip(".")


def section() -> str:
    return "## {}\n\n".format(zh_fake.sentence().rstrip(".")) + \
        "{}\n\n".format(zh_fake.paragraph(10))*2


def clean_database(app: Flask) -> None:
    print("clean database...")
    with app.app_context():
        db.drop_all()
        db.create_all()


def create_superuser(app: Flask) -> None:
    print("create superuser...")
    with app.app_context():
        admin = User("admin", "admin", "admin@example.org",
                     stuff=True, superuser=True)
        db.session.add(admin)
        db.session.commit()


def create_users(app: Flask) -> None:
    print("create some fake users...")
    with app.app_context():
        for _ in range(10):
            username = name()
            user = User(username, "password",
                        "{}@{}.org".format(username, word()))
            db.session.add(user)
        db.session.commit()


def create_categories(app: Flask) -> None:
    print("create some fake categories...")
    with app.app_context():
        categorie_names = ["python", "php", "javascript", "c++", "world"]
        for name in categorie_names:
            category = Category(name)
            db.session.add(category)
        db.session.commit()


def create_articles(app: Flask) -> None:
    print("create some fake articles")
    with app.app_context():


def main() -> None:
    app = create_app()
    clean_database(app)
    create_superuser(app)
    create_users(app)
    print("done")


if __name__ == "__main__":
    main()
