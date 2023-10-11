import React, {useState} from 'react';
import {Box, TextField, IconButton, Grid} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import {getAuthUsername} from "./PrivateRoute";
import ResponsiveAppBar from "./ResponsiveAppBar";
import "../styles/Chat.css"


const Chat = () => {
    const [messages, setMessages] = useState<{text: String, isUser: boolean}[]>([]);
    const [messageText, setMessageText] = useState('');

    // const chatDisplayRef = useRef<HTMLDivElement | null>(null);
    //
    // useEffect(() => {
    //     // Scroll to the bottom of the chat display area whenever messages change
    //     if (chatDisplayRef.current) {
    //         chatDisplayRef.current.scrollTop = chatDisplayRef.current.scrollHeight;
    //     }
    // }, [messages]);

    const handleSendMessage = () => {
        if (messageText.trim() === '') {
            return;
        }
        const newMessage = {
            text: messageText,
            isUser: true // Change to false for robot responses
        };

        setMessages(prevMessages => Array.prototype.concat(prevMessages, [newMessage]));

        fetch('/chat', {
            method: 'POST',
            body: JSON.stringify({
                message: messageText,
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8'
            }
        }).then(res => {
            res.json().then(data => {
                    const robotResponse = {
                        text: data['robot_message'],
                        isUser: false
                    };
                    setMessages(prevMessages => Array.prototype.concat(prevMessages, [robotResponse]));
                }
            )
        }).then(() => setMessageText(''))
    };

    return (
        <>
            <ResponsiveAppBar />
            <div className={'user-chat-container'}>
                <div className={'user-chat-interface'}>
                    <Box p={2}>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <div className={'chat-display-box'}>
                                    {messages.map((message, index) => (
                                        <div
                                            key={index}
                                            className={message.isUser ? 'user-message' : 'robot-message'}
                                        >
                                            {message.isUser ?
                                                `${getAuthUsername()}: ${message.text}`
                                                : `Robot: ${message.text}`}
                                        </div>
                                    ))}
                                </div>
                            </Grid>
                        </Grid>
                    </Box>
                </div>

                <div className={'user-input-area'}>
                    <Box p={2}>
                        <Grid container spacing={2}>
                            <Grid item xs={10}>
                                <TextField
                                    fullWidth
                                    label="Type your message..."
                                    variant="outlined"
                                    value={messageText}
                                    onChange={(e) => setMessageText(e.target.value)}
                                    onKeyPress={(e) => {
                                        if (e.key === 'Enter') {
                                            handleSendMessage();
                                        }
                                    }}
                                />
                            </Grid>
                            <Grid item xs={2}>
                                <IconButton
                                    onClick={handleSendMessage}
                                    color="primary"
                                    aria-label="Send Message">
                                    <SendIcon fontSize={"large"} />
                                </IconButton>
                            </Grid>
                        </Grid>
                    </Box>
                </div>
            </div>
        </>

    );
};

export default Chat;
