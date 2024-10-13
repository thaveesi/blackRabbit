import React, { useEffect, useState } from 'react';
import axios from 'axios';  // Use axios for API calls

interface Event {
    _id: string;
    contract: string;
    date: string;
    time: string;
    agent: string;
    action: string;
}

interface ContractInfo {
    contract_id: string;
    name: string;
    addr: string;
    source_code: string;
}

interface ContractWithEvents {
    contract_info: ContractInfo;
    events: Event[];
}

const ActivityTables: React.FC = () => {
    const [contractsWithEvents, setContractsWithEvents] = useState<ContractWithEvents[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedContractIndex, setSelectedContractIndex] = useState<number>(0);

    // Fetch the 4 latest contracts and their events
    useEffect(() => {
        const fetchContractsAndEvents = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/contracts/recent');
                const recentContracts = response.data;

                // Limit to 4 contracts
                const contractsToFetch = recentContracts.slice(0, 4);

                const contractsWithEventsPromises = contractsToFetch.map(async (contract: any) => {
                    try {
                        const eventsResponse = await axios.get(`http://127.0.0.1:5000/contracts/${contract.contract_id}/events`);
                        const events = eventsResponse.data.events;

                        // Only include contracts that have event data
                        if (events && events.length > 0) {
                            return {
                                contract_info: contract,
                                events: events,
                            };
                        } else {
                            return null; // Indicate that this contract should be skipped
                        }
                    } catch (err) {
                        // Handle error for this specific contract
                        console.error(`Error fetching events for contract ${contract.contract_id}:`, err);
                        return null; // Skip this contract
                    }
                });

                // Wait for all promises to resolve
                const results = await Promise.all(contractsWithEventsPromises);

                // Filter out null values (contracts without events or with errors)
                const successfulContracts = results.filter((item): item is ContractWithEvents => item !== null);

                setContractsWithEvents(successfulContracts);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch contracts and events');
                setLoading(false);
            }
        };

        fetchContractsAndEvents();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error || contractsWithEvents.length === 0) {
        return <div>Error: {error || 'No data available'}</div>;
    }

    const agentIcons: { [key: string]: string } = {
        Bob: '🧑‍💼',   // Icon for Bob
        Alice: '👩‍💼', // Icon for Alice
        Eve: '🧑‍🔬',    // Icon for Eve
    };

    // Ensure the selectedContractIndex is within bounds
    const validSelectedContractIndex = selectedContractIndex < contractsWithEvents.length ? selectedContractIndex : 0;

    const selectedContract = contractsWithEvents[validSelectedContractIndex];

    return (
        <div className="p-4">
            {/* Buttons */}
            <div className="flex flex-wrap space-x-2 mb-4">
                {contractsWithEvents.map((contractWithEvents, index) => (
                    <button
                        key={index}
                        onClick={() => setSelectedContractIndex(index)}
                        className={`px-4 py-2 rounded-full focus:outline-none ${
                            index === validSelectedContractIndex
                                ? 'bg-blue-500 text-white'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                    >
                        {contractWithEvents.contract_info.name}
                    </button>
                ))}
            </div>

            {/* Selected Table */}
            <div className="w-full">
                <div className="p-4 bg-white border rounded-lg">
                    {/* Contract Name and Address */}
                    <h2 className="text-md font-semibold mb-2">
                        {selectedContract.contract_info.name}
                    </h2>
                    <h3 className="text-sm font-light text-gray-500 mb-4">
                        {selectedContract.contract_info.addr}
                    </h3>

                    <div className="mx-auto bg-white rounded-lg overflow-x-auto">
                        <table className="min-w-full text-left table-auto">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="py-2 px-4 border-t border-b border-l border-gray-200 text-sm font-semibold text-gray-600">DATE</th>
                                    <th className="py-2 px-4 border-t border-b border-l border-gray-200 text-sm font-semibold text-gray-600">TIME</th>
                                    <th className="py-2 px-4 border-t border-b border-l border-gray-200 text-sm font-semibold text-gray-600">AGENT</th>
                                    <th className="py-2 px-4 border-t border-b border-l border-r border-gray-200 text-sm font-semibold text-gray-600">ACTION</th>
                                </tr>
                            </thead>
                            <tbody>
                                {selectedContract.events.map((event, idx) => (
                                    <tr key={idx}>
                                        <td className="py-2 px-4 border-b border-l border-gray-200 text-gray-600">{event.date}</td>
                                        <td className="py-2 px-4 border-b border-l border-gray-200 text-gray-600">{event.time}</td>
                                        <td className="py-2 px-4 border-b border-l border-gray-200 flex items-center text-gray-600">
                                            <span className="mr-2">{agentIcons[event.agent] || '👤'}</span>
                                            <span>{event.agent}</span>
                                        </td>
                                        <td className="py-2 px-4 border-b border-l border-r border-gray-200 text-gray-600">{event.action}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ActivityTables;