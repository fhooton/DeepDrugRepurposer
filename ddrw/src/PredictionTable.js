import _ from "lodash";
import React, { useState } from "react";
import { Table } from "semantic-ui-react";
export const PredictionsTable = ({ predictions, type }) => {
  console.log({ predictions });
  const [state, setState] = useState({
    column: null,
    data: predictions,
    direction: null
  });

  const handleSort = clickedColumn => () => {
    const { column, data, direction } = state;

    if (column !== clickedColumn) {
      setState({
        column: clickedColumn,
        data: _.sortBy(data, [clickedColumn]),
        direction: "ascending"
      });

      return;
    }

    setState({
      data: data.reverse(),
      direction: direction === "ascending" ? "descending" : "ascending"
    });
  };

  const { column, data, direction } = state;

  return (
    // <div style={{ }}>
    <Table sortable celled fixed selectable>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell
            sorted={column === "label" ? direction : null}
            onClick={handleSort("label")}
          >
            {type === "drug" && "Target Name"}
            {type === "target" && "Drug Name"}
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "probability" ? direction : null}
            onClick={handleSort("probability")}
          >
            Probability
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "result" ? direction : null}
            onClick={handleSort("result")}
          >
            Result
          </Table.HeaderCell>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {_.map(data, ({ probability, result, label }) => (
          <Table.Row key={label}>
            <Table.Cell>{label}</Table.Cell>
            <Table.Cell>{probability}</Table.Cell>
            <Table.Cell>{result}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
    // </div>
  );
};
