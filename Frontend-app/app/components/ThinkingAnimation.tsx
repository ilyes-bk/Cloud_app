import React from "react";
const ThinkingAnimation = () => {
    return (
      <svg
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
        style={{ width: "200px", height: "200px" }}
      >
        {/* First uneven wave */}
        <path
          d="M50 50 
             m -20 0 
             q 10 -10 20 0 
             q 10 10 20 0 
             q -10 10 -20 0 
             q -10 -10 -20 0 Z"
          fill="none"
          stroke="#007acc"
          strokeWidth="1"
        >
          <animateTransform
            attributeName="transform"
            type="scale"
            from="1"
            to="2"
            dur="2s"
            repeatCount="indefinite"
          />
          <animate attributeName="opacity" from="1" to="0" dur="2s" repeatCount="indefinite" />
        </path>
  
        {/* Second uneven wave (delayed) */}
        <path
          d="M50 50 
             m -15 0 
             q 8 -15 15 0 
             q 8 15 15 0 
             q -8 15 -15 0 
             q -8 -15 -15 0 Z"
          fill="none"
          stroke="#61dafb"
          strokeWidth="1"
        >
          <animateTransform
            attributeName="transform"
            type="scale"
            from="1"
            to="2"
            dur="2s"
            begin="1s"
            repeatCount="indefinite"
          />
          <animate attributeName="opacity" from="1" to="0" dur="2s" begin="1s" repeatCount="indefinite" />
        </path>
      </svg>
    );
  };
export default ThinkingAnimation