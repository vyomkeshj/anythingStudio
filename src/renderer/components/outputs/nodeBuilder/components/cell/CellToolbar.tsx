import React from "react";
import { Button, Text } from '@chakra-ui/react';
import { selectCell, cellActions } from '@datalayer/jupyter-react';
import {useDispatch} from 'react-redux';

const CellToolbar: React.FC = () => {
  const cell = selectCell();
  const dispatch = useDispatch();

  return (
    <>
      <Button
        color="primary"
        onClick={() => dispatch(cellActions.execute())}
        >
          Run
      </Button>
      {/*<Button*/}
      {/*  color="secondary"*/}
      {/*  onClick={() => console.log('run')}*/}
      {/*  >*/}
      {/*    Reset outputs count*/}
      {/*</Button>*/}
      {/*<Text>*/}
      {/*  Outputs count: {cell.outputsCount}*/}
      {/*</Text>*/}
    </>
  );
}

export default CellToolbar;
