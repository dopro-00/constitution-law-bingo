# PDF 생성 도구

인쇄용 완성본은 저장소의 `outputs/`에 있습니다. 수정 후 다시 생성할 때에만 아래 도구가 필요합니다.

## 실행

Python 3.10 이상에서 저장소 루트 기준으로 실행합니다.

```sh
python -m pip install -r requirements.txt
python tools/build_pdf.py
```

Windows에서는 맑은 고딕 글꼴을 기본으로 사용합니다. 다른 운영체제에서는 `BINGO_FONT_REGULAR`와 `BINGO_FONT_BOLD` 환경 변수에 한글을 지원하는 일반·굵은 TrueType 글꼴 파일 경로를 지정합니다.

## 수정 위치

- `data/concepts.json`: 최종 개념 번호, 개념, 헌법 근거, 조문 발췌문, 교과서 쪽수
- `tools/build_pdf.py`: 인쇄 배치, 안내 문구, 교사용 해설
- `docs/`: 수업 개요, 운영안, 개념·조문 대응 자료, 정답표

현재 배치는 46개 개념과 기본 39개·확장 7개를 기준으로 합니다. 개념 수나 문장 길이를 바꾸면 생성 도구의 배치 확인이 실패할 수 있으므로 페이지를 조정하고 PDF를 눈으로 확인해야 합니다. PDF를 다시 만들면 `docs/`의 대응 자료와 정답표도 함께 갱신하세요.
