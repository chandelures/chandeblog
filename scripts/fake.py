import random
from flask import Flask
import faker
from app import create_app
from app.models import db
from app.models.auth import User
from app.models.blog import Article, Category

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


def subsection() -> str:
    return "### {}\n\n".format(zh_fake.sentence().rstrip(".")) + \
        "{}\n\n".format(zh_fake.paragraph(10))*3


def abstract() -> str:
    return "{}\n\n".format(zh_fake.paragraph(8)) * 2


def content() -> str:
    return abstract() + section()*2 + subsection()*2 + \
        section() + subsection()*3


def get_admin(app: Flask) -> User:
    with app.app_context():
        return User.query.filter_by(superuser=True).first()


def get_random_category(app: Flask) -> Category:
    with app.app_context():
        return random.choice(Category.query.all())


def clean_database(app: Flask) -> None:
    print("clean database...")
    with app.app_context():
        db.drop_all()
        db.create_all()


def create_superuser(app: Flask) -> None:
    print("create superuser...")
    with app.app_context():
        admin = User("admin", "admin@example.org", stuff=True, superuser=True)
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()


def create_users(app: Flask) -> None:
    print("create some fake users...")
    with app.app_context():
        for _ in range(10):
            username = name()
            user = User(username, "{}@{}.org".format(username, word()))
            user.set_password("password")
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
        for _ in range(100):
            article = Article(title(),
                              abstract(),
                              content(),
                              author=get_admin(app).uid,
                              category=get_random_category(app).slug)
            db.session.add(article)
            db.session.commit()


def main() -> None:
    app = create_app()
    clean_database(app)
    create_superuser(app)
    create_users(app)
    create_categories(app)
    create_articles(app)
    print("done")


if __name__ == "__main__":
    main()
