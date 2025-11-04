import tkinter as tk
from tkinter import scrolledtext
import math
import re

# 보안을 강화한 계산 함수
def safe_eval(expression):
    """
    안전하게 수학적 표현식을 평가합니다.
    허용된 수학 함수 및 상수만 사용할 수 있습니다.
    """
    # 1. 표현식을 Python의 math 모듈이 이해할 수 있는 형태로 변환
    # 거듭제곱 연산자 변경
    expression = expression.replace('^', '**')
    # 상수 변경
    expression = expression.replace('π', 'math.pi')
    expression = expression.replace('e', 'math.e')
    # 제곱근 함수 변경
    expression = expression.replace('√', 'math.sqrt')
    
    # 2. 삼각함수(sin, cos, tan)를 각도(degree) 기반으로 계산하도록 변환
    # 예: "sin(30)" -> "math.sin(math.radians(30))"
    for func in ['sin', 'cos', 'tan']:
        expression = re.sub(r'\b' + func + r'\((.*?)\)', r'math.' + func + r'(math.radians(\1))', expression)

    # 3. 로그 함수 이름 변경
    expression = expression.replace('ln', 'math.log') # 자연로그
    expression = expression.replace('log', 'math.log10') # 상용로그

    # 허용된 이름 공간 정의
    allowed_names = {
        "math": math,
        "abs": abs,
        "float": float,
        "int": int,
    }

    # 코드를 직접 컴파일하여 __builtins__를 비활성화 (보안 강화)
    code = compile(expression, "<string>", "eval")
    
    # eval 실행
    return eval(code, {"__builtins__": {}}, allowed_names)


# GUI 애플리케이션 클래스
class ScientificCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("공학용 계산기")
        self.root.geometry("800x600") # 창 크기 확장

        # 메인 프레임
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # 계산기 프레임 (디스플레이 + 버튼)
        calculator_frame = tk.Frame(main_frame, bd=5, relief=tk.RIDGE)
        calculator_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # 계산식 표시 화면
        self.display_var = tk.StringVar()
        self.display = tk.Entry(calculator_frame, textvariable=self.display_var, font=('Arial', 28), bd=10, insertwidth=2, width=20, borderwidth=4, justify='right')
        self.display.grid(row=0, column=0, columnspan=5, pady=15, sticky="nsew")

        # 버튼 생성
        self.create_buttons(calculator_frame)

        # 계산 기록 프레임
        history_frame = tk.Frame(main_frame, bd=5, relief=tk.RIDGE)
        history_frame.pack(side="right", fill="both", expand=True)
        
        history_label = tk.Label(history_frame, text="계산 기록", font=('Arial', 16))
        history_label.pack(pady=5)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=20, width=30, font=('Arial', 12), state='disabled')
        self.history_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        clear_history_button = tk.Button(history_frame, text="기록 지우기", font=('Arial', 12), command=self.clear_history)
        clear_history_button.pack(pady=5, fill="x", padx=5)

    def create_buttons(self, parent_frame):
        buttons = [
            ('sin', 'cos', 'tan', 'log', 'ln'),
            ('(', ')', '√', '^', 'π'),
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', '←'),
            ('1', '2', '3', '-', '='),
            ('0', '.', 'e', '+')
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # '=' 버튼은 2행을 차지하도록 설정
                rowspan = 2 if text == '=' else 1
                
                # 버튼에 따라 다른 동작 할당
                cmd = None
                if text == '=':
                    cmd = self.calculate
                elif text == 'C':
                    cmd = self.clear_display
                elif text == '←':
                    cmd = self.backspace
                elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
                    cmd = lambda t=text: self.append_to_display(t + '(')
                else:
                    cmd = lambda t=text: self.append_to_display(t)

                btn = tk.Button(parent_frame, text=text, font=('Arial', 18), command=cmd, height=2)
                
                # '=' 버튼은 5열에 위치
                if text == '=':
                     btn.grid(row=i + 1, column=j, rowspan=rowspan, sticky="nsew", padx=5, pady=5)
                # '0', '.', 'e', '+' 버튼은 4열까지 확장
                elif i == 5:
                     btn.grid(row=i + 1, column=j, columnspan=1 if text != '+' else 2, sticky="nsew", padx=5, pady=5)
                else:
                     btn.grid(row=i + 1, column=j, sticky="nsew", padx=5, pady=5)

        # 그리드 가중치 설정 (창 크기 조절시 버튼도 함께 조절)
        parent_frame.grid_rowconfigure(0, weight=1)
        for i in range(len(buttons) + 1):
             parent_frame.grid_rowconfigure(i + 1, weight=1)
        for i in range(5):
            parent_frame.grid_columnconfigure(i, weight=1)

    def append_to_display(self, text):
        if self.display.cget('fg') == 'red':
            self.clear_display()
        self.display_var.set(self.display_var.get() + text)

    def clear_display(self):
        self.display_var.set("")
        self.display.config(fg='black')

    def backspace(self):
        self.display_var.set(self.display_var.get()[:-1])

    def calculate(self):
        expression = self.display_var.get()
        if not expression: return
        
        try:
            result = safe_eval(expression)
            # 결과가 정수이면 정수로, 아니면 실수로 표시
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display_var.set(str(result))
            self.display.config(fg='red')
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            self.display_var.set("계산 오류")
            self.display.config(fg='red')
            self.add_to_history(f"{expression} = 오류: {e}")

    def add_to_history(self, record):
        self.history_text.config(state='normal')
        self.history_text.insert(tk.END, record + "\n\n")
        self.history_text.config(state='disabled')
        self.history_text.see(tk.END)

    def clear_history(self):
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculatorApp(root)
    root.mainloop()
