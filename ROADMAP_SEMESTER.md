# 26-2학기 주차별 실행 계획 (KOSPI Predictive Analytics)

15주 학기 기준. 검증(정상성/공적분/구조변화)이 모델링보다 먼저 와야 하므로 앞부분에 배치했습니다.

| 주차 | 작업 | 산출물 |
|---|---|---|
| 1주 | 레포 셋업, 데이터 수집 스크립트 작성 (`collect_data.py`) | 코스피/금리/환율 병합 데이터셋 |
| 2주 | 정상성 검정 (ADF, KPSS) | `test_stationarity.py` + 검정 결과표 |
| 3주 | 공적분 검정 (Engle-Granger, Johansen) | `test_cointegration.py` + 결과표 |
| 4주 | 구조변화 탐지 (Chow test, CUSUM) | `detect_structural_breaks.py` + 붕괴 시점 시각화 |
| 5주 | 중간 점검: 1~4주 결과 정리, README Results 섹션 1차 작성 | 중간 리포트 |
| 6주 | 피처 엔지니어링 (시차, 이동평균, 변동성, RSI) | `build_features.py` |
| 7주 | 데이터 누수 방지 유닛테스트 작성 + CI 연결 | `tests/test_no_leakage.py` 완성, GitHub Actions 통과 |
| 8주 | 베이스라인 모델 (ARIMA, VAR, 시차회귀) | `train_baselines.py` |
| 9주 | Random Forest / XGBoost 모델 | `train_models.py` (ML 파트) |
| 10주 | LSTM 모델 | `train_models.py` (딥러닝 파트) |
| 11주 | 워크포워드 검증 프레임워크 구축 | `evaluate.py` (검증 로직) |
| 12주 | Diebold-Mariano 유의성 검정 | `evaluate.py` (유의성 검정 로직) |
| 13주 | SHAP 해석 + MLflow 실험 로그 정리 | SHAP 요약 플롯, 실험 기록 |
| 14주 | 최종 리포트 작성 (결과 해석, 가설 기각 시 설명 포함) | README Results/최종 리포트 완성 |
| 15주 | 전체 재현성 점검, 발표자료/포트폴리오용 요약 정리 | 최종 제출본 |

## 우선순위 팁

- **1~5주가 가장 중요**해요. 여기서 관계가 불안정하거나 공적분이 안 나오면, 뒷부분(ML 모델링) 설계를 조정해야 할 수도 있어요.
- 시간이 부족해지면 **LSTM(10주)을 가장 먼저 줄이세요**. ARIMA/VAR/RF/XGBoost 비교만으로도 충분히 완성도 있는 결과가 나와요. LSTM은 "있으면 좋은" 항목이지 핵심은 아니에요.
- 반대로 **1~4주(통계 검정)와 11~12주(워크포워드+유의성 검정)는 절대 생략하면 안 돼요** — 이게 이 프로젝트를 "흔한 주가예측 프로젝트"와 구분 짓는 핵심이에요.
