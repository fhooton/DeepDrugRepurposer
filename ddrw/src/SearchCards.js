import React from "react";
import { Card } from "semantic-ui-react";

export const SearchCards = ({ item, getPredictions }) => {
  return (
    <Card className="" fluid inverted >
      {/* <div className="row col-11 col-md-9 col-xl-10"> */}
      {/* <div className="col"> */}
      <Card.Content
        onClick={event => {
          getPredictions(item);
        }}
      >
        <Card.Header className="text-truncate">{item.name}</Card.Header>
        <Card.Meta>{item.id}</Card.Meta>
        <Card.Description className="text-truncate">
          {item.repr}
        </Card.Description>
      </Card.Content>
      {/* </div> */}
      {/* </div> */}
      {/* <div className="ml-auto col-1 col-md-3 col-xl-2 "> */}
      {/* <Card.Content> */}
      {/* <span className="d-none d-md-inline-block">{item.id}</span> */}
      {/* </Card.Content> */}
      {/* </Card></div> */}
    </Card>
  );
};
