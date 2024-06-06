import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext.js";
import { Home } from "../pages/home.js";
import { useNavigate } from "react-router-dom";


export const Dashboard = () => {
    const { store } = useContext(Context)
    const navigate = useNavigate()

    useEffect(() => {
        if (!store.isLogin) {
            navigate('/')
        }
    }, [])



    return (
        <div>
            <h1>ESTAS LOGUEADO, PAGINA RESTRINGIDA</h1>
            <div class="spinner-grow text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-secondary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-success" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-danger" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-warning" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-info" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-light" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-dark" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    )
}


export default Dashboard

