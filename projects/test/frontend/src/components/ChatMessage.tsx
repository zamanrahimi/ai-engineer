import React from "react";
import { Message } from "../types";

interface Props {
    message: Message;
}

const ChatMessage: React.FC<Props> = ({ message }) => {
    const isUser = message.sender === "user";
    return (
        <div
            style={{
                display: "flex",
                justifyContent: isUser ? "flex-end" : "flex-start",
                padding: "5px",
            }}
        >
            <div
                style={{
                    backgroundColor: isUser ? "#10A37F" : "#F1F1F1",
                    color: isUser ? "white" : "black",
                    padding: "10px 15px",
                    borderRadius: "15px",
                    maxWidth: "70%",
                    wordBreak: "break-word",
                }}
            >
                {message.text}
            </div>
        </div>
    );
};

export default ChatMessage;
