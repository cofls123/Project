import tkinter.messagebox
import tkinter
import random

# 전역 변수
index = 0
timer = 0
score = 0
difficulty = 0
tsugi = 0
timerCount = 0 # 진행 시간 체크
noClickTimer = 0  # 클릭 없는 시간 (프레임 단위)
turnCount = 0
bonusCount = 0  # 지금까지 지급한 보너스 횟수
autoPlace = False
jokerHold = False  # 조커 한 턴 유지 여부 체크용 변수

cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0


# 최고 기록 불러오기 (게임 시작 시)
hisc = 100
inFile = open('hiscRecord.txt', 'r')
inStr = inFile.read()
if inStr.isdigit():
    hisc = int(inStr)
inFile.close()

#공간정보 저장
neko = [] 
check = []
for i in range(12):
    neko.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # 리스트 안쪽에 리스트(2차원 배열)
    check.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0])

# 블럭 정보 저장
blockCount = [0,0,0,0,0,0,0]

# 함수 영역
def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

#esc 눌렀을 때 게임 리셋
def key_down(e):
    global index, score, timerCount, tsugi, noClickTimer
    if e.keysym == 'Escape':
        answer = tkinter.messagebox.askyesno('종료 확인','게임을 종료하시겠습니까?')
        if answer:
            index=0
            score=0
            timerCount=0
            tsugi = 0
            
            # 화면 클리어
            cvs.delete("NEKO")
            cvs.delete("CURSOR")
            cvs.delete("INFO")
            cvs.delete("OVER")

def mouse_press(e):
    global mouse_c
    mouse_c = 1

def draw_neko():
    cvs.delete("NEKO")  # 캔버스에서 태그 'NEKO'을 삭제 / 지우고 밑에서 다시 그리는 것을 반복
    for y in range(12):  # 세로
        for x in range(10):  # 가로
            if neko[y][x] > 0:  # 모든 칸에 대해서 실행 / y에 있는 값 중에 x번째 값 / neko[y]가 변수
                cvs.create_image(x * 72 + 60, y * 72 + 60, image=img_neko[neko[y][x]], tag="NEKO") #'NEKO' 생성

# 조커 블록이 있을 때의 나머지 블록들은 같아야 함 / 2개의 블록
def is_match(a, b):
    if a == 0 or b == 0: # 빈칸은 매칭 제외
        return False
    if a == 8 or b == 8: # 어떤 블록과도 매칭
        return True
    return a == b

# 조커 블록이 있을 때의 나머지 블록들은 같아야 함 / 3개의 블록
def is_match_three(a, b, c):
    # a, b, c 중 0이 있으면 안됨
    if 0 in (a, b, c):
        return False    
    threeBlocks = [a, b, c]
    # 조커를 제외한 블록 리스트
    filtered = [x for x in threeBlocks if x != 8]    
     # 조커가 포함되어도 조커가 아닌 블록들은 모두 동일해야 함
    first = filtered[0]
    return all(x == first for x in filtered)

# 조커 블록이 있을 때의 나머지 블록들은 같아야 함 / 4개의 블록
def is_match_four(a, b, c, d):
    if 0 in (a, b, c, d):
        return False
    fourBlocks = [a, b, c, d]
    filtered = [x for x in fourBlocks if x != 8]
    first = filtered[0]
    return all(x == first for x in filtered)


def check_neko():
    for y in range(12):
        for x in range(10):  # 모든 칸에 대해서 실행
            check[y][x] = neko[y][x]  # neko -> check (복사) / 위치 체크하는 부분

    for y in range(1, 11):
        for x in range(10):  # 맨 윗줄와 아래줄을 제외한 모든 칸에 대해서 실행
            if check[y][x] > 0:  # 세로 블럭
                if is_match_three(check[y - 1][x], check[y][x], check[y + 1][x]):
                    if neko[y][x] != 8: blockCount[neko[y][x]-1] +=3
                    neko[y - 1][x] = 7
                    neko[y][x] = 7
                    neko[y + 1][x] = 7

    for y in range(12):
        for x in range(1, 9):  # 맨 왼쪽과 맨 오른쪽을 제외한 모든 칸에 대해서 실행
            if check[y][x] > 0:  # 가로 블록
                if is_match_three(check[y][x - 1], check[y][x], check[y][x + 1]):
                    if neko[y][x] != 8: blockCount[neko[y][x]-1] +=3
                    neko[y][x - 1] = 7 # 파괴 전 이펙트
                    neko[y][x] = 7
                    neko[y][x + 1] = 7

    for y in range(1, 11):
        for x in range(1, 9):
            if check[y][x] > 0:  # 대각선 블록
                if is_match(check[y - 1][x - 1], check[y][x]) and is_match(check[y + 1][x + 1], check[y][x]):
                    if neko[y][x] != 8: blockCount[neko[y][x]-1] +=3
                    neko[y - 1][x - 1] = 7
                    neko[y][x] = 7
                    neko[y + 1][x + 1] = 7
                if is_match(check[y + 1][x - 1], check[y][x]) and is_match(check[y - 1][x + 1], check[y][x]):
                    if neko[y][x] != 8: blockCount[neko[y][x]-1] +=3
                    neko[y + 1][x - 1] = 7
                    neko[y][x] = 7
                    neko[y - 1][x + 1] = 7

    for y in range(0, 11):
        for x in range(0, 9):
            if check[y][x] > 0:  # 네모 블록
                if is_match_four(check[y + 1][x], check[y][x + 1], check[y][x], check[y+1][x+1]):
                    if neko[y][x] != 8: blockCount[neko[y][x]-1] +=4
                    neko[y][x] = 7
                    neko[y][x+1] = 7
                    neko[y + 1][x] = 7
                    neko[y + 1][x + 1] = 7

def sweep_neko():
    num = 0
    for y in range(12):
        for x in range(10):  # 모든 칸에 대해서 실행
            if neko[y][x] == 7:
                neko[y][x] = 0  # 빈칸
                num = num + 1   # 파괴된 블럭 개수를 표현
    return num

def drop_neko(): #블럭이 아래로 떨어지는 것
    flg = False
    for y in range(10, -1, -1):  # 아래에서 위로 검사
        for x in range(10):  #모든 블럭에 대해서 검사
            if neko[y][x] != 0 and neko[y + 1][x] == 0:  # 아래 블럭이 없을 때 위의 블럭이 아래로 이동
                neko[y + 1][x] = neko[y][x]
                neko[y][x] = 0
                flg = True  # 계속 검사해서 블럭이 내려갈 수 있도록 반복
    return flg

def over_neko():
    for x in range(10):
        if neko[0][x] > 0:  # 맨 윗줄에 블럭이 있으면
            return True  # 게임 종료
    return False

def set_neko():
    for x in range(10):
        neko[0][x] = random.randint(0, difficulty)  # 블럭을 생성 (0 빈, 1~6 일반블럭)

def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Times New Roman", siz, "bold")
    cvs.create_text(x + 2, y + 2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

def game_main():  # 0-6개의 구간으로 나눠짐 index
    global index, timer, score, hisc, difficulty, tsugi, timerCount, noClickTimer
    global turnCount, blockCount, autoPlace, jokerHold, total, bonusCount
    global cursor_x, cursor_y, mouse_c
    if index == 0:  # 타이틀 로고
        draw_txt("야옹야옹", 312, 240, 100, "violet", "TITLE")
        cvs.create_rectangle(168, 384, 456, 456, fill="skyblue", width=0, tag="TITLE")
        draw_txt("Easy", 312, 420, 40, "white", "TITLE")
        cvs.create_rectangle(168, 528, 456, 600, fill="lightgreen", width=0, tag="TITLE")
        draw_txt("Normal", 312, 564, 40, "white", "TITLE")
        cvs.create_rectangle(168, 672, 456, 744, fill="orange", width=0, tag="TITLE")
        draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        index = 1
        mouse_c = 0
    elif index == 1:  # 타이틀 화면, 시작 대기
        difficulty = 0
        if mouse_c == 1:
            if 168 < mouse_x and mouse_x < 456 and 384 < mouse_y and mouse_y < 456:
                difficulty = 4
            if 168 < mouse_x and mouse_x < 456 and 528 < mouse_y and mouse_y < 600:
                difficulty = 5
            if 168 < mouse_x and mouse_x < 456 and 672 < mouse_y and mouse_y < 744:
                difficulty = 6
        if difficulty > 0:
            for y in range(12):
                for x in range(10):
                    neko[y][x] = 0
            #리셋 시키는 변수들          
            mouse_c = 0
            score = 0
            tsugi = 0
            cursor_x = 0
            cursor_y = 0
            turnCount = 0
            timerCount = 0
            blockCount = [0,0,0,0,0,0,0]
            set_neko()
            draw_neko()
            cvs.delete("TITLE")
            index = 2
    elif index == 2:  # 블록 낙하
        if drop_neko() == False:
            # 한 턴 유지 → 이후 변환
            if jokerHold:
                for y in range(12):
                    for x in range(10):
                        if neko[y][x] == 8:
                            neko[y][x] = random.randint(1, difficulty)
                jokerHold = False
            else:
                # 조커가 존재할 시 유지 시작
                for y in range(12):
                    for x in range(10):
                        if neko[y][x] == 8:
                            jokerHold = True
                            break
                    if jokerHold:
                        break
            index = 3
        draw_neko()
    elif index == 3:  # 나란히 놓인 블록 확인
        check_neko()
        draw_neko()
        index = 4
    elif index == 4:  # 나란히 놓인 고양이 블록이 있다면
        # 최고 기록 저장 (게임 도중 점수가 갱신될 경우)
        if score > hisc:
            hisc = score
            outFile = open("hiscRecord.txt", "w")
            outFile.write(str(hisc))
            outFile.close()

        sc = sweep_neko()
        score = score + sc * difficulty * 2 # 기본 점수
        
        # 보너스 점수
        if total // 10 > bonusCount:
            score += 10
            bonusCount += 1               
            
        if sc > 0:
            index = 2
        else:
            if not over_neko():
                # autoPlace가 True면 조커 등장 조건 무시
                if not autoPlace and turnCount%5 == 0 and turnCount>0: # 5턴 때마다 조커 블록 등장
                    tsugi = 8 # 조커 블록 등장
                else:
                    tsugi = random.randint(1, difficulty)  
                index = 5
            else:
                index = 6
                timer = 0
        draw_neko()
    elif index == 5:  # 마우스 입력 대기

        if 24 <= mouse_x and mouse_x < 24 + 72 * 10 and 24 <= mouse_y and mouse_y < 24 + 72 * 12:
            cursor_x = int((mouse_x - 24) / 72)  
            cursor_y = int((mouse_y - 24) / 72) 
            if mouse_c == 1:
                mouse_c = 0
                set_neko()
                neko[cursor_y][cursor_x] = tsugi
                tsugi = 0
                turnCount += 1 # 블록을 배치한 뒤 turnCount += 1
                index = 2
                noClickTimer = 0 # 클릭 시 타이머 리셋 

        # 자동 배치 타이머  
        noClickTimer+=1   
        if noClickTimer >= 50:
            autoPlace = True
            set_neko()
            if tsugi !=0:
                neko[random.randint(0, 11)][random.randint(0, 9)] = tsugi
                tsugi = 0               
                index = 2
                noClickTimer = 0 # 클릭 안할 시 타이머 리셋 
        else:
            autoPlace = False

        cvs.delete("CURSOR")  # 커서가 지워졌다가 생길 수 있도록
        cvs.create_image(cursor_x * 72 + 60, cursor_y * 72 + 60, image=cursor, tag="CURSOR")  #이미지를 그리고 커서를 입힘
        draw_neko()
    elif index == 6:  # 게임 오버
        timer = timer + 1
        if timer == 1:
            draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 50:
            cvs.delete("OVER")
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE " + str(score), 160, 60, 32, "blue", "INFO")
    draw_txt("HISC " + str(hisc), 450, 60, 32, "yellow", "INFO")
    #파괴된 블록 개수 합산
    total = sum(blockCount)
    draw_txt("BlockCount  " + str(total), 890, 100, 24, "blue", "INFO")
    if tsugi > 0:
        cvs.create_image(890, 260, image=img_neko[tsugi], tag="INFO")
    
    # 타이머 증가 및 표시 (프레임 단위)
    if index in [2,3,4,5]: # 게임 플레이 하는 시간 동안 타이머 표시
        timerCount += 1
        min = timerCount // 60
        sec = timerCount % 60
        draw_txt(f"TIME {min:02}:{sec:02}", 890, 60, 24, "white", "INFO")
    root.after(100, game_main)
    

# 메인 영역: tkinter 기본구조
root = tkinter.Tk()
root.title("블록 낙하 퍼즐 '야옹야옹'")
root.resizable(False, False)  # 창 크기 변경 불가능
root.bind("<Motion>", mouse_move)
root.bind("<ButtonPress>", mouse_press)
root.bind("<KeyPress>", key_down)
cvs = tkinter.Canvas(root, width=1056, height=912)
cvs.pack()

#이미지와 관련된 영역
bg = tkinter.PhotoImage(file="neko_bg_EX.png")
cursor = tkinter.PhotoImage(file="neko_cursor.png")
img_neko = [
    None,
    tkinter.PhotoImage(file="neko1.png"),
    tkinter.PhotoImage(file="neko2.png"),
    tkinter.PhotoImage(file="neko3.png"),
    tkinter.PhotoImage(file="neko4.png"),
    tkinter.PhotoImage(file="neko5.png"),
    tkinter.PhotoImage(file="neko6.png"),
    tkinter.PhotoImage(file="neko_niku.png"),
    tkinter.PhotoImage(file="neko0.png") # 조커 블록 이미지
] 

cvs.create_image(528, 456, image=bg)
game_main()
root.mainloop()
