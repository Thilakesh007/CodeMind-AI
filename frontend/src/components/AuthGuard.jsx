import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

const AuthGuard = () => {
  const [isChecking, setIsChecking] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if token exists in localStorage
    const token = localStorage.getItem('auth_token');
    
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
    
    // Tiny delay to prevent flash of content
    setTimeout(() => {
      setIsChecking(false);
    }, 300);
  }, []);

  if (isChecking) {
    return (
      <div className="h-screen w-screen bg-[#0d1117] flex items-center justify-center">
        <Loader2 className="animate-spin h-8 w-8 text-[#58a6ff]" />
      </div>
    );
  }

  // If not authenticated, redirect to /login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated, render the child routes
  return <Outlet />;
};

export default AuthGuard;
