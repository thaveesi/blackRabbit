import { Routes, Route, Link } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Contracts from './components/Contracts'
import './App.css'

function App() {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md">
        <div className="p-4">
          <Link to="/" className="text-2xl font-bold text-blue-600">G</Link>
        </div>
        <nav className="mt-8">
          <Link to="/" className="block py-2 px-4 text-gray-600 hover:bg-gray-200">Dashboard</Link>
          <Link to="/contracts" className="block py-2 px-4 text-gray-600 hover:bg-gray-200">Contracts</Link>
          <Link to="/reports" className="block py-2 px-4 text-gray-600 hover:bg-gray-200">Reports</Link>
        </nav>
        <div className="mt-auto p-4">
          <Link to="/help" className="block py-2 text-gray-600 hover:text-gray-800">Help</Link>
          <Link to="/settings" className="block py-2 text-gray-600 hover:text-gray-800">Settings</Link>
          <button className="block py-2 text-gray-600 hover:text-gray-800">Log out</button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/contracts" element={<Contracts />} />
          {/* <Route path="/reports" element={<Reports />} /> */}
          {/* Add routes for Help and Settings if needed */}
        </Routes>
      </main>
    </div>
  )
}

export default App
