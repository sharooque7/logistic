
import React from "react";

interface RouteCardProps {
  route_id: string;
  station_code: string;
  stop_count: number;
}

const RouteCard: React.FC<RouteCardProps> = ({ route_id, station_code, stop_count }) => {
  return (
    <div className="bg-white shadow rounded p-4 hover:shadow-lg transition">
      <h3 className="font-semibold text-lg">{route_id}</h3>
      <p>Station: {station_code}</p>
      <p>Total Stops: {stop_count}</p>
      <button className="mt-2 bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
        View Route
      </button>
    </div>
  );
};

export default RouteCard;
