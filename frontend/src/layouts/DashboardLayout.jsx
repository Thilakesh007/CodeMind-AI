import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { Home, FolderGit2, MessageSquare, Sun, Moon } from 'lucide-react';

const DashboardLayout = () => {
  const location = useLocation();
  const [isLightMode, setIsLightMode] = useState(document.body.classList.contains('light-theme'));

  const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Dashboard', href: '/dashboard', icon: FolderGit2 },
    { name: 'AI Chat', href: '/chat', icon: MessageSquare },
  ];

  return (
    <div className="flex h-screen bg-[#050505] text-gray-300 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-[#0a0a0a] border-r border-[#262626] flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-[#262626]">
          <h1 className="text-xl font-bold text-white tracking-tight">CodeMind AI</h1>
        </div>
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-3">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href || (location.pathname !== '/' && item.href !== '/' && location.pathname.startsWith(item.href));
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-[#a855f7]/10 text-[#a855f7]'
                        : 'hover:bg-[#171717] text-gray-400 hover:text-white'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>

        </nav>
        
        {/* User Profile / Logout */}
        <div className="p-4 border-t border-[#262626]">
          <div className="flex items-center justify-between">
            <div className="flex items-center overflow-hidden">
              <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-white font-bold text-xs flex-shrink-0 shadow-[0_0_10px_rgba(124,58,237,0.3)]">
                {localStorage.getItem('user_email')?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="ml-3 truncate">
                <p className="text-sm font-medium text-white truncate">{localStorage.getItem('user_email') || 'User'}</p>
                <p className="text-xs text-gray-500">Developer</p>
              </div>
            </div>
            <div className="flex items-center space-x-1 ml-2">
              <button 
                onClick={() => {
                  const isLight = document.body.classList.contains('light-theme');
                  if (isLight) {
                    document.body.classList.remove('light-theme');
                    setIsLightMode(false);
                  } else {
                    document.body.classList.add('light-theme');
                    setIsLightMode(true);
                  }
                }}
                className="p-1.5 text-gray-500 hover:text-white hover:bg-[#171717] rounded-lg transition-colors"
                title={isLightMode ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
              >
                {isLightMode ? <Moon className="h-4 w-4 flex-shrink-0" /> : <Sun className="h-4 w-4 flex-shrink-0" />}
              </button>
              <button 
                onClick={() => {
                  localStorage.removeItem('auth_token');
                  localStorage.removeItem('user_email');
                  window.location.href = '/login';
                }}
                className="p-1.5 text-gray-500 hover:text-red-400 hover:bg-[#171717] rounded-lg transition-colors"
                title="Sign Out"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
