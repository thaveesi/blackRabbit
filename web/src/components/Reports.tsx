import { useGetReports } from "../hooks/useReports";
export default function Reports() {
    const reports = useGetReports();

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-6">Reports</h1>
            <div className="bg-white rounded-lg shadow overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="py-2 px-4 text-left">Date</th>
                            <th className="py-2 px-4 text-left">Time</th>
                            <th className="py-2 px-4 text-left">Contract</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reports.map((report, index) => (
                            <tr key={index} className="border-b">
                                <td>{new Date(report.createdAt).toLocaleDateString()}</td>
                                <td>{new Date(report.createdAt).toLocaleTimeString()}</td>
                                <td>{report.contract}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}