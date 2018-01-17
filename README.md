# blockchain_vaccination_records

## Docker

Before you can use the demo compose file of this project, you need to build the base image containing all project dependency.
Run `docker build -f base.Dockerfile -t blockchain_base .` in the project root directory to build the base image.

After building the base image you can run `docker-compose up` to start the demo network.

### Testing

- run tests with `pytest` in root directory of the repo
- in order to get the test coverage run: `py.test --cov blockchain tests --cov-report=html`
