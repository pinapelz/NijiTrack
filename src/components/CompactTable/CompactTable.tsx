import React from 'react';

interface CompactTableProps {
  tableData: {
    dates: string[];
    milestones: string[];
  }

}

const CompactTable: React.FC<CompactTableProps> = ({ tableData }) => {
  return (
    <div className="max-w-full mx-auto bg-gray-100 shadow-md rounded-lg overflow-hidden">
      <div className="flex gap-x-4">
        <div className="w-1/2 px-4 py-5">
          <h2 className="text-lg font-semibold text-gray-900">Dates</h2>
          <ul className="mt-3">
            {tableData.dates.map((date, index) => (
              <li key={index} className="text-gray-700 text-sm py-1 border-b border-gray-200">{date}</li>
            ))}
          </ul>
        </div>
        <div className="w-1/2 px-4 py-5">
          <h2 className="text-lg font-semibold text-gray-900">Milestones</h2>
          <ul className="mt-3">
            {tableData.milestones.map((milestone, index) => (
              <li key={index} className="text-gray-700 text-sm py-1 border-b border-gray-200">{milestone.toLocaleString()}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CompactTable;
