board = {}
chessboard = document.getElementById('chessboard')
for (var i = 0; i < 8; i++) {
    const newRow = document.createElement('div')
    newRow.className = 'row'
    chessboard.appendChild(newRow)
    for (var j = 0; j < 8; j++) {
        const newSquare = document.createElement('div')
        newSquare.classList.add('square')
        
        index = (i * 8) + j
        if ((i + j) % 2 == 0) {
            newSquare.classList.add('light')
        } else {
            newSquare.classList.add('dark') 
        }
        
        newRow.appendChild(newSquare)
        board[index] = newSquare
        
    }   
}

IMAGES = {}
pieces = ['bP', 'bR', 'bN', 'bK', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'wK']
    for (var i = 0; i < pieces.length; i++) {
        piece = pieces[i];
        src = "/static/images/" + piece + ".png";
        IMAGES[piece] = src
    }

pieces_overlay = document.getElementById('pieces-overlay')

function create_piece(notation, index) {
    piece = document.createElement('img')
    piece.src = IMAGES[notation]

    pieces_overlay.appendChild(piece)

    set_piece(piece, index)
}
function set_piece(piece, index) {
    square = board[index].getBoundingClientRect();

    piece.style.left = square.left - pieces_overlay.offsetLeft + 'px';
    piece.style.top  = square.top - pieces_overlay.offsetTop + 'px';
}
create_piece('wR', 2)
create_piece('wR', 3)