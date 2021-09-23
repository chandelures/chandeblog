from fabric import Connection, task

BACKEND_DIR = '/www/chandeblog'
FRONTEND_DIR = '/www/chandeblog-frontend'


def connect() -> Connection:
    HOST = input("host: ")
    conn = Connection(HOST)
    return conn


def backend(conn) -> None:
    with conn.cd('{}'.format(BACKEND_DIR)):
        conn.run("""
            git pull &&
            venv/bin/pip install -r requirements.txt &&
            venv/bin/python manage.py migrate
        """)
    conn.sudo('supervisorctl restart gunicorn')


def frontend(conn) -> None:
    with conn.cd('{}'.format(BACKEND_DIR)):
        conn.run("""
            git pull &&
            git submodule update
        """)
    with conn.cd('{}/chandeblog-frontend'.format(BACKEND_DIR)):
        conn.run("""
            npm install &&
            npm run build
        """)
    conn.sudo('supervisorctl restart nuxt')


@task
def deploy(ctx):
    conn = connect()
    backend(conn)
    frontend(conn)
    return ctx


@task
def deploy_back(ctx):
    conn = connect()
    backend(conn)
    return ctx


@task
def deploy_front(ctx):
    conn = connect()
    frontend(conn)
    return ctx
