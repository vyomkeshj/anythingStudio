import Game from "./pages/Game";
import Start from "./pages/Start";
import Finished from "./pages/Finished";
import useTickTackToe from "./hooks/useTicTacToe";
import { memo } from "react";
import { UINodeOutputProps } from "../props";
const TicTacToeComponent =  memo(({ ui_message_registry }: UINodeOutputProps) => {
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
