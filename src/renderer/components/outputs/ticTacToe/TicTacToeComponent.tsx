import Game from "./pages/Game";
import Start from "./pages/Start";
import Finished from "./pages/Finished";
import useTickTackToe from "./hooks/useTicTacToe";
import { memo } from "react";
import { OutputProps } from "../props";
const TicTacToeComponent =  memo(({ label, id, outputId, schemaId, ui_message_registry }: OutputProps) => {
  const {board, status, winner, handleClick, handleRestart, handleStart} = useTickTackToe();
  return (
    <div className="tictac">
      {status === "created" && <Start handleStart={handleStart} />}
      {status === "finished" && (
        <Finished name={winner} restart={handleRestart} />
      )}
      {status === "started" && (
        <Game board={board} handleClick={handleClick} />
      )}
    </div>
  );
});
export default TicTacToeComponent;
