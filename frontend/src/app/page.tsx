"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import {
  Home, Compass, Library, History,
  Search, Paperclip, Sparkles, Image as ImageIcon,
  Microscope, Send, ChevronDown, Copy, Check
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";
import remarkGfm from "remark-gfm";

// Smart filter: strips complete <think>...</think> blocks
// and hides content from an unclosed <think> tag during streaming
function processContent(raw: string): string {
  // Remove fully closed think blocks
  let result = raw.replace(/<think>[\s\S]*?<\/think>/gi, "");
  // If there's still an unclosed <think>, hide everything from it onwards
  const openIdx = result.indexOf("<think>");
  if (openIdx !== -1) {
    result = result.substring(0, openIdx);
  }
  return result.trim();
}

function CopyButton({ text, label }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      style={{
        display: "flex",
        alignItems: "center",
        gap: "4px",
        padding: "4px 8px",
        borderRadius: "6px",
        background: copied ? "#dcfce7" : "#f1f5f9",
        color: copied ? "#166534" : "#64748b",
        border: "none",
        fontSize: "12px",
        cursor: "pointer",
        transition: "all 0.2s"
      }}
    >
      {copied ? <Check size={14} /> : <Copy size={14} />}
      {label && <span>{copied ? "Copied!" : label}</span>}
    </button>
  );
}

export default function App() {
  const [messages, setMessages] = useState<{ role: string, content: string }[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeChat, setActiveChat] = useState<string | null>(null);
  const chatPanelRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom on new messages or during streaming
  useEffect(() => {
    if (chatPanelRef.current) {
      chatPanelRef.current.scrollTop = chatPanelRef.current.scrollHeight;
    }
  }, [messages, isStreaming]);

  // Auto-resize textarea as content grows
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 300)}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage, { role: "assistant", content: "" }]);
    const currentInput = input;
    setInput("");
    setIsStreaming(true);

    try {
      const response = await fetch(`http://localhost:8000/chat/default/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: currentInput })
      });

      if (!response.body) return;
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            let content = line.replace("data: ", "");
            try {
              // Parse the JSON-encoded string from the backend
              content = JSON.parse(content);
            } catch (e) {
              // fallback if not valid JSON
            }
            assistantContent += content;
            setMessages(prev => {
              const newMessages = [...prev];
              newMessages[newMessages.length - 1].content = processContent(assistantContent);
              return newMessages;
            });
          }
        }
      }
    } catch (error) {
      console.error("Streaming error:", error);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="app-container">

      {/* Main Chat Area */}
      <main className="main-content">

        {/* Home View (Initial state) */}
        {messages.length === 0 ? (
          <div className="chat-panel">
            <div className="orb" style={{
              width: '80px', height: '80px', borderRadius: '50%', background: 'radial-gradient(circle at 30% 30%, #fff, #93c5fd 50%, #3b82f6)',
              boxShadow: '0 20px 40px -10px rgba(59,130,246,0.3)', marginBottom: '32px',
              animation: 'float 6s ease-in-out infinite'
            }}></div>
            <h1 style={{ fontSize: '36px', fontWeight: '700', letterSpacing: '-1px', textAlign: 'center' }}>
              Your AI <span style={{ color: '#6366f1' }}>Writing Companion</span> <br /> 
              Draft. Refine. <span style={{ color: '#6366f1' }}>Polish.</span>
            </h1>
          </div>
        ) : (
          <div ref={chatPanelRef} className="chat-panel" style={{ justifyContent: 'flex-start', paddingTop: '100px' }}>
            <div className="message-list">
              {messages.map((m, idx) => (
                <div key={idx} className="animate-in" style={{ padding: '0 20px' }}>
                  <div style={{ display: 'flex', gap: '16px' }}>
                    <div style={{
                      minWidth: '32px', height: '32px', borderRadius: '8px',
                      background: m.role === 'user' ? '#e2e8f0' : '#6366f1',
                      display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white'
                    }}>
                      {m.role === 'user' ? 'U' : <Sparkles size={16} />}
                    </div>
                    <div style={{ flex: 1, fontSize: '15px', lineHeight: '1.7', color: '#1e293b', minWidth: 0 }}>
                      {m.role === 'user' ? (
                        <span>{m.content}</span>
                      ) : m.content ? (
                        <div style={{ position: 'relative' }}>
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              code({ node, className, children, ...props }: any) {
                                const match = /language-(\w+)/.exec(className || '');
                                const isBlock = String(children).includes('\n');
                                const codeString = String(children).replace(/\n$/, '');
                                return isBlock ? (
                                  <div style={{ position: 'relative', margin: '16px 0' }}>
                                    <div style={{ position: 'absolute', top: '8px', right: '8px', zIndex: 10 }}>
                                      <CopyButton text={codeString} label="Copy Code" />
                                    </div>
                                    <SyntaxHighlighter
                                      style={oneLight as any}
                                      language={match ? match[1] : 'text'}
                                      PreTag="div"
                                      customStyle={{ 
                                        borderRadius: '12px', 
                                        fontSize: '13.5px', 
                                        padding: '16px', 
                                        border: '1px solid #e2e8f0',
                                        fontFamily: 'var(--font-mono)'
                                      }}
                                    >
                                      {codeString}
                                    </SyntaxHighlighter>
                                  </div>
                                ) : (
                                  <code style={{ background: '#f1f5f9', padding: '2px 6px', borderRadius: '4px', fontSize: '13px' }}>{children}</code>
                                );
                              },
                               h1({ children }: any) { return <h1 style={{ fontSize: '2.5rem', marginBottom: '1.5rem', color: '#0f172a' }}>{children}</h1>; },
                               h2({ children }: any) { return <h2 style={{ fontSize: '1.8rem', marginTop: '2rem', marginBottom: '1rem', color: '#1e293b' }}>{children}</h2>; },
                               h3({ children }: any) { return <h3 style={{ fontSize: '1.3rem', marginTop: '1.5rem', marginBottom: '0.75rem', color: '#334155' }}>{children}</h3>; },
                               p({ children }: any) { return <p style={{ margin: '12px 0', fontSize: '16px', lineHeight: '1.75' }}>{children}</p>; },
                               ul({ children }: any) { return <ul style={{ paddingLeft: '24px', margin: '12px 0' }}>{children}</ul>; },
                               ol({ children }: any) { return <ol style={{ paddingLeft: '24px', margin: '12px 0' }}>{children}</ol>; },
                               blockquote({ children }: any) { return <blockquote style={{ borderLeft: '4px solid #e2e8f0', paddingLeft: '16px', margin: '16px 0', color: '#64748b', fontStyle: 'italic' }}>{children}</blockquote>; },
                             }}
                           >
                             {m.content}
                           </ReactMarkdown>
                          {!isStreaming && (
                            <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                              <CopyButton text={m.content} label="Copy Full Response" />
                            </div>
                          )}
                        </div>
                      ) : (
                        <span style={{ color: '#94a3b8' }}>...</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Input Box */}
        <div className="chat-input-container">
          <div className="chat-input-box">
            <textarea
              ref={textareaRef}
              className="chat-input"
              placeholder="Paste your draft or describe what you want to write..."
              style={{ minHeight: '50px', maxHeight: '300px', overflowY: 'auto' }}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <div className="input-actions" style={{ justifyContent: 'flex-end' }}>
              <div style={{ display: 'none' }}>
                {/* Removed Reasoning, Image, Research, and Attachment as requested */}
              </div>
              <button
                onClick={handleSend}
                style={{
                  background: isStreaming ? '#e2e8f0' : '#6366f1',
                  color: 'white', border: 'none', borderRadius: '12px', padding: '8px 16px', cursor: 'pointer',
                  display: 'flex', alignItems: 'center', gap: '8px'
                }}
                disabled={isStreaming}
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </main>

      <style jsx global>{`
        @keyframes float {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
          100% { transform: translateY(0px); }
        }
      `}</style>
    </div>
  );
}
