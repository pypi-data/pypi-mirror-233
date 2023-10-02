import sys
import re

from .scaminsight import ScamInsight


def main():
    if len(sys.argv) >= 4:
        print("프로그램 실행에 필요한 인수의 개수가 너무 많습니다. 프로그램을 종료합니다.")
        sys.exit()
    if len(sys.argv) == 3:
        if not re.match("^-[wados]$", sys.argv[1]):
            print("프로그램 실행에 필요한 인수가 잘못되었습니다. 프로그램을 종료합니다.")
        argv = sys.argv[1]
        url = sys.argv[2]
    elif len(sys.argv) == 2:
        argv = "-all"
        url = sys.argv[1]
    else:
        print("프로그램 실행에 필요한 인수의 개수가 너무 적습니다. 프로그램을 종료합니다.")
        # Readme 파일 작성시 여기에 출력

        sys.exit()
    scam_insight = ScamInsight(url, "images", '92c0de09edbbebd92d986e460da71547c95ef84475357ad80abf075efbda8fae')
    result = scam_insight.run(argv)
    print(result) if not isinstance(result, Exception) else print("프로그램 실행 중 에러가 발생하였습니다")


if __name__ == "__main__":
    main()
