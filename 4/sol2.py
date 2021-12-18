rows = [x.strip() for x in open('input.txt')]

numbers = rows[0].split(',')
boards = []

for i in range(len(rows)):
  if i % 6 == 2:
    boards += [[filter(lambda x: len(x), rows[i + x].split(' ')) for x in range(5)]]


def out(board, i):
  print i

  for row in after_n(board, numbers, i):
    print '\t'.join(row)


def is_solved(board):
  for i in range(5):
    if (board[i][0] == 'x') and (board[i][1] == 'x') and (board[i][2] == 'x') and (board[i][3] == 'x') and (board[i][4] == 'x'):
      print 'a' + str(i)
      return True
    if (board[0][i] == 'x') and (board[1][i] == 'x') and (board[2][i] == 'x') and (board[3][i] == 'x') and (board[4][i] == 'x'):
      print 'b' + str(i)
      return True
  if board[0][0] == 'x' and board[1][1] == 'x' and board[2][2] == 'x' and board[3][3] == 'x' and board[4][4] == 'x':
    print 'c'
    return True
  if (board[4][0] == 'x') and (board[3][1] == 'x') and (board[2][2] == 'x') and (board[1][3] == 'x') and (board[0][4] == 'x'):
    print 'd'
    print board
    return True
  return False

def after_n(board, numbers, n):
  board_cpy = [[x for x in y] for y in board]
  for row in range(5):
    for col in range(5):
      if board_cpy[row][col] in numbers[:n]:
        board_cpy[row][col] = 'x'
  return board_cpy

def moves_to_finish(board, numbers):
  for i in range(len(numbers)):
    board_cpy = after_n(board, numbers, i)
    if is_solved(board_cpy):
      out(board_cpy, i)
      return i
  return 99999


min_val = 0
min_board = None

for board in boards:
  moves = moves_to_finish(board, numbers)
  if moves > min_val:
    min_val = moves
    min_board = board

print min_val

out = after_n(min_board, numbers, min_val)
s = 0
for row in out:
  print ' '.join(row)
  for x in row:
    if x != 'x':
      s += int(x)

print numbers[min_val - 1]
print s
