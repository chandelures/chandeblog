from fabric import Connection, task

BACKEND_DIR = '/www/chandeblog'
FRONTEND_DIR = '/www/chandeblog-frontend'


def connect():
    HOST = input("host: ")
    conn = Connection(HOST)
    return conn


def backend(conn):
    with conn.cd('{}'.format(BACKEND_DIR)):
        conn.run("""
            git pull &&
            venv/bin/pip install -r requirements.txt &&
            venv/bin/python manage.py migrate
        """)
    conn.sudo('supervisorctl restart gunicorn')


def frontend(conn):
    with conn.cd('{}'.format(FRONTEND_DIR)):
        conn.run("""
            git pull &&
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
