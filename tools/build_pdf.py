from pathlib import Path
import json, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, black, white

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
font_regular=os.environ.get('BINGO_FONT_REGULAR','C:/Windows/Fonts/malgun.ttf')
font_bold=os.environ.get('BINGO_FONT_BOLD','C:/Windows/Fonts/malgunbd.ttf')
if not Path(font_regular).is_file() or not Path(font_bold).is_file():
    raise SystemExit('Set BINGO_FONT_REGULAR and BINGO_FONT_BOLD to Korean-capable TrueType font files.')
pdfmetrics.registerFont(TTFont('MG',font_regular))
pdfmetrics.registerFont(TTFont('MGB',font_bold))
W,H=A4; M=36; CW=(W-2*M-18)/2
INK=HexColor('#202C38'); GRAY=HexColor('#59616A'); LINE=HexColor('#B7BFC6'); PALE=HexColor('#F0F3F5')
rows=json.loads((ROOT/'data/concepts.json').read_text(encoding='utf8'))
assert len(rows)==46
assert [r['n'] for r in rows]==list(range(1,47))

def para(c,text,x,top,width,size=10,leading=None,bold=False,color=INK):
    st=ParagraphStyle('p',fontName='MGB' if bold else 'MG',fontSize=size,leading=leading or size*1.45,textColor=color,wordWrap='CJK',splitLongWords=True)
    p=Paragraph(text,st); _,h=p.wrap(width,1000); p.drawOn(c,x,top-h); return top-h

def bar(c,text,x,top,width):
    c.setFillColor(PALE);c.rect(x,top-24,width,24,fill=1,stroke=0)
    para(c,text,x+8,top-4,width-16,10.5,bold=True);return top-31

def head(c,tag,title,page,total,student=False):
    c.setFillColor(INK);c.setFont('MGB',9);c.drawString(M,H-35,'헌법과 국가 기관  /  국가기관 빙고')
    c.setFont('MG',8);c.drawRightString(W-M,H-35,tag)
    para(c,title,M,H-49,W-2*M,22,27,bold=True)
    c.setStrokeColor(INK);c.setLineWidth(1);c.line(M,H-87,W-M,H-87)
    if student:
        para(c,'학년 _____  반 _____  번호 _____  이름 __________________',M,H-97,W-2*M,9.5)
    c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(M,32,W-M,32)
    c.setFont('MG',7.5);c.setFillColor(GRAY)
    if not student:
        c.drawString(M,20,'동아출판 22개정 중학 사회② 1단원 기반  |  헌법 조문으로 구성과 기능 연결하기')
    c.drawRightString(W-M,20,f'{page} / {total}')
    return H-(128 if student else 106)

def newpdf(name):
    c=canvas.Canvas(str(OUT/name),pagesize=A4);c.setTitle(name.removesuffix('.pdf'));c.setAuthor('수업 자료');return c

c=newpdf('국가기관_빙고_학생용.pdf')
y=head(c,'학습지 1 앞면 · 개념 목록','01  배운 개념 모아 보기',1,4,True)
y=para(c,'헌법 조문 학습지의 빈칸에 아래 <b>개념 번호</b>를 쓰세요.<br/>1~39번은 기본 범위, 40~46번은 헌법재판소 선택 확장 범위입니다.',M,y,W-2*M,10)
y-=14
left=bar(c,'대통령과 행정부',M,y,CW)
for r in rows[:19]:
    left=para(c,f"<b>{r['n']:02d}</b>　{r['concept']}",M+4,left,CW-8,9.7,14)-7
left-=5;left=bar(c,'법원',M,left,CW)
for r in rows[34:39]:
    left=para(c,f"<b>{r['n']:02d}</b>　{r['concept']}",M+4,left,CW-8,9.7,14)-7
right=bar(c,'국회',M+CW+18,y,CW)
for r in rows[19:34]:
    right=para(c,f"<b>{r['n']:02d}</b>　{r['concept']}",M+CW+22,right,CW-8,9.7,14)-7
right-=5;right=bar(c,'선택 확장 · 헌법재판소',M+CW+18,right,CW)
for r in rows[39:]:
    right=para(c,f"<b>{r['n']:02d}</b>　{r['concept']}",M+CW+22,right,CW-8,9.7,14)-7
assert min(left,right)>43,(left,right)
c.showPage()
y=head(c,'학습지 1 뒷면 · 빙고판','02  조문 번호로 빙고!',2,4,True)
y=para(c,'① 조문을 읽고 개념 번호 연결하기(10분) → ② 빙고판 만들기 → ③ 돌아가며 발표하기',M,y,W-2*M,10,bold=True)-9
y=para(c,'선생님이 정한 범위에서 <b>서로 다른 조문 25개</b>를 골라 마음대로 배치하세요. 각 칸에는 <b>조·항·호 번호</b>를 적습니다. 예: 제66조 제4항 / 제111조 제1항 제5호. 한 묶음으로 제시된 두 항은 한 칸에 함께 씁니다.',M,y,W-2*M,10)-16
size=87;top=y;gx=(W-5*size)/2
c.setStrokeColor(INK);c.setLineWidth(.9)
for k in range(6):
    c.line(gx+k*size,top,gx+k*size,top-5*size)
    c.line(gx,top-k*size,gx+5*size,top-k*size)
y=top-5*size-18
y=bar(c,'발표와 표시 규칙',M,y,W-2*M)
y=para(c,'• 내 차례에는 <b>조문 번호 + 조문의 핵심 내용 + 관련 개념 번호</b>를 말합니다.<br/>• 연결이 맞으면 그 조문이 있는 <b>모든 학생</b>이 해당 칸에 표시합니다.<br/>• 연결이 틀리면 <b>아무도 표시하지 않고 다음 차례</b>로 넘깁니다. 그 조문은 뒤에 다시 고를 수 있습니다.<br/>• 이미 맞게 발표된 조문은 다시 고르지 않습니다. 가로·세로·대각선 중 <b>3줄</b>을 먼저 완성하면 빙고!',M,y,W-2*M,10,15)-12
y=para(c,'마무리  |  오늘 연결한 조문 하나와 그 조문이 정한 국가기관의 구성 또는 기능을 써 보세요.',M,y,W-2*M,9.5,bold=True)-16
c.setStrokeColor(LINE);c.line(M,y,W-M,y)
assert y>44,y
c.showPage()

# Core clauses are in constitutional order, so concept numbering does not reveal answers.
core=sorted(rows[:39],key=lambda r:(int(r['ref'].split('조')[0][1:]),int(r['ref'].split('제')[2].split('항')[0]) if '항' in r['ref'] and '·' not in r['ref'] else 0))
# 24 clauses on front, 15 core plus 7 extension on back.
front=core[:24];back=core[24:]+rows[39:]
def clause(c,r,x,y,width):
    title=r['ref']
    end=para(c,title,x+5,y,width-84,9.8,13,bold=True)
    c.setFont('MG',8.7);c.setFillColor(INK);c.drawRightString(x+width-5,y-10,'개념 (        )')
    y2=min(end,y-15)-3
    y2=para(c,r['quote'],x+5,y2,width-10,9.4,12.6)-5
    c.setStrokeColor(LINE);c.setLineWidth(.35);c.line(x,y2+3,x+width,y2+3)
    return y2-3

for p,data in [(3,front),(4,back)]:
    y=head(c,'학습지 2 '+('앞면' if p==3 else '뒷면')+' · 헌법 조문','03  헌법에서 근거 찾기'+(' (계속)' if p==4 else ''),p,4,True)
    y=para(c,'각 조문 옆에 가장 직접적으로 연결되는 <b>개념 번호 하나</b>를 쓰세요.<br/>조문은 필요한 항·호를 발췌했습니다. ……는 중간 생략이며, 띄어쓰기는 읽기 편하게 정리했습니다.',M,y,W-2*M,9.1,13)-12
    count=12
    for col,part in enumerate([data[:count],data[count:]]):
        yy=y;x=M+col*(CW+18)
        for r in part:
            if r['n']==40:
                yy=bar(c,'선택 확장 · 헌법재판소',x,yy,CW)
            yy=clause(c,r,x,yy,CW)
        print('clause bottom',p,col,round(yy,1))
        assert yy>52,(p,col,yy)
    c.showPage()
c.save()

c=newpdf('국가기관_빙고_교사용_정답과_운영안.pdf')
y=head(c,'교사용 · 정답표','조문 ↔ 개념 번호 정답',1,2)
y=para(c,'학생용 조문 학습지에 제시된 순서입니다. 학생에게 이 정답표는 배부하지 않습니다.',M,y,W-2*M,9.3)-13
ordered=front+back
for col,part in enumerate([ordered[:23],ordered[23:]]):
    x=M+col*(CW+18);yy=bar(c,'헌법 조문  →  개념 번호 · 개념',x,y,CW)
    for r in part:
        yy=para(c,f"<b>{r['ref']} → {r['n']:02d}</b>",x+4,yy,CW-8,9,12)
        yy=para(c,r['concept'],x+4,yy-1,CW-8,8.4,11)-3
        c.setStrokeColor(LINE);c.setLineWidth(.3);c.line(x,yy+1,x+CW,yy+1)
    print('answer bottom',col,yy);assert yy>45,yy
c.showPage()
y=head(c,'교사용 · 운영과 출처','수업 운영 메모',2,2)
def section(title,text):
    global y
    y=bar(c,title,M,y,W-2*M)
    y=para(c,text,M+4,y,W-2*M-8,10,15)-16
section('인쇄·범위 설정',
    '학생용 PDF 4쪽을 <b>A4 양면, 긴 쪽 넘김</b>으로 인쇄하면 학생당 두 장입니다. 첫째 장은 개념 목록과 빙고판, 둘째 장은 헌법 조문 목록입니다. 기본 범위는 개념 1~39번, 헌법재판소까지 마무리할 때에는 40~46번도 포함합니다.')
section('권장 진행 · 약 30~35분',
    '<b>안내 3분</b> → <b>조문-개념 연결 10분</b> → <b>빙고판 작성 4분</b> → <b>빙고 12~15분</b> → <b>마무리 3분</b>. 기본 범위 전체를 연결하려면 연결 시간을 늘리거나 짝 활동으로 진행합니다. 4~6명 모둠별 순환을 권장하며, 전체 학급으로 할 때에는 발표 순서를 미리 정합니다.')
section('발표·정답 판정',
    '발표 예: “<b>제66조 제4항</b>, 행정권은 대통령을 수반으로 하는 정부에 속한다. 관련 개념은 <b>4번</b>입니다.” 교사가 조문 번호·핵심 내용·개념 번호의 연결을 확인한 뒤 표시하게 합니다. 오답이면 표시 없이 다음 차례로 넘기며, 오답으로 발표한 조문은 이후 다시 선택할 수 있습니다. 제104조 제1·2항과 제111조 제2·3항은 각각 <b>한 묶음·한 칸</b>으로 처리합니다. 3줄 동시 완성은 공동 승리로 인정합니다.')
section('혼동하기 쉬운 연결',
    '• <b>국회의 탄핵 소추(34번)</b>와 <b>헌법재판소의 탄핵 심판(44번)</b>을 구분합니다.<br/>• <b>법원의 위헌 법률 심판 제청(39번)</b>과 <b>헌법재판소의 위헌 법률 심판(42번)</b>을 구분합니다.<br/>• <b>제99조</b>는 감사원의 결산 검사와 국회 보고를 명시합니다. 국회의 결산 심사는 교과서 개념과 연결한 것이며, 헌법에 “국회는 결산을 심사한다”라고 그대로 적힌 것은 아닙니다.<br/>• <b>제60조 제1항</b>의 동의 대상은 헌법에 열거된 조약입니다. 모든 조약에 국회 동의가 필요한 것은 아닙니다.<br/>• <b>제72조</b>의 중요 정책 국민 투표와 <b>제130조 제2항</b>의 헌법 개정 국민 투표는 구분합니다. 후자는 개정 절차상 필수입니다.')
section('선정 기준과 교과서 범위',
    '교과서 본문·헌법 자료·권력 분립 도표·교사용 도움 자료에서 헌법 조문과 직접 연결되는 내용을 선정했습니다. 기관 이름만 쓰기보다 선출·임명·구성·권한을 구별해 번호를 부여했습니다. 상임 위원회의 법률안 심사, 각급 법원의 세부 사건 관할, 국회의원·장관 겸직의 세부 사항은 개별 법률의 규정이 중심이므로 별도 문항으로 넣지 않았습니다. 정부 형태와 권력 분립은 제41조·제67조, 제40조·제66조 제4항·제101조 제1항 등을 함께 보며 종합합니다.')
y=bar(c,'출처',M,y,W-2*M)
y=para(c,'교과서: 동아출판 「22개정 중학 사회②」 1단원, 인쇄면 8~19쪽(제공된 교사용 PDF 3~14쪽).<br/>헌법: 국가법령정보센터 「대한민국헌법」, 헌법 제10호, 시행 1988. 2. 25. / 확인일 2026. 11. 2.<br/><link href="https://www.law.go.kr/법령/대한민국헌법" color="#245579">https://www.law.go.kr/법령/대한민국헌법</link>',M+4,y,W-2*M-8,8.5,12)
print('guide bottom',y);assert y>42,y
c.showPage();c.save()
print('Created',*[str(p) for p in OUT.glob('*.pdf')],sep='\n')
