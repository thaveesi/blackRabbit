import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';  // Use axios for API calls

interface Event {
    _id: string;
    created_at: string;
    agent: string;
    action: string;
}

interface ContractData {
    contract_info: {
        name: string;
        addr: string;
        source_code: string;
    };
}

const ContractDetails: React.FC = () => {
    const { contract_id } = useParams<{ contract_id: string }>(); // Get contract_id from the URL params
    const [events, setEvents] = useState<Event[]>([]); // Event data state
    const [contractData, setContractData] = useState<ContractData | null>(null); // Contract data state
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    // Fetch contract events from MongoDB via an API every 3 seconds
    useEffect(() => {
        const fetchContractEvents = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/contracts/${contract_id}/events`);
                setEvents(response.data.events);
            } catch (err) {
                console.error('Failed to fetch contract events', err);  // Log the error but don't update state
            }
        };

        // Set interval to call fetchContractEvents every 3 seconds
        const intervalId = setInterval(fetchContractEvents, 3000);

        // Clean up the interval when the component unmounts
        return () => clearInterval(intervalId);
    }, [contract_id]);

    // Fetch contract data on page load (runs once)
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
                setError('Failed to fetch contract data');
                setLoading(false);
            }
        };

        fetchContractData();
    }, [contract_id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    // Get contract name and source code from the fetched contract data
    const contractName = contractData?.contract_info.name || 'Unknown Contract';
    const contractAddress = contractData?.contract_info.addr || 'Unknown Address';
    const sourceCode = contractData?.contract_info.source_code || '// No source code available';

    // Format date and time from createdAt field
    const formatDateTime = (isoString: string) => {
        const dateObj = new Date(isoString);
        if (isNaN(dateObj.getTime())) {
            return 'Invalid Date'; // Check if the date is valid
        }
        return dateObj.toLocaleString('en-US', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false,
        }).replace(',', ''); // Format MM/DD HH:mm:ss
    };

    const agentIcons: { [key: string]: React.ReactNode } = {
        planner: (
            // SVG Icon for Bob
            <svg
                width="27"
                height="27"
                viewBox="0 0 27 27"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                xmlnsXlink="http://www.w3.org/1999/xlink"
            >
                <rect width="27" height="27" fill="url(#pattern0_97_6948)" />
                <defs>
                    <pattern
                        id="pattern0_97_6948"
                        patternContentUnits="objectBoundingBox"
                        width="1"
                        height="1"
                    >
                        <use
                            xlinkHref="#image0_97_6948"
                            transform="scale(0.004)"
                        />
                    </pattern>
                    <image
                        id="image0_97_6948"
                        width="250"
                        height="250"
                        xlinkHref="data:image/png;base64,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"
                    />
                </defs>
            </svg>
        ),
        executor: (
            <svg width="27" height="27" viewBox="0 0 27 27" fill="none" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
                <rect width="27" height="27" fill="url(#pattern0_100_2535)" />
                <defs>
                    <pattern id="pattern0_100_2535" patternContentUnits="objectBoundingBox" width="1" height="1">
                        <use xlinkHref="#image0_100_2535" transform="scale(0.004)" />
                    </pattern>
                    <image id="image0_100_2535" width="250" height="250" xlinkHref="data:image/png;base64,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" />
                </defs>
            </svg>

        ), // Icon for Alice
        reflector: (
            <svg width="27" height="27" viewBox="0 0 27 27" fill="none" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
                <rect width="27" height="27" fill="url(#pattern0_100_2537)" />
                <defs>
                    <pattern id="pattern0_100_2537" patternContentUnits="objectBoundingBox" width="1" height="1">
                        <use xlinkHref="#image0_100_2537" transform="scale(0.004)" />
                    </pattern>
                    <image id="image0_100_2537" width="250" height="250" xlinkHref="data:image/png;base64,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" />
                </defs>
            </svg>

        ),   // Icon for Eve
        NA: (
            <svg width="27" height="27" viewBox="0 0 27 27" fill="none" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
                <rect width="27" height="27" fill="url(#pattern0_100_2548)" />
                <defs>
                    <pattern id="pattern0_100_2548" patternContentUnits="objectBoundingBox" width="1" height="1">
                        <use xlinkHref="#image0_100_2548" transform="scale(0.004)" />
                    </pattern>
                    <image id="image0_100_2548" width="250" height="250" xlinkHref="data:image/png;base64,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" />
                </defs>
            </svg>

        )
    };

    return (
        <div className="flex flex-col lg:flex-row p-8">
            {/* Left Section: Code Block (2/5 width) */}
            <div className="lg:w-2/5 bg-gray-20 p-6 overflow-x-auto">
                <h1 className="text-2xl font-bold mb-4">Penetration Test Results - {contractName}</h1>
                <div className="bg-black text-white p-2 rounded-lg max-w-full overflow-x-auto">
                    <pre className="whitespace-pre-wrap break-all text-sm leading-tight">
                        {sourceCode}
                    </pre>
                </div>
            </div>

            {/* Right Section: Agents & Activity Feed (3/5 width) */}
            <div className="lg:w-3/5 lg:pl-6 mt-8 lg:mt-0">
                {/* Activity Feed */}
                <div className="p-4 bg-white">
                    <h1 className="text-xl font-semibold mb-4">Activity Feed</h1>
                    <h2 className="text-md font-light text-gray-400 mb-2">{contractName} - {contractAddress}</h2>
                    <div className="mx-auto bg-white rounded-lg border border-gray-300 shadow-sm overflow-x-auto">
                        <table className="min-w-full text-left table-auto">
                            <thead className="bg-gray-100 border-b">
                                <tr>
                                    <th className="py-4 px-4 border-r text-base font-semibold text-gray-600">CREATED AT</th>
                                    <th className="py-4 px-4 border-r text-base font-semibold text-gray-600">AGENT</th>
                                    <th className="py-4 px-4 text-base font-semibold text-gray-600">ACTION</th>
                                </tr>
                            </thead>
                            <tbody>
                                {/* Render event rows */}
                                {events.map((event: Event, idx: number) => (
                                    <tr key={idx} className="border-b">
                                        <td className="py-4 px-4 border-r text-gray-600">{event.created_at}</td>
                                        <td className="py-4 px-4 border-r flex items-center text-gray-600">
                                            <span className="mr-2">{agentIcons[event.agent] || '👤'}</span>
                                            <span>{event.agent}</span>
                                        </td>
                                        <td className="py-4 px-4 text-gray-600">{event.action}</td>
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

export default ContractDetails;