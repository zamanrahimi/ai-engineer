import React, { useState } from "react";

interface Props {
    onSend: (message: string) => void;
}

const ChatInput: React.FC<Props> = ({ onSend }) => {
    const [text, setText] = useState("");

    const handleSend = () => {
        if (text.trim() !== "") {
            onSend(text);
            setText("");
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") handleSend();
    };

    return (
        <div style={{ display: "flex", padding: "10px", gap: "10px" }}>
            <input
                style={{ flex: 1, padding: "10px", borderRadius: "10px", border: "1px solid #ccc" }}
                type="text"
                placeholder="Type a message..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyPress={handleKeyPress}
            />
            <button
                style={{
                    backgroundColor: "#10A37F",
                    color: "white",
                    border: "none",
                    padding: "10px 15px",
                    borderRadius: "10px",
                    cursor: "pointer",
                }}
                onClick={handleSend}
            >
                Send
            </button>
        </div>
    );
};

export default ChatInput;
