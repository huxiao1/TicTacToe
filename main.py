import sys
from TicTacToe import TicTacToe
from utils import write_move, read_opponent_move, print_board
import time

def play_ai_vs_ai(game, first_player, strategy):
    current_player = first_player

    while True:
        player = current_player

        # 在行动前检查游戏是否结束
        winner = game.check_winner()
        if winner:
            if winner == 'draw':
                print("It's a draw!")
            else:
                print(f"Player {winner.upper()} wins!")
            break

        print(f"Player {player.upper()}'s turn.")
        time.sleep(1)

        if strategy == 'alpha-beta':
            # 使用 Alpha-Beta 剪枝算法
            best_eval = -float('inf') if player == 'x' else float('inf')
            best_moves = []

            for move in game.get_legal_moves():
                game.make_move(move[0], move[1], player)
                eval = game.alpha_beta(0, -float('inf'), float('inf'), player == 'o')
                game.undo_move(move[0], move[1])

                if player == 'x':
                    if eval > best_eval:
                        best_eval = eval
                        best_moves = [move]
                    elif eval == best_eval:
                        best_moves.append(move)
                else:
                    if eval < best_eval:
                        best_eval = eval
                        best_moves = [move]
                    elif eval == best_eval:
                        best_moves.append(move)

            if not best_moves:
                print("No valid moves left.")
                break

            best_move = best_moves[0]  # 可以随机选择最佳移动
        elif strategy == 'mcts':
            # 使用蒙特卡洛树搜索算法
            best_move = game.mcts(player)
            if best_move is None:
                print("No valid moves left.")
                break
        else:
            print("Invalid strategy.")
            return

        game.make_move(best_move[0], best_move[1], player)
        print(f"Player {player.upper()} played at row {best_move[0]+1}, col {best_move[1]+1}")
        print_board(game.board)

        # 切换玩家
        current_player = 'o' if current_player == 'x' else 'x'

def play_ai_vs_agent(game, first_player, strategy):
    x_player = 'x'  # AI 控制的 'x'
    o_player = 'o'  # 对手控制的 'o'
    count_draw = 0

    print("********************************")
    print("        Tic Tac Toe AI")
    print("********************************\n")
    print(f"AI plays as X, waiting for opponent's moves as O.\n")
    print_board(game.board)

    # 确定初始玩家
    if first_player == 'x':
        # AI 先手
        print("AI is thinking...")
        time.sleep(1)

        # AI 下棋（与之前相同的逻辑）
        best_move = ai_make_move(game, x_player, strategy)
        if best_move is None:
            print("No valid moves left.")
            return

        game.make_move(best_move[0], best_move[1], x_player)
        write_move(x_player, best_move[0], best_move[1])
        print(f"AI played at row {best_move[0]+1}, col {best_move[1]+1}")
        print_board(game.board)
        print(game.moves_count)
        count_draw = count_draw + 1
        print("count_draw1", count_draw)
        # 检查游戏是否结束
        winner = game.check_winner()
        if winner:
            announce_winner(winner)
            return

        current_player = 'o'  # 接下来轮到对手
    else:
        current_player = 'o'  # 对手先手

    while True:
        if current_player == 'x':
            # AI 的回合
            print("AI is thinking...")
            time.sleep(1)

            best_move = ai_make_move(game, x_player, strategy)
            if best_move is None:
                print("No valid moves left.")
                break

            game.make_move(best_move[0], best_move[1], x_player)
            write_move(x_player, best_move[0], best_move[1])
            print(f"AI played at row {best_move[0]+1}, col {best_move[1]+1}")
            print_board(game.board)

            # 检查游戏是否结束
            winner = game.check_winner()
            if winner:
                announce_winner(winner)
                break
            
            count_draw = count_draw + 1
            print("count_draw2", count_draw)

            if count_draw == game.n * game.n:
                print("It's a draw!")
                break

            current_player = 'o'  # 切换到对手
        else:
            # 对手的回合
            print("Waiting for opponent's move...")
            while True:
                row, col = read_opponent_move(x_player)
                if game.is_valid_move(row, col):
                    game.make_move(row, col, o_player)
                    break
                else:
                    print(f"Invalid move by opponent at row {row+1}, col {col+1}. Waiting for a valid move...")
                    continue  # 继续等待对手的有效移动

            print(f"Opponent played at row {row+1}, col {col+1}")
            print_board(game.board)

            # 检查游戏是否结束
            winner = game.check_winner()
            if winner:
                announce_winner(winner)
                break

            count_draw = count_draw + 1
            print("count_draw3", count_draw)            
            if count_draw == game.n * game.n:
                print("It's a draw!")
                break

            current_player = 'x'  # 切换到 AI

    # 游戏结束，输出结果已在循环中处理，无需再次检查

def ai_make_move(game, player, strategy):
    if strategy == 'alpha-beta':
        best_eval = -float('inf')
        best_moves = []

        for move in game.get_legal_moves():
            game.make_move(move[0], move[1], player)
            eval = game.alpha_beta(0, -float('inf'), float('inf'), False)
            game.undo_move(move[0], move[1])

            if eval > best_eval:
                best_eval = eval
                best_moves = [move]
            elif eval == best_eval:
                best_moves.append(move)

        if not best_moves:
            return None

        return best_moves[0]
    elif strategy == 'mcts':
        best_move = game.mcts(player)
        return best_move
    else:
        print("Invalid strategy.")
        return None

def announce_winner(winner):
    if winner == 'draw':
        print("It's a draw!")
    else:
        print(f"Player {winner.upper()} wins!")

 

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py n k [xo]")
    else:
        n, k, first_player = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
        game = TicTacToe(n, k)

        print("Please select an option:")
        print("1> AI vs AI")
        print("2> AI vs Agent")
        selection = input("Your selection: ")

        print("Select the strategy:")
        print("1> Alpha-Beta")
        print("2> Monte Carlo Tree Search")
        strategy_choice = input("Your selection: ")

        if strategy_choice == '1':
            strategy = 'alpha-beta'
        elif strategy_choice == '2':
            strategy = 'mcts'
        else:
            print("Invalid strategy selection.")
            exit()

        if selection == '1':
            play_ai_vs_ai(game, first_player, strategy)
        elif selection == '2':
            play_ai_vs_agent(game, first_player, strategy)
        else:
            print("Invalid selection.")
