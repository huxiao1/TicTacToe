import random
import math
import copy

class Node:
    def __init__(self, state, parent, player):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.player = player

    def uct(self):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + math.sqrt(2 * math.log(self.parent.visits) / self.visits)

class TicTacToe:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.board = [[' ' for _ in range(n)] for _ in range(n)]
        self.moves_count = 0

    def is_valid_move(self, row, col):
        return 0 <= row < self.n and 0 <= col < self.n and self.board[row][col] == ' '

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.moves_count += 1
            return True
        return False

    def undo_move(self, row, col):
        if self.board[row][col] != ' ':
            self.board[row][col] = ' '
            self.moves_count -= 1

    def get_legal_moves(self):
        return [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']

    def check_winner(self):
        directions = [(0,1), (1,0), (1,1), (-1,1)]
        for x in range(self.n):
            for y in range(self.n):
                player = self.board[x][y]
                if player != ' ':
                    for dx, dy in directions:
                        count = 1
                        nx, ny = x + dx, y + dy
                        while 0 <= nx < self.n and 0 <= ny < self.n and self.board[nx][ny] == player:
                            count += 1
                            if count == self.k:
                                return player
                            nx += dx
                            ny += dy
        if self.moves_count == self.n * self.n:
            return 'draw'
        return None

    def evaluate(self):
        winner = self.check_winner()
        if winner == 'x':
            return 1
        elif winner == 'o':
            return -1
        elif winner == 'draw':
            return 0
        else:
            return None

    def alpha_beta(self, depth, alpha, beta, is_maximizing_player):
        evaluation = self.evaluate()
        if evaluation is not None:
            return evaluation

        if is_maximizing_player:
            max_eval = -float('inf')
            for move in self.get_legal_moves():
                self.make_move(move[0], move[1], 'x')
                eval = self.alpha_beta(depth + 1, alpha, beta, False)
                self.undo_move(move[0], move[1])
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_legal_moves():
                self.make_move(move[0], move[1], 'o')
                eval = self.alpha_beta(depth + 1, alpha, beta, True)
                self.undo_move(move[0], move[1])
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def mcts(self, player, simulations=1000):
        winner = self.check_winner()
        if winner:
            return None

        root = Node(copy.deepcopy(self.board), None, player)
        for _ in range(simulations):
            node = root
            self.board = copy.deepcopy(root.state)
            simulation_player = player

            # Selection
            while node.children:
                node = max(node.children, key=lambda n: n.uct())
                self.board = copy.deepcopy(node.state)
                winner = self.check_winner()
                if winner:
                    break
                simulation_player = 'o' if simulation_player == 'x' else 'x'

            winner = self.check_winner()
            if winner:
                reward = 1 if winner == player else -1 if winner != 'draw' else 0
                # Backpropagation
                while node:
                    node.visits += 1
                    if node.player == player:
                        node.wins += reward
                    else:
                        node.wins -= reward
                    node = node.parent
                continue

            # Expansion
            legal_moves = self.get_legal_moves()
            for move in legal_moves:
                self.make_move(move[0], move[1], simulation_player)
                child_state = copy.deepcopy(self.board)
                child_node = Node(child_state, node, simulation_player)
                node.children.append(child_node)
                self.undo_move(move[0], move[1])

            # Simulation
            if node.children:
                node = random.choice(node.children)
                self.board = copy.deepcopy(node.state)
                simulation_player = node.player
            else:
                continue

            winner = self.check_winner()
            while winner is None:
                legal_moves = self.get_legal_moves()
                if not legal_moves:
                    break
                move = random.choice(legal_moves)
                simulation_player = 'o' if simulation_player == 'x' else 'x'
                self.make_move(move[0], move[1], simulation_player)
                winner = self.check_winner()

            # Backpropagation
            reward = 1 if winner == player else -1 if winner != 'draw' else 0
            while node:
                node.visits += 1
                if node.player == player:
                    node.wins += reward
                else:
                    node.wins -= reward
                node = node.parent

        if not root.children:
            return None

        best_child = max(root.children, key=lambda n: n.visits)
        best_move = None
        for i in range(self.n):
            for j in range(self.n):
                if root.state[i][j] != best_child.state[i][j]:
                    best_move = (i, j)
                    break
            if best_move:
                break

        self.board = copy.deepcopy(root.state)
        return best_move
