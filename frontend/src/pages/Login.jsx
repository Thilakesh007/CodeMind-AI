import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, Loader2, Zap, User } from 'lucide-react';
import api from '../services/api';

const Login = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loadingAction, setLoadingAction] = useState(null);
  const navigate = useNavigate();
  const handleAuth = async (e) => {
    e.preventDefault();
    if (!email || !password || (isSignUp && !name)) return;
    
    setLoadingAction('signin');
    try {
      if (isSignUp) {
        const res = await api.post('/auth/signup', { name, email, password });
        localStorage.setItem('auth_token', res.data.token);
        localStorage.setItem('user_email', res.data.email);
        navigate('/');
      } else {
        const res = await api.post('/auth/signin', { email, password });
        localStorage.setItem('auth_token', res.data.token);
        localStorage.setItem('user_email', res.data.email);
        navigate('/');
      }
    } catch (err) {
      alert(err.response?.data?.detail || "Authentication failed");
    } finally {
      setLoadingAction(null);
    }
  };

  const handleGoogleLogin = () => {
    setLoadingAction('google');
    window.location.href = 'http://localhost:8000/auth/google/login';
  };

  const handleGithubLogin = () => {
    setLoadingAction('github');
    window.location.href = 'http://localhost:8000/auth/github/login';
  };

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center relative overflow-hidden font-sans">
      
      {/* Background glowing orbs for premium feel */}
      <div className="absolute top-[-20%] left-[20%] w-[50%] h-[50%] bg-[#7c3aed] rounded-full blur-[150px] opacity-20 animate-pulse"></div>
      <div className="absolute bottom-[-10%] right-[10%] w-[40%] h-[40%] bg-[#c084fc] rounded-full blur-[150px] opacity-10 animate-pulse" style={{ animationDelay: '2s' }}></div>

      <div className="relative z-10 w-full max-w-md p-8 bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl shadow-2xl backdrop-blur-md">
        <div className="flex flex-col items-center mb-8">
          <div className="bg-[#171717] p-3 rounded-xl border border-[#262626] mb-4 shadow-inner">
            <Zap className="h-8 w-8 text-[#a855f7]" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">
            {isSignUp ? "Create an Account" : "Welcome Back"}
          </h2>
          <p className="text-gray-400 text-center">
            {isSignUp ? "Sign up to start analyzing your repositories." : "Sign in to your intelligent workspace."}
          </p>
        </div>
        
        <div className="flex flex-col space-y-3 mb-6">
          <button 
            onClick={handleGoogleLogin}
            disabled={loadingAction !== null}
            className="w-full flex items-center justify-center bg-white hover:bg-gray-200 text-black py-3 rounded-xl font-semibold transition-all shadow-sm disabled:opacity-70 group"
          >
            {loadingAction === 'google' ? (
              <Loader2 className="animate-spin h-5 w-5 text-gray-900" />
            ) : (
              <>
                <svg className="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" viewBox="0 0 48 48">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                </svg>
                Continue with Google
              </>
            )}
          </button>
          
          <button 
            onClick={handleGithubLogin}
            disabled={loadingAction !== null}
            className="w-full flex items-center justify-center bg-[#24292e] hover:bg-[#2f363d] text-white py-3 rounded-xl font-semibold transition-all shadow-sm disabled:opacity-70 group"
          >
            {loadingAction === 'github' ? (
              <Loader2 className="animate-spin h-5 w-5 text-white" />
            ) : (
              <>
                <svg className="w-5 h-5 mr-3 group-hover:scale-110 transition-transform fill-current" viewBox="0 0 24 24">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
                </svg>
                Continue with GitHub
              </>
            )}
          </button>
        </div>

        <div className="flex items-center mb-6">
          <div className="flex-grow border-t border-[#262626]"></div>
          <span className="mx-4 text-xs text-gray-500 font-medium uppercase tracking-widest">Or continue with email</span>
          <div className="flex-grow border-t border-[#262626]"></div>
        </div>

        <form onSubmit={handleAuth} className="space-y-4">
          
          {isSignUp && (
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1.5">Full Name</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-500" />
                </div>
                <input
                  type="text"
                  required={isSignUp}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-[#121212] border border-[#262626] rounded-xl py-3 pl-10 pr-3 text-white focus:outline-none focus:border-[#a855f7] focus:ring-1 focus:ring-[#a855f7] transition-all"
                  placeholder="John Doe"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1.5">Email Address</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail className="h-5 w-5 text-gray-500" />
              </div>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-[#121212] border border-[#262626] rounded-xl py-3 pl-10 pr-3 text-white focus:outline-none focus:border-[#a855f7] focus:ring-1 focus:ring-[#a855f7] transition-all"
                placeholder="developer@example.com"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1.5">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-gray-500" />
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-[#121212] border border-[#262626] rounded-xl py-3 pl-10 pr-3 text-white focus:outline-none focus:border-[#a855f7] focus:ring-1 focus:ring-[#a855f7] transition-all"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loadingAction !== null || !email || !password || (isSignUp && !name)}
            className="w-full flex items-center justify-center bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition-all mt-6 shadow-[0_0_15px_rgba(124,58,237,0.3)] hover:shadow-[0_0_25px_rgba(124,58,237,0.5)]"
          >
            {loadingAction === 'signin' ? <Loader2 className="animate-spin h-5 w-5" /> : (isSignUp ? 'Sign Up' : 'Sign In')}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-400">
          {isSignUp ? "Already have an account?" : "Don't have an account?"}
          <button 
            type="button"
            onClick={() => setIsSignUp(!isSignUp)}
            className="ml-2 text-[#a855f7] hover:text-[#c084fc] hover:underline font-medium transition-colors"
          >
            {isSignUp ? "Sign In" : "Sign Up"}
          </button>
        </div>

        <div className="mt-6 text-center text-xs text-gray-500">
          By continuing, you agree to our <a href="#" className="text-[#a855f7] hover:underline transition-colors">Terms of Service</a> and <a href="#" className="text-[#a855f7] hover:underline transition-colors">Privacy Policy</a>.
        </div>
      </div>
    </div>
  );
};

export default Login;
