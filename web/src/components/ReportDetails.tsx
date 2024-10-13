import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

interface ContractInfo {
    contract_info: {
        _id: string;
        abi: any[];
        addr: string;
        contract_id: string;
        contract_name: string;
        source_code: string; // Assuming you have the contract source code in JSON
    };
}

const ReportDetails: React.FC = () => {
    const { contract_id } = useParams<{ contract_id: string }>(); // Get contract_id from the URL params
    const [contractData, setContractData] = useState<ContractInfo | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchContractData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/contracts/${contract_id}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch contract data');
                }
                const data = await response.json();
                setContractData(data);
                setLoading(false);
            } catch (err) {
                // setError(err.message);
                setLoading(false);
            }
        };

        fetchContractData();
    }, [contract_id]); // Dependency on contract_id, will re-run when it changes

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    // Extract contract name and source code from the data
    const contractName = contractData?.contract_info.contract_name || 'Unknown Contract';
    const sourceCode = contractData?.contract_info.source_code || '// No source code available';

    return (
        <div className="flex flex-col lg:flex-row p-8">
            {/* Left Section: Code Block */}
            <div className="lg:w-2/3 bg-gray-100 p-6 rounded-lg shadow-lg">
                <h1 className="text-2xl font-bold mb-4">Penetration Test Results - {contractName}</h1>
                <div className="bg-black text-white p-2 rounded-lg max-w-full overflow-x-auto">
                    <pre className="whitespace-pre-wrap break-all text-sm leading-tight">
                        {sourceCode}
                    </pre>
                </div>
            </div>
    
            {/* Right Section: Agents & Activity Feed */}
            <div className="lg:w-1/3 lg:pl-6 mt-8 lg:mt-0">
                {/* Agents List */}
                <div className="mb-6">
                    <h2 className="text-xl font-semibold mb-4">Agents</h2>
                    <ul>
                        <li className="flex items-center mb-2">
                            <span className="h-2 w-2 bg-blue-500 rounded-full mr-2"></span> Bob
                        </li>
                        <li className="flex items-center mb-2">
                            <span className="h-2 w-2 bg-purple-500 rounded-full mr-2"></span> Alice
                        </li>
                        <li className="flex items-center mb-2">
                            <span className="h-2 w-2 bg-orange-500 rounded-full mr-2"></span> Eve
                        </li>
                    </ul>
                </div>
    
                {/* Activity Feed */}
                <div className="bg-white p-4 rounded-lg shadow-lg">
                    <h2 className="text-xl font-semibold mb-4">Activity Feed</h2>
                    <table className="min-w-full text-left table-auto">
                        <thead>
                            <tr>
                                <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">CONTRACT</th>
                                {/* <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">DATE</th> */}
                                <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">TIME</th>
                                <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">AGENT</th>
                                <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">ACTION</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td className="py-2 px-4 border-b border-gray-200">CT_01</td>
                                {/* <td className="py-2 px-4 border-b border-gray-200">10/12/24</td> */}
                                <td className="py-2 px-4 border-b border-gray-200">02:45</td>
                                <td className="py-2 px-4 border-b border-gray-200">Bob</td>
                                <td className="py-2 px-4 border-b border-gray-200">Delegated to Alice</td>
                            </tr>
                            <tr>
                                <td className="py-2 px-4 border-b border-gray-200">CT_02</td>
                                {/* <td className="py-2 px-4 border-b border-gray-200">10/12/24</td> */}
                                <td className="py-2 px-4 border-b border-gray-200">02:34</td>
                                <td className="py-2 px-4 border-b border-gray-200">Alice</td>
                                <td className="py-2 px-4 border-b border-gray-200">Passed to Eve</td>
                            </tr>
                            <tr>
                                <td className="py-2 px-4 border-b border-gray-200">CT_03</td>
                                {/* <td className="py-2 px-4 border-b border-gray-200">10/12/24</td> */}
                                <td className="py-2 px-4 border-b border-gray-200">02:30</td>
                                <td className="py-2 px-4 border-b border-gray-200">Eve</td>
                                <td className="py-2 px-4 border-b border-gray-200">Analyzed output</td>
                            </tr>
                            {/* Additional hardcoded rows as needed */}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ReportDetails;