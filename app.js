const { useState, useEffect, useRef } = React;

const COLS = 10;
const ROWS = 20;
const EMPTY_ROW = Array(COLS).fill(0);

const SHAPES = [
  [[1, 1, 1, 1]], // I
  [[1, 1, 0], [0, 1, 1]], // Z
  [[0, 1, 1], [1, 1, 0]], // S
  [[1, 1, 1], [0, 1, 0]], // T
  [[1, 1, 1], [1, 0, 0]], // L
  [[1, 1, 1], [0, 0, 1]], // J
  [[1, 1], [1, 1]],       // O
];

function randomShape() {
  const index = Math.floor(Math.random() * SHAPES.length);
  return SHAPES[index];
}

function rotate(shape) {
  return shape[0].map((_, i) => shape.map(row => row[i]).reverse());
}

function App() {
  const [board, setBoard] = useState(Array.from({ length: ROWS }, () => [...EMPTY_ROW]));
  const [piece, setPiece] = useState({ x: 3, y: 0, shape: randomShape() });
  const [score, setScore] = useState(0);
  const dropInterval = useRef(null);

  useEffect(() => {
    function handleKey(e) {
      if (e.key === 'ArrowLeft') move(-1);
      else if (e.key === 'ArrowRight') move(1);
      else if (e.key === 'ArrowDown') drop();
      else if (e.key === 'ArrowUp') rotatePiece();
      else if (e.key === ' ') hardDrop();
    }
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [piece]);

  useEffect(() => {
    dropInterval.current = setInterval(() => drop(), 500);
    return () => clearInterval(dropInterval.current);
  });

  function valid(offsetX = 0, offsetY = 0, testShape = piece.shape) {
    for (let y = 0; y < testShape.length; y++) {
      for (let x = 0; x < testShape[y].length; x++) {
        if (!testShape[y][x]) continue;
        const newX = piece.x + x + offsetX;
        const newY = piece.y + y + offsetY;
        if (newX < 0 || newX >= COLS || newY >= ROWS) return false;
        if (newY >= 0 && board[newY][newX]) return false;
      }
    }
    return true;
  }

  function mergePiece(newBoard) {
    piece.shape.forEach((row, y) => {
      row.forEach((cell, x) => {
        if (cell && piece.y + y >= 0) {
          newBoard[piece.y + y][piece.x + x] = 1;
        }
      });
    });
  }

  function clearLines(newBoard) {
    let cleared = 0;
    for (let y = ROWS - 1; y >= 0; y--) {
      if (newBoard[y].every(cell => cell)) {
        newBoard.splice(y, 1);
        newBoard.unshift([...EMPTY_ROW]);
        cleared++;
        y++;
      }
    }
    if (cleared) setScore(score + cleared);
  }

  function drop() {
    if (valid(0, 1)) {
      setPiece(p => ({ ...p, y: p.y + 1 }));
    } else {
      const newBoard = board.map(row => [...row]);
      mergePiece(newBoard);
      clearLines(newBoard);
      setBoard(newBoard);
      setPiece({ x: 3, y: 0, shape: randomShape() });
      if (!valid()) {
        alert('Game Over!');
        setBoard(Array.from({ length: ROWS }, () => [...EMPTY_ROW]));
        setScore(0);
      }
    }
  }

  function hardDrop() {
    let offset = 0;
    while (valid(0, offset + 1)) offset++;
    setPiece(p => ({ ...p, y: p.y + offset }));
    drop();
  }

  function move(dir) {
    if (valid(dir, 0)) setPiece(p => ({ ...p, x: p.x + dir }));
  }

  function rotatePiece() {
    const newShape = rotate(piece.shape);
    if (valid(0, 0, newShape)) setPiece(p => ({ ...p, shape: newShape }));
  }

  const cells = board.map(row => row.slice());
  piece.shape.forEach((row, y) => {
    row.forEach((cell, x) => {
      if (cell && piece.y + y >= 0) {
        cells[piece.y + y][piece.x + x] = 1;
      }
    });
  });

  return (
    <div className="container">
      <div id="game">
        {cells.map((row, y) =>
          row.map((cell, x) => (
            <div key={`${y}-${x}`} className={`cell${cell ? ' filled' : ''}`}></div>
          ))
        )}
      </div>
      <div id="score">Score: {score}</div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
