import React, { useState } from "react";
import "./TicTacToe.css";

const TicTacToe = () => {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isPlayerTurn, setIsPlayerTurn] = useState(true);
  const [winner, setWinner] = useState(null);

  const winningCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];

  const checkWinner = (board) => {
    for (let i = 0; i < winningCombinations.length; i++) {
      const [a, b, c] = winningCombinations[i];
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return board[a];
      }
    }
    return null;
  };

  const isBoardFull = (board) => {
    return board.every((square) => square !== null);
  };

  const handleClick = (index) => {
    if (!board[index] && !winner && isPlayerTurn) {
      const newBoard = board.slice();
      newBoard[index] = "X"; // Player's move
      setBoard(newBoard);
      const gameWinner = checkWinner(newBoard);
      if (gameWinner) {
        setWinner(gameWinner);
      } else if (isBoardFull(newBoard)) {
        setWinner("Draw");
      } else {
        setIsPlayerTurn(false);
        setTimeout(() => makeAIMove(newBoard), 500);
      }
    }
  };

  const makeAIMove = (newBoard) => {
    const bestMove = findBestMove(newBoard);
    newBoard[bestMove] = "O"; // AI's move
    setBoard(newBoard);
    const gameWinner = checkWinner(newBoard);
    if (gameWinner) {
      setWinner(gameWinner);
    } else if (isBoardFull(newBoard)) {
      setWinner("Draw");
    }
    setIsPlayerTurn(true);
  };

  const findBestMove = (newBoard) => {
    let bestVal = -Infinity;
    let bestMove = -1;

    for (let i = 0; i < 9; i++) {
      if (newBoard[i] === null) {
        newBoard[i] = "O"; // AI move
        let moveVal = minimax(newBoard, 0, false);
        newBoard[i] = null; // Undo move

        if (moveVal > bestVal) {
          bestMove = i;
          bestVal = moveVal;
        }
      }
    }

    return bestMove;
  };

  const minimax = (newBoard, depth, isMaximizing) => {
    const winner = checkWinner(newBoard);

    if (winner === "O") return 10 - depth;
    if (winner === "X") return depth - 10;
    if (isBoardFull(newBoard)) return 0;

    if (isMaximizing) {
      let bestVal = -Infinity;

      for (let i = 0; i < 9; i++) {
        if (newBoard[i] === null) {
          newBoard[i] = "O";
          bestVal = Math.max(bestVal, minimax(newBoard, depth + 1, false));
          newBoard[i] = null;
        }
      }
      return bestVal;
    } else {
      let bestVal = Infinity;

      for (let i = 0; i < 9; i++) {
        if (newBoard[i] === null) {
          newBoard[i] = "X";
          bestVal = Math.min(bestVal, minimax(newBoard, depth + 1, true));
          newBoard[i] = null;
        }
      }
      return bestVal;
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setIsPlayerTurn(true);
    setWinner(null);
  };

  const renderSquare = (index) => {
    return (
      <button className="square" onClick={() => handleClick(index)}>
        {board[index]}
      </button>
    );
  };

  return (
    <div className="game-container">
      <h1>Tic Tac Toe</h1>
      {winner ? <h2>{winner === "Draw" ? "It's a Draw!" : `${winner} Wins!`}</h2> : <h2>{isPlayerTurn ? "Your Turn" : "AI's Turn"}</h2>}
      <div className="board">
        {board.map((_, index) => renderSquare(index))}
      </div>
      {winner && <button className="reset-button" onClick={resetGame}>Play Again</button>}
    </div>
  );
};

export default TicTacToe;