import React from 'react';
import {useState, ChangeEvent} from 'react';
import {Button, Stack, TextField} from "@mui/material";
import OutboundIcon from '@mui/icons-material/Outbound';
import {useNavigate} from "react-router-dom";
import {setAuth} from "./PrivateRoute";


const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false);
    const navigate = useNavigate();

    const handleNameChange = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setUsername(e.target.value);
    }

    const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setPassword(e.target.value);
    }

    const handleClick = () => {
        console.log("posting");
        fetch("/login", {
            method: "POST",
            body: JSON.stringify({
                username: username,
                password: password
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(r => {
            r.json().then(data => {
                if (data['status']) {
                    setAuth(true, username).then(() => {
                        navigate('/chat');
                    })
                } else {
                    console.log("Login failed");
                    setError(true);
                }
            })
        })
    }

    return (
        <>
            <Stack direction={'column'}
                   alignItems={'center'}
                   justifyContent={'center'}
                   style={{border: 'groove', width: 400}}
                   display={'flex'}
                   spacing={3}>
                &ensp;
                <TextField label={'Username'}
                           variant={'outlined'}
                           style={{width: 300}}
                           error={error}
                           onChange={handleNameChange}></TextField>
                <TextField label={'Password'}
                           type={'password'}
                           variant={'outlined'}
                           style={{width: 300}}
                           error={error}
                           helperText={error ? "Incorrect username and/or password" : null}
                           onChange={handlePasswordChange}></TextField>
                <Button variant={'contained'}
                        color={'primary'}
                        endIcon={<OutboundIcon />}
                        onClick={() => handleClick()}>Login</Button>
                &ensp;
            </Stack>
        </>
    )
}

export default Login;