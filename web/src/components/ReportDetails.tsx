import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // For getting contract_id from URL
import Markdown from 'markdown-to-jsx'; // Use markdown-to-jsx for rendering markdown


export default function ReportDetails() {
  const { contract_id } = useParams<{ contract_id: string }>(); // Get contract_id from the URL
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/report/${contract_id}`);
        if (!response.ok) {
          throw new Error("Failed to fetch the report");
        }
        const data = await response.json();
        setReport(data);
      } catch (err) {
        // setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    // if (contract_id) {
      fetchReport();
    // }
  }, [contract_id]);

  if (loading) {
    return <p>Loading report...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (!report) {
    return <p>No report found.</p>;
  }
  console.log(report.results);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">{report.contract_name} Report</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        {/* Render the markdown content from the "results" field */}
        <Markdown>{report.results}</Markdown>
      </div>
    </div>
  );
}