# TODO: Docker Setup for Capstone-Lumina

- [x] Update docker-compose.yml to add volumes for syncing code, environment variables, and frontend depends_on backend.
- [x] Update backend/Dockerfile to copy only app directory instead of entire backend directory.
- [x] Update backend/app/api/query.py to add a simple /api/ask POST endpoint for AI model demonstration.
- [ ] Test the setup by running docker-compose build --no-cache and docker-compose up.
- [ ] Verify backend routes work (health check, docs, upload).
- [ ] Verify frontend runs and can communicate with backend.
- [ ] Test live AI model demonstration via /api/ask endpoint.
