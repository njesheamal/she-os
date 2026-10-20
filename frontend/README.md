# SHÉ OS frontend

The orrery is the SvelteKit landing page at `/`. The legacy `/orrery` route redirects to `/`.
The frontend lives under `frontend/` and talks to the FastAPI backend through a Vite dev proxy, avoiding browser CORS errors during local development.

## Run it locally

1. Start the backend on port `8000`.
2. In `frontend/`, run:

```sh
npm install
npm run dev
```

3. Open the forwarded `5173` URL shown in the terminal.

The browser requests `/api/...` through the typed `src/lib/api.ts` client. Vite proxies those requests to `http://localhost:8000` in dev, keeping browser requests same-origin while the backend remains unchanged.

## Notes

- Published field notes are requested via `/api/field-notes?status=published`; if that endpoint is unavailable, the sky keeps a quiet empty constellation.
- No backend CORS configuration changes are required.
- The app is built for local development only; production deployment can be handled separately.
