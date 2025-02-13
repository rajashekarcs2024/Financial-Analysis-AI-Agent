import React, { useState, useRef, useEffect } from 'react';
import { Card } from "../components/ui/card";
import { Mic, MicOff, Send, Settings, Loader, BrainCircuit, Clock } from 'lucide-react';

const OptimusPrime = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim() || isProcessing) return;

    // Add user message
    const userMessage = {
        type: 'user',
        content: inputText,
        timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsProcessing(true);

    try {
        // Send request
        await fetch('/api/send-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: inputText }),
        });

        // Poll for response
        const pollInterval = setInterval(async () => {
            try {
                const responseData = await fetch('/api/get-response');
                const data = await responseData.json();

                if (data.status !== 'waiting' && data.analysis_result) {
                    clearInterval(pollInterval);
                    setIsProcessing(false);

                    // Check if we have the expected data structure
                    if (data.analysis_result && data.analysis_result.analysis) {
                        // Add agent responses
                        data.analysis_result.analysis.forEach(response => {
                            if (response) {  // Add null check
                                setMessages(prev => [...prev, {
                                    type: 'agent',
                                    agentName: response.name || 'Agent',
                                    content: response.content || 'No content available',
                                    timestamp: new Date().toLocaleTimeString()
                                }]);
                            }
                        });
                    }
                }
            } catch (error) {
                clearInterval(pollInterval);
                setIsProcessing(false);
                console.error('Error polling response:', error);
            }
        }, 1000);

    } catch (error) {
        setIsProcessing(false);
        setMessages(prev => [...prev, {
            type: 'error',
            content: 'Failed to send message. Please try again.',
            timestamp: new Date().toLocaleTimeString()
        }]);
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // Voice recording functionality will be added later
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <div className="flex h-[800px]">
        {/* Main Chat Interface */}
        <div className="flex-1 flex flex-col">
          <Card className="p-4 flex-1 flex flex-col">
            {/* Chat Header */}
            <div className="flex justify-between items-center mb-4 pb-4 border-b">
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-6 h-6 text-blue-500" />
                <h1 className="text-xl font-semibold">Financial Analysis Assistant</h1>
              </div>
              <button className="p-2 hover:bg-gray-100 rounded-full">
                <Settings className="w-5 h-5" />
              </button>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto space-y-4 mb-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-blue-500 text-white'
                        : message.type === 'error'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-gray-100'
                    }`}
                  >
                    {message.type === 'agent' && (
                      <div className="text-sm text-gray-500 mb-1">
                        {message.agentName}
                      </div>
                    )}
                    <p className="whitespace-pre-wrap">{message.content}</p>
                    <div className="text-xs mt-1 opacity-70 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {message.timestamp}
                    </div>
                  </div>
                </div>
              ))}
              {isProcessing && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-3 rounded-lg flex items-center gap-2">
                    <Loader className="w-4 h-4 animate-spin" />
                    Processing your request...
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t pt-4">
              <div className="flex gap-2">
                <button
                  onClick={toggleRecording}
                  className={`p-3 rounded-full transition-colors ${
                    isRecording ? 'bg-red-500 text-white' : 'hover:bg-gray-100'
                  }`}
                >
                  {isRecording ? (
                    <MicOff className="w-5 h-5" />
                  ) : (
                    <Mic className="w-5 h-5" />
                  )}
                </button>
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Type your message..."
                  className="flex-1 p-3 border rounded-lg"
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  disabled={isProcessing}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isProcessing || !inputText.trim()}
                  className="p-3 bg-blue-500 text-white rounded-lg flex items-center gap-2 disabled:opacity-50"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default OptimusPrime;