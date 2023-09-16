import React from 'react';
import VisHeader from '../grid_components/VisHeader';
import { useSearchContext } from "../../contexts/SearchContext";


const FilterOptionsGrid = () => {
  const { search } = useSearchContext();

  return (
    <div className="vis-container">
      <VisHeader title="Filtered by" subtitle="Click on parts of the grid or chart to filter the dataset." />
      <article>
        <ul>
          {Object.entries(search).map(([key, value]) => (
            <li key={key}>
              {key}: {value === false ? "" : value.toString()}
            </li>
          ))}
        </ul>
      </article>
    </div>

  );
};

export default FilterOptionsGrid;