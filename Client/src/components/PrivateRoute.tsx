import { Outlet, Navigate } from 'react-router-dom'


let auth = {'status': false, 'username': ''};

export const setAuth = (status: boolean, username: string) => {
    auth.status = status;
    auth.username = username;
    return Promise.resolve();
}

export const getAuthStatus = () => {
    return auth.status;
}

export const getAuthUsername = () => {
    return auth.username;
}

const PrivateRoute = () => {
    return (
        auth.status ? <Outlet /> : <Navigate to={'/login'} />
    )
}

export default PrivateRoute;