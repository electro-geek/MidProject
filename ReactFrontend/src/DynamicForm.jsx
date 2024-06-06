
import React, { useState } from 'react';

const Dynamic = () => {
  const [rows, setRows] = useState([{ 
    parameterName: '', 
    startValue: '', 
    minValue: '', 
    type: 'Intraday', 
    start: '', 
    end: '' 
  }]);

  const handleChange = (index, field, value) => {
    const newRows = [...rows];
    newRows[index][field] = value;
    setRows(newRows);
  };

  const handleAddRow = () => {
    setRows([...rows, { 
      parameterName: '', 
      startValue: '', 
      minValue: '', 
      type: 'Intraday', 
      start: '', 
      end: '' 
    }]);
  };

  const handleSubmit = async () => {
    const response = await fetch('http://localhost:5000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(rows),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Generated Data:', data);
    } else {
      console.error('Error generating data');
    }
  };

  return (
    <div>
      {rows.map((row, index) => (
        <div key={index} style={{ marginBottom: '20px' }}>
          <input
            type="text"
            placeholder="Parameter Name"
            value={row.parameterName}
            onChange={(e) => handleChange(index, 'parameterName', e.target.value)}
          />
          <input
            type="number"
            placeholder="Start Value"
            value={row.startValue}
            onChange={(e) => handleChange(index, 'startValue', e.target.value)}
          />
          <input
            type="number"
            placeholder="Min Value"
            value={row.minValue}
            onChange={(e) => handleChange(index, 'minValue', e.target.value)}
          />
          <select
            value={row.type}
            onChange={(e) => handleChange(index, 'type', e.target.value)}
          >
            <option value="Intraday">Intraday</option>
            <option value="Interday">Interday</option>
          </select>
          {row.type === 'Intraday' ? (
            <>
              <input
                type="time"
                placeholder="Start Time"
                value={row.start}
                onChange={(e) => handleChange(index, 'start', e.target.value)}
              />
              <input
                type="time"
                placeholder="End Time"
                value={row.end}
                onChange={(e) => handleChange(index, 'end', e.target.value)}
              />
            </>
          ) : (
            <>
              <input
                type="date"
                placeholder="Start Date"
                value={row.start}
                onChange={(e) => handleChange(index, 'start', e.target.value)}
              />
              <input
                type="date"
                placeholder="End Date"
                value={row.end}
                onChange={(e) => handleChange(index, 'end', e.target.value)}
              />
            </>
          )}
        </div>
      ))}
      <button onClick={handleAddRow}>+</button>
      <button onClick={handleSubmit}>Generate</button>
    </div>
  );
};

export default Dynamic;
