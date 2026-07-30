import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/axios";

export default function Register() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);

    async function handleRegister(e) {

        e.preventDefault();

        setLoading(true);

        try {

            await api.post("/register", {

                username,

                email,

                password

            });

            alert("Registration successful!");

            navigate("/login");

        } catch (err) {

            console.error(err);

            alert(
                err.response?.data?.detail ||
                "Registration failed."
            );

        } finally {

            setLoading(false);

        }

    }

    return (

        <div className="min-h-screen flex items-center justify-center bg-slate-950">

            <form
                onSubmit={handleRegister}
                className="bg-slate-900 p-8 rounded-xl w-96 shadow-xl"
            >

                <h1 className="text-3xl text-white font-bold mb-6">

                    Register

                </h1>

                <input
                    className="w-full mb-4 p-3 rounded bg-slate-800 text-white"
                    placeholder="Username"
                    value={username}
                    onChange={(e)=>setUsername(e.target.value)}
                />

                <input
                    className="w-full mb-4 p-3 rounded bg-slate-800 text-white"
                    placeholder="Email"
                    value={email}
                    onChange={(e)=>setEmail(e.target.value)}
                />

                <input
                    type="password"
                    className="w-full mb-6 p-3 rounded bg-slate-800 text-white"
                    placeholder="Password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                />

                <button
                    className="w-full bg-cyan-600 hover:bg-cyan-700 py-3 rounded text-white font-semibold"
                    disabled={loading}
                >

                    {loading ? "Registering..." : "Register"}

                </button>

                <p className="text-slate-400 mt-6 text-center">

                    Already have an account?

                    <Link
                        to="/login"
                        className="text-cyan-400 ml-2"
                    >
                        Login
                    </Link>

                </p>

            </form>

        </div>

    );

}