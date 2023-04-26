import React from "react";
import { Button, Text } from '@chakra-ui/react';
import { selectCell, cellActions } from '@datalayer/jupyter-react';

const CellToolbar: React.FC = () => {
  const cell = selectCell();
  return (
    <>
      <Text as="h5">Cell Example</Text>
      <Button
        color="primary"
        onClick={() => console.log('run')}
        >
          Run
      </Button>
      <Button
        color="secondary"
        onClick={() => console.log('run')}
        >
          Reset outputs count
      </Button>
      <Text>
        Outputs count: {cell.outputsCount}
      </Text>
    </>
  );
}

export default CellToolbar;
