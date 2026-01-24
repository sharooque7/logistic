import type { Route } from "../data/mockRoutes";
import { API_BASE } from "../config/api";

export async function fetchRoutes(skip = 0, limit = 25): Promise<Route[]> {
  const res = await fetch(`${API_BASE}/routes?skip=${skip}&limit=${limit}`);

  if (!res.ok) {
    throw new Error("Failed to fetch routes");
  }

  return res.json(); // await the JSON parsing
}

export async function fetchRouteStats(): Promise<{
  route_count: number;
  stop_count: number;
}> {
  const res = await fetch(`${API_BASE}/routes/total_routes_and_stops`);

  if (!res.ok) {
    throw new Error("Failed to fetch route stats");
  }

  return res.json();
}
export interface StopCoordinate {
  stop_code: string;
  planned_sequence?: number;
  actual_sequence?: number;
  lat: number;
  lng: number;
  zone_id: string;
  type: string;
}

export interface RouteComparison {
  route: Route;
  planned_route: StopCoordinate[];
  actual_route: StopCoordinate[];
}

export async function fetchRouteComparison(
  routeId: string,
): Promise<RouteComparison> {
  const res = await fetch(`${API_BASE}/routes/${routeId}/comparison`);
  if (!res.ok) {
    throw new Error(`Failed to fetch comparison for route ${routeId}`);
  }

  return res.json(); // await the JSON parsing
}

export async function generatePlannedRoute(routeId: string) {
  const res = await fetch(
    `${API_BASE}/routes/${routeId}/generate/planned_routes`,
    { method: "POST" },
  );
  if (!res.ok) throw new Error("Failed to generate planned route");
  return res.json(); // Should return the planned_route object
}

// api/rotues.ts
export async function fetchRouteMetrics(routeId: string) {
  const res = await fetch(`${API_BASE}/routes/${routeId}/metrics`);
  if (!res.ok) throw new Error("Failed to fetch route metrics");
  return res.json(); // Should return the metrics object
}
