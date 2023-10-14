import VisHeader from '../grid_components/VisHeader';
import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";


const FilterOptionsGrid = () => {
  const { filterOptions } = useDashboardFilteredContext();

  return (
    <div className="vis-container">
      <VisHeader title="Filtered by" subtitle="Click on parts of the grid or chart to filter the dataset." />
      <article>
        <ul>
          {Object.entries(filterOptions).map(([key, value]) => (
            <li key={key}>
              {key}: {value === null ? "" : value.toString()}
            </li>
          ))}
        </ul>
      </article>
    </div>

  );
};

export default FilterOptionsGrid;