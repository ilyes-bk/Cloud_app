import React, { useEffect, useState } from "react";
import { useNavigate } from "@remix-run/react";
import { useLocation } from "@remix-run/react";
const ToggleButton = () => {
  const [isChats, setIsChats] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const toggle = () => {
    if (isChats) {
      navigate("/t"); // Navigate to Tasks page
    } else {
      navigate("/"); // Navigate to Chats page
    }
    setIsChats(!isChats); // Toggle the state
  };
  useEffect(() => {
    if (location.pathname.startsWith("/t")) {
      setIsChats(false);
    } else {
      setIsChats(true);
    }
  }, []);
  return (
    <div className="flex items-center justify-center py-4">
      <button
        onClick={toggle}
        className={`flex items-center justify-between w-40 px-4 py-2 rounded-full border-2 transition-all duration-300 ${
          isChats
            ? "bg-blue-500 border-blue-500"
            : "bg-green-500 border-green-500"
        }`}
      >
        <span
          className={`flex-1 text-center transition-opacity duration-300 ${
            isChats ? "opacity-100 text-white" : "opacity-50 text-gray-200"
          }`}
        >
          Chats
        </span>
        <span
          className={`flex-1 text-center transition-opacity duration-300 ${
            isChats ? "opacity-50 text-gray-200" : "opacity-100 text-white"
          }`}
        >
          Tasks
        </span>
      </button>
    </div>
  );
};

export default ToggleButton;
