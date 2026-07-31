import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { FolderGit2, Calendar, HardDrive, Loader2, X, File as FileIcon, Trash2 } from 'lucide-react';
import FolderTree from '../components/FolderTree';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [treeModalOpen, setTreeModalOpen] = useState(false);
  const [selectedTreeProject, setSelectedTreeProject] = useState('');
  const [treeData, setTreeData] = useState(null);
  const [loadingTree, setLoadingTree] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.get('/projects');
        setProjects(response.data.projects);
      } catch (error) {
        console.error("Failed to fetch projects", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, []);

  const handleDeleteProject = async (projectName) => {
    if (window.confirm(`Are you sure you want to delete the repository "${projectName}"? This will permanently delete the files and AI vectors.`)) {
      try {
        const response = await api.delete(`/projects/${encodeURIComponent(projectName)}`);
        if (response.data.success) {
          setProjects(projects.filter(p => p.name !== projectName));
        }
      } catch (error) {
        console.error("Failed to delete project", error);
        alert("Failed to delete project. Check console for details.");
      }
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400">
        <Loader2 className="animate-spin h-8 w-8 mr-3" />
        Loading your projects...
      </div>
    );
  }

  const openTreeModal = async (projectName) => {
    setSelectedTreeProject(projectName);
    setTreeModalOpen(true);
    setLoadingTree(true);
    setTreeData(null);
    try {
      const response = await api.get(`/tree/${encodeURIComponent(projectName)}`);
      if (response.data.success) {
        setTreeData(response.data.tree);
      } else {
        console.error(response.data.message);
      }
    } catch (error) {
      console.error("Failed to fetch tree", error);
    } finally {
      setLoadingTree(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold text-white mb-2">Project Dashboard</h2>
      <p className="text-gray-400 mb-8">View and manage all repositories currently indexed by CodeMind AI.</p>

      {projects.length === 0 ? (
        <div className="bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl p-10 text-center backdrop-blur-md shadow-lg">
          <FolderGit2 className="mx-auto h-12 w-12 text-gray-500 mb-4" />
          <h3 className="text-xl text-white font-semibold mb-2">No projects indexed yet</h3>
          <p className="text-gray-400">Head over to the Home page to upload a ZIP or clone a GitHub repository.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div key={project.name} className="bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl p-5 hover:border-[#a855f7] hover:shadow-[0_0_15px_rgba(168,85,247,0.15)] transition-all group relative backdrop-blur-md">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <FolderGit2 className="h-6 w-6 text-[#a855f7] mr-3" />
                  <h3 className="text-lg font-semibold text-white truncate max-w-[200px]" title={project.name}>
                    {project.name}
                  </h3>
                </div>
                <button
                  onClick={() => handleDeleteProject(project.name)}
                  className="text-gray-500 hover:text-red-500 transition-colors p-1"
                  title="Delete Repository"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
              
              <div className="space-y-2 mt-4 text-sm text-gray-400">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 mr-2 text-gray-500" />
                  Indexed on {new Date(project.indexed_at).toLocaleDateString()}
                </div>
                <div className="flex items-center truncate">
                  <HardDrive className="h-4 w-4 mr-2 text-gray-500 flex-shrink-0" />
                  <span className="truncate">{project.path}</span>
                </div>
              </div>

              <div className="mt-6 flex space-x-2">
                <button 
                  onClick={() => openTreeModal(project.name)}
                  className="flex-1 bg-[#171717] hover:bg-[#262626] text-white py-2 rounded-xl text-sm transition-colors border border-[#262626] flex items-center justify-center"
                >
                  <FileIcon className="h-4 w-4 mr-2" />
                  View Files
                </button>
                <button 
                  onClick={() => navigate('/chat', { state: { project: project.name } })}
                  className="flex-1 bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] text-white py-2 rounded-xl text-sm transition-all shadow-[0_0_10px_rgba(124,58,237,0.2)] flex items-center justify-center"
                >
                  Query with AI
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Folder Tree Modal */}
      {treeModalOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-[#0a0a0a] border border-[#262626] rounded-2xl w-full max-w-2xl max-h-[90vh] flex flex-col shadow-[0_0_30px_rgba(168,85,247,0.1)]">
            <div className="flex items-center justify-between p-4 border-b border-[#262626]">
              <div className="flex items-center">
                <FolderGit2 className="h-5 w-5 text-[#a855f7] mr-2" />
                <h3 className="text-lg font-semibold text-white">{selectedTreeProject}</h3>
              </div>
              <button 
                onClick={() => setTreeModalOpen(false)}
                className="text-gray-400 hover:text-white transition-colors p-1"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <div className="p-4 overflow-hidden flex flex-col flex-1">
              {loadingTree ? (
                <div className="flex flex-col items-center justify-center h-48 text-gray-400">
                  <Loader2 className="animate-spin h-8 w-8 mb-4" />
                  Loading project files...
                </div>
              ) : (
                <FolderTree treeData={treeData} />
              )}
            </div>
            
            <div className="p-4 border-t border-[#262626] flex justify-end">
              <button 
                onClick={() => {
                  setTreeModalOpen(false);
                  navigate('/chat', { state: { project: selectedTreeProject } });
                }}
                className="bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] text-white py-2 px-6 rounded-xl text-sm transition-all shadow-[0_0_10px_rgba(124,58,237,0.2)]"
              >
                Query with AI
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
