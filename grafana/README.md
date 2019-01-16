## Grafana Example

_This example adapted from [stefanwalther/docker-grafana](https://github.com/stefanwalther/docker-grafana)_

Configuration can be modified through `config.env` and `./config/grafana.ini`
Dashboards and dataset definitions can be declared in `./config`

To run:

 - run: `docker-compose up` in this directory.
 - point browser @ [http://localhost:3000](http://localhost:3000)
 - Sign in using the credentials found in config.env under `GF_SECURITY`
 - Attach your first data source and enjoy!

* Note. If you're familiar with Redash, Grafana may be unintuitive as you start with a visual element and then add a query to it. You can take a look at the [documentation](http://docs.grafana.org/features/datasources/postgres/).

Volumes are not mounted, so doing a `docker-compose down` will remove any saved state in Grafana, not declared in `config/datasets` or `config/dashboards`