import React from 'react'
import {Button, Stack, TextField} from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import {useNavigate} from "react-router-dom";

const Welcome = () => {

    const navigate = useNavigate();
    const handleClick = () => {
        navigate('/chat');
    }

    return (
        <Stack direction={'column'}
               alignItems={'center'}
               justifyContent={'center'}
               display={'flex'}
               spacing={3}>
            <h1>Welcome to React Client</h1>
            <Button
                variant={'contained'}
                color={'primary'}
                endIcon={<SearchIcon />}
                onClick={handleClick}>Chat and Search</Button>
        </Stack>
    )
}

export default Welcome;