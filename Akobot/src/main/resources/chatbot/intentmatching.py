#intent matching 하기 (DB로부터 인텐트 목록 가져오기)
import pandas as pd
import extracting # extracting.py import
import sys

usr_input = sys.argv[1]

'''
#load json (DB)
with open('.json', 'r') as f:
    json_data = json.load(f)
print(json.dumps(json_data, indent="\t") )
'''

#user keyword-intent keyword matching with dictionary {key:valuelist}
'''
로드한 파일을 dict로 변환하여 intents 만들예정
'''
intents={
                #level 1
                '전체모집요강':['total',1],
                '수시':['susi',1],
                '정시':['jungsi',1],
                '모집인원':['recruit',1],
                '작년도경쟁률':['competition',1],
                '지원자격유의사항':['note',1],
                '외국인특별전형':['foreign',1],
                '전형요소별평가방법':['test',1],
                '전형일정':['schedule',1],  
                #level 3
                '두드림소프트웨어':['susi_dodreamsoft',3],
                '불교추천':['susi_buddhism',3],
                '학교장추천':['susi_principal',3],
                '논술':['susi_essay',3],
                '두드림':['susi_dodream',3],
                '고른기회':['susi_regular',3],
                '특수교육대상자':['susi_special',3],
                '재직자':['susi_incumbent',3],
                '실기':['susi_performance',3],
                #level 4
                '일반전형':['jungsi_normal',4],
                '농어촌전형':['jungsi_farming',4],
                '특성화고교':['jungsi_specialized',4],
                '재직자':['jungsi_incumbent',4],
                '기초생활수급자및차상위계층':['jungsi_basic',4],
                #level 6
                '수시경쟁률':['competition_susi',6],
                '정시경쟁률':['competition_jungsi',6],
                #level 7
                '농어촌학생재학거주인정기준':['note_farming',7],
                '특성화고교졸업자동일계열기준학과':['note_special',7],
                '재직기간산정기준':['note_incumbent',7],
                #level 9
                '서류종합평가':['test_documnet',9],
                '면접평가':['test_interview',9],
                '학교생활기록부':['test_records',9],
                '대학수학능력시험':['test_SAT',9],
                #level 10
                '재외국민/외국인일정':['schedule_foreigner',10],
                '정시일정':['schedule_jungsi',10],
                '수시일정':['schedule_susi',10],
                #fallback intent
                '잘못된 입력':['fallback',0]
             }

##################### keyword-intent matching ########################
# 인텐트 한글명 1D 리스트
intent_keywords=intents.keys() 

# [인텐트 영문명, 인텐트 레벨]의 2D 리스트
intent_list=list(intents.values()) 

# 인텐트 영문명 1D 리스트 (아직 사용안함)
intent_names= pd.DataFrame(intent_list)[0].to_list()

# 인텐트 레벨 1D 리스트
intent_levels= pd.DataFrame(intent_list)[1].to_list()

# 매칭된 [인텐트 영문명, 인텐트 레벨]를 갖는 2D 리스트
matchings=[]
'''
for user_keyword in extracting.keywords: # extracted keywords from user input
    for intent_keyword in intent_keywords: # intent list from DB
        if intent_keyword in user_keyword: # if extracted keyword contains intent name
            matchings.append(intents[intent_keyword]) 
            break
'''

for user_keyword in extracting.extracKeywords(usr_input): # extracted keywords from user input
    for intent_keyword in intent_keywords: # intent list from DB
        if intent_keyword in user_keyword: # if extracted keyword contains intent name
            matchings.append(intents[intent_keyword])
            break

# 매칭된 인텐트 수가 0이면 fallback 발생
if len(matchings)==0:
    matchings.append(intents['잘못된 입력'])

######################## 매칭 결과 정리 ###########################
# 매칭된 인텐트 중 중복제거
seen = []
matchings= [x for x in matchings if x not in seen and not seen.append(x)]

# 매칭된 인텐트 중 포함관계 존재시, 상위인텐트 제거
'''
매칭 결과에 1과 2이상의 레벨 인텐트가 존재하는 경우,
둘의 이름을 비교하여 직속 상/하위 여부 판단 후,
만약 직속 상관관계를 가진다면 레벨이 1인 인텐트를 제거
'''
for element in matchings:
    if element[1]==1: #레벨이 1
        for another in matchings:
            if another[1]>1 and (element[0] in another[0]):
                matchings.remove(element)


######################## python 연동 ###########################
# python 서버 연결되게끔 cmd 창에서의 출력

# 최종 매칭된 인텐트 [인텐트 영문명, 영어 레벨] 출력
print(matchings)
