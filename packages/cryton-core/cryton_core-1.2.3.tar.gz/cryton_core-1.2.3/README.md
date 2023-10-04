![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-core/badges/master/coverage.svg)

[//]: # (TODO: add badges for python versions, black, pylint, flake8, unit tests, integration tests)

# Cryton Core
Cryton Core is the center point of the Cryton toolset. It is used for:
- Creating, planning, and scheduling attack scenarios
- Generating reports from attack scenarios
- Controlling Workers and scenarios execution

Cryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that **only 
the latest version is supported** and issues regarding different OS or distributions may **not** be resolved.

For more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/core/).

## Quick-start
To be able to execute attack scenarios, you also need to install **[Cryton Worker](https://gitlab.ics.muni.cz/cryton/cryton-worker)** 
and **[Cryton CLI](https://gitlab.ics.muni.cz/cryton/cryton-cli)** packages.  
Optionally you can install [Cryton Frontend](https://gitlab.ics.muni.cz/cryton/cryton-frontend) for a non-command line experience.

Make sure Git, Docker, and Docker Compose plugin are installed:
- [Git](https://git-scm.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Optionally, check out these Docker [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).

The following script clones the repository and runs the Docker Compose configuration. The compose file contains the necessary prerequisites
(Postgres, PgBouncer, RabbitMQ), Cryton Core itself (listener and REST API), and a proxy that allows access to the Cryton Core's REST API
at http://0.0.0.0:8000/.
```shell
git clone https://gitlab.ics.muni.cz/cryton/cryton-core.git
cd cryton-core
sed -i "s|CRYTON_CORE_RABBIT_HOST=127.0.0.1|CRYTON_CORE_RABBIT_HOST=cryton-rabbit|" .env
sed -i "s|CRYTON_CORE_DB_HOST=127.0.0.1|CRYTON_CORE_DB_HOST=cryton-pgbouncer|" .env
sed -i "s|CRYTON_CORE_API_USE_STATIC_FILES=false|CRYTON_CORE_API_USE_STATIC_FILES=true|" .env
docker compose up -d
```

For more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/core/).

## Contributing
Contributions are welcome. Please **contribute to the [project mirror](https://gitlab.com/cryton-toolset/cryton-core)** on gitlab.com.
For more information see the [contribution page](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/contribution-guide/).
