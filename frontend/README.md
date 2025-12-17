# Clustering Platform Frontend

React + TypeScript frontend for the Clustering Platform web application.

## Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Environment** (Optional)
   ```bash
   cp .env.example .env
   # Edit .env if backend is running on different port
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```

The frontend will start on http://localhost:5173 (or next available port)

## Features

### AI-Assisted Mode
- Drag-and-drop file upload
- Device management (add/delete devices)
- Manual device sync
- Automatic clustering on uploaded files

### Advanced Mode
- Data file browser with search and filters
- Jupyter notebook launcher
- Pre-populated analysis code

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AIMode/          # AI-Assisted Mode components
│   │   ├── AdvancedMode/     # Advanced Mode components
│   │   └── common/          # Shared components and styles
│   ├── services/
│   │   └── api.ts           # API client
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── package.json
└── vite.config.ts
```

## Development

- **Dev Server**: `npm run dev`
- **Build**: `npm run build`
- **Preview**: `npm run preview`

## Backend Connection

Make sure the backend is running on http://localhost:8000 (or update VITE_API_URL in .env)
