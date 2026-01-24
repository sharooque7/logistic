import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Popup,
} from "react-leaflet";

import type { Route } from "../data/mockRoutes";
import L from "leaflet";
import { useState } from "react";

const createBalloonIcon = (text: string, color: string) =>
  new L.DivIcon({
    html: `
      <div style="position: relative; display: flex; flex-direction: column; align-items: center; font-size:12px;">
        <!-- Balloon -->
        <div style="
          background-color: ${color};
          color: white;
          padding: 4px 8px;
          border-radius: 12px;
          font-weight: bold;
          white-space: nowrap;
          text-align: center;
          border: 1px solid white;
        ">
          ${text}
        </div>
        <!-- Tail -->
        <div style="
          width: 0;
          height: 0;
          border-left: 6px solid transparent;
          border-right: 6px solid transparent;
          border-top: 8px solid ${color};
          margin-top: -1px;
        "></div>
      </div>
    `,
    className: "", // remove default styling
    iconSize: [40, 30],
    iconAnchor: [20, 30], // bottom center for the tail
  });

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

function toLatLng(
  stops: StopCoordinate[],
  sequenceKey: "planned_sequence" | "actual_sequence",
): [number, number][] {
  return stops
    .slice() // copy to avoid mutating original
    .sort((a, b) => (a[sequenceKey] ?? 0) - (b[sequenceKey] ?? 0))
    .map((stop) => [stop.lat, stop.lng] as [number, number]);
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

interface MainSectionProps {
  route?: Route | null;
  planned_route?: StopCoordinate[];
  actual_route?: StopCoordinate[];
  metrics?: RouteMetrics | null;
  loading?: boolean;
}

export default function MainSection({
  route,
  planned_route = [],
  actual_route = [],
  metrics,
  loading,
}: MainSectionProps) {
  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400">
        Loading route data...
      </div>
    );
  }

  if (!route) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400">
        Select a route to view map & metrics
      </div>
    );
  }

  // Center map at the first Station stop
  const station = planned_route.find((stop) => stop.type === "Station");
  const [showPlanned, setShowPlanned] = useState(true);

  const center: [number, number] = station
    ? [station.lat, station.lng]
    : [34.007369, -118.143927]; // fallback

  const plannedLatLng = toLatLng(planned_route, "planned_sequence");
  const actualLatLng = toLatLng(actual_route, "actual_sequence");

  return (
    <div className="flex-1 flex flex-col p-4 gap-4 bg-gray-950">
      <div className="flex gap-2 mb-2">
        <button
          className={`px-3 py-1 rounded ${showPlanned ? "bg-blue-600" : "bg-gray-700"}`}
          onClick={() => setShowPlanned(true)}
        >
          Planned Route
        </button>
        <button
          className={`px-3 py-1 rounded ${!showPlanned ? "bg-red-600" : "bg-gray-700"}`}
          onClick={() => setShowPlanned(false)}
        >
          Actual Route
        </button>
      </div>

      {/* Map */}
      <div className="flex-1 rounded-lg overflow-hidden shadow-lg">
        <MapContainer
          center={center}
          zoom={13}
          scrollWheelZoom
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />

          {showPlanned && plannedLatLng && (
            <Polyline positions={plannedLatLng} color="#3B82F6" weight={4} />
          )}
          {!showPlanned && actualLatLng && (
            <Polyline
              positions={actualLatLng}
              color="#EF4444"
              weight={4}
              dashArray="5,10"
            />
          )}

          {showPlanned &&
            plannedLatLng?.map((coord, idx) => (
              <Marker
                position={coord}
                key={`planned-${idx}`}
                icon={createBalloonIcon(
                  planned_route[idx].planned_sequence +
                    " " +
                    planned_route[idx].stop_code,
                  "#3B82F6",
                )}
              >
                <Popup
                  className="!p-1 !m-0 !text-xs !bg-gray-800 !text-white !rounded"
                  closeButton={false}
                  autoClose={false}
                >
                  <div className="flex flex-col items-center">
                    <span className="font-bold">
                      {planned_route[idx].stop_code}
                    </span>
                    <span className="text-[10px]">
                      {coord[0].toFixed(4)}, {coord[1].toFixed(4)}
                    </span>
                  </div>
                </Popup>
              </Marker>
            ))}
          {!showPlanned &&
            actualLatLng?.map((coord, idx) => (
              <Marker
                position={coord}
                key={`actual-${idx}`}
                icon={createBalloonIcon(
                  actual_route[idx].actual_sequence +
                    " " +
                    actual_route[idx].stop_code,
                  "#EF4444",
                )}
              >
                {" "}
                <Popup
                  className="!p-1 !m-0 !text-xs !bg-gray-800 !text-white !rounded"
                  closeButton={false}
                  autoClose={false}
                >
                  <div className="flex flex-col items-center">
                    <span className="font-bold">
                      {actual_route[idx].stop_code}
                    </span>
                    <span className="text-[10px]">
                      {coord[0].toFixed(4)}, {coord[1].toFixed(4)}
                    </span>
                  </div>
                </Popup>
              </Marker>
            ))}
        </MapContainer>
      </div>

      {/* Metrics */}
      {metrics && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 text-sm">
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-gray-400 text-xs">Planned Distance</div>
              <div className="text-blue-400 font-semibold text-lg">
                {metrics.total_planned_distance_km} km
              </div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-gray-400 text-xs">Actual Distance</div>
              <div className="text-red-400 font-semibold text-lg">
                {metrics.total_actual_distance_km} km
              </div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-gray-400 text-xs">Distance Delta</div>
              <div
                className={`font-semibold text-lg ${
                  metrics.distance_delta_km >= 0
                    ? "text-green-400"
                    : "text-red-400"
                }`}
              >
                {metrics.distance_delta_km} km
              </div>
              <div className="text-xs text-gray-400">
                {metrics.distance_delta_percent}%
              </div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-gray-400 text-xs">Order Match</div>
              <div className="text-green-400 font-semibold text-lg">
                {metrics.order_match_percentage}%
              </div>
              <div className="text-xs text-gray-400">
                {metrics.order_matched_stops} / {metrics.total_stops} stops
              </div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-gray-400 text-xs">Prefix Match (Top-10)</div>
              <div className="text-purple-400 font-semibold text-lg">
                {metrics.prefix_match_count}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
