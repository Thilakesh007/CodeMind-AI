import React, { useState } from 'react';
import api from '../services/api';
import { UploadCloud, CheckCircle, Loader2 } from 'lucide-react';

const Home = () => {
  const [file, setFile] = useState(null);
  const [gitUrl, setGitUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(''); // 'uploading', 'cloning', 'indexing', 'success', 'error'
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setStatus('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    await processRepository(async () => {
      setStatus('uploading');
      const formData = new FormData();
      formData.append('file', file);
      
      const uploadRes = await api.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (!uploadRes.data.success) {
        throw new Error(uploadRes.data.message || 'Upload failed');
      }
      return uploadRes.data.repository;
    });
  };

  const handleClone = async () => {
    if (!gitUrl) return;
    await processRepository(async () => {
      setStatus('cloning');
      const cloneRes = await api.post('/clone', { url: gitUrl });
      
      if (!cloneRes.data.success) {
        throw new Error(cloneRes.data.message || 'Clone failed');
      }
      return cloneRes.data.repository;
    });
  };

  const processRepository = async (uploadOrCloneFn) => {
    setLoading(true);
    setErrorMessage('');

    try {
      const projectName = await uploadOrCloneFn();

      // 2. Index the repository
      setStatus('indexing');
      await api.post(`/index?project_name=${encodeURIComponent(projectName)}`);

      setStatus('success');
      setFile(null);
      setGitUrl('');
    } catch (err) {
      console.error(err);
      setStatus('error');
      setErrorMessage(err.response?.data?.detail || err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold text-white mb-6">Welcome to CodeMind AI</h2>
      <p className="text-gray-400 mb-8">
        Intelligent Codebase Assistant. Upload your repository or connect via GitHub to start querying your codebase using Retrieval-Augmented Generation.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Upload ZIP Card */}
        <div className="bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl p-6 transition-all hover:border-[#a855f7] hover:shadow-[0_0_15px_rgba(168,85,247,0.1)] relative overflow-hidden backdrop-blur-md">
          <h3 className="text-xl font-semibold text-white mb-2">Upload ZIP</h3>
          <p className="text-sm text-gray-400 mb-6">Upload a compressed repository file for local indexing.</p>
          
          <div className="border-2 border-dashed border-[#262626] rounded-xl p-6 text-center hover:border-[#a855f7] transition-all cursor-pointer relative bg-[#050505]/50">
            <input 
              type="file" 
              accept=".zip" 
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              disabled={loading}
            />
            <UploadCloud className="mx-auto h-8 w-8 text-gray-400 mb-2" />
            <p className="text-sm text-gray-300">
              {file ? file.name : "Drag & drop a .zip file here, or click to select"}
            </p>
          </div>

          <button 
            onClick={handleUpload}
            disabled={!file || loading}
            className={`mt-4 w-full py-3 rounded-xl font-medium flex justify-center items-center transition-all ${
              !file || loading 
                ? 'bg-[#171717] border border-[#262626] text-gray-500 cursor-not-allowed' 
                : 'bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] text-white shadow-[0_0_10px_rgba(124,58,237,0.2)]'
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-2 h-5 w-5" />
                {status === 'uploading' ? 'Uploading...' : 'Indexing (this may take a while)...'}
              </>
            ) : (
              'Upload and Index'
            )}
          </button>

          {status === 'success' && (
            <div className="mt-4 p-3 bg-green-900 bg-opacity-30 border border-green-800 rounded text-green-400 flex items-center text-sm">
              <CheckCircle className="h-4 w-4 mr-2" />
              Repository successfully indexed! You can now ask questions in the AI Chat.
            </div>
          )}

          {status === 'error' && (
            <div className="mt-4 p-3 bg-red-900 bg-opacity-30 border border-red-800 rounded text-red-400 text-sm">
              <p className="font-semibold mb-1">Error</p>
              {errorMessage}
            </div>
          )}

        </div>

        {/* Clone GitHub Card */}
        <div className="bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl p-6 relative overflow-hidden transition-all hover:border-[#a855f7] hover:shadow-[0_0_15px_rgba(168,85,247,0.1)] backdrop-blur-md">
          <h3 className="text-xl font-semibold text-white mb-2">Clone Repository</h3>
          <p className="text-sm text-gray-400 mb-6">Provide a GitHub URL to clone and index directly.</p>
          <div className="space-y-4 mt-[3.5rem]">
            <input 
              type="text" 
              placeholder="https://github.com/user/repo"
              value={gitUrl}
              onChange={(e) => setGitUrl(e.target.value)}
              className="w-full bg-[#121212] border border-[#262626] rounded-xl py-3 px-4 text-white focus:outline-none focus:border-[#a855f7] focus:ring-1 focus:ring-[#a855f7] transition-all"
              disabled={loading}
            />
            <button 
              onClick={handleClone}
              disabled={!gitUrl || loading} 
              className={`w-full py-3 rounded-xl font-medium flex justify-center items-center transition-all ${
                !gitUrl || loading 
                  ? 'bg-[#171717] border border-[#262626] text-gray-500 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] text-white shadow-[0_0_10px_rgba(124,58,237,0.2)]'
              }`}
            >
               {loading && status === 'cloning' ? (
                <>
                  <Loader2 className="animate-spin mr-2 h-5 w-5" />
                  Cloning...
                </>
              ) : loading && status === 'indexing' && gitUrl ? (
                <>
                  <Loader2 className="animate-spin mr-2 h-5 w-5" />
                  Indexing...
                </>
              ) : (
                'Clone and Index'
              )}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Home;
