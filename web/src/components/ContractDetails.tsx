import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';  // Use axios for API calls

interface Event {
    _id: string;
    contract: string;
    date: string;
    time: string;
    agent: string;
    action: string;
}

interface ContractData {
    contract_info: {
        contract_name: string;
        source_code: string;
    };
}

interface GroupedEvents {
    [contract: string]: Event[];
}

const ContractDetails: React.FC = () => {
    const { contract_id } = useParams<{ contract_id: string }>(); // Get contract_id from the URL params
    const [events, setEvents] = useState<Event[]>([]); // Event data state
    const [contractData, setContractData] = useState<ContractData | null>(null); // Contract data state
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    // Fetch contract events from MongoDB via an API
    useEffect(() => {
        const fetchContractEvents = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/contracts/${contract_id}/events`);
                setEvents(response.data.events);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch contract events');
                setLoading(false);
            }
        };

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

        fetchContractEvents();
        fetchContractData();
    }, [contract_id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    // Get contract name and source code from the fetched contract data
    const contractName = contractData?.contract_info.contract_name || 'Unknown Contract';
    const sourceCode = contractData?.contract_info.source_code || '// No source code available';

    // Group events by contract
    const groupedEvents: GroupedEvents = events.reduce((acc: GroupedEvents, event: Event) => {
        (acc[event.contract] = acc[event.contract] || []).push(event);
        return acc;
    }, {});  // Initial value is an empty object with type GroupedEvents

    return (
        <div className="flex flex-col lg:flex-row p-8">
            {/* Left Section: Code Block */}
            <div className="lg:w-1/2 bg-gray-20 p-6 rounded-lg border border-gray-300 border-opacity-40 overflow-x-auto">
                <h1 className="text-2xl font-bold mb-4">Penetration Test Results - {contractName}</h1>
                <div className="bg-black text-white p-2 rounded-lg max-w-full overflow-x-auto">
                    <pre className="whitespace-pre-wrap break-all text-sm leading-tight">
                        {sourceCode}
                    </pre>
                </div>
            </div>

            {/* Right Section: Agents & Activity Feed */}
            <div className="lg:w-1/2 lg:pl-6 mt-8 lg:mt-0">
                {/* Activity Feed */}
                <div className="bg-gray-20 p-4 rounded-lg border border-gray-300 border-opacity-40">
                    <h2 className="text-xl font-semibold mb-4">Activity Feed</h2>

                    {Object.keys(groupedEvents).map((contract, index) => (
                        <table className="min-w-full text-left table-auto" key={index}>
                            <thead>
                                <tr>
                                    <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">CONTRACT</th>
                                    <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">DATE</th>
                                    <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">TIME</th>
                                    <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">AGENT</th>
                                    <th className="py-2 px-4 border-b border-gray-300 text-sm font-semibold text-gray-600">ACTION</th>
                                </tr>
                            </thead>
                            <tbody>
                                {/* Display merged cell for CONTRACT */}
                                <tr>
                                    <td className="py-2 px-4 border-b border-gray-200" rowSpan={groupedEvents[contract].length}>{contract}</td>
                                    {/* First row's other data */}
                                    <td className="py-2 px-4 border-b border-gray-200">{groupedEvents[contract][0].date}</td>
                                    <td className="py-2 px-4 border-b border-gray-200">{groupedEvents[contract][0].time}</td>
                                    <td className="py-2 px-4 border-b border-gray-200">{groupedEvents[contract][0].agent}</td>
                                    <td className="py-2 px-4 border-b border-gray-200">{groupedEvents[contract][0].action}</td>
                                </tr>

                                {/* Render remaining rows under the same contract */}
                                {groupedEvents[contract].slice(1).map((event, idx) => (
                                    <tr key={idx}>
                                        <td className="py-2 px-4 border-b border-gray-200">{event.date}</td>
                                        <td className="py-2 px-4 border-b border-gray-200">{event.time}</td>
                                        <td className="py-2 px-4 border-b border-gray-200">{event.agent}</td>
                                        <td className="py-2 px-4 border-b border-gray-200">{event.action}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ContractDetails;