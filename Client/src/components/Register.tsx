import React from 'react';
import {useState, ChangeEvent, useEffect} from 'react';
import {Button, Stack, TextField} from "@mui/material";
import OutboundIcon from '@mui/icons-material/Outbound';
import {useNavigate} from "react-router-dom";


const Register = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmation, setConfirmation] = useState("");
    const [passwordError, setPasswordError] = useState(false);
    const [usernameError, setUsernameError] = useState(false);
    const navigate = useNavigate();

    const handleNameChange = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setUsername(e.target.value);
    }

    const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setPassword(e.target.value);
    }

    const handleConfirmationChange = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setConfirmation(e.target.value);
    }

    const handleClick = () => {
        if (confirmation !== password) {
            setPasswordError(true);
            return;
        } else {
            setPasswordError(false);
            console.log("posting");
            fetch("/register", {
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
                        setUsernameError(false);
                        navigate('/register-success');
                    } else {
                        setUsernameError(true);
                        console.log("Registration failed");
                    }
                })
            })
        }
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
                           error={usernameError}
                           helperText={usernameError ? "Username already exists" : null}
                           onChange={handleNameChange}></TextField>
                <TextField label={'Password'}
                           type={'password'}
                           variant={'outlined'}
                           style={{width: 300}}
                           onChange={handlePasswordChange}></TextField>
                <TextField label={'Confirm Password'}
                           type={'password'}
                           variant={'outlined'}
                           style={{width: 300}}
                           error={passwordError}
                           helperText={passwordError ? "Passwords do not match" : null}
                           onChange={handleConfirmationChange}></TextField>
                <Button variant={'contained'}
                        color={'primary'}
                        endIcon={<OutboundIcon />}
                        onClick={() => handleClick()}>Register</Button>
                &ensp;
            </Stack>
        </>
    )
}


export default Register;