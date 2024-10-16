import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Use this for navigation
import ActivityTables from './ActivityTables';
import { ConnectButton } from '@rainbow-me/rainbowkit';

// Define the RecentContract component with dynamic fetching
const RecentContract = ({ contract, status }: { contract: any; status: string }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/contract/${contract.contract_id}`);
  };

  return (
    <div
      className="bg-white cursor-pointer h-20"
      onClick={handleClick}
    >
      <h2 className="font-semibold text-xl">{contract.name}</h2>
      <span
        className={`text-sm font-semibold ${status === 'Successful'
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
};

// ActivityRow component remains the same
const ActivityRow = ({
  date,
  time,
  contract,
  agent,
  action,
  issue,
  priority,
}: {
  date: string;
  time: string;
  contract: string;
  agent: string;
  action: string;
  issue: string;
  priority: string;
}) => (
  <tr className="border-b">
    <td className="py-2 px-4">{date}</td>
    <td className="py-2 px-4">{time}</td>
    <td className="py-2 px-4">{contract}</td>
    <td className="py-2 px-4">{agent}</td>
    <td className="py-2 px-4">{action}</td>
    <td className="py-2 px-4">{issue}</td>
    <td className={`py-2 px-4 ${priority === 'High' ? 'text-red-500' : ''}`}>
      {priority}
    </td>
  </tr>
);

// Main Dashboard component
const Dashboard: React.FC = () => {
  const [contracts, setContracts] = useState<any[]>([]); // State to hold the fetched contracts

  // Fetch recent contracts from the backend
  useEffect(() => {
    const fetchContracts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/contracts/recent');
        const data = await response.json();
        setContracts(data);
      } catch (error) {
        console.error('Error fetching contracts:', error);
      }
    };

    fetchContracts();
  }, []);

  return (
    <div className="px-8 py-8 my-8 ">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <div>
          {/* <button className="bg-blue-600 rounded-xl text-white px-4 py-2 rounded mr-2">
            Connect Wallet
          </button> */}
          <div className='className="bg-blue-600 rounded-xl text-white px-4 py-2 rounded mr-2"'>
            <ConnectButton />
          </div>
          {/* <button className="bg-gray-800 rounded-xl text-white px-4 py-2 rounded">
            Test New Contract
          </button> */}
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-4">Recent Contracts</h2>
      <div className="grid grid-cols-5 gap-4 mb-8">
        {contracts.map((contract) => (
          <div key={contract.contract_id} className="border border-gray-300 p-4 rounded-lg">
            <RecentContract
              contract={contract}
              status={
                contract.created_at || 'Completed' // Adjust status field based on your data
              }
            />
          </div>
        ))}
      </div>

      <h2 className="text-xl font-semibold mb-4">Activity Feed</h2>
      <ActivityTables />
    </div>
  );
};

export default Dashboard;