import copy # used to make deepcopy of the board.


def is_empty(board):
    for row in range(8):
        for col in range(8):
            if board[row][col] != " ":
                return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """"This function analyses the sequence of length length that ends at location (y end, x end). The function
    returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, and "CLOSED" if the
    sequence is closed. Assume that the sequence is complete (i.e., you are not just given a subsequence)
    and valid, and contains stones of only one colour."""
    start_status = ""
    end = ""

    # going to check if the x_end and y_end are first valid coordinates
    if (max(y_end, x_end) >= len(board)) or (min(y_end, x_end) < 0):
        return "Closed"
    # this code is not needed as wwe assume the sequences are valid and complete

    # check if the end values are open or closed
    if (min(y_end + d_y, x_end + d_x) < 0) or (max(y_end + d_y, x_end + d_x) >= len(board)):
        end = "Closed"  # checking if the block next to y or x exceeds the boundaries of the box
    elif board[y_end + d_y][x_end + d_x] == " ":
        end = "Open"  # checking if the square next to the end is empty
    else:
        end = "Closed"

    # checking start values
    if (min(y_end - length * (d_y), x_end - length * d_x) < 0) or (
            max(y_end - length * (d_y), x_end - length * d_x) >= len(board)):
        start_status = "Closed"
    elif board[y_end - length * d_y][x_end - length * d_x] == " ":
        start_status = "Open"
    else:
        start_status = "Closed"

    # Now combining the start value and end value: determine if open or closed
    if start_status == "Open" and end == "Open":
        return "OPEN"
    elif start_status == "Closed" and end == "Closed":
        return "CLOSED"
    else:
        return "SEMIOPEN"

    # This function is tested to work


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    ''''This function analyses the row (let’s call it R) of squares that starts at the location (y start,x start)
    and goes in the direction (d y,d x). Note that this use of the word row is different from “a row in
    a table”. Here the word row means a sequence of squares, which are adjacent either horizontally,
    or vertically, or diagonally. The function returns a tuple whose first element is the number of open
    sequences of colour col of length length in the row R, and whose second element is the number of
    semi-open sequences of colour col of length length in the row R.'''

    open_count, semi_count, current_length = 0, 0, 0
    sequence_status = ""

    for i in range(len(board) + 1):
        if y_start + d_y > len(board) or x_start + d_x > len(board) or y_start + d_y < 0 or x_start + d_x < 0:
            return open_count, semi_count

        elif board[y_start][x_start] == col:
            # need a function to return the length of a sequence.
            current_length = get_length(board, col, y_start, x_start, d_y, d_x)

            if current_length == length:
                sequence_status = is_bounded(board, (y_start + d_y * (length - 1)), (x_start + d_x * (length - 1)),
                                             length, d_y, d_x)
                y_start += (length - 1) * d_y
                x_start += (length - 1) * d_x

                if sequence_status == "OPEN":
                    open_count = open_count + 1
                if sequence_status == "SEMIOPEN":
                    semi_count = semi_count + 1


            else:
                y_start += (current_length - 1) * d_y
                x_start += (current_length - 1) * d_x

        y_start += d_y
        x_start += d_x


def get_length(board, col, y_start, x_start, d_y, d_x):
    '''helper function to get the length of a sequence'''

    length = 1  # always starts on a block of correct colour therefore starts with a value of 1.

    for i in range(len(board) + 1):
        if max(y_start + d_y, x_start + d_x) >= len(board) or min(y_start + d_y, x_start + d_x) < 0 or \
                board[y_start + d_y][x_start + d_x] != col:
            return length

        y_start += d_y
        x_start += d_x
        length += 1


def detect_rows(board, col, length):
    """This function analyses the board board. The function returns a tuple, whose first element is the
    number of open sequences of colour col of length length on the entire board, and whose second
    element is the number of semi-open sequences of colour col of length length on the entire board.
    Only complete sequences count. For example, Fig. 1 is considered to contain one open row of length
    3, and no other rows. Assume length is an integer greater or equal to 2."""

    open_count, semi_count = 0, 0
    # analyze the diagonals, vertical rows and the horizontal rows.

    # analyzing rows direction (0,1)
    for columns in range(len(board)):
        count = detect_row(board, col, columns, 0, length, 0, 1)
        open_count += count[0]
        semi_count += count[1]

    # analyzing the columns
    for rows in range(len(board)):
        count = detect_row(board, col, 0, rows, length, 1, 0)
        open_count += count[0]
        semi_count += count[1]

    # analyzing diagonals from top left to right and right to left - SIDES ONLY
    for column in range(len(board)):
        # top left to bottom right
        count = detect_row(board, col, column, 0, length, 1, 1)
        open_count += count[0]
        semi_count += count[1]

        count = detect_row(board, col, column, 7, length, 1, -1)
        open_count += count[0]
        semi_count += count[1]

    # same thing but for the TOP diagonals. 1, len(board) - 1 to not have any overlap.
    for column in range(1, len(board)-1):
        count = detect_row(board, col, 0, column, length, 1, 1)
        open_count += count[0]
        semi_count += count[1]

        count = detect_row(board, col, 0, column, length, 1, -1)
        open_count += count[0]
        semi_count += count[1]

    return open_count, semi_count

    # This function passes the testing


def search_max(board):
    """This function uses the function score() (provided) to find the optimal move for black. It finds the
    location (y,x), such that (y,x) is empty and putting a black stone on (y,x) maximizes the score of
    the board as calculated by score(). The function returns a tuple (y, x) such that putting a black
    stone in coordinates (y, x) maximizes the potential score (if there are several such tuples, you can
    return any one of them). After the function returns, the contents of board must remain the same."""

    # need to create a deep copy of the board so that the original is unaffected by the function

    board_copy = copy.deepcopy(board)
    current_score = score(board)
    testing_score = 0
    x = 0
    y = 0

    for row in range(len(board)):
        for column in range(len(board)):
            if board_copy[row][column] == " ":
                board_copy[row][column] = "b"
                testing_score = score(board_copy)
                board_copy[row][column] = " "

                if testing_score >= current_score:
                    current_score = testing_score
                    y = row
                    x = column

    return y, x

    # tested to work.


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def board_full(board):
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == " ":
                return False

    return True


def detect_winning_row(board, col, y_start, x_start, length, d_y, d_x):
    """This is an adaption of the previous detect row function"""
    current_length = 0, 0

    status = False

    for i in range(len(board) + 1):
        if y_start + d_y > len(board) or x_start + d_x > len(board) or y_start + d_y < 0 or x_start + d_x < 0:
            return status

        elif board[y_start][x_start] == col:
            # need a function to return the length of a sequence.
            current_length = get_length(board, col, y_start, x_start, d_y, d_x)

            if current_length == length:
                status = True
            else:
                y_start += (current_length - 1) * d_y
                x_start += (current_length - 1) * d_x

        y_start += d_y
        x_start += d_x


def detect_winning_rows(board, col, length):
    # adaptation of the detect winning rows function but calls the detect winning row function to locate any winning
    # sequences in the board.

    # analyzing rows direction (0,1)
    for columns in range(len(board)):
        if detect_winning_row(board, col, columns, 0, length, 0, 1):
            return True

    # analyzing the columns
    for rows in range(len(board)):
        if detect_winning_row(board, col, 0, rows, length, 1, 0):
            return True

    # analyzing diagonals from top left to right and right to left - SIDES ONLY
    for column in range(len(board)):
        # top left to bottom right
        if detect_winning_row(board, col, column, 0, length, 1, 1):
            return True

        if detect_winning_row(board, col, column, 7, length, 1, -1):
            return True

    # same thing but for the TOP diagonals.
    for column in range(1, len(board)):
        if detect_winning_row(board, col, 0, column, length, 1, 1):
            return True

        if detect_winning_row(board, col, 0, column, length, 1, -1):
            return True

    return False


def is_win(board):
    # detects if there are any winning rows of each colour

    black_count = detect_winning_rows(board, "b", 5)
    white_count = detect_winning_rows(board, "w", 5)

    if black_count > 0:
        return "Black won"
    elif white_count > 0:
        return "White won"
    elif board_full(board):
        return "Draw"
    else:
        return "Continue playing"


def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        # print(is_win(board))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        while True:
            print("Your move:")
            move_y = int(input("y coord: "))
            move_x = int(input("x coord: "))

            if  board[move_y][move_x] == " ":
                break
            else:
                print("Try again, that square is full!")

        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(is_win(board))
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_row(board, "w", 0, x, length, d_y, d_x))
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4, 6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3;
    x = 5;
    d_x = -1;
    d_y = 1;
    length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     

    y = 5;
    x = 3;
    d_x = -1;
    d_y = 1;
    length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    print(play_gomoku(8))

    # Some testing code that was borrwed from somebody else.

    # # Test 1: easy_testset_for_main_functions()
    # print("Test 1")
    # easy_testset_for_main_functions()
    #
    # # Test 2: some_test()
    # print("===============================================", "\nTest 2")
    # board = make_empty_board(8)
    # some_tests()
    #
    # # Test 3: is_clear() test
    # # Testing w/ empty board
    # print("===============================================", "\nTest 3")
    # board = make_empty_board(8)
    # if is_empty(board):
    #     print("a)Test Passed")
    #
    #     # Testing w/ non empty board
    # board[0][0] = 'w'
    # if not is_empty(board):
    #     print("b)Test Passed")
    #
    # # Test 4: is_bounded()
    # # Testing semiopen sequence
    # print("===============================================", "\nTest 4")
    # put_seq_on_board(board, 0, 0, 1, 0, 3, 'b')
    # if is_bounded(board, 2, 0, 3, 1, 0) == 'SEMIOPEN':
    #     print("a)Test Passed")
    #
    #     # Testing open sequence
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 1, 1, 0, 3, 'b')
    # if is_bounded(board, 3, 1, 3, 1, 0) == 'OPEN':
    #     print("b)Test Passed")
    #
    #     # Testing closed sequence
    # board = make_empty_board(8)
    # put_seq_on_board(board, 5, 0, 1, 1, 3, 'b')
    # if is_bounded(board, 7, 2, 3, 1, 1) == 'CLOSED':
    #     print("c)Test Passed")
    #
    # # Test 5: detect_row()
    # # Testing semiopen sequence
    # print("===============================================", "\nTest 5")
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 0, 1, 0, 3, 'b')
    # if detect_row(board, 'b', 0, 0, 3, 1, 0) == (0, 1):
    #     print("a)Test Passed")
    #
    #     # Testing open sequence
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 0, 1, 0, 3, 'b')
    # if detect_row(board, 'b', 0, 0, 3, 1, 0) == (1, 0):
    #     print("b)Test Passed")
    #
    #     # Testing open and semiopen sequence
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 0, 1, 0, 3, 'b')
    # put_seq_on_board(board, 5, 0, 1, 0, 3, 'b')
    # if detect_row(board, 'b', 0, 0, 3, 1, 0) == (1, 1):
    #     print("c)Test Passed")
    #
    #     # Testing sequences of varying lengths (4 and 3)
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 0, 1, 0, 4, 'b')
    # put_seq_on_board(board, 5, 0, 1, 0, 3, 'b')
    # if detect_row(board, 'b', 0, 0, 3, 1, 0) == (0, 1):
    #     print("d)Test Passed")
    #
    #     # Testing diagonal sequences
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 1, 1, 1, 4, 'b')
    # if detect_row(board, 'b', 0, 0, 4, 1, 1) == (1, 0):
    #     print("e)Test Passed")
    #
    # board = make_empty_board(8)
    # put_seq_on_board(board, 6, 2, -1, 1, 4, 'b')
    # if detect_row(board, 'b', 7, 1, 4, -1, 1) == (1, 0):
    #     print("f)Test Passed")
    #
    # # Test 6: detect_rows()
    # print("===============================================", "\nTest 6")
    # # Testing one row-open
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 1, 1, 1, 4, 'b')
    # if detect_rows(board, 'b', 4) == (1, 0):
    #     print("a)Test Passed")
    #
    #     # Testing one row-open, one row-semiopen
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 1, 1, 1, 4, 'b')
    # put_seq_on_board(board, 0, 6, 1, 0, 4, 'b')
    # if detect_rows(board, 'b', 4) == (1, 1):
    #     print("b)Test Passed")
    #
    #     # Testing one row-open, one row-semiopen, connected
    # board = make_empty_board(8)
    # put_seq_on_board(board, 2, 3, 0, 1, 4, 'b')
    # put_seq_on_board(board, 0, 6, 1, 0, 4, 'b')
    # if detect_rows(board, 'b', 4) == (1, 1):
    #     print("c)Test Passed")
    #
    #     # Testing one row-open but of wrong length
    # board = make_empty_board(8)
    # put_seq_on_board(board, 1, 1, 1, 1, 4, 'b')
    # if detect_rows(board, 'b', 3) == (0, 0):
    #     print("d)Test Passed")
    #
    # # Test 7: is_win()
    # print("===============================================", "\nTest 7")
    # # Testing win for black and white
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 6, 1, 0, 5, 'b')
    # if is_win(board) == "Black won":
    #     print("a)Test Passed")
    #
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 6, 1, 0, 5, 'w')
    # if is_win(board) == "White won":
    #     print("b)Test Passed")
    #
    #     # Testing continue playing for sequence of 4, board 1 square short of full, and sequence of 6
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 6, 1, 0, 4, 'b')
    # if is_win(board) == "Continue playing":
    #     print("c)Test Passed")
    #
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 6, 1, 0, 4, 'w')
    # if is_win(board) == "Continue playing":
    #     print("d)Test Passed")
    #
    # board = make_empty_board(8)
    # for i in range(4):
    #     put_seq_on_board(board, 0, i, 1, 0, 8, 'b')
    #     put_seq_on_board(board, 0, i + 4, 1, 0, 8, 'w')
    # board[7][7] = ' '
    # if is_win(board) == "Continue playing":
    #     print("e)Test Passed")
    #
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 6, 1, 0, 6, 'w')
    # if is_win(board) == "Continue playing":
    #     print("f)Test Passed")
    #
    #     # Testing draw
    # board = make_empty_board(8)
    # for i in range(4):
    #     put_seq_on_board(board, 0, i, 1, 0, 8, 'b')
    #     put_seq_on_board(board, 0, i + 4, 1, 0, 8, 'w')
    # if is_win(board) == "Draw":
    #     print("g)Test Passed")
