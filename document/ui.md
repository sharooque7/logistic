# 📝 Route Intelligence React App – Documentation

## **Overview**

This React application provides a dashboard for delivery route comparison. It includes:

- **Login functionality** (mock)
- **Dashboard with route statistics**
- **Route selection and metrics**
- **Protected routes using React Router**
- **Login/logout with localStorage persistence**

The app is structured with:

```
/src
  /components
    Header.tsx
    DashboardStats.tsx
    RouteList.tsx
    MainSection.tsx
  /pages
    Login.tsx
    MainApp.tsx
  /api
    rotues.ts
  /data
    auth.ts
    mockRoutes.ts
  App.tsx
```

---

## **1. Routing and Auth (`App.tsx`)**

### Purpose

- Manages routing (`/`, `/login`, `/insights`)
- Handles user authentication state
- Redirects users based on login status

### Behavior

| Path        | Behavior                                                                       |
| ----------- | ------------------------------------------------------------------------------ |
| `/`         | Redirects to `/login` if not logged in; `/insights` if logged in               |
| `/login`    | Shows login page; redirects to `/insights` if logged in                        |
| `/insights` | Protected route; shows dashboard if logged in; otherwise redirects to `/login` |

### Code Highlights

```tsx
<Routes>
  <Route path="/" element={<Navigate to={user ? "/insights" : "/login"} />} />
  <Route
    path="/login"
    element={
      user ? (
        <Navigate to="/insights" />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )
    }
  />
  <Route
    path="/insights"
    element={
      user ? (
        <MainApp user={user} onLogout={handleLogout} />
      ) : (
        <Navigate to="/login" />
      )
    }
  />
</Routes>
```

- **`user` state** tracks currently logged-in username.
- **`handleLoginSuccess`** saves user in `localStorage` and updates state.
- **`handleLogout`** removes user from `localStorage` and resets state.

---

## **2. Login Page (`LoginPage.tsx`)**

### Purpose

- Collects username and password (mock)
- Calls `onLoginSuccess` when login succeeds

### Example Mock Login

```ts
export const mockLogin = (username: string, password: string) => {
  return username === "admin" && password === "admin123";
};
```

### Props

| Prop             | Type         | Description                           |
| ---------------- | ------------ | ------------------------------------- |
| `onLoginSuccess` | `() => void` | Callback executed on successful login |

### Features

- Displays error message for invalid credentials
- Shows login hint (`admin / admin123`)
- Handles form submission

---

## **3. Main Dashboard (`MainApp.tsx`)**

### Purpose

- Shows route intelligence dashboard
- Fetches and displays route statistics, planned vs actual routes, and metrics
- Handles route selection
- Displays header with logout and username

### Props

| Prop       | Type         | Description        |
| ---------- | ------------ | ------------------ |
| `user`     | `string`     | Logged-in username |
| `onLogout` | `() => void` | Logout callback    |

### Components Used

- `Header` → Displays username and logout button
- `DashboardStats` → Displays route stats
- `RouteList` → Sidebar with route selection & pagination
- `MainSection` → Main content area for selected route comparison

### Dashboard State

| State             | Type                       | Description                        |
| ----------------- | -------------------------- | ---------------------------------- |
| `routes`          | `Route[]`                  | List of current page routes        |
| `stats`           | `TotalRoutesAndTotalStops` | Summary stats of all routes        |
| `selectedRouteId` | `string \| null`           | Currently selected route           |
| `routeComparison` | `RouteComparison \| null`  | Planned vs actual route comparison |
| `routeMetrics`    | `RouteMetrics \| null`     | Metrics for selected route         |
| `loading`         | `boolean`                  | Loading state for routes           |
| `routeLoading`    | `boolean`                  | Loading state for route comparison |

### Example: Route Metrics

```ts
export interface RouteMetrics {
  route_id: string;
  total_planned_distance_km: number;
  total_actual_distance_km: number;
  distance_delta_km: number;
  distance_delta_percent: number;
  order_matched_stops: number;
  order_match_percentage: number;
  prefix_match_count: number;
  total_stops: number;
}
```

---

## **4. Header Component (`Header.tsx`)**

### Purpose

- Displays app name
- Shows logged-in username
- Logout button

### Props

| Prop       | Type         | Description        |
| ---------- | ------------ | ------------------ |
| `username` | `string`     | Logged-in username |
| `onLogout` | `() => void` | Logout callback    |

### Features

- Dropdown menu to logout
- Triggers `onLogout` → clears user state → redirect to login

---

## **5. Authentication Flow**

1. User visits `/` → redirected to `/login` if not authenticated.
2. User enters credentials → calls `handleLoginSuccess` → saves username in localStorage → redirect to `/insights`.
3. User sees dashboard (`MainApp`) with stats and route list.
4. User clicks logout → calls `onLogout` → clears localStorage → redirects to `/login`.

---

## **6. Local Storage Keys**

| Key        | Value    | Usage                                           |
| ---------- | -------- | ----------------------------------------------- |
| `username` | `string` | Stores currently logged-in user for persistence |

---

## **7. API / Data**

- **Routes API (`api/rotues.ts`)**
  - `fetchRoutes(offset, limit)` → returns route page
  - `fetchRouteStats()` → returns dashboard stats
  - `fetchRouteComparison(routeId)` → returns planned vs actual route
  - `fetchRouteMetrics(routeId)` → returns route metrics

- **Mock Auth (`data/auth.ts`)**
  - `mockLogin(username, password)` → boolean

- **Mock Routes (`data/mockRoutes.ts`)**
  - Provides `Route`, `RouteMetrics`, `TotalRoutesAndTotalStops` interfaces
  - Mock route data for testing

---

## **8. Folder Structure**

```
src/
├─ api/
│  └─ rotues.ts
├─ components/
│  ├─ Header.tsx
│  ├─ DashboardStats.tsx
│  ├─ RouteList.tsx
│  └─ MainSection.tsx
├─ data/
│  ├─ auth.ts
│  └─ mockRoutes.ts
├─ pages/
│  ├─ Login.tsx
│  └─ MainApp.tsx
└─ App.tsx
```

---

## **9. Key Notes / Tips**

- Always store **username** in `localStorage` to persist session.
- Routing uses `React Router v6`.
- Dashboard does not contain login logic; auth is handled in `App.tsx`.
- Login page triggers `handleLoginSuccess` with a mock user.
- Logout is handled via `Header` → calls `onLogout` → navigates back to `/login`.
- Dashboard uses `useEffect` to fetch initial route stats and the first page of routes.

---

This documentation is now **complete and ready to hand over** for your dev team or for onboarding new developers.

---

If you want, I can also make a **diagram showing the login → insights → logout flow**, which visually explains the routing and state management. It helps a lot for quick understanding.

Do you want me to create that?
Absolutely! Let me provide you with a **clear, structured documentation** for your React login + dashboard app with routing, login/logout, and route dashboard. This will serve as a reference for both usage and future maintenance.

---

# 📝 Route Intelligence React App – Documentation

## **Overview**

This React application provides a dashboard for delivery route comparison. It includes:

- **Login functionality** (mock)
- **Dashboard with route statistics**
- **Route selection and metrics**
- **Protected routes using React Router**
- **Login/logout with localStorage persistence**

The app is structured with:

```
/src
  /components
    Header.tsx
    DashboardStats.tsx
    RouteList.tsx
    MainSection.tsx
  /pages
    Login.tsx
    MainApp.tsx
  /api
    rotues.ts
  /data
    auth.ts
    mockRoutes.ts
  App.tsx
```

---

## **1. Routing and Auth (`App.tsx`)**

### Purpose

- Manages routing (`/`, `/login`, `/insights`)
- Handles user authentication state
- Redirects users based on login status

### Behavior

| Path        | Behavior                                                                       |
| ----------- | ------------------------------------------------------------------------------ |
| `/`         | Redirects to `/login` if not logged in; `/insights` if logged in               |
| `/login`    | Shows login page; redirects to `/insights` if logged in                        |
| `/insights` | Protected route; shows dashboard if logged in; otherwise redirects to `/login` |

### Code Highlights

```tsx
<Routes>
  <Route path="/" element={<Navigate to={user ? "/insights" : "/login"} />} />
  <Route
    path="/login"
    element={
      user ? (
        <Navigate to="/insights" />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )
    }
  />
  <Route
    path="/insights"
    element={
      user ? (
        <MainApp user={user} onLogout={handleLogout} />
      ) : (
        <Navigate to="/login" />
      )
    }
  />
</Routes>
```

- **`user` state** tracks currently logged-in username.
- **`handleLoginSuccess`** saves user in `localStorage` and updates state.
- **`handleLogout`** removes user from `localStorage` and resets state.

---

## **2. Login Page (`LoginPage.tsx`)**

### Purpose

- Collects username and password (mock)
- Calls `onLoginSuccess` when login succeeds

### Example Mock Login

```ts
export const mockLogin = (username: string, password: string) => {
  return username === "admin" && password === "admin123";
};
```

### Props

| Prop             | Type         | Description                           |
| ---------------- | ------------ | ------------------------------------- |
| `onLoginSuccess` | `() => void` | Callback executed on successful login |

### Features

- Displays error message for invalid credentials
- Shows login hint (`admin / admin123`)
- Handles form submission

---

## **3. Main Dashboard (`MainApp.tsx`)**

### Purpose

- Shows route intelligence dashboard
- Fetches and displays route statistics, planned vs actual routes, and metrics
- Handles route selection
- Displays header with logout and username

### Props

| Prop       | Type         | Description        |
| ---------- | ------------ | ------------------ |
| `user`     | `string`     | Logged-in username |
| `onLogout` | `() => void` | Logout callback    |

### Components Used

- `Header` → Displays username and logout button
- `DashboardStats` → Displays route stats
- `RouteList` → Sidebar with route selection & pagination
- `MainSection` → Main content area for selected route comparison

### Dashboard State

| State             | Type                       | Description                        |
| ----------------- | -------------------------- | ---------------------------------- |
| `routes`          | `Route[]`                  | List of current page routes        |
| `stats`           | `TotalRoutesAndTotalStops` | Summary stats of all routes        |
| `selectedRouteId` | `string \| null`           | Currently selected route           |
| `routeComparison` | `RouteComparison \| null`  | Planned vs actual route comparison |
| `routeMetrics`    | `RouteMetrics \| null`     | Metrics for selected route         |
| `loading`         | `boolean`                  | Loading state for routes           |
| `routeLoading`    | `boolean`                  | Loading state for route comparison |

### Example: Route Metrics

```ts
export interface RouteMetrics {
  route_id: string;
  total_planned_distance_km: number;
  total_actual_distance_km: number;
  distance_delta_km: number;
  distance_delta_percent: number;
  order_matched_stops: number;
  order_match_percentage: number;
  prefix_match_count: number;
  total_stops: number;
}
```

---

## **4. Header Component (`Header.tsx`)**

### Purpose

- Displays app name
- Shows logged-in username
- Logout button

### Props

| Prop       | Type         | Description        |
| ---------- | ------------ | ------------------ |
| `username` | `string`     | Logged-in username |
| `onLogout` | `() => void` | Logout callback    |

### Features

- Dropdown menu to logout
- Triggers `onLogout` → clears user state → redirect to login

---

## **5. Authentication Flow**

1. User visits `/` → redirected to `/login` if not authenticated.
2. User enters credentials → calls `handleLoginSuccess` → saves username in localStorage → redirect to `/insights`.
3. User sees dashboard (`MainApp`) with stats and route list.
4. User clicks logout → calls `onLogout` → clears localStorage → redirects to `/login`.

---

## **6. Local Storage Keys**

| Key        | Value    | Usage                                           |
| ---------- | -------- | ----------------------------------------------- |
| `username` | `string` | Stores currently logged-in user for persistence |

---

## **7. API / Data**

- **Routes API (`api/rotues.ts`)**
  - `fetchRoutes(offset, limit)` → returns route page
  - `fetchRouteStats()` → returns dashboard stats
  - `fetchRouteComparison(routeId)` → returns planned vs actual route
  - `fetchRouteMetrics(routeId)` → returns route metrics

- **Mock Auth (`data/auth.ts`)**
  - `mockLogin(username, password)` → boolean

- **Mock Routes (`data/mockRoutes.ts`)**
  - Provides `Route`, `RouteMetrics`, `TotalRoutesAndTotalStops` interfaces
  - Mock route data for testing

---

## **8. Folder Structure**

```
src/
├─ api/
│  └─ rotues.ts
├─ components/
│  ├─ Header.tsx
│  ├─ DashboardStats.tsx
│  ├─ RouteList.tsx
│  └─ MainSection.tsx
├─ data/
│  ├─ auth.ts
│  └─ mockRoutes.ts
├─ pages/
│  ├─ Login.tsx
│  └─ MainApp.tsx
└─ App.tsx
```

---

## **9. Key Notes / Tips**

- Always store **username** in `localStorage` to persist session.
- Routing uses `React Router v6`.
- Dashboard does not contain login logic; auth is handled in `App.tsx`.
- Login page triggers `handleLoginSuccess` with a mock user.
- Logout is handled via `Header` → calls `onLogout` → navigates back to `/login`.
- Dashboard uses `useEffect` to fetch initial route stats and the first page of routes.

---
