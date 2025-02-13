from turtle import pu
from fabric import Connection
from invoke import task
from colorama import Fore, init, Style

GIT_REPO = "git@github.com:fgaudin/GisDemo.git"
BASE_DIR = "/var/www"

init()


def print_task(text):
    print(Fore.CYAN + text)
    print(Style.RESET_ALL)


def print_success(text):
    print(Fore.GREEN + text)
    print(Style.RESET_ALL)


@task
def install_dependencies(c):
    print_task("Installing dependencies...")
    cnx = Connection(c.host)

    cnx.run("sudo apt update")
    cnx.run(
        "sudo apt install -y python3-virtualenv postgis postgresql-server-dev-16 nginx"
    )


@task
def pull_code(c):
    cnx = Connection(c.host)

    print_task("Cleaning up previous code...")
    cnx.sudo(f"rm -rf /var/www/releases/{c.sha}")

    print_task(f"Pulling code for {c.sha}...")
    cnx.sudo(f"mkdir -p {BASE_DIR}/releases")
    cnx.sudo(f"chown -R {c.user}:{c.user} {BASE_DIR}/releases")
    cnx.run(f"mkdir -p {BASE_DIR}/releases/{c.sha}")
    with cnx.cd(f"{BASE_DIR}/releases/{c.sha}"):
        cnx.run(f"git init")
        cnx.run(f"git remote add origin {GIT_REPO}")
        cnx.run(f"git fetch origin {c.sha}")
        cnx.run("git reset --hard FETCH_HEAD")


@task
def setup_db(c):
    print_task("Setting up database...")

    cnx = Connection(c.host)
    result = cnx.sudo(f"createdb {c.db_name}", user="postgres", warn=True)
    if result.ok:
        print_task("Creating DB user...")
        cnx.sudo(f"createuser --superuser {c.db_user}", user="postgres")
        cnx.sudo(
            f"psql -c \"ALTER USER {c.db_user} WITH PASSWORD '{c.db_password}'\"",
            user="postgres",
        )
        cnx.sudo(f'psql -c "ALTER USER {c.db_user} CREATEDB"', user="postgres")
        cnx.sudo(
            f"psql -c \"ALTER ROLE {c.db_user} SET client_encoding TO 'utf8'\"",
            user="postgres",
        )
        cnx.sudo(
            f"psql -c \"ALTER ROLE {c.db_user} SET default_transaction_isolation TO 'read committed'\"",
            user="postgres",
        )
        cnx.sudo(
            f"psql -c \"ALTER ROLE {c.db_user} SET timezone TO 'UTC'\"",
            user="postgres",
        )
        cnx.sudo(
            f'psql -c "GRANT ALL PRIVILEGES ON DATABASE {c.db_name} TO {c.db_user}"',
            user="postgres",
        )
        cnx.sudo(
            f'psql -c "CREATE EXTENSION postgis"',
            user="postgres",
        )
    else:
        print_task("Database seems to already exist")


@task
def fix_env(c):
    print_task("Fixing environment variables...")

    cnx = Connection(c.host)

    cnx.put("./install_files/bash_non_interactive", ".bash_non_interactive")
    cnx.run(
        r"""grep -qF bash_non_interactive .bashrc || sed -i '1s/^/\.\ \~\/\.bash_non_interactive\n/' .bashrc"""
    )


@task(setup_db, fix_env)
def install_backend(c):
    print_task("Installing backend...")

    cnx = Connection(c.host)

    print_task("Installing or upgrading uv")
    result = cnx.run("uv self update", warn=True)
    if result.ok:
        print_success("uv is up to date")
    else:
        cnx.run("curl -LsSf https://astral.sh/uv/install.sh | sh")

    print_task("Setting up virtual env...")

    cnx.put("./backend/Vogel/.env", f"{BASE_DIR}/releases/{c.sha}/backend/Vogel/.env")

    with cnx.cd(f"{BASE_DIR}/releases/{c.sha}/backend/Vogel"):
        cnx.run(rf"""sed -i~ '/^SECRET_KEY=/s/=.*/={c.secret_key}/' .env""")
        cnx.run(rf"""sed -i~ '/^ALLOWED_HOSTS=/s/=.*/={c.domain}/' .env""")
        cnx.run(
            rf"""sed -i~ '/^DATABASE_URL=/s/=.*/=postgis:\/\/{c.db_user}:{c.db_password}@127.0.0.1:5432\/{c.db_name}/' .env"""
        )

        cnx.run("uv sync")
        cnx.run("uv run ./manage.py collectstatic --noinput")
        cnx.run("uv run ./manage.py migrate")

    print_task("Setting up systemd service...")
    cnx.put("./install_files/gunicorn.socket", "./gunicorn.socket")
    cnx.put("./install_files/gunicorn.service", "./gunicorn.service")
    cnx.sudo("cp ./gunicorn.socket /etc/systemd/system/gunicorn.socket")
    cnx.sudo("cp ./gunicorn.service /etc/systemd/system/gunicorn.service")
    cnx.sudo("systemctl start gunicorn.socket")
    cnx.sudo("systemctl enable gunicorn.socket")


@task
def install_frontend(c):
    print_task("Installing frontend...")

    cnx = Connection(c.host)

    print_task("Installing nvm if needed")

    result = cnx.run("nvm version", warn=True)
    if not result.ok:
        cnx.run(
            "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash"
        )
        cnx.run("nvm install node")

    cnx.sudo(f"rm -rf {BASE_DIR}/releases/{c.sha}/frontend/Vogel/dist")
    with cnx.cd(f"{BASE_DIR}/releases/{c.sha}/frontend/Vogel"):
        cnx.run("npm install")
        cnx.run("npm run build")
    cnx.sudo(
        f"chown -R www-data:www-data {BASE_DIR}/releases/{c.sha}/frontend/Vogel/dist"
    )


@task
def install_nginx(c):
    print_task("Installing Nginx...")
    cnx = Connection(c.host)
    cnx.run("mkdir -p ./tmp")
    cnx.put("./install_files/nginx_site", "./tmp/nginx_site")
    cnx.sudo("mv ./tmp/nginx_site /etc/nginx/sites-available/vogel")
    cnx.sudo("rm -f /etc/nginx/sites-enabled/default")
    cnx.sudo("ln -sf /etc/nginx/sites-available/vogel /etc/nginx/sites-enabled/vogel")


@task
def activate(c):
    print_task("Activating new release...")
    cnx = Connection(c.host)
    cnx.sudo(f"rm -f {BASE_DIR}/current")
    cnx.sudo(f"ln -s {BASE_DIR}/releases/{c.sha} {BASE_DIR}/current")
    cnx.sudo("systemctl restart nginx")


DEPLOY_TASKS = [
    install_dependencies,
    pull_code,
    install_backend,
    install_frontend,
    install_nginx,
    activate,
]


@task(*DEPLOY_TASKS)
def start_deploy(c):
    print_success(f"Deployed: {c.sha}")


@task(post=[start_deploy])
def deploy(c, sha):
    c.update({"sha": sha})


@task
def check_env(c):
    cnx = Connection(c.host, inline_ssh_env=True)
    cnx.run(
        "env",
    )
