from pathlib import Path
from flask import Flask
import faker
from app import create_app
from app.models import db
from app.models.auth import User
from app.models.blog import Post

en_fake = faker.Faker("en_US")
zh_fake = faker.Faker("zh_CN")

CURRENT_DIR = Path(__file__).resolve().parent


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


def description() -> str:
    return "{}\n\n".format(zh_fake.paragraph(8)) * 2


def content() -> str:
    return description() + section()*2 + subsection()*2 + \
        section() + subsection()*3


def get_admin(app: Flask) -> User:
    with app.app_context():
        return User.query.filter_by(superuser=True).first()


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


def create_posts(app: Flask) -> None:
    print("create some fake posts")
    with app.app_context():
        for _ in range(100):
            post = Post(
                title(),
                description(),
                content(),
            )
            db.session.add(post)
            db.session.commit()


def create_sample_posts(app: Flask) -> None:
    print("create a sample post")
    with app.app_context():
        with open("{}/sample.md".format(CURRENT_DIR), "r") as f:
            content = f.read()
        post = Post(
            "Markdown示例",
            description(),
            content,
        )
        db.session.add(post)
        db.session.commit()


def main() -> None:
    app = create_app()
    clean_database(app)
    create_superuser(app)
    create_users(app)
    create_posts(app)
    create_sample_posts(app)
    print("done")


if __name__ == "__main__":
    main()
