import React from "react";
import { Icon, List } from "semantic-ui-react";

export const SearchCards = ({ item, getPredictions }) => {
  return (
    <List.Item className="p-3 d-flex justify-content-between">
      <div className="row col-11 col-md-9 col-xl-10">
           
        <div className="my-auto">
                    
          <Icon name="dna" className="" />
                 
        </div>
        <div className="col">
                    
          <List.Content
            onClick={event => {
              getPredictions(item);
            }}
          >
                        
            <List.Header className="text-truncate">
                            {item.name}
                          
            </List.Header>
                        
            <List.Description className="text-truncate">
                            
              {item.repr}
                          
            </List.Description>
                      
          </List.Content>
                  
        </div>
              
      </div>
            
      <div className="ml-auto col-1 col-md-3 col-xl-2 ">
                
        <List.Content>
                    
          <span className="d-none d-md-inline-block">
                       
            {item.id}         
          </span>
                               
        </List.Content>
              
      </div>
          
    </List.Item>
  );
};
