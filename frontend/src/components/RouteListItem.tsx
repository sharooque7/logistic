import type { Route } from "../data/mockRoutes";
import { FaClock, FaMapMarkerAlt, FaRoute } from "react-icons/fa";
import { GrCapacity } from "react-icons/gr";

export default function RouteListItem({
  route,
  selected,
  onClick,
}: {
  route: Route;
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-lg p-3 border transition-all duration-200
        ${
          selected
            ? "bg-blue-600 border-blue-500 shadow-lg"
            : "bg-gray-800 border-gray-700 hover:bg-gray-700 hover:shadow-md"
        }`}
    >
      {/* Header: Route ID + Score */}
      <div className="flex justify-between items-center mb-2">
        <div className="font-semibold text-sm ">{route.route_id}</div>
        {/* <span
          className={`px-2 py-0.5 text-xs rounded-full font-medium
            ${
              route.route_score === "High"
                ? "bg-green-500 text-white"
                : route.route_score === "Medium"
                  ? "bg-yellow-500 text-white"
                  : "bg-red-500 text-white"
            }`}
        >
          {route.route_score}
        </span> */}
      </div>

      {/* Route Details */}
      <div className="text-gray-400 text-xs space-y-1">
        <div className="flex items-center gap-1">
          <FaMapMarkerAlt className="text-gray-400 w-3 h-3" />
          Station: {route.station_code}
        </div>
        <div className="flex items-center gap-1">
          <FaRoute className="w-3 h-3" /> Total Stops: {route.stop_count}
        </div>
        <div className="flex items-center gap-1">
          <FaClock className="w-3 h-3" /> Departure: {route.departure_time_utc}{" "}
          ({route.date_YYYY_MM_DD})
        </div>
        <div className="flex items-center gap-1">
          <GrCapacity className="w-3 h-3" />
          Capacity: {Math.round(
            route.executor_capacity_cm3,
          ).toLocaleString()}{" "}
          cm³
        </div>
      </div>
    </div>
  );
}
