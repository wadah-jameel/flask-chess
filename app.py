from flask import Flask, render_template, request, jsonify
import chess
import random

app = Flask(__name__)

# In-memory storage for the game state (for demo purposes)
# In a production app, use a database or session-based storage.
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    move_uci = data.get('move')
    
    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
            
            # Simple AI: Make a random move if the game isn't over
            if not board.is_game_over():
                ai_move = random.choice(list(board.legal_moves))
                board.push(ai_move)
            
            return jsonify({
                'fen': board.fen(),
                'game_over': board.is_game_over(),
                'status': board.result()
            })
        else:
            return jsonify({'error': 'Invalid move'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/reset', methods=['POST'])
def reset():
    board.reset()
    return jsonify({'fen': board.fen()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
