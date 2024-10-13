import { Routes, Route, Link } from 'react-router-dom'
import { FiHome, FiFileText, FiFile } from 'react-icons/fi' // Importing icons
import Dashboard from './components/Dashboard'
import Contracts from './components/Contracts'
import ContractDetails from './components/ContractDetails'
import ReportDetails from './components/ReportDetails'
import Reports from './components/Reports'
import './App.css'

function App() {
  return (
    <div className="flex h-screen bg-white-100">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-100 shadow-md flex flex-col">
        <div className="p-4">
          <Link to="/" className="text-2xl font-bold text-blue-600">MAS</Link>
        </div>
        <nav className="mt-8 flex-1">
          <Link to="/" className="flex items-center py-2 px-4 text-gray-600 hover:bg-gray-200">
            <FiHome className="mr-2" /> {/* Icon for Dashboard */}
            Dashboard
          </Link>
          <Link to="/contracts" className="flex items-center py-2 px-4 text-gray-600 hover:bg-gray-200">
            <FiFile className="mr-2" /> {/* Icon for Contracts */}
            Contracts
          </Link>
          <Link to="/reports" className="flex items-center py-2 px-4 text-gray-600 hover:bg-gray-200">
            <FiFileText className="mr-2" /> {/* Icon for Reports */}
            Reports
          </Link>
        </nav>

        {/* User Profile at the bottom */}
        <div className="mt-auto p-4 bg-gray-50 border-t border-gray-200">
          <div className="flex items-center">
            {/* Dummy Image */}
            <img
              src="https://image-cdn.hypb.st/https%3A%2F%2Fhypebeast.com%2Fimage%2F2021%2F10%2Fbored-ape-yacht-club-nft-3-4-million-record-sothebys-metaverse-1.jpg?q=75&w=500&cbr=1&fit=max"
              alt="Profile"
              className="w-10 h-10 rounded-full mr-3"
            />
            <div>
              <p className="font-semibold text-gray-700">Elon Mask</p> {/* Dummy Name */}
              <p className="text-sm text-gray-500">elon.mask@tusla.car</p> {/* Dummy Email */}
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/contracts" element={<Contracts />} />
          <Route path="/contract/:contract_id" element={<ContractDetails />} /> {/* Dynamic Route */}
          <Route path="/reports" element={<Reports />} />
          <Route path="/report/:contract_id" element={<ReportDetails />} /> {/* Dynamic Route */}
        </Routes>
      </main>
    </div>
  )
}

export default App