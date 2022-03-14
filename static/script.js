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

function set_piece(piece) {
    piece.src = IMAGES[piece.dataset.notation]
    square    = board[piece.dataset.index].getBoundingClientRect();

    piece.style.left = square.left - pieces_overlay.offsetLeft + 'px';
    piece.style.top  = square.top - pieces_overlay.offsetTop + 'px';
}

function move_piece(piece, index) {
    square    = board[index].getBoundingClientRect();

    piece.style.left = square.left - pieces_overlay.offsetLeft + 'px';
    piece.style.top  = square.top - pieces_overlay.offsetTop + 'px';
}
pieces = pieces_overlay.getElementsByTagName("img")
for (var i = 0; i < pieces.length; i++){
    set_piece(pieces[i])
    console.log(1)
}
