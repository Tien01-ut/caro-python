"""
AI Player for Caro Game using Minimax algorithm
"""

import random
from shared.constants import WIN_CONDITION


class AIPlayer:
    """AI player using Minimax algorithm with alpha-beta pruning"""
    
    def __init__(self, difficulty="medium", board_size=15):
        """
        Initialize AI player
        difficulty: "easy", "medium", "hard"
        board_size: size of the game board
        """
        self.difficulty = difficulty
        self.board_size = board_size
        # Reduced depth for faster response (0 = immediate, 1 = look ahead 1 move)
        self.max_depth = {"easy": 0, "medium": 1, "hard": 2}[difficulty]
        self.ai_symbol = 2  # AI plays as O (2)
        self.player_symbol = 1  # Player is X (1)
    
    def get_move(self, board):
        """Get best move for AI"""
        if self.difficulty == "easy":
            return self.get_random_move(board)
        else:
            return self.get_best_move(board)
    
    def get_random_move(self, board):
        """Get random valid move (easy mode)"""
        valid_moves = []
        for i in range(self.self.board_size):
            for j in range(self.self.board_size):
                if board[i][j] == 0:
                    valid_moves.append((i, j))
        
        if valid_moves:
            return random.choice(valid_moves)
        return None
    
    def get_best_move(self, board):
        """Get best move using Minimax with alpha-beta pruning"""
        # First check if there's an immediate winning move
        winning_move = self.find_winning_move(board, self.ai_symbol)
        if winning_move:
            return winning_move
        
        # Check if need to block opponent's winning move
        blocking_move = self.find_winning_move(board, self.player_symbol)
        if blocking_move:
            return blocking_move
        
        best_score = float('-inf')
        best_move = None
        
        # Get moves near existing pieces (optimization)
        moves = self.get_smart_moves(board)
        
        for move in moves:
            i, j = move
            board[i][j] = self.ai_symbol
            score = self.minimax(board, 0, False, float('-inf'), float('inf'))
            board[i][j] = 0
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move else self.get_random_move(board)
    
    def find_winning_move(self, board, symbol):
        """Find immediate winning move for symbol"""
        for i in range(self.self.board_size):
            for j in range(self.self.board_size):
                if board[i][j] == 0:
                    board[i][j] = symbol
                    if self.check_winner(board, symbol):
                        board[i][j] = 0
                        return (i, j)
                    board[i][j] = 0
        return None
    
    def get_smart_moves(self, board):
        """Get moves near existing pieces (optimization)"""
        moves = set()
        has_piece = False
        
        # Check if board is empty
        for i in range(self.self.board_size):
            for j in range(self.self.board_size):
                if board[i][j] != 0:
                    has_piece = True
                    # Add cells around this piece (reduced range for speed)
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            ni, nj = i + di, j + dj
                            if (0 <= ni < self.board_size and 0 <= nj < self.board_size 
                                and board[ni][nj] == 0):
                                moves.add((ni, nj))
        
        # If board is empty, start in center
        if not has_piece:
            center = self.board_size // 2
            return [(center, center)]
        
        # Limit number of moves to consider (max 15 for speed)
        moves_list = list(moves) if moves else [(self.board_size // 2, self.board_size // 2)]
        if len(moves_list) > 15:
            # Prioritize moves closer to center
            center = self.board_size // 2
            moves_list.sort(key=lambda m: abs(m[0] - center) + abs(m[1] - center))
            moves_list = moves_list[:15]
        
        return moves_list
    
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning"""
        # Check terminal states
        ai_win = self.check_winner(board, self.ai_symbol)
        player_win = self.check_winner(board, self.player_symbol)
        
        if ai_win:
            return 1000 - depth
        if player_win:
            return -1000 + depth
        if depth >= self.max_depth or self.is_board_full(board):
            return self.evaluate_board(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_smart_moves(board):
                i, j = move
                board[i][j] = self.ai_symbol
                eval_score = self.minimax(board, depth + 1, False, alpha, beta)
                board[i][j] = 0
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_smart_moves(board):
                i, j = move
                board[i][j] = self.player_symbol
                eval_score = self.minimax(board, depth + 1, True, alpha, beta)
                board[i][j] = 0
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def evaluate_board(self, board):
        """Evaluate board position"""
        score = 0
        
        # Evaluate all lines
        # Rows
        for i in range(self.self.board_size):
            for j in range(self.board_size - WIN_CONDITION + 1):
                line = [board[i][j + k] for k in range(WIN_CONDITION)]
                score += self.evaluate_line(line)
        
        # Columns
        for i in range(self.board_size - WIN_CONDITION + 1):
            for j in range(self.self.board_size):
                line = [board[i + k][j] for k in range(WIN_CONDITION)]
                score += self.evaluate_line(line)
        
        # Diagonals (top-left to bottom-right)
        for i in range(self.board_size - WIN_CONDITION + 1):
            for j in range(self.board_size - WIN_CONDITION + 1):
                line = [board[i + k][j + k] for k in range(WIN_CONDITION)]
                score += self.evaluate_line(line)
        
        # Diagonals (top-right to bottom-left)
        for i in range(self.board_size - WIN_CONDITION + 1):
            for j in range(WIN_CONDITION - 1, self.board_size):
                line = [board[i + k][j - k] for k in range(WIN_CONDITION)]
                score += self.evaluate_line(line)
        
        return score
    
    def evaluate_line(self, line):
        """Evaluate a line of 5 cells"""
        ai_count = line.count(self.ai_symbol)
        player_count = line.count(self.player_symbol)
        empty_count = line.count(0)
        
        # If both players have pieces, line is blocked
        if ai_count > 0 and player_count > 0:
            return 0
        
        # AI has pieces
        if ai_count > 0:
            if ai_count == 4 and empty_count == 1:
                return 500  # About to win
            elif ai_count == 3 and empty_count == 2:
                return 100
            elif ai_count == 2 and empty_count == 3:
                return 10
            elif ai_count == 1 and empty_count == 4:
                return 1
        
        # Player has pieces (negative for AI)
        if player_count > 0:
            if player_count == 4 and empty_count == 1:
                return -500  # Must block
            elif player_count == 3 and empty_count == 2:
                return -100
            elif player_count == 2 and empty_count == 3:
                return -10
            elif player_count == 1 and empty_count == 4:
                return -1
        
        return 0
    
    def check_winner(self, board, symbol):
        """Check if symbol has won"""
        # Check rows
        for i in range(self.self.board_size):
            for j in range(self.board_size - WIN_CONDITION + 1):
                if all(board[i][j + k] == symbol for k in range(WIN_CONDITION)):
                    return True
        
        # Check columns
        for i in range(self.board_size - WIN_CONDITION + 1):
            for j in range(self.self.board_size):
                if all(board[i + k][j] == symbol for k in range(WIN_CONDITION)):
                    return True
        
        # Check diagonals (top-left to bottom-right)
        for i in range(self.board_size - WIN_CONDITION + 1):
            for j in range(self.board_size - WIN_CONDITION + 1):
                if all(board[i + k][j + k] == symbol for k in range(WIN_CONDITION)):
                    return True
        
        # Check diagonals (top-right to bottom-left)
        for i in range(self.board_size - WIN_CONDITION + 1):
            for j in range(WIN_CONDITION - 1, self.board_size):
                if all(board[i + k][j - k] == symbol for k in range(WIN_CONDITION)):
                    return True
        
        return False
    
    def is_board_full(self, board):
        """Check if board is full"""
        for i in range(self.self.board_size):
            for j in range(self.self.board_size):
                if board[i][j] == 0:
                    return False
        return True
