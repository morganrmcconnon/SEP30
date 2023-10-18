// import file from "../../assets/file.svg";
// import settings from "../../assets/settings.svg";
import reset from "../../assets/reset.svg"
import { ALL_KEY_MAPS } from "../../constants/ValueMaps";
import CountryName from "../../constants/CountryName";

import { FilterOptionsType, useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";

const SidebarPreferences = () => {
  const { resetFilter, filterOptions, updateFilterOption } = useDashboardFilteredContext();
  return (
    <>
      <h3 className="sidebar-title">PREFERENCES</h3>
      <nav>
        <ul className="sidebar-list">
          <li onClick={() => resetFilter()} title="Reset all filter options">
            <img className="sidebar-icon" src={reset} alt="reset" />
            <h3>Reset all</h3>
          </li>
        </ul>
      {/* </nav>
      <h3 className="sidebar-title">
        {
          // Count the number of entries in the search variable where the search is true
          Object.entries(filterOptions).reduce((acc, [_, value]) => {
            if (value === null) return acc;
            return acc + 1;
          }, 0) == 0 ? '' : 'FILTERS APPLIED'
        }
      </h3>
      <nav> */}
        {Object.entries(filterOptions)
          .filter(([_, value]) => value !== null)
          .map(([key, value]) => (
            <>
              <h3 className="sidebar-title">{
                value === null ? '' : ` ${key.toUpperCase()}:`
              }</h3>
              <ul className="sidebar-list" onClick={() => updateFilterOption(key as keyof FilterOptionsType, value)} title={`Remove filter option for ${key === 'location' ? 'Country' : key} = ${value}`}>
                <li key={key}>
                  <img className="sidebar-icon" src={reset} alt="reset" />
                  {
                    value === null ? '' :
                      key === 'location' ? (
                        <h3>{CountryName[value]}</h3>
                      ) : key in ALL_KEY_MAPS ? (
                        <h3>{ALL_KEY_MAPS[key][value.toString()]}</h3>
                      ) : (
                        <h3>{value}</h3>
                      )
                  }
                </li>
              </ul>
            </>
          ))}
      </nav>
    </>
  );
};

export default SidebarPreferences;
