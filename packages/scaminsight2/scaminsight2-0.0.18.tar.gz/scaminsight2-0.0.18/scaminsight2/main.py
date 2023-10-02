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
        print("본인쨩은 Readme 잘 못쓰는거시야요 하와와....")
        print(
            "-a: alienvalue api 및 웹 페이지 파싱 정보와 ssl인증서 유효여부, -o observatory api, -w whois search,-d duckduckgo search, -s screenshot capture(현재 디렉터리 아래에 images폴더에 생성댐),인수 안쓰면 다하는거시야 응애")

        sys.exit()
    scam_insight = ScamInsight(url, "images", '92c0de09edbbebd92d986e460da71547c95ef84475357ad80abf075efbda8fae')
    result = scam_insight.run(argv)
    print(result) if not isinstance(result, Exception) else print("프로그램 실행 중 에러가 발생하였습니다")


if __name__ == "__main__":
    main()
