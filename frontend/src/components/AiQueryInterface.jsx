import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Loader2, Send, FileCode, FolderGit2, MessageSquare, Code, FileText, Layers, CheckSquare, FileEdit, Zap, History, Plus, Trash2, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import api from '../services/api';

const MODES = [
  { id: 'chat', label: 'General Chat', endpoint: '/chat/', placeholder: 'Ask a question about your repository...', icon: MessageSquare },
  { id: 'review', label: 'Code Review', endpoint: '/review/', placeholder: 'e.g. Review the authentication flow...', icon: Code },
  { id: 'documentation', label: 'Generate Docs', endpoint: '/documentation/', placeholder: 'e.g. Generate docs for api/users.py...', icon: FileText },
  { id: 'architecture', label: 'Architecture', endpoint: '/architecture/', placeholder: 'e.g. Explain how the database connects...', icon: Layers },
  { id: 'tests', label: 'Unit Tests', endpoint: '/tests/', placeholder: 'e.g. Write tests for the login component...', icon: CheckSquare },
  { id: 'readme', label: 'README Gen', endpoint: '/readme/', placeholder: 'e.g. Write a comprehensive README for this project...', icon: FileEdit },
];

const AiQueryInterface = ({ title = "AI Workspace" }) => {
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const location = useLocation();
  const [selectedProject, setSelectedProject] = useState(location.state?.project || '');
  const [projects, setProjects] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [models, setModels] = useState([]);

  const [activeMode, setActiveMode] = useState(MODES[0]);

  // Chat History State
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [chatList, setChatList] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.get('/projects');
        setProjects(response.data.projects);
      } catch (error) {
        console.error("Failed to fetch projects", error);
      }
    };
    const fetchModels = async () => {
      try {
        const response = await api.get('/settings/models');
        setModels(response.data.models || []);
        if (response.data.models && response.data.models.length > 0) {
            setSelectedModel(response.data.models[0]);
        }
      } catch (error) {
        console.error("Failed to fetch models", error);
      }
    };
    fetchProjects();
    fetchModels();
    fetchChatList();
  }, []);

  const fetchChatList = async () => {
    try {
      const res = await api.get('/history');
      setChatList(res.data.chats);
    } catch (e) {
      console.error("Failed to fetch history", e);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [history, loading]);

  const saveChatHistory = async (messagesToSave, chatIdToUse = currentChatId) => {
    try {
      const res = await api.post('/history', {
        chat_id: chatIdToUse,
        title: null,
        messages: messagesToSave
      });
      if (res.data.success) {
        if (!chatIdToUse) {
          setCurrentChatId(res.data.chat_id);
        }
        fetchChatList(); // Refresh list to update titles/times
        return res.data.chat_id;
      }
    } catch (e) {
      console.error("Failed to save chat", e);
    }
    return chatIdToUse;
  };

  const loadChat = async (id) => {
    try {
      const res = await api.get(`/history/${id}`);
      setHistory(res.data.messages || []);
      setCurrentChatId(res.data.id);
    } catch (e) {
      console.error("Failed to load chat", e);
    }
  };

  const deleteChat = async (e, id) => {
    e.stopPropagation();
    if (window.confirm("Delete this chat?")) {
      try {
        await api.delete(`/history/${id}`);
        if (currentChatId === id) {
          startNewChat();
        } else {
          fetchChatList();
        }
      } catch (err) {
        console.error("Failed to delete chat", err);
      }
    }
  };

  const startNewChat = () => {
    setHistory([]);
    setCurrentChatId(null);
    setQuery('');
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim() || loading) return;

    const userMessage = { role: 'user', content: query, mode: activeMode };
    const newHistory = [...history, userMessage];
    setHistory(newHistory);
    setQuery('');
    setLoading(true);

    // Save immediately so user message is saved
    let activeChatId = await saveChatHistory(newHistory);

    try {
      const cleanHistory = newHistory.map(msg => ({ role: msg.role, content: msg.content }));
      const payload = { question: userMessage.content, history: cleanHistory };
      if (selectedProject) {
        payload.project = selectedProject;
      }
      if (selectedModel) {
        payload.model = selectedModel;
      }

      setHistory(prev => [...prev, { role: 'ai', content: '', sources: [], mode: activeMode }]);

      const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${baseUrl}${activeMode.endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      setLoading(false); // Stop thinking spinner once stream starts

      let finalContent = "";
      let finalSources = [];
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last element in the buffer because it might be incomplete (no newline yet)
        buffer = lines.pop();

        for (const line of lines) {
          if (line.trim() === '') continue;
          try {
            const data = JSON.parse(line);
            if (data.sources) {
              finalSources = data.sources;
              setHistory(prev => {
                const updated = [...prev];
                const lastIdx = updated.length - 1;
                updated[lastIdx] = { ...updated[lastIdx], sources: finalSources };
                return updated;
              });
            }
            if (data.chunk) {
              finalContent += data.chunk;
              setHistory(prev => {
                const updated = [...prev];
                const lastIdx = updated.length - 1;
                updated[lastIdx] = { ...updated[lastIdx], content: updated[lastIdx].content + data.chunk };
                return updated;
              });
            }
          } catch (e) {
            console.error("Error parsing JSON chunk", e);
          }
        }
      }

      // Save again once stream is fully done
      const completedHistory = [...newHistory, { role: 'ai', content: finalContent, sources: finalSources, mode: activeMode }];
      saveChatHistory(completedHistory, activeChatId);

    } catch (err) {
      console.error(err);
      const errorHistory = [...newHistory, { role: 'ai', content: '❌ **Error:** Failed to reach the AI backend.' }];
      setHistory(errorHistory);
      saveChatHistory(errorHistory, activeChatId);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (mode) => {
    setActiveMode(mode);
    setQuery(`Can you please ${mode.label.toLowerCase()} for my project?`);
  };

  return (
    <div className="h-full flex overflow-hidden">

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64 border-r border-[#262626]' : 'w-0 border-r-0'} transition-all duration-300 flex flex-col bg-[#0a0a0a] overflow-hidden flex-shrink-0`}>
        <div className="p-4 border-b border-[#262626]">
          <button
            onClick={startNewChat}
            className="w-full flex items-center justify-center bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] text-white py-2 rounded-xl font-medium transition-all text-sm whitespace-nowrap shadow-[0_0_10px_rgba(124,58,237,0.2)]"
          >
            <Plus className="h-4 w-4 mr-2" /> New Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {chatList.length === 0 ? (
            <p className="text-gray-500 text-xs text-center mt-4 whitespace-nowrap">No history yet.</p>
          ) : (
            chatList.map(chat => (
              <div
                key={chat.id}
                onClick={() => loadChat(chat.id)}
                className={`group flex items-center justify-between p-2 rounded-lg cursor-pointer transition-colors text-sm ${currentChatId === chat.id ? 'bg-[#171717] border border-[#262626]' : 'hover:bg-[#171717] border border-transparent'
                  }`}
              >
                <div className="flex items-center overflow-hidden w-full">
                  <MessageSquare className="h-4 w-4 text-gray-400 mr-2 flex-shrink-0" />
                  <span className="text-gray-300 truncate w-full">{chat.title}</span>
                </div>
                <button
                  onClick={(e) => deleteChat(e, chat.id)}
                  className="text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity p-1 ml-1 flex-shrink-0"
                  title="Delete Chat"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative min-w-0">
        <div className="flex items-center justify-between p-4 border-b border-[#262626] flex-wrap gap-4 bg-[#050505]">
          <div className="flex items-center">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="mr-3 text-gray-400 hover:text-white transition-colors p-1"
              title="Toggle Sidebar"
            >
              {sidebarOpen ? <PanelLeftClose className="h-5 w-5" /> : <PanelLeftOpen className="h-5 w-5" />}
            </button>
            <h2 className="text-xl font-bold text-white flex items-center">
              <Zap className="text-[#a855f7] mr-2 h-5 w-5" />
              {title}
            </h2>
          </div>

          <div className="flex items-center space-x-4">
            {/* Mode Selector */}
            <div className="flex items-center bg-[#0a0a0a] border border-[#262626] rounded-xl px-3 py-1.5 flex-shrink-0">
              <activeMode.icon className="h-4 w-4 text-[#a855f7] mr-2" />
              <select
                value={activeMode.id}
                onChange={(e) => setActiveMode(MODES.find(m => m.id === e.target.value))}
                className="bg-transparent text-sm text-white focus:outline-none cursor-pointer"
              >
                {MODES.map(m => (
                  <option key={m.id} value={m.id} className="bg-[#0a0a0a]">{m.label}</option>
                ))}
              </select>
            </div>

            {/* Project Selector */}
            <div className="flex items-center bg-[#0a0a0a] border border-[#262626] rounded-xl px-3 py-1.5 flex-shrink-0">
              <FolderGit2 className="h-4 w-4 text-gray-400 mr-2" />
              <select
                value={selectedProject}
                onChange={(e) => setSelectedProject(e.target.value)}
                className="bg-transparent text-sm text-white focus:outline-none cursor-pointer"
              >
                <option value="" className="bg-[#0a0a0a]">All Projects</option>
                {projects.map(p => (
                  <option key={p.name} value={p.name} className="bg-[#0a0a0a]">{p.name}</option>
                ))}
              </select>
            </div>

            {/* Model Selector */}
            {models.length > 0 && (
              <div className="flex items-center bg-[#0a0a0a] border border-[#262626] rounded-xl px-3 py-1.5 flex-shrink-0">
                <Zap className="h-4 w-4 text-gray-400 mr-2" />
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="bg-transparent text-sm text-white focus:outline-none cursor-pointer"
                >
                  <option value="" className="bg-[#0a0a0a]">Default Model</option>
                  {models.map(m => (
                    <option key={m} value={m} className="bg-[#0a0a0a]">{m}</option>
                  ))}
                </select>
              </div>
            )}
          </div>
        </div>

        <div className="flex-1 bg-[#050505] flex flex-col overflow-hidden relative">

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {history.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center max-w-2xl mx-auto px-4">
                <MessageSquare className="h-16 w-16 text-gray-600 mb-6" />
                <h3 className="text-2xl font-semibold text-white mb-2">Welcome to your AI Workspace</h3>
                <p className="text-gray-400 mb-8">
                  Select a project and a mode to start querying your codebase. What would you like to do?
                </p>

                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 w-full">
                  {MODES.slice(1).map((mode) => (
                    <button
                      key={mode.id}
                      onClick={() => handleQuickAction(mode)}
                      className="flex flex-col items-center p-4 bg-[#0a0a0a] border border-[#262626] rounded-xl hover:border-[#a855f7] hover:bg-[#171717] hover:shadow-[0_0_15px_rgba(168,85,247,0.1)] transition-all group"
                    >
                      <mode.icon className="h-8 w-8 text-gray-400 group-hover:text-[#a855f7] mb-3 transition-colors" />
                      <span className="text-sm font-medium text-gray-300 group-hover:text-white text-center">{mode.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              history.map((msg, idx) => (
                <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                  <div className={`max-w-[95%] lg:max-w-[85%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-[#7c3aed]/20 text-white border border-[#7c3aed]/30' : 'bg-[#0a0a0a]/80 border border-[#262626] text-gray-300 backdrop-blur-sm shadow-md'
                    }`}>

                    {/* Mode Badge for AI Responses */}
                    {msg.role === 'ai' && msg.mode && (
                      <div className="flex items-center text-xs font-semibold text-[#a855f7] mb-2 uppercase tracking-wider">
                        {(() => {
                          const MsgIcon = MODES.find(m => m.id === (msg.mode.id || msg.mode))?.icon || MessageSquare;
                          return <MsgIcon className="h-3 w-3 mr-1.5" />;
                        })()}
                        {msg.mode.label || 'AI'}
                      </div>
                    )}

                    <div className="prose prose-invert max-w-none overflow-hidden">
                      {msg.role === 'user' ? (
                        <p className="m-0 whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        <ReactMarkdown
                          components={{
                            code({ node, inline, className, children, ...props }) {
                              const match = /language-(\w+)/.exec(className || '')
                              const language = match ? match[1] : '';

                              return !inline && match ? (
                                <div className="relative mt-4 mb-4">
                                  {language === 'diff' && (
                                    <div className="absolute top-0 right-0 bg-[#262626] text-gray-300 text-[10px] uppercase font-bold px-3 py-1 rounded-bl-lg rounded-tr-xl z-10">
                                      Code Diff Suggestion
                                    </div>
                                  )}
                                  <SyntaxHighlighter
                                    {...props}
                                    children={String(children).replace(/\n$/, '')}
                                    style={vscDarkPlus}
                                    language={language}
                                    PreTag="div"
                                    wrapLines={language === 'diff'}
                                    lineProps={(lineNumber) => {
                                      if (language !== 'diff') return {};
                                      const line = String(children).split('\n')[lineNumber - 1];
                                      if (line.startsWith('+')) {
                                        return { style: { display: 'block', backgroundColor: 'rgba(34, 197, 94, 0.15)', width: '100%' } };
                                      } else if (line.startsWith('-')) {
                                        return { style: { display: 'block', backgroundColor: 'rgba(239, 68, 68, 0.15)', width: '100%' } };
                                      }
                                      return { style: { display: 'block', width: '100%' } };
                                    }}
                                    className={`rounded-xl !bg-[#050505] !border !border-[#262626] max-w-full overflow-x-auto shadow-inner ${language === 'diff' ? 'pt-8' : ''}`}
                                  />
                                </div>
                              ) : (
                                <code {...props} className="bg-[#171717] px-1.5 py-0.5 rounded text-sm font-mono text-[#c084fc] border border-[#262626]">
                                  {children}
                                </code>
                              )
                            }
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      )}
                    </div>

                    {/* Sources Dropdown */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-[#262626]">
                        <details className="text-xs text-gray-400 group">
                          <summary className="cursor-pointer hover:text-gray-300 flex items-center outline-none">
                            <FileCode className="h-4 w-4 mr-1 inline text-[#a855f7]" />
                            <span>View {msg.sources.length} sources used</span>
                          </summary>
                          <div className="mt-2 space-y-2 max-h-48 overflow-y-auto pr-2">
                            {msg.sources.map((src, i) => (
                              <div key={i} className="bg-[#050505] p-2 rounded-xl border border-[#262626]">
                                <p className="font-mono text-[#a855f7] mb-1">{src.metadata?.file}</p>
                                <pre className="whitespace-pre-wrap font-mono text-[10px] text-gray-500 bg-black p-2 rounded-lg overflow-x-auto border border-[#171717]">
                                  {src.content.substring(0, 150)}...
                                </pre>
                              </div>
                            ))}
                          </div>
                        </details>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {loading && (
              <div className="flex items-start">
                <div className="bg-[#0a0a0a] border border-[#262626] rounded-2xl p-4 flex items-center text-gray-400 shadow-md">
                  <Loader2 className="animate-spin h-5 w-5 mr-3 text-[#a855f7]" />
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 bg-[#050505] border-t border-[#262626]">
            <form onSubmit={handleSubmit} className="relative flex items-center max-w-4xl mx-auto">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-[#121212] border border-[#262626] rounded-2xl py-4 pl-5 pr-14 text-white focus:outline-none focus:border-[#a855f7] focus:ring-1 focus:ring-[#a855f7] transition-all shadow-inner"
                placeholder={`${activeMode.placeholder} (Use @filename to include specific files)`}
                disabled={loading}
              />
              <button
                type="submit"
                disabled={!query.trim() || loading}
                className="absolute right-2 p-2.5 bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] disabled:from-gray-700 disabled:to-gray-800 text-white rounded-xl transition-all shadow-[0_0_10px_rgba(124,58,237,0.2)]"
              >
                <Send className="h-5 w-5" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AiQueryInterface;
