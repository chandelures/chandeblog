from fabric import Connection, task


@task
def deploy(ctx):
    HOST = input("host: ")
    conn = Connection(HOST)
    backend_dir = '/www/chandeblog'
    frontend_dir = '/www/chandeblog-frontend'

    with conn.cd('{}'.format(backend_dir)):
        conn.run("""
            git pull &&
            venv/bin/pip install -r requirements.txt &&
            venv/bin/python manage.py migrate
        """)

    with conn.cd('{}'.format(frontend_dir)):
        conn.run("""
            git pull &&
            npm install &&
            npm run build
        """)

    conn.sudo('supervisorctl restart gunicorn nuxt')
    return ctx
