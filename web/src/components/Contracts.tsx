import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const RecentContract = ({ name, status }: { name: string; status: string }) => (
    <div className="bg-white p-4 rounded-lg">
        <h3 className="font-semibold">{name}</h3>
        <span
            className={`text-sm ${status === 'Successful'
                ? 'text-green-500'
                : status === 'Issues Found'
                    ? 'text-red-500'
                    : status === 'Warnings'
                        ? 'text-yellow-500'
                        : ''
                }`}
        >
            {status}
        </span>
    </div>
);

const Contracts: React.FC = () => {
    const [name, setName] = useState<string>(''); // State for the name input
    const [address, setAddress] = useState<string>(''); // State for the address input
    const [errorMessage, setErrorMessage] = useState<string>(''); // State for error messages (if any)
    const navigate = useNavigate(); // Initialize navigate

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault(); // Prevent form from reloading the page

        try {
            // API request payload
            const payload = {
                name,
                address,
            };

            // Send POST request to the API
            const response = await fetch('http://127.0.0.1:5000/contracts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            // Check if response is successful
            if (response.ok) {
                const data = await response.json();
                console.log('Contract created successfully:', data);

                // Extract contract_id from the response
                const contractId = data.contract.contract_id;

                // Redirect to the contract details page
                navigate(`/contract/${contractId}`);

                // Handle success (e.g., show a success message or clear the form)
                setName(''); // Clear the name field
                setAddress(''); // Clear the address field
                setErrorMessage(''); // Clear any error messages
            } else {
                // Handle failure
                const errorData = await response.json();
                setErrorMessage(`Error: ${errorData.message || 'Failed to create contract'}`);
                console.error('Failed to create contract:', errorData);
            }
        } catch (error) {
            console.error('Error creating contract:', error);
            setErrorMessage('An error occurred while creating the contract. Please try again.');
        }
    };

    return (
        <div className="flex px-16 py-16 my-8 min-h-screen bg-white">
            <div className="w-full max-w-lg">
                {/* <h1 className="text-3xl font-bold text-center mb-8">Smart Contracts</h1> */}

                <h1 className="text-4xl font-bold mb-4">Penetration Test</h1>
                <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg">
                    <div className="mb-6">
                        <label className="block text-gray-800 text-sm font-bold mb-2" htmlFor="name">
                            Name
                        </label>
                        <input
                            type="text"
                            id="name"
                            className="appearance-none border rounded-xl w-full py-3 px-4 text-gray-800 leading-tight focus:outline-none"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Enter Contract Name"
                            required
                        />
                    </div>

                    <div className="mb-6">
                        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="address">
                            Smart Contract Address
                        </label>
                        <input
                            type="text"
                            id="address"
                            className="appearance-none border rounded-xl w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            placeholder="Enter Smart Contract Address"
                            required
                        />
                    </div>

                    {errorMessage && <p className="text-red-500 text-sm mb-4">{errorMessage}</p>}

                    <div className="flex items-center justify-between">
                        <button
                            type="submit"
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 my-6 rounded-xl focus:outline-none focus:shadow-outline w-half"
                        >
                            Run Test
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Contracts;