import tkinter as tk
from tkinter import scrolledtext
import re

# 계산 로직을 수행하는 함수
def evaluate_expression(expression):
    """
    정규표현식을 사용하여 수식을 파싱하고 계산합니다.
    """
    match = re.match(r'^\s*(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)\s*$', expression)
    
    if not match:
        return "오류: 형식"

    num1_str, operator, num2_str = match.groups()

    try:
        num1 = float(num1_str)
        num2 = float(num2_str)

        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "오류: 0으로 나눔"
            return num1 / num2
    except ValueError:
        return "오류: 숫자 변환"
    except Exception:
        return "알 수 없는 오류"

# GUI 애플리케이션 클래스
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI 계산기 (기록 기능 포함)")
        self.root.geometry("600x500") # 창 너비를 600으로 넓힘

        # 메인 프레임
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # 계산기 디스플레이 및 버튼이 있는 왼쪽 프레임
        calculator_frame = tk.Frame(main_frame)
        calculator_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # 계산식과 결과를 표시할 화면
        self.display_var = tk.StringVar()
        self.display = tk.Entry(calculator_frame, textvariable=self.display_var, font=('Arial', 24), bd=10, insertwidth=2, width=14, borderwidth=4, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, pady=10, sticky="nsew")

        # 버튼 생성
        self.create_buttons(calculator_frame)

        # 계산 기록이 표시될 오른쪽 프레임
        history_frame = tk.Frame(main_frame)
        history_frame.pack(side="right", fill="both", expand=True)
        
        history_label = tk.Label(history_frame, text="계산 기록", font=('Arial', 14))
        history_label.pack(pady=(0, 5))
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=15, width=25, font=('Arial', 12), state='disabled')
        self.history_text.pack(fill="both", expand=True)
        
        clear_history_button = tk.Button(history_frame, text="기록 지우기", command=self.clear_history)
        clear_history_button.pack(pady=5, fill="x")

    def create_buttons(self, parent_frame):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        row_val = 1
        col_val = 0
        
        for button_text in buttons:
            action = None
            if button_text == '=':
                action = self.calculate
            elif button_text == 'C':
                action = self.clear_display
            else:
                action = lambda txt=button_text: self.append_to_display(txt)
            
            btn = tk.Button(parent_frame, text=button_text, padx=20, pady=20, font=('Arial', 18), command=action)
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
            
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
        
        for i in range(5):
            parent_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            parent_frame.grid_columnconfigure(i, weight=1)

    def append_to_display(self, text):
        if self.display.cget('fg') == 'red':
            self.clear_display()
        
        current_text = self.display_var.get()
        self.display_var.set(current_text + text)

    def clear_display(self):
        self.display_var.set("")
        self.display.config(fg='black')

    def calculate(self):
        expression = self.display_var.get()
        if not expression:
            return
            
        try:
            result = evaluate_expression(expression)
            
            self.display_var.set(str(result))
            self.display.config(fg='red')
            
            # 계산 기록 추가
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            self.display_var.set("Error")
            self.display.config(fg='red')
            self.add_to_history(f"{expression} = Error")
            
    def add_to_history(self, record):
        self.history_text.config(state='normal')
        self.history_text.insert(tk.END, record + "\n")
        self.history_text.config(state='disabled')
        self.history_text.see(tk.END) # 스크롤을 맨 아래로 이동

    def clear_history(self):
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state='disabled')

# 메인 실행 부분
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
