import { FaRoute, FaMapSigns } from "react-icons/fa";
import { type TotalRoutesAndTotalStops } from "../data/mockRoutes";

interface DashboardStatsProps {
  data?: TotalRoutesAndTotalStops; // optional, since data might not be loaded yet
}

export default function DashboardStats({ data }: DashboardStatsProps) {
  if (!data) {
    return (
      <div className="flex flex-col gap-3">
        <div className="bg-gray-800 rounded-lg p-3 animate-pulse h-16" />
        <div className="bg-gray-800 rounded-lg p-3 animate-pulse h-16" />
      </div>
    );
  }

  const stats = [
    {
      label: "Total Routes",
      value: data.route_count,
      icon: <FaRoute className="w-5 h-5 text-blue-400" />,
    },
    {
      label: "Total Stops",
      value: data.stop_count,
      icon: <FaMapSigns className="w-5 h-5 text-green-400" />,
    },
  ];

  return (
    <div className="flex flex-col gap-3">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="flex items-center justify-between bg-gray-800 rounded-lg p-3 hover:bg-gray-700 transition"
        >
          <div className="flex items-center gap-2">
            {stat.icon}
            <span className="text-gray-400 text-sm">{stat.label}</span>
          </div>
          <div className="text-lg font-bold text-white">{stat.value}</div>
        </div>
      ))}
    </div>
  );
}
