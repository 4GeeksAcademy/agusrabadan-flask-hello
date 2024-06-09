import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const Signup = () => {
    const { actions } = useContext(Context);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [errorMessage, setErrorMessage] = useState(""); // Para almacenar el mensaje de error
    const navigate = useNavigate();

    const handleEmailChange = (event) => setEmail(event.target.value);
    const handlePasswordChange = (event) => setPassword(event.target.value);
    const handleFirstNameChange = (event) => setFirstName(event.target.value);
    const handleLastNameChange = (event) => setLastName(event.target.value);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const dataToSend = { email, password, first_name: firstName, last_name: lastName };
        const url = `${process.env.BACKEND_URL}/api/signup`;

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        };

        try {
            const response = await fetch(url, options);
            if (response.status === 409) {
                // Usuario ya existe
                setErrorMessage("User already exists");
            } else if (!response.ok) {
                console.log('Error:', response.status, response.statusText);
                setErrorMessage("An error occurred. Please try again.");
            } else {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                actions.setIsLogin(true);
                actions.setCurrentUser({
                    email: data.email,
                    first_name: data.first_name,
                    last_name: data.last_name,
                    id: data.id
                });
                navigate('/dashboard');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            setErrorMessage("An error occurred. Please try again.");
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="card-title text-center mb-3 display-5">Create account</h2>
                            {errorMessage && <div className="alert alert-danger" role="alert">{errorMessage}</div>}
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
                                    <label htmlFor="firstName" className="mb-1">First Name:</label>
                                    <input type="text" className="form-control" id="firstName"
                                        value={firstName} onChange={handleFirstNameChange} required />
                                </div>
                                <div className="form-group mt-3 h6">
                                    <label htmlFor="lastName" className="mb-1">Last Name:</label>
                                    <input type="text" className="form-control" id="lastName"
                                        value={lastName} onChange={handleLastNameChange} required />
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
    );
};
