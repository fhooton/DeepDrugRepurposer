import React, { useState } from "react";
import "./App.css";
import data from "./data/searchbar.json";

function App() {
  // console.log(data);
  const [searchInput, setSearchInput] = useState("");
  const [results, setResults] = useState([]);
  const filterData = value => {
    return data.filter(
      x =>
        x.id.includes(value) || x.name.includes(value) || x.repr.includes(value)
    );
  };
  const fetchData = value => {
    setSearchInput(value);
    if (value.trim() == "") {
      setResults([]);
    } else {
      const tmp = filterData(value);
      setResults(tmp);
    }
  };
  const getPredictions = (id, type) => {
    console.log(id, type);
  };
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-12 ">
          <input
            className="form-control"
            placeholder="Enter a drug or target name"
            value={searchInput}
            onChange={event => fetchData(event.target.value)}
          />
        </div>
      </div>
      <ul className="list-group list-group-flush">
        {results.map((item, index) => (
          <li
            className="list-group-item"
            onClick={event => getPredictions(item.id, item.Type)}
          >
            {item.id}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
