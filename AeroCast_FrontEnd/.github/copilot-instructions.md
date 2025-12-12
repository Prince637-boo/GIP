# AeroCast Frontend - AI Coding Agent Instructions

This document provides comprehensive guidance for AI coding agents working on the AeroCast weather and baggage tracking application frontend.

## 🎯 Project Overview

**AeroCast** is a weather forecasting and baggage tracking application for airports, built with React 19, TypeScript, and modern tooling. The application features:

- Real-time weather predictions for airports
- Baggage tracking with QR codes
- User authentication with JWT tokens
- Dashboard with role-based access
- B2B subscription management

## 🏗️ Architecture Principles

### Tech Stack

- **React 19.2.0** + **TypeScript 5.9.3** - UI framework with strict typing
- **Vite 7.2.6** - Build tool with HMR
- **React Router 7.10.0** - Client-side routing
- **TanStack Query 5.90.11** - Server state management with caching
- **Zustand 5.0.9** - Client state management (auth)
- **Valibot 1.2.0** + **React Hook Form 7.68.0** - Form validation
- **Axios** - HTTP client with interceptors
- **Shadcn/UI** - Component library (new-york style)
- **Tailwind CSS 4.1.17** - Styling with custom weather theme

### Key Design Patterns

1. **Service Layer Pattern**: All API calls go through static service classes with TanStack Query keys
2. **HOC for Route Protection**: `ProtectedRoute` wrapper for authenticated routes
3. **Mock-First Development**: Use mock APIs during development, easy swap to real endpoints
4. **Schema-Driven Validation**: Valibot schemas define both validation and TypeScript types
5. **Centralized Auth**: Zustand store with sessionStorage persistence

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── dashboard/      # Dashboard-specific (Sidebar, Header, config)
│   ├── baggage/        # Baggage tracking (QRCard, timeline)
│   └── ui/             # Shadcn components (button, input, card, etc.)
├── layouts/            # Page layouts (RootLayout, DashboardLayout)
├── pages/              # Route pages (HomePage, LoginPage, DashboardPage, etc.)
├── stores/             # Zustand stores (useAuth.ts)
├── service/            # API service layer
│   ├── http/           # Axios instance with interceptors
│   └── *.service.ts    # Service classes (auth, meteo, bagages, etc.)
├── lib/                # Utilities (auth helpers, routerGuard, apiMock)
├── schemas/            # Valibot validation schemas
├── types/              # TypeScript type definitions
└── styles/             # Global styles (globals.css)
```

## 🔐 Authentication Flow

### How It Works

1. **Login/Register**: User submits credentials via forms with Valibot validation
2. **Mock API**: `apiMock.ts` simulates backend responses (returns JWT)
3. **Token Storage**: JWT stored in `sessionStorage` (NOT localStorage - security requirement)
4. **Zustand Store**: `useAuth.ts` manages auth state with persistence
5. **Axios Interceptors**: Auto-inject token, check expiration before requests
6. **Route Protection**: `ProtectedRoute` HOC wraps dashboard routes

### Mock Credentials

For development, use these credentials:

- **Email**: `admin@aerocast.com`
- **Password**: `password123`

### Token Management

```typescript
// Token helpers in src/lib/auth.ts
decodeToken(token: string): TokenPayload | null
isTokenExpired(token: string): boolean
checkAuthToken(): boolean

// Zustand store usage
const { user, token, setAuth, logout, checkAuth } = useAuth()
```

### Key Implementation Details

- Tokens expire after 24 hours
- Expiration checked before EVERY request in axios interceptor
- Auto-logout with toast notification on expiration
- Redirect to `/login?redirectTo=/dashboard` for protected routes

## 🛠️ Development Workflows

### Adding a New Service

1. **Create service file**: `src/service/[name].service.ts`
2. **Define query keys**: Static `keys` object for TanStack Query
3. **Implement methods**: Static methods using `axios` instance
4. **Export service**: Default export of the service class

**Template:**

```typescript
import { axiosInstance } from "./http/instance.http";

export class MyService {
  static keys = {
    all: ["myService"] as const,
    list: () => [...MyService.keys.all, "list"] as const,
    detail: (id: string) => [...MyService.keys.all, "detail", id] as const,
  };

  static async getList() {
    const { data } = await axiosInstance.get("/api/my-endpoint");
    return data;
  }

  static async getDetail(id: string) {
    const { data } = await axiosInstance.get(`/api/my-endpoint/${id}`);
    return data;
  }
}

export default MyService;
```

### Adding a New Form with Validation

1. **Define schema**: Create Valibot schema in `src/schemas/`
2. **Extract types**: Use `InferInput<typeof schema>` for form types
3. **Create form**: Use `react-hook-form` with `@hookform/resolvers/valibot`
4. **Handle submission**: Call service method, update state, show toast

**Example:**

```typescript
// src/schemas/contact.schemas.ts
import * as v from "valibot";

export const contactSchema = v.object({
  email: v.pipe(v.string(), v.email("Email invalide")),
  message: v.pipe(v.string(), v.minLength(10, "Minimum 10 caractères")),
});

export type ContactInput = v.InferInput<typeof contactSchema>;

// Component
import { useForm } from "react-hook-form";
import { valibotResolver } from "@hookform/resolvers/valibot";

const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm<ContactInput>({
  resolver: valibotResolver(contactSchema),
});
```

### Adding a New Protected Route

1. **Create page component**: `src/pages/[name]/[name]Page.tsx`
2. **Import ProtectedRoute**: From `src/lib/routerGuard.tsx`
3. **Wrap in router**: Add to dashboard routes in `App.tsx`

**Example:**

```tsx
// In App.tsx
import { ProtectedRoute } from '@/lib/routerGuard'
import MyPage from '@/pages/my/MyPage'

// Inside RouterProvider routes
{
  path: '/dashboard/my-page',
  element: (
    <ProtectedRoute>
      <DashboardLayout>
        <MyPage />
      </DashboardLayout>
    </ProtectedRoute>
  ),
}
```

### Adding Items to Dashboard Sidebar

Edit `src/components/dashboard/sidebar.config.ts`:

```typescript
export const DASHBOARD_MENU: DashboardMenuItem[] = [
  {
    label: "Mon Item",
    href: "/dashboard/my-item",
    icon: "tabler:my-icon", // Iconify icon name
    badge: "NEW", // Optional
    items: [
      // Optional sub-items
      { label: "Sub Item", href: "/dashboard/my-item/sub" },
    ],
  },
];
```

## 🎨 UI & Styling Guidelines

### Tailwind Theme

Custom weather-themed colors defined in `src/styles/globals.css`:

```css
@theme {
  --color-primary: oklch(0.62 0.19 245); /* Blue sky */
  --color-secondary: oklch(0.7 0.15 250);
  --color-background: oklch(0.97 0.01 247); /* Light sky */
  --color-card: oklch(1 0 0);
  /* ... more theme colors */
}
```

### Using Shadcn Components

Components are in `src/components/ui/`. Import and use:

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <Button variant="default">Click me</Button>
  </CardContent>
</Card>;
```

### Using Icons

Iconify icons via CSS classes (configured in globals.css):

```tsx
<span className="i-tabler-cloud text-xl text-primary" />
<span className="i-tabler-plane text-2xl text-secondary" />
```

Find icons at [Iconify](https://icon-sets.iconify.design/) (use `tabler` set).

## 🔄 State Management

### When to Use What

- **Zustand** (`src/stores/`): Global client state (auth, user preferences)
- **TanStack Query**: Server state (API data, caching, loading states)
- **React State** (`useState`): Local component state

### TanStack Query Pattern

```tsx
import { useQuery } from "@tanstack/react-query";
import MeteoService from "@/service/meteo.service";

function MyComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: MeteoService.keys.predictions("CDG"),
    queryFn: () => MeteoService.getPredictions("CDG"),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error.message}</div>;

  return <div>{data.temperature}°C</div>;
}
```

## 🚨 Common Pitfalls & Solutions

### Problem: Vite doesn't recognize `@/` path alias

**Solution**: Ensure both configs have the alias:

```typescript
// tsconfig.json & tsconfig.app.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}

// vite.config.ts
import path from 'path'
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Problem: localStorage security errors with Zustand

**Solution**: Use `sessionStorage` instead:

```typescript
// In Zustand persist config
storage: createJSONStorage(() => sessionStorage); // NOT localStorage
```

### Problem: Axios 401 after token expiration

**Solution**: Already handled in `src/service/http/instance.http.ts` interceptor. It:

1. Checks token expiration before request
2. Auto-logouts and redirects to login
3. Shows toast notification

### Problem: TypeScript errors with Valibot schemas

**Solution**: Always use `InferInput` for form types:

```typescript
import * as v from "valibot";
export type MyFormData = v.InferInput<typeof mySchema>; // Correct
```

## 📝 Code Style & Conventions

### Naming Conventions

- **Files**: PascalCase for components (`MyComponent.tsx`), camelCase for utilities (`myUtil.ts`)
- **Types**: PascalCase (`User`, `AuthResponse`)
- **Functions**: camelCase (`handleSubmit`, `fetchData`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`, `DASHBOARD_MENU`)
- **Service Classes**: PascalCase ending in `Service` (`MeteoService`, `BagagesService`)

### Import Order

1. React & external libraries
2. Internal services & stores
3. Components (UI first, then custom)
4. Types & schemas
5. Styles & assets

### Error Messages

Use French for user-facing messages:

```typescript
toast.error("Erreur lors de la connexion");
toast.success("Connexion réussie");
```

### Component Structure

```tsx
// 1. Imports
import { useState } from "react";
import { Button } from "@/components/ui/button";
import type { User } from "@/types";

// 2. Types (if not in separate file)
interface MyComponentProps {
  user: User;
  onSave: () => void;
}

// 3. Component
export function MyComponent({ user, onSave }: MyComponentProps) {
  // 3a. Hooks
  const [state, setState] = useState("");

  // 3b. Handlers
  const handleClick = () => {
    /* ... */
  };

  // 3c. Effects
  useEffect(() => {
    /* ... */
  }, []);

  // 3d. Render
  return <div>...</div>;
}

// 4. Default export (optional)
export default MyComponent;
```

## 🧪 Testing Approach

### Current State

Tests are not yet implemented. When adding tests:

1. Use **Vitest** (already configured with Vite)
2. Use **React Testing Library** for component tests
3. Mock service calls with **MSW** (Mock Service Worker)
4. Test user flows, not implementation details

## 🚀 Deployment Notes

### Environment Variables

Create `.env` file (see `.env.example`):

```bash
VITE_API_BASE_URL=http://localhost:3000
VITE_WS_URL=ws://localhost:3000
```

### Build Command

```bash
pnpm build
```

Outputs to `dist/` directory. Serve with any static host (Vercel, Netlify, etc.).

## 📚 Key Files Reference

| File                                         | Purpose               | When to Edit         |
| -------------------------------------------- | --------------------- | -------------------- |
| `src/App.tsx`                                | Router configuration  | Adding new routes    |
| `src/stores/useAuth.ts`                      | Auth state            | Modifying auth logic |
| `src/service/http/instance.http.ts`          | Axios config          | Adding interceptors  |
| `src/lib/apiMock.ts`                         | Mock API responses    | Development testing  |
| `src/types/index.ts`                         | Type definitions      | Adding new entities  |
| `src/schemas/`                               | Validation schemas    | Form validation      |
| `src/components/dashboard/sidebar.config.ts` | Sidebar menu          | Adding menu items    |
| `src/styles/globals.css`                     | Theme & global styles | Theming changes      |
| `vite.config.ts`                             | Build configuration   | Aliases, plugins     |

## 🤝 Collaboration Guidelines

### Before Starting Work

1. Check existing services and components - avoid duplication
2. Follow established patterns (service layer, validation schemas)
3. Use mock API for development, comment where real API will go

### Code Review Checklist

- [ ] TypeScript strict mode passes (`tsc -b`)
- [ ] Valibot schemas for all forms
- [ ] Service methods use TanStack Query keys
- [ ] Protected routes wrapped in `ProtectedRoute`
- [ ] French error messages for users
- [ ] Icons from Iconify (tabler set)
- [ ] No `any` types (use `unknown` if necessary)
- [ ] No direct `localStorage` access (use `sessionStorage` via Zustand)

## 🔗 Useful Resources

- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Valibot Docs](https://valibot.dev/)
- [React Hook Form](https://react-hook-form.com/)
- [Shadcn/UI](https://ui.shadcn.com/)
- [Iconify Icons](https://icon-sets.iconify.design/)
- [Zustand Docs](https://zustand-demo.pmnd.rs/)

---

**Last Updated**: 2025-01-XX  
**Maintainer**: AeroCast Team
