# Uni Arena Frontend

Vue 3 + TypeScript frontend for the Uni Arena Sports Management System.

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Next generation frontend tooling
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management for Vue
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Heroicons** - Beautiful hand-crafted SVG icons

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Variables

Create a `.env` file in the frontend directory (optional):

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at http://localhost:5173

### 4. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── assets/          # Static assets (CSS, images)
│   ├── components/      # Reusable Vue components
│   ├── layouts/         # Layout components
│   ├── router/          # Vue Router configuration
│   ├── services/        # API service layer
│   ├── stores/          # Pinia stores (state management)
│   ├── types/           # TypeScript type definitions
│   ├── views/           # Page components
│   │   ├── admin/       # Admin views
│   │   ├── auth/        # Authentication views
│   │   ├── coach/       # Coach views
│   │   ├── organizer/   # Organizer views
│   │   ├── player/      # Player views
│   │   └── viewer/      # Public/Viewer views
│   ├── App.vue          # Root component
│   └── main.ts          # Application entry point
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Features

### Authentication
- User login and registration
- JWT token management
- Protected routes based on user roles
- Automatic token refresh handling

### Role-Based Access
- **Admin**: Manage institutions and users
- **Organizer**: Manage sports, teams, tournaments, venues, schedules
- **Coach**: Manage teams and line-ups
- **Player**: View profile, matches, and statistics
- **Viewer**: Public access to matches, tournaments, and live scores

### Key Features
- Live score updates with real-time refresh
- Match scheduling and management
- Tournament management
- Team and player management
- Statistics tracking
- Notifications system
- Responsive design

## API Integration

The frontend communicates with the backend API through the `api.ts` service file. All API calls are centralized and include:

- Automatic token injection
- Error handling
- Response interceptors
- Type-safe request/response handling

## Development

### Adding New Views

1. Create a new Vue component in the appropriate `views/` subdirectory
2. Add the route in `src/router/index.ts`
3. Update navigation in the corresponding layout component

### Adding New API Endpoints

1. Add the method to `src/services/api.ts`
2. Use the method in your components/stores
3. Update TypeScript types in `src/types/index.ts` if needed

## Build & Deploy

The production build creates optimized static files in the `dist/` directory that can be served by any static file server.

```bash
npm run build
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Part of the Uni Arena Sports Management System.
