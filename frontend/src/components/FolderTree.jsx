import React, { useState } from 'react';
import { ChevronRight, ChevronDown, Folder, File, Code, FileText, Image as ImageIcon } from 'lucide-react';

const getFileIcon = (filename) => {
  const ext = filename.split('.').pop().toLowerCase();
  
  if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'].includes(ext)) return <ImageIcon className="h-4 w-4 text-[#a855f7]" />;
  if (['md', 'txt', 'csv'].includes(ext)) return <FileText className="h-4 w-4 text-gray-400" />;
  if (['js', 'jsx', 'ts', 'tsx', 'py', 'java', 'cpp', 'c', 'html', 'css', 'json'].includes(ext)) return <Code className="h-4 w-4 text-[#c084fc]" />;
  
  return <File className="h-4 w-4 text-gray-400" />;
};

const TreeNode = ({ node, level = 0 }) => {
  const [isOpen, setIsOpen] = useState(level === 0); // Open root by default
  const isFolder = node.type === 'folder';

  return (
    <div className="w-full">
      <div 
        className={`flex items-center py-1 hover:bg-[#171717] cursor-pointer rounded px-1 transition-colors`}
        style={{ paddingLeft: `${level * 16 + 4}px` }}
        onClick={() => isFolder && setIsOpen(!isOpen)}
      >
        {isFolder ? (
          <div className="flex items-center text-gray-300">
            {isOpen ? <ChevronDown className="h-4 w-4 mr-1 text-gray-500" /> : <ChevronRight className="h-4 w-4 mr-1 text-gray-500" />}
            <Folder className={`h-4 w-4 mr-2 ${isOpen ? 'text-[#a855f7]' : 'text-gray-400'}`} fill={isOpen ? '#a855f7' : 'none'} />
            <span className="text-sm select-none">{node.name}</span>
          </div>
        ) : (
          <div className="flex items-center text-gray-300 pl-5">
            <span className="mr-2">{getFileIcon(node.name)}</span>
            <span className="text-sm select-none">{node.name}</span>
          </div>
        )}
      </div>

      {isFolder && isOpen && node.children && (
        <div className="flex flex-col">
          {node.children.map((child, index) => (
            <TreeNode key={`${child.name}-${index}`} node={child} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

const FolderTree = ({ treeData }) => {
  if (!treeData) {
    return <div className="text-gray-500 text-sm italic">No folder structure available.</div>;
  }

  return (
    <div className="w-full bg-[#0a0a0a] border border-[#262626] rounded-xl p-3 overflow-x-auto max-h-[600px] overflow-y-auto shadow-inner">
      <TreeNode node={treeData} />
    </div>
  );
};

export default FolderTree;
