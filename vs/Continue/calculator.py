import re

# 터미널에서 글자색을 바꾸기 위한 ANSI 이스케이프 코드
RED = '\033[91m'
RESET = '\033[0m'

def calculate():
    """
    사용자로부터 계산식을 입력받아 4칙 연산을 수행하고,
    결과를 빨간색으로 출력하는 함수.
    'exit'를 입력하면 프로그램이 종료됩니다.
    """
    print("간단한 4칙 연산 계산기입니다.")
    print("계산할 식을 입력하세요 (예: 3.5 + 4)")
    print("종료하려면 'exit'를 입력하세요.")

    while True:
        try:
            # 사용자로부터 식 입력받기
            expression = input("> ").strip()

            # 'exit' 입력 시 루프 종료
            if expression.lower() == 'exit':
                print("계산기를 종료합니다.")
                break

            # 정규표현식을 사용하여 숫자와 연산자 분리
            # 공백이 있거나 없어도 처리 가능 (예: "3+4", "3 + 4")
            match = re.match(r'^\s*(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)\s*$', expression)
            
            if not match:
                print(f"{RED}잘못된 형식입니다. 숫자, 연산자, 숫자 순으로 입력해주세요.{RESET}")
                continue

            num1_str, operator, num2_str = match.groups()

            # 문자열을 실수로 변환
            num1 = float(num1_str)
            num2 = float(num2_str)

            result = 0
            # 연산자에 따라 계산 수행
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                # 0으로 나누는 경우 예외 처리
                if num2 == 0:
                    print(f"{RED}오류: 0으로 나눌 수 없습니다.{RESET}")
                    continue
                result = num1 / num2
            
            # 결과를 빨간색으로 출력
            print(f"결과: {RED}{result}{RESET}")

        except ValueError:
            # 숫자로 변환할 수 없는 값이 들어온 경우
            print(f"{RED}오류: 유효한 숫자를 입력해주세요.{RESET}")
        except Exception as e:
            # 그 외 예상치 못한 오류 처리
            print(f"{RED}알 수 없는 오류가 발생했습니다: {e}{RESET}")

if __name__ == "__main__":
    calculate()
