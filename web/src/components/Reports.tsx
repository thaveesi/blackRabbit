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
        <div className="px-8 py-8 my-8">
            <h1 className="text-4xl font-bold mb-6">Reports</h1>
            {/* Wrap the table inside a div with width 80% and center it */}
            <div className="w-3/5 bg-white rounded-lg border-l border-r border-t border-gray-500 border-opacity-30 overflow-x-auto">
                <table className="min-w-full p-10 table-auto text-left">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="py-4 px-6 border-b border-gray-200 text-base font-semibold text-gray-600 w-1/4">DATE</th>
                            <th className="py-4 px-6 border-b border-gray-200 border-l border-gray-100 text-base font-semibold text-gray-600 w-1/4">TIME</th>
                            <th className="py-4 px-6 border-b border-gray-200 border-l border-gray-100 text-base font-semibold text-gray-600">CONTRACT NAME</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reports.map((report, index) => (
                            <tr
                                key={index}
                                className="border-b hover:bg-gray-100 cursor-pointer transition-all"
                                onClick={() => handleRowClick(report.contract_id)}
                            >
                                <td className="py-4 px-6 border-b border-gray-200 text-gray-600">
                                    {new Date(report.created_at).toLocaleDateString()}
                                </td>
                                <td className="py-4 px-6 border-b border-gray-200 border-l border-gray-100 text-gray-600">
                                    {new Date(report.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })}
                                </td>
                                <td className="py-4 px-6 border-b border-gray-200 border-l border-gray-100 text-gray-600">
                                    {report.contract_name}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}