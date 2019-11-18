import axios from "axios";
import React, { useState } from "react";
import { Header, Icon, Input, List } from "semantic-ui-react";
import "./App.css";
import data from "./data/searchbar.json";
import { PredictionsTable } from "./PredictionTable";
import { SearchCards } from "./SearchCards";
function App() {
  // console.log(data);
  const [searchInput, setSearchInput] = useState("");
  const [results, setResults] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const filterData = value => {
    return data.filter(
      x =>
        x.id.includes(value) || x.name.includes(value) || x.repr.includes(value)
    );
  };
  const fetchData = value => {
    setSearchInput(value);
    setPredictions([]);
    if (value.trim() === "") {
      setResults([]);
    } else {
      const tmp = filterData(value).slice(0, 15);
      setResults(tmp);
    }
  };
  const getPredictions = item => {
    setResults([item]);
    setSearchInput("");
    const url = "http://35.237.223.152:5000/predict";
    const param = {};
    param[item.Type] = item.id;
    axios
      .post(url, param)
      .then(result => setPredictions(result.data))
      .catch(err => console.log(err));
    console.log(predictions);
  };
  return (
    <div className="container-fluid">
      <div className="row">
        <Header as="h1" icon textAlign="center" className="mx-auto my-4 ">
          <Icon name="dna" size="tiny" />
          <Header.Content>Deep Drug Repurposer</Header.Content>
        </Header>
      </div>

      <div className="row">
        <div className="col-12 mb-1">
          <Input
            fluid
            size="large"
            placeholder="Enter a drug or target name"
            value={searchInput}
            onChange={event => fetchData(event.target.value)}
          />
        </div>
      </div>
      <List size="small">
        {results.map((item, index) => (
          <SearchCards
            item={item}
            getPredictions={getPredictions}
            key={item.id}
          />
          // <li
          //   className="list-group-item"
          //   onClick={event => getPredictions(item)}
          // >
          //   {(item.id, item.name, item.repr)}
          // </li>
        ))}
      </List>
      {predictions.predictions && predictions.predictions.length > 0 && (
        <PredictionsTable
          predictions={predictions.predictions}
          type={results[0].Type}
        />
      )}
      {/* {predictions.predictions && predictions.predictions[0].label} */}
    </div>
  );
}

export default App;
