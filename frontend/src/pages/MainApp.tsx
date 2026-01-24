import { useEffect, useState } from "react";
import Header from "../components/Header";
import LoginPage from "../pages/Login";
import DashboardStats from "../components/DashboardStats";
import RouteList from "../components/RouteList";
import MainSection from "../components/MainSection";

import {
  fetchRoutes,
  fetchRouteStats,
  fetchRouteComparison,
  generatePlannedRoute,
  fetchRouteMetrics,
} from "../api/rotues";
import type { RouteComparison } from "../api/rotues";
import type { Route, TotalRoutesAndTotalStops } from "../data/mockRoutes";

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

const PAGE_SIZE = 10;

interface LoginPageProps {
  username: string;
  onLoginSuccess: (user: string) => void;
  onLogout: () => void;
}

export default function MainApp({
  username,
  onLoginSuccess,
  onLogout,
}: LoginPageProps) {
  // 📊 DASHBOARD STATE
  const [routes, setRoutes] = useState<Route[]>([]);
  const [stats, setStats] = useState<TotalRoutesAndTotalStops>();
  const [selectedRouteId, setSelectedRouteId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [routeComparison, setRouteComparison] =
    useState<RouteComparison | null>(null);
  const [routeLoading, setRouteLoading] = useState(false);
  const [routeMetrics, setRouteMetrics] = useState<RouteMetrics | null>(null);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  // 🔑 LOGIN / LOGOUT HANDLERS
  const handleLoginSuccess = (username: string) => {
    onLoginSuccess(username);
  };

  const handleLogout = () => {
    // optional cleanup
    setRoutes([]);
    setStats(undefined);
    setSelectedRouteId(null);
    setRouteComparison(null);
    setRouteMetrics(null);

    onLogout();
  };

  // 🚫 If not logged in → show login page
  if (!username) {
    return <LoginPage onLoginSuccess={() => handleLoginSuccess("Admin")} />;
  }

  // Load stats and first page
  useEffect(() => {
    async function loadSidebarData() {
      setLoading(true);
      try {
        const statsData = await fetchRouteStats();
        setStats(statsData);

        if (statsData) {
          setTotalPages(Math.ceil(statsData.route_count / PAGE_SIZE));
          await loadRoutesPage(0, statsData);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadSidebarData();
  }, []);

  const loadRoutesPage = async (
    pageNum: number,
    statsData: TotalRoutesAndTotalStops | null = stats || null,
  ) => {
    if (!statsData) return;

    setLoading(true);
    try {
      const data = await fetchRoutes(pageNum * PAGE_SIZE, PAGE_SIZE);
      setRoutes(data);
      setPage(pageNum);

      if (data.length > 0) {
        handleRouteSelect(data[0].route_id);
      } else {
        setSelectedRouteId(null);
        setRouteComparison(null);
        setRouteMetrics(null);
      }
    } catch (err) {
      console.error("Failed to load routes:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRouteSelect = async (routeId: string) => {
    setSelectedRouteId(routeId);
    setRouteLoading(true);
    try {
      await generatePlannedRoute(routeId);

      const data = await fetchRouteComparison(routeId);
      setRouteComparison(data);

      const metricsData = await fetchRouteMetrics(routeId);
      if (metricsData.metrics) setRouteMetrics(metricsData.metrics);
    } catch (err) {
      console.error(err);
    } finally {
      setRouteLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-gray-100">
      {/* ✅ HEADER WITH LOGOUT */}
      <Header username={username} onLogout={handleLogout} />

      <div className="flex flex-1 overflow-hidden">
        <aside className="w-80 bg-gray-950 border-r border-gray-800 p-4 flex flex-col gap-4">
          {stats && <DashboardStats data={stats} />}

          <div className="flex-1 overflow-y-auto">
            <RouteList
              routes={routes}
              selectedRouteId={selectedRouteId}
              onSelect={handleRouteSelect}
              page={page}
              totalPages={totalPages}
              onPageChange={loadRoutesPage}
              loading={loading}
            />
          </div>
        </aside>

        <main className="flex-1 bg-gray-950 flex">
          <MainSection
            route={routes.find((r) => r.route_id === selectedRouteId) || null}
            planned_route={routeComparison?.planned_route}
            actual_route={routeComparison?.actual_route}
            metrics={routeMetrics}
            loading={routeLoading}
          />
        </main>
      </div>
    </div>
  );
}
