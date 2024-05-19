import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import ClipLoader from 'react-spinners/ClipLoader';

function LoadingModal({ isLoading, message, timer }) {
  const [countdown, setCountdown] = useState(timer);

  useEffect(() => {
    let intervalId = null; // Declare intervalId outside of any conditions

    if (isLoading && countdown > 0) {
      intervalId = setInterval(() => {
        setCountdown(currentCountdown => {
          if (currentCountdown <= 1) {
            clearInterval(intervalId);
            return 0;
          }
          return currentCountdown - 1;
        });
      }, 1000);
    }

    // Always return a cleanup function
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isLoading, countdown, timer]); // Added timer to dependencies for completeness

  if (!isLoading || countdown <= 0) return null;

  const modalContent = (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999999, // High z-index to ensure it covers other elements
      width: '100vw',
      height: '100vh',
    }}>
      <div style={{
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <ClipLoader size={150} color={"#123abc"} loading={isLoading} />
        <div style={{
          position: 'absolute',
          color: 'white',
          fontWeight: 'bold',
          textAlign: 'center'
        }}>
          {message} {countdown}s
        </div>
      </div>
    </div>
  );

  return ReactDOM.createPortal(
    modalContent,
    document.body  // Assuming your index.html has a <body> tag
  );
}

export default LoadingModal;
