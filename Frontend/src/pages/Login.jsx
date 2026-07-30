import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function Login() {

    const navigate = useNavigate();

    const { login } = useAuth();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);

    async function handleLogin(e) {

        e.preventDefault();

        setLoading(true);

        try {
          const response = await api.post("/login", {
            username,
            password,
        });

          

           
            login(response.data.access_token);

            navigate("/chat");

        } catch (err) {

            console.error(err);

            alert(
                err.response?.data?.detail ||
                "Invalid username or password."
            );

        } finally {

            setLoading(false);

        }

    }

    return (

        <div className="min-h-screen flex items-center justify-center bg-slate-950">

            <form
                onSubmit={handleLogin}
                className="bg-slate-900 p-8 rounded-xl w-96 shadow-xl"
            >

                <h1 className="text-3xl font-bold text-white mb-6">

                    Login

                </h1>

                <input
                    className="w-full mb-4 p-3 rounded bg-slate-800 text-white"
                    placeholder="Username"
                    value={username}
                    onChange={(e)=>setUsername(e.target.value)}
                />

                <input
                    type="password"
                    className="w-full mb-6 p-3 rounded bg-slate-800 text-white"
                    placeholder="Password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                />

                <button
                    disabled={loading}
                    className="w-full bg-cyan-600 hover:bg-cyan-700 py-3 rounded text-white font-semibold"
                >

                    {loading ? "Logging in..." : "Login"}

                </button>

                <p className="text-slate-400 mt-6 text-center">

                    Don't have an account?

                    <Link
                        to="/register"
                        className="text-cyan-400 ml-2"
                    >
                        Register
                    </Link>

                </p>

            </form>

        </div>

    );

}