import React from 'react';
import './LoadingAnimation.css'; // Import the CSS file

const LoadingAnimation = () => {
  return (
    <div className="flex items-center justify-center space-x-1">
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce200"></div>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce400"></div>
    </div>
  );
};

export default LoadingAnimation