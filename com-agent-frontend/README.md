# Communication Assistant Frontend

React + Vite frontend for the Communication Assistant.

## Setup

```bash
npm install
```

Create `.env`:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

## Run

```bash
npm run dev
```

The frontend calls `POST /chat` on `VITE_API_URL`. If `VITE_API_URL` is not set, it falls back to `/api`.

## Build

```bash
npm run build
```
