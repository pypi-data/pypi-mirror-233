from typing import List
from pydantic import BaseModel

class LifestylesData(BaseModel):
    optionKey: int
    answerText: str


class ProblemsData(BaseModel):
    optionKey: int
    answerText: str


class AnswerData(BaseModel):
    lot: int # 눈을 감고 잠을 청한 시각
    ast: int # 잠이 들기 시작한 시각
    aet: int # 잠에서 완전히 깨어난 시각
    dns: bool # 전혀 자지 못함
    # lifestyles: List[LifestylesData]
    nap: int # 낮잠을 잔 시간 (분)
    # pill: bool
    # problems: List[ProblemsData]
    sleepQuality: int
    tst: int
    # waso: int # 잠에서 깬 총 시간 (분)


class SleepData(BaseModel):
    answer: AnswerData
    date: int
    # userId: int