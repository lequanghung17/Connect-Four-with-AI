# Connect-Four-with-AI

## 1. Minimax Algorithm
- Minimax là một thuật toán tìm kiếm tối ưu được sử dụng trong các trò chơi đối kháng, trong đó có hai người chơi: người chơi hiện tại (AI) và đối thủ (người chơi). Mục tiêu của thuật toán này là giúp AI tìm ra nước đi tốt nhất bằng cách dự đoán tất cả các tình huống có thể xảy ra trong trò chơi.
  - Maximizing Player (AI): AAI cố gắng tìm kiếm các nước đi có giá trị cao nhất. Nó sẽ xem xét tất cả các nhánh có thể có và chọn nhánh có điểm số cao nhất. Điểm này được đánh giá dựa trên trạng thái bàn cờ.
  - Minimizing Player (Player): Người chơi sẽ cố gắng làm giảm điểm số của AI, tức là người chơi muốn tối thiểu hóa điểm số của AI, vì vậy AI cần dự đoán những nước đi mà người chơi sẽ thực hiện để đánh bại nó.
 
- Khi AI đang chơi, thuật toán Minimax sẽ xây dựng một cây tìm kiếm trong đó mỗi nút đại diện cho một trạng thái bàn cờ sau một nước đi, và mỗi nhánh đại diện cho một nước đi có thể có. Mỗi cấp độ của cây sẽ luân phiên giữa lượt của AI (maximizing player) và lượt của người chơi (minimizing player).

`Ví dụ:`

  ![image](https://github.com/user-attachments/assets/ec9a0d9e-4f53-40a6-8b89-282950036a12)
  
`Ở tầng chứa những ô màu trắng sẽ chọn giá trị Max từ các giá trị của các ô ở tầng dưới nó, trong khi tầng chứa các ô màu đen sẽ chọn ngược lại (giá trị Min). Ví dụ ở tầng cuối cùng ta có các cặp giá trị [-1,3], [5,1], ... vậy nên ở tầng bên trên, các giá trị xuất hiện ở các ô trắng sẽ là [3],[5],..., tương tự với các ô màu đen.`

- Khi thuật toán Minimax tìm kiếm đến các lá cây (nơi không có nước đi nữa, tức là trò chơi đã kết thúc hoặc không còn bước đi hợp lệ), thuật toán sẽ đánh giá kết quả của trạng thái đó:

  - Nếu AI thắng, điểm số là +1.
  - nNếu người chơi thắng, điểm số là -1.
  - Nếu trò chơi hòa hoặc không còn nước đi hợp lệ, điểm số là 0.

- Sau đó, thuật toán Minimax quay lại các cấp trên để quyết định nước đi tối ưu cho người chơi (AI và người chơi thay phiên nhau).

## 2. Minimax với Alpha-Beta Pruning

- Trong trò chơi thực tế, việc duyệt qua tất cả các nhánh của cây tìm kiếm có thể tốn rất nhiều thời gian, đặc biệt là khi độ sâu của cây tìm kiếm lớn. Alpha-Beta Pruning là một cải tiến giúp giảm thiểu thời gian tính toán bằng cách cắt tỉa các nhánh không cần thiết trong cây tìm kiếm.

  - Alpha: Đây là giá trị tối thiểu mà maximizing player (AI) có thể đảm bảo được trong quá trình tìm kiếm. Nếu một nhánh trong cây tìm kiếm có giá trị nhỏ hơn Alpha, AI sẽ không cần phải xem xét nhánh đó nữa, vì AI đã biết rằng không có giá trị nào tốt hơn giá trị Alpha đã tìm được.
  - Beta: Đây là giá trị tối đa mà minimizing player (người chơi) có thể đảm bảo được. Nếu một nhánh có giá trị lớn hơn Beta, người chơi sẽ không cần phải xem xét nhánh đó nữa, vì người chơi đã biết rằng không có giá trị nào tệ hơn giá trị Beta.

- Nếu giá trị của một nhánh không thể thay đổi quyết định hiện tại của AI hoặc người chơi, thì nhánh đó sẽ bị cắt tỉa, không cần phải tính toán thêm.

` Ví dụ:`

![image](https://github.com/user-attachments/assets/a77aa04b-f5ba-42a8-b7ac-773e5d43f49b)

` Từ các căp giá trị ở tầng cuối là [-1,3], [5,X]. Ta sẽ điền được giá trị cho các ô trắng ở tầng bên trên bằng cách lấy giá trị Max của từng cặp, với ô trắng đầu tiên sẽ có giá trị = 3, ô trắng thứ 2 sẽ có giá trị = Y với Y >= 5. Ở tầng bên trên tiếp theo, ta sẽ chọn giá trị Min giữa 2 ô trắng và ta biết rằng chắc chắn giá trị đó sẽ là 3 vì 3 < 5. Vì vậy, 3 sẽ luôn là giá trị được điền và ta sẽ không cần quan tâm giá trị của Y và X, hay nói cách khác, ta sẽ không cần duyệt qua nhánh bên phải.`

` 1 ví dụ khác về sự khác biệt giữa Minimax không có AB Pruning và có AB Pruning`

![image](https://github.com/user-attachments/assets/bfa90a5a-b520-4fae-a131-816c69aa28d4)

### Hàm Maximizing Player (AI):

- AI cố gắng tối đa hóa điểm số, tức là nó sẽ chọn giá trị lớn nhất từ các nhánh con.

- Khi AI duyệt qua cây, Alpha được cập nhật để theo dõi giá trị tối ưu nhất mà AI có thể đảm bảo. Nếu giá trị của một nhánh lớn hơn giá trị hiện tại của Alpha, AI sẽ thay đổi Alpha.

- Nếu AI gặp một nhánh mà Beta của người chơi (Minimizing Player) nhỏ hơn hoặc bằng Alpha, thuật toán sẽ cắt tỉa nhánh này, vì AI biết rằng người chơi không thể làm giảm giá trị của AI xuống dưới giá trị đã có trong Alpha.

### Hàm Minimizing Player (Player):

- Người chơi cố gắng tối thiểu hóa điểm số của AI, tức là chọn nhánh có giá trị thấp nhất để giảm điểm cho AI.

- Khi người chơi duyệt qua cây, Beta được cập nhật để theo dõi giá trị tối ưu nhất mà người chơi có thể đảm bảo. Nếu giá trị của một nhánh nhỏ hơn giá trị hiện tại của Beta, người chơi sẽ thay đổi Beta.

- Nếu người chơi gặp một nhánh mà Alpha của AI (Maximizing Player) lớn hơn hoặc bằng Beta, thuật toán sẽ cắt tỉa nhánh này, vì người chơi biết rằng AI sẽ không chọn nhánh này do nó không có lợi cho AI.

### Code for Minimax with Alpha-Beta Pruning

```
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: 
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: 
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
```

## Tài liệu đọc hiểu và tham khảo

- [Wikipedia](https://en.wikipedia.org/wiki/Minimax)
- [Youtube](https://www.youtube.com/watch?v=l-hh51ncgDI&t=143s)
- [GeeksforGeeks](https://www.geeksforgeeks.org/mini-max-algorithm-in-artificial-intelligence/)


