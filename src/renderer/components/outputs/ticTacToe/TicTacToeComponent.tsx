import React, { memo, useEffect, useState } from "react";
import { OutputProps } from "../props";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import "./TicTacToeComponent.css";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";

interface MoveFromComputer {
  row: number;
  col: number;
}

interface MoveFromUser {
  row: number;
  col: number;
}

const TicTacToeComponent = memo(({ label, id, outputId, schemaId, ui_message_registry }: OutputProps) => {
  const [board, setBoard] = useState(Array(3).fill(Array(3).fill(null)));

  const handleMoveFromComputer = (message: ToUIOutputMessage<MoveFromComputer>) => {
    setBoard((prevBoard) => {
      const data = message.data;
      const newBoard = JSON.parse(JSON.stringify(prevBoard));
      newBoard[data.row][data.col] = "O";
      return newBoard;
    });
  };

  const handlers = {
    move_from_computer: handleMoveFromComputer,
  };

  const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>, row: number, col: number) => {
    if (board[row][col]) return;

    setBoard((prevBoard) => {
      const newBoard = JSON.parse(JSON.stringify(prevBoard));
      newBoard[row][col] = "X";
      return newBoard;
    });

    const message: MoveFromUser = {
      row: row,
      col: col,
    };

    sendMessage("move_from_user", message);
  };

  const renderSquare = (row: number, col: number) => {
    return (
      <button className="square" onClick={(event) => handleClick(event, row, col)}>
        {board[row][col]}
      </button>
    );
  };

  const renderRow = (row: number) => {
    return (
      <div className="board-row" key={row}>
        {renderSquare(row, 0)}
        {renderSquare(row, 1)}
        {renderSquare(row, 2)}
      </div>
    );
  };

  const renderBoard = () => {
    return (
      <div>
        {renderRow(0)}
        {renderRow(1)}
        {renderRow(2)}
      </div>
    );
  };

  return (
    <div className="tic-tac-toe">
      <div className="board">{renderBoard()}</div>
    </div>
  );
});

export default TicTacToeComponent;
