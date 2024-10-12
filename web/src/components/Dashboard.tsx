import React from 'react'

const RecentContract = ({ name, status }: { name: string; status: string }) => (
  <div className="bg-white p-4 rounded-lg shadow">
    <h3 className="font-semibold">{name}</h3>
    <span className={`text-sm ${
      status === 'Successful' ? 'text-green-500' :
      status === 'Issues Found' ? 'text-red-500' :
      status === 'Warnings' ? 'text-yellow-500' : ''
    }`}>
      {status}
    </span>
  </div>
)

const ActivityRow = ({ date, time, contract, agent, action, issue, priority }: {
  date: string; time: string; contract: string; agent: string; action: string; issue: string; priority: string;
}) => (
  <tr className="border-b">
    <td className="py-2 px-4">{date}</td>
    <td className="py-2 px-4">{time}</td>
    <td className="py-2 px-4">{contract}</td>
    <td className="py-2 px-4">{agent}</td>
    <td className="py-2 px-4">{action}</td>
    <td className="py-2 px-4">{issue}</td>
    <td className={`py-2 px-4 ${priority === 'High' ? 'text-red-500' : ''}`}>{priority}</td>
  </tr>
)

const Dashboard: React.FC = () => {
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mr-2">Connect Wallet</button>
          <button className="bg-gray-800 text-white px-4 py-2 rounded">Test New Contract</button>
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-4">Recent Contracts</h2>
      <div className="grid grid-cols-5 gap-4 mb-8">
        <RecentContract name="Smart Contract A" status="Successful" />
        <RecentContract name="Smart Contract B" status="Issues Found" />
        <RecentContract name="Smart Contract C" status="Warnings" />
        <RecentContract name="Smart Contract D" status="Successful" />
        <RecentContract name="Smart Contract E" status="Successful" />
      </div>

      <h2 className="text-xl font-semibold mb-4">Activity Feed</h2>
      <div className="bg-white rounded-lg shadow overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="py-2 px-4 text-left">Date</th>
              <th className="py-2 px-4 text-left">Time</th>
              <th className="py-2 px-4 text-left">Contract</th>
              <th className="py-2 px-4 text-left">Agent</th>
              <th className="py-2 px-4 text-left">Action</th>
              <th className="py-2 px-4 text-left">Issue</th>
              <th className="py-2 px-4 text-left">Priority</th>
            </tr>
          </thead>
          <tbody>
            <ActivityRow date="10/12/2024" time="2:40" contract="Contract A" agent="Bob" action="Deployed to testnet" issue="None" priority="None" />
            <ActivityRow date="10/12/2024" time="2:37" contract="Contract C" agent="Alice" action="Vulnerability detected" issue="Reentrancy" priority="High" />
            <ActivityRow date="10/12/2024" time="2:15" contract="Contract E" agent="Eve" action="Passed all tests" issue="None" priority="None" />
            <ActivityRow date="10/12/2024" time="2:07" contract="Contract P" agent="Alice" action="Vulnerability detected" issue="Timestamp dependance" priority="High" />
            <ActivityRow date="10/12/2024" time="1:56" contract="Contract B" agent="Bob" action="Deployed to testnet" issue="None" priority="None" />
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Dashboard
