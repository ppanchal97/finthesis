import React, { useState } from 'react';
import { DeepChat } from 'deep-chat-react';
import dynamic from "next/dynamic";
import { text } from 'stream/consumers';

interface Message {
    text: string;
    isUser: boolean;
}

interface NewsTextProps {
    title: string;
    description: string;
    fullText: string;
}

const QAComponent: React.FC<NewsTextProps> = ({ title, description, fullText }) => {
    const DeepChat = dynamic(
        () => import("deep-chat-react").then((mod) => mod.DeepChat),
        {
            ssr: false,
        },
    );

    return (
        <div className="flex items-center mt-auto">
            <DeepChat
                directConnection={{
                    openAI: { key: "api-key" }
                }}
                style={{
                    backgroundColor: '#191B1E',
                    width: '100%',
                    fontSize: '16px',
                    height: '450px',
                    borderRadius: '15px',
                    alignItems: 'center'
                }}
                textInput={{
                    styles: {
                        container: {
                            'backgroundColor': '#191B1E',
                            'color': '#ffffff',
                            'height': '50px',
                            'borderRadius': '20px',
                            'alignItems': 'center',
                        }
                    }
                }}
            />
        </div>
    );
};

export default QAComponent;
