import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Navbar() {

    const navigate = useNavigate();

    const { logout } = useAuth();

    function handleLogout() {

        logout();

        navigate("/login");

    }

    return (

        <div className="h-16 border-b border-slate-700 bg-slate-900 flex items-center justify-between px-6">

            <h1 className="text-white font-semibold text-lg">

                Production RAG

            </h1>

            <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition"
            >

                Logout

            </button>

        </div>

    );

}