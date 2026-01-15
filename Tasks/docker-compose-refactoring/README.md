# Containerization of application with local compose stack

## Context

The development team has been working on a new application that is ready to be deployed to a server. The application consists of a Node.js-based backend (in the `backend` folder) and a React-based frontend (in the `ui` folder). The backend persists data in a PostgreSQL database.

**Your first task is to containerize these two applications**, creating a `Dockerfile` / `Containerfile` for the frontend and backend. You are _not_ tied to Docker (Desktop) for this task, you can use any alternative containerization technology that you are comfortable with (e.g. Podman (Desktop) or Rancher Desktop), as long as it creates OCI-compatible images.

In the _production_ environment, the application could run in any kind of container orchestration system (e.g. Kubernetes). To make the _local_ deployment experience as similar as possible to the production environment, **your second task is to build a (Docker) _compose stack_**, allowing the developers to easily build and run the entire application locally with a single command. There is already a `compose.yml` file in the repository, but it is incomplete, because you still need to add the services for the frontend and backend.

## Hints

- **If** you have a Node.js runtime installed on your machine, and if you want to try out the application (before containerizing it):
  - run `docker compose up -d`, to start the PostgreSQL database
  - change into the `backend` directory, install the dependencies with `npm` and run `npm start`
  - change into the `ui` directory, install the dependencies with `npm` and run `npm start`, then click on the link that is printed to the console, to open the frontend in your browser
- You might need to change small bits of the backend code to improve its configurability via environment variables
- Make sure that the `compose.yaml` file configures _building_ the images, too, not just _running_ them
- You should first focus on getting the containerization and compose stack to work in its most basic form, using minimal effort. Only start optimizing once your solution works. Bonus points include:
  - Write a short documentation (e.g. in `react-nodejs-postgres/README.md`) for the development team, explaining how to build and run the application with the compose stack
  - Improve the build speed of the image, especially when developers frequently change the code
  - Have the backend wait for the PostgreSQL database to be _fully ready_, before the backend starts
