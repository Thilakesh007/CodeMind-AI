import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Save, Database, Moon, Sun, Loader2, CheckCircle2 } from 'lucide-react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

const Settings = () => {
  const [ollamaHost, setOllamaHost] = useState('');
  const [primaryModel, setPrimaryModel] = useState('');
  const [aiProvider, setAiProvider] = useState('ollama');
  const [openaiApiKey, setOpenaiApiKey] = useState('');
  const [anthropicApiKey, setAnthropicApiKey] = useState('');
  const [geminiApiKey, setGeminiApiKey] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState(null);
  
  // Theme state
  const [isLightMode, setIsLightMode] = useState(document.body.classList.contains('light-theme'));
  
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await api.get('/settings');
        setOllamaHost(response.data.ollama_host);
        setPrimaryModel(response.data.primary_model);
        setAiProvider(response.data.ai_provider || 'ollama');
        setOpenaiApiKey(response.data.openai_api_key || '');
        setAnthropicApiKey(response.data.anthropic_api_key || '');
        setGeminiApiKey(response.data.gemini_api_key || '');
      } catch (error) {
        console.error("Failed to fetch settings", error);
      } finally {
        setLoading(false);
      }
    };
    fetchSettings();
  }, []);

  const handleSaveSettings = async () => {
    setSaving(true);
    setSaveMessage(null);
    try {
      await api.post('/settings', {
        ollama_host: ollamaHost,
        primary_model: primaryModel,
        ai_provider: aiProvider,
        openai_api_key: openaiApiKey,
        anthropic_api_key: anthropicApiKey,
        gemini_api_key: geminiApiKey
      });
      setSaveMessage({ type: 'success', text: 'Settings saved successfully!' });
      setTimeout(() => setSaveMessage(null), 3000);
    } catch (error) {
      console.error("Failed to save settings", error);
      setSaveMessage({ type: 'error', text: 'Failed to save settings.' });
    } finally {
      setSaving(false);
    }
  };

  const handleClearDatabase = async () => {
    if (window.confirm("Are you absolutely sure? This will delete all your indexed projects and ChromaDB vectors. This action cannot be undone.")) {
      try {
        await api.post('/settings/clear-db');
        alert("Database cleared successfully!");
        navigate('/'); // Redirect to home so they see it's empty
      } catch (error) {
        console.error("Failed to clear database", error);
        alert("Failed to clear database. Check console for details.");
      }
    }
  };

  const toggleTheme = (lightMode) => {
    setIsLightMode(lightMode);
    if (lightMode) {
      document.body.classList.add('light-theme');
    } else {
      document.body.classList.remove('light-theme');
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400">
        <Loader2 className="animate-spin h-8 w-8 mr-3" />
        Loading settings...
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto pb-10">
      <div className="flex items-center mb-8 border-b border-[#262626] pb-4">
        <SettingsIcon className="h-8 w-8 text-[#a855f7] mr-3" />
        <h2 className="text-3xl font-bold text-white">Settings</h2>
      </div>

      <div className="space-y-8">
        

        {/* Database Management */}
        <div className="bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl p-6 transition-all hover:border-[#a855f7] hover:shadow-[0_0_15px_rgba(168,85,247,0.1)] backdrop-blur-md">
          <div className="flex items-center mb-4">
            <Database className="h-5 w-5 text-[#a855f7] mr-2" />
            <h3 className="text-xl font-semibold text-white">Vector Database</h3>
          </div>
          <p className="text-sm text-gray-400 mb-4">Manage your ChromaDB embedding storage. Clearing the database will remove all indexed repositories permanently.</p>
          <button 
            onClick={handleClearDatabase}
            className="bg-red-900 bg-opacity-30 border border-red-800 text-red-400 hover:bg-opacity-50 px-6 py-2.5 rounded-xl font-medium transition-colors text-sm flex items-center"
          >
            Clear Database
          </button>
        </div>

        {/* Appearance */}
        <div className="bg-[#0a0a0a]/80 border border-[#262626] rounded-2xl p-6 transition-all hover:border-[#a855f7] hover:shadow-[0_0_15px_rgba(168,85,247,0.1)] backdrop-blur-md">
          <h3 className="text-xl font-semibold text-white mb-4">Appearance</h3>
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => toggleTheme(false)}
              className={`flex items-center px-6 py-2.5 rounded-xl font-medium text-sm transition-all ${
                !isLightMode 
                  ? "bg-[#a855f7]/20 border border-[#a855f7] text-[#a855f7] shadow-[0_0_10px_rgba(168,85,247,0.2)]" 
                  : "bg-[#121212] border border-[#262626] text-gray-400 hover:text-gray-300"
              }`}
            >
              <Moon className="h-4 w-4 mr-2" />
              Dark Mode {!isLightMode && "(Active)"}
            </button>
            <button 
              onClick={() => toggleTheme(true)}
              className={`flex items-center px-6 py-2.5 rounded-xl font-medium text-sm transition-all ${
                isLightMode 
                  ? "bg-[#a855f7]/20 border border-[#a855f7] text-[#a855f7] shadow-[0_0_10px_rgba(168,85,247,0.2)]" 
                  : "bg-[#121212] border border-[#262626] text-gray-400 hover:text-gray-300"
              }`}
            >
              <Sun className="h-4 w-4 mr-2" />
              Light Mode {isLightMode && "(Active)"}
            </button>
          </div>
        </div>

        <div className="flex justify-between items-center mt-8">
          <div>
            {saveMessage && (
              <div className={`flex items-center text-sm ${saveMessage.type === 'success' ? 'text-green-400' : 'text-red-400'}`}>
                {saveMessage.type === 'success' && <CheckCircle2 className="h-4 w-4 mr-2" />}
                {saveMessage.text}
              </div>
            )}
          </div>
          <button 
            onClick={handleSaveSettings}
            disabled={saving}
            className="flex items-center bg-gradient-to-r from-[#7c3aed] to-[#4c1d95] hover:from-[#8b5cf6] hover:to-[#5b21b6] disabled:opacity-50 text-white px-8 py-3 rounded-xl font-medium transition-all shadow-[0_0_10px_rgba(124,58,237,0.2)]"
          >
            {saving ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Save className="h-4 w-4 mr-2" />}
            Save Settings
          </button>
        </div>

      </div>
    </div>
  );
};

export default Settings;
