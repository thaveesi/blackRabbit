import React from 'react';
import { useGetReports } from '../hooks/useReports';
import { useNavigate } from 'react-router-dom'; // Import the useNavigate hook

export default function Reports() {
    const reports = useGetReports();
    const navigate = useNavigate(); // Initialize the navigate hook

    const handleRowClick = (contractId: string) => {
        navigate(`/report/${contractId}`); // Navigate to the report detail page
    };

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-6">Reports</h1>
            {/* Wrap the table inside a div with width 80% and center it */}
            <div className="w-4/5 mx-auto bg-white rounded-lg shadow-lg overflow-x-auto">
                <table className="w-full table-auto">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="py-3 px-6 text-left">Date</th>
                            <th className="py-3 px-6 text-left">Time</th>
                            <th className="py-3 px-6 text-left">Contract Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reports.map((report, index) => (
                            <tr
                                key={index}
                                className="border-b hover:bg-gray-100 cursor-pointer transition-all"
                                onClick={() => handleRowClick(report.contract_id)}
                            >
                                <td className="py-2 px-6">
                                    {new Date(report.created_at).toLocaleDateString()}
                                </td>
                                <td className="py-2 px-6">
                                    {new Date(report.created_at).toLocaleTimeString()}
                                </td>
                                <td className="py-2 px-6">{report.contract_name}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}