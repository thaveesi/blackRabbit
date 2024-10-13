import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // For getting contract_id from URL
import ReactMarkdown from 'react-markdown'; // Import react-markdown
import remarkGfm from 'remark-gfm'; // To support GitHub Flavored Markdown
import rehypeRaw from 'rehype-raw'; // To allow HTML in Markdown

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
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
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

  // Define custom component mappings for Markdown elements
  const components = {
    h1: ({ node, ...props }) => (
      <h1 className="text-3xl font-bold my-4" {...props} />
    ),
    h2: ({ node, ...props }) => (
      <h2 className="text-2xl font-semibold my-4" {...props} />
    ),
    h3: ({ node, ...props }) => (
      <h3 className="text-xl font-semibold my-2" {...props} />
    ),
    p: ({ node, ...props }) => (
      <p className="text-base leading-6 my-2" {...props} />
    ),
    ul: ({ node, ...props }) => (
      <ul className="list-disc ml-6 my-2" {...props} />
    ),
    ol: ({ node, ...props }) => (
      <ol className="list-decimal ml-6 my-2" {...props} />
    ),
    blockquote: ({ node, ...props }) => (
      <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600 my-4" {...props} />
    ),
    code: ({ node, inline, className, children, ...props }) => {
      return inline ? (
        <code className="bg-gray-100 text-red-500 font-mono px-2 py-1 rounded" {...props}>
          {children}
        </code>
      ) : (
        <pre className="bg-gray-900 text-white font-mono p-4 rounded my-2 overflow-auto" {...props}>
          <code>{children}</code>
        </pre>
      );
    },
    table: ({ node, ...props }) => (
      <table className="min-w-full table-auto border-collapse border border-gray-300 my-4" {...props} />
    ),
    thead: ({ node, ...props }) => (
      <thead className="bg-gray-100" {...props} />
    ),
    th: ({ node, ...props }) => (
      <th className="px-4 py-2 border border-gray-300 text-left font-semibold" {...props} />
    ),
    td: ({ node, ...props }) => (
      <td className="px-4 py-2 border border-gray-300 text-left" {...props} />
    ),
    tr: ({ node, ...props }) => (
      <tr className="even:bg-gray-50" {...props} />
    ),
    // Add more custom components if needed
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">{report.contract_name} Report</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        {/* Render the markdown content from the "results" field with custom styling */}
        <ReactMarkdown
          children={report.results}
          components={components}
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
        />
      </div>
    </div>
  );
}