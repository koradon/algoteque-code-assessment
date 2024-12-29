Solution to the assessment from the pdf file

I am using `uv` to run the application and tests. Project is configured to use `python 3.12`.
Application is written in `fastapi` framework.

I am using Makefile with some standard commands to run the application and tests. This ensures me that every developer is using the same setup on local environment.
Preferably this application should be run in docker container using docker compose file.

To run tests:
```bash
make test
```

To run tests with coverage:
```bash
make test-cov
```

To run application 
locally:
```bash
make run
```
or in docker:
```bash
docker compose up web
```

File with providers data is located in `data/providers.json` and is loaded on application startup.
Data from that file is stored in application context and is available to all services and is loaded only once.

URL for the quote calculation endpoint is `http://localhost:8000/quote`.
Online docs are available at `http://localhost:8000/docs`.
I added insomnia file with example request to the project.

