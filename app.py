import streamlit as st
import pandas as pd

st.set_page_config(page_title='공부·과제 성향 테스트', page_icon='💜', layout='centered')

st.markdown('''<style>
.stApp {background:linear-gradient(140deg,#fcfaff,#f0e8ff)}
.block-container {max-width:850px;padding-top:2rem}
h1,h2,h3 {color:#6841a5}
.question-card {background:#fff;border:1px solid #e3d3fa;border-radius:16px;padding:18px 22px 12px;margin:18px 0 8px;box-shadow:0 3px 12px #7755aa12}
.question-title {font-weight:750;color:#6841a5;font-size:1.08rem}
.result-card {background:white;border:2px solid #c3a8f4;border-radius:20px;padding:24px;text-align:center}
.result-code {font-size:2.5rem;font-weight:800;color:#7546c2}
</style>''', unsafe_allow_html=True)

# 4개 지표의 총 10개 문항. 각 문항은 1~5점의 양극 척도입니다.
# radio와 slider를 혼합해 사용합니다.
QUESTIONS = [
    ('환경','공부할 때 더 집중이 잘 되는 장소는?', '적당한 소음이 있는 카페','완벽히 조용한 독서실','radio'),
    ('환경','오랜 시간 공부할 공간을 고른다면?', '사람들의 움직임과 생활 소음이 있는 곳','외부 자극이 최소화된 정적인 곳','slider'),
    ('진행','마감일이 일주일 남았을 때 보통 어떻게 시작하나요?', '마감이 가까워지면 집중적으로 시작','미리 시작해 매일 조금씩 진행','radio'),
    ('진행','시험이나 발표를 준비할 때 더 익숙한 방식은?', '짧은 기간에 몰아서 집중','여러 날에 걸쳐 나누어 준비','slider'),
    ('진행','과제 진행이 예상보다 늦어지면 어떻게 하나요?', '마지막에 집중 시간을 늘려 해결','매일 작업량을 조정해 해결','radio'),
    ('사고','새 과제를 받으면 가장 먼저 하는 일은?', '전체 방향과 아이디어 구상','구체적인 실행 단계 정리','slider'),
    ('사고','복잡한 문제를 해결할 때 선호하는 접근은?', '전체 구조와 핵심 원리부터 파악','세부 문제를 하나씩 해결','radio'),
    ('협업','팀 과제를 진행할 때 더 편한 방식은?', '내가 맡은 부분을 독립적으로 완성','팀원과 자주 의견을 교환하며 완성','slider'),
    ('협업','과제 중 어려운 문제를 만나면 보통 어떻게 하나요?', '혼자 충분히 고민한 후 해결','다른 사람과 상의하며 해결','radio'),
    ('협업','팀 프로젝트 진행 상황을 관리하는 방식은?', '각자 책임지고 결과를 공유','중간 과정을 수시로 공유하고 조율','slider'),
]

# 사용자가 제공한 16개 유형의 이름과 설명을 그대로 보존합니다.
RESULTS = {
 'NSBI': ('자유로운 영혼의 천재 기획자','적당한 소음이 있는 카페에서 마감 직전의 압박감을 에너지 삼아 기발한 아이디어를 쏟아냅니다. 남들의 간섭 없이 혼자서 전체 판을 짤 때 최고의 퍼포먼스를 냅니다.'),
 'NSBC': ('아이디어를 불태우는 열정적인 브레인스토머','시끌벅적한 분위기 속에서 팀원들과 수다 떨듯 아이디어를 주고받으며 큰 그림을 그립니다. 데드라인이 다가올수록 초인적인 추진력을 발휘하는 분위기 메이커입니다.'),
 'NSDI': ('마감 1시간 전의 카공족 해결사','카페 백색소음을 배경으로 막판 스퍼트를 올려 세세한 자료 조사와 문서 작업을 혼자서 뚝딱 해치웁니다. 발등에 불이 떨어져야 디테일이 살아나는 실전파입니다.'),
 'NSDC': ('위기 상황에서 빛나는 단기전 멀티플레이어','급한 프로젝트나 시험 기간에 스터디 카페·라디오 등을 틀어놓고 동료들과 실시간으로 소통하며 빠진 부분을 꼼꼼히 채워 넣습니다. 위기 대처 능력이 뛰어납니다.'),
 'NMBI': ('카페에서 미래를 설계하는 꾸준한 전략가','매일 단골 카페에 출석 도장을 찍으며 장기 프로젝트의 로드맵이나 공부 커리큘럼을 혼자서 차근차근 구상합니다. 조급해하지 않고 큰 방향성을 꾸준히 다듬어 갑니다.'),
 'NMBC': ('커피 한 잔과 함께 성장하는 네트워커','스터디 모임이나 오픈 오피스에서 동료들과 주기적으로 진행 상황을 공유하며 큰 방향을 맞춰갑니다. 함께 대화하며 얻는 영감으로 꾸준히 전진하는 타입입니다.'),
 'NMDI': ('매일 조금씩 완성하는 카공족 성실러','적당한 생활 소음이 있어야 오히려 집중이 잘 되며, 매일 정해진 분량의 공부나 업무 디테일을 혼자서 묵묵히 처리합니다. 겉보기엔 여유로워 보여도 속이 꽉 찬 실속파입니다.'),
 'NMDC': ('소통으로 디테일을 다듬는 오픈형 조율자','개방된 공간에서 팀원들과 수시로 피드백을 주고받으며 실무의 작은 오류까지 꼼꼼하게 잡아냅니다. 꾸준한 커뮤니케이션으로 완성도를 높이는 협업의 윤활유입니다.'),
 'QSBI': ('고독한 밤의 혁신가, 새벽형 천재','모두가 잠든 조용한 방에서 마감 직전 무서운 몰입력을 발휘합니다. 혼자서 남들이 생각하지 못한 창의적인 구조와 핵심 논리를 단숨에 세우는 승부사 기질이 있습니다.'),
 'QSBC': ('핵심만 짚어내는 단기전 전략 리더','조용한 환경에서 혼자 큰 틀을 빠르게 잡은 뒤, 팀원들과 핵심 방향만 압축적으로 공유해 단기간에 프로젝트를 돌파합니다. 불필요한 잡담보다 효율적인 의사결정을 선호합니다.'),
 'QSDI': ('진공 상태의 완벽주의 벼락치기 장인','노이즈 캔슬링 이어폰을 끼고 외부와 완전히 단절된 상태에서 막판 스퍼트를 올립니다. 짧은 시간 안에 방대한 암기나 꼼꼼한 데이터 정리를 혼자 해내는 초집중 타입입니다.'),
 'QSDC': ('조용히 판을 뒤집는 실무 해결사','평온한 공간에서 혼자 치열하게 디테일을 파고든 뒤, 결정적인 순간에 팀원들과 조율해 결과물의 퀄리티를 확 끌어올립니다. 마감 직전 가장 믿음직한 구원투수입니다.'),
 'QMBI': ('조용한 서재의 마스터플래너','방해받지 않는 공간에서 매일 일정 시간을 투자해 거시적인 계획과 장기 목표를 혼자 설계합니다. 한 번 세운 큰 그림을 끝까지 밀고 나가는 뚝심 있는 사색가입니다.'),
 'QMBC': ('깊이 있는 대화로 방향을 잡는 사색형 리더','정돈된 환경에서 차분하게 전체 맥락을 짚어내고, 동료들과 정기적인 회의를 통해 팀이 올바른 방향으로 가고 있는지 꾸준히 점검하는 안정적인 조율자입니다.'),
 'QMDI': ('오차 제로에 도전하는 독서실 모범생','완벽한 정적 속에서 매일 계획된 분량을 한 치의 오차도 없이 혼자 완수합니다. 꼼꼼한 필기, 체계적인 폴더 정리 등 성실함과 디테일의 끝판왕입니다.'),
 'QMDC': ('빈틈없는 체크리스트의 협업 수호자','차분한 환경에서 세부 일정과 할 일을 매일 관리하며, 팀원들과 진행 상황을 꼼꼼히 공유해 프로젝트가 펑크 나지 않도록 지키는 가장 든든한 팀플레이어입니다.')
}

AXES = [
 ('환경','N','Q','카페·생활 소음','조용한 독서실'),
 ('진행','S','M','마감 집중','꾸준한 분할'),
 ('사고','B','D','큰 그림·아이디어','세부 실행'),
 ('협업','I','C','독립 수행','소통·조율'),
]

if 'result_open' not in st.session_state:
    st.session_state.result_open = False

# slider는 처음에 3점으로 표시되지만, 체크박스로 답변을 확정해야 합니다.
# 이렇게 하면 3점(중립)도 명시적인 응답으로 구분할 수 있습니다.
def reset():
    for i, item in enumerate(QUESTIONS):
        st.session_state.pop(f'answer_{i}', None)
        st.session_state.pop(f'confirmed_{i}', None)
    st.session_state.result_open = False

st.title('💜 공부·과제 성향 테스트')
st.write('10개의 질문으로 나의 공부 스타일을 알아보세요. 결과는 16가지 유형 중 하나로 표시됩니다.')
st.caption('1점은 왼쪽 성향, 5점은 오른쪽 성향에 매우 가깝다는 뜻입니다. 3점은 중립입니다.')

for i, (axis, question, left, right, kind) in enumerate(QUESTIONS):
    if i == 0:
        st.subheader('① 학습 환경 및 과제 수행 방식')
    if i == 5:
        st.subheader('② 사고방식 및 협업 태도')
    st.markdown(f'<div class="question-card"><div class="question-title">Q{i+1}. {question}</div><small>왼쪽: {left}　/　오른쪽: {right}</small></div>', unsafe_allow_html=True)
    if kind == 'radio':
        st.radio('나와 가까운 정도', [1,2,3,4,5], index=None,
                 format_func=lambda x: f'{x}점 — '+('왼쪽 매우 선호' if x==1 else '왼쪽 약간 선호' if x==2 else '비슷함' if x==3 else '오른쪽 약간 선호' if x==4 else '오른쪽 매우 선호'),
                 key=f'answer_{i}', horizontal=True)
    else:
        st.slider('나와 가까운 정도 (1~5점)', 1, 5, 3, key=f'answer_{i}')
        st.checkbox('이 문항 응답 완료 (3점 중립 선택도 가능)', key=f'confirmed_{i}')

# 실시간 진행률: 라디오는 선택 시, 슬라이더는 응답 확정 시 완료로 계산
completed = sum(
    (st.session_state.get(f'answer_{i}') is not None if item[4]=='radio'
     else st.session_state.get(f'confirmed_{i}', False))
    for i,item in enumerate(QUESTIONS)
)
st.markdown('### 📊 응답 진행률')
st.progress(completed/len(QUESTIONS))
st.write(f'**{completed} / {len(QUESTIONS)}문항 완료**')

if st.button('✨ 결과 확인하기', type='primary', use_container_width=True, disabled=completed<10):
    st.session_state.result_open = True

if st.session_state.result_open and completed == 10:
    scores = {axis: [st.session_state[f'answer_{i}'] for i, q in enumerate(QUESTIONS) if q[0]==axis]
              for axis,*_ in AXES}
    means = {axis: sum(vals)/len(vals) for axis, vals in scores.items()}

    # 평균 3점은 중립. 16유형을 반드시 제공하기 위해 동률 시
    # 해당 지표의 첫 번째 질문을 우선하고, 그것도 3점이면 왼쪽을 선택합니다.
    codes=[]
    neutral_axes=[]
    for axis,left_code,right_code,_,_ in AXES:
        avg=means[axis]
        if avg==3:
            neutral_axes.append(axis)
            first=scores[axis][0]
            codes.append(right_code if first>3 else left_code)
        else:
            codes.append(left_code if avg<3 else right_code)
    result_code=''.join(codes)
    name,description=RESULTS[result_code]

    st.divider()
    st.markdown('## 🎉 나의 공부·과제 성향')
    st.markdown(f'<div class="result-card"><div class="result-code">{result_code}</div><h2>{name}</h2><p>{description}</p></div>', unsafe_allow_html=True)
    st.markdown('### 📈 4가지 성향 비교')
    for axis,left_code,right_code,left_label,right_label in AXES:
        avg=means[axis]
        # 1~5점을 0~100%로 변환. 양쪽 점수 합은 100%.
        left_pct=round((5-avg)*25,1)
        right_pct=round((avg-1)*25,1)
        st.write(f'**{axis}** — {left_label} ({left_code}) / {right_label} ({right_code})')
        df=pd.DataFrame({'점수':[left_pct,right_pct]}, index=[left_label,right_label])
        st.bar_chart(df, horizontal=True, color='#9870df', x_label='상대적 선호도 (%)', use_container_width=True)
        st.caption(f'평균 {avg:.2f}점 · {left_code} {left_pct:.1f}% / {right_code} {right_pct:.1f}%')

    # 같은 영역의 문항 점수 차이가 큰 경우에는 결과 해석에 주의
    inconsistent=[axis for axis,vals in scores.items() if max(vals)-min(vals)>=3]
    if inconsistent:
        st.warning('응답 차이가 큰 영역: '+', '.join(inconsistent)+' — 상황에 따라 선호가 달라질 수 있습니다.')
    if neutral_axes:
        st.info('중립 평균 영역: '+', '.join(neutral_axes)+' — 해당 영역은 첫 문항의 방향으로 임시 분류했습니다. 첫 문항도 중립이면 왼쪽 성향으로 분류합니다.')
    st.caption('본 검사는 재미와 자기 이해를 위한 비공식 테스트이며, 심리측정학적 신뢰도와 타당도가 검증된 검사는 아닙니다.')
    st.button('🔄 다시 검사하기', on_click=reset, use_container_width=True)

st.divider()
st.caption('💜 공부·과제 성향 테스트 | 10문항 · 5점 척도 · 16가지 유형')
