import React from "react";
import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const Signup = () => {

    const { actions } = useContext(Context)
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [first_name, setName] = useState("");
    const [last_name, setLastName] = useState("");
    const navigate = useNavigate();

    const handleEmailChange = (event) => { setEmail(event.target.value); };
    const handlePasswordChange = (event) => { setPassword(event.target.value); };
    const handleNameChange = (event) => { setName(event.target.value); };
    const handleLastNameChange = (event) => { setLastName(event.target.value); };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const dataToSend = { email, password, first_name, last_name };
        const url = `${process.env.BACKEND_URL}/api/signup`;
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        };
        const response = await fetch(url, options)
        console.log(response)
        if (!response.ok) {
            console.log('Error: ', response.status, response.statusText)
            return
        }
        const data = await response.json()
        console.log(data);
        // Aquí comienza nuestra lógica
        localStorage.setItem('token', data.access_token)
        actions.setIsLogin(true)
        navigate('/dashboard')

    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="card-title text-center mb-3 display-5">Create account</h2>
                            <form onSubmit={handleSubmit}>
                                <div className="form-group mt-3 h6">
                                    <label htmlFor="email" className="mb-1">Email:</label>
                                    <input type="email" className="form-control" id="email"
                                        value={email} onChange={handleEmailChange} required />
                                </div>
                                <div className="form-group mt-3 h6">
                                    <label htmlFor="password" className="mb-1">Password:</label>
                                    <input type="password" className="form-control" id="password"
                                        value={password} onChange={handlePasswordChange} required />
                                </div>
                                <div className="form-group mt-3 h6">
                                    <label htmlFor="name" className="mb-1">Name:</label>
                                    <input type="text" className="form-control" id="name"
                                        value={first_name} onChange={handleNameChange} required />
                                </div>
                                <div className="form-group mt-3 h6">
                                    <label htmlFor="lastName" className="mb-1">Last Name:</label>
                                    <input type="text" className="form-control" id="lastName"
                                        value={last_name} onChange={handleLastNameChange} required />
                                </div>
                                <div className="text-center">
                                    <button type="submit" className="btn btn-primary mt-5">Create account</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}