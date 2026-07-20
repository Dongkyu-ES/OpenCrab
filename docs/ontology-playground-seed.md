# Ontology-Playground Seed Corpus

기초 학습자료 코퍼스. Microsoft [Ontology-Playground](https://github.com/microsoft/Ontology-Playground)의
learn 콘텐츠(13개 트랙 / 60개 아티클)를 OpenCrab 스토어에 시드해 두고, 에이전트들이
가져오기 → 업데이트 → 재인제스트하며 지식체계를 점진적으로 키워가기 위한 기반이다.

## 구성

```
seeds/ontology-playground/
├── corpus/            # 원본 learn 마크다운 74개 (MIT, ATTRIBUTION.md 참고)
├── distilled/knowledge.md   # 증류 다이제스트: 트리·패턴 카탈로그·트랙별 엔티티/관계 표
├── backbone.json      # 개념 백본: 핵심 개념 9 + 설계 패턴 12 + 안티패턴 5 + 트랙→패턴 매핑
└── ATTRIBUTION.md
scripts/seed_ontology_playground.py   # 멱등 시드 스크립트
```

시드 후 스토어 상태 (2026-07-20 기준):

| 레이어 | 내용 | 규모 |
|---|---|---|
| 벡터 (ChromaDB) | 아티클을 `##` 섹션 단위로 청킹 (quiz/embed 태그 제거) | 361 청크 |
| resource | 트랙별 `Document` (`doc-oplay-*`) + 다이제스트 | 14 |
| evidence | 아티클별 `TextUnit` (`tu-oplay-*`) | 62 |
| concept | `Topic` 1 + `Concept` 26 (core/pattern/antipattern) | 27 |
| 엣지 | `contains` / `mentions`(알리아스 스캔) / `exemplifies`(트랙 교육 매핑) / `related_to` | 501 |

벡터 청크의 `textunit_id` 메타데이터가 그래프의 TextUnit 노드를 가리키므로,
벡터 히트 → 그래프 문맥(어느 트랙, 어떤 패턴을 exemplify하는지)으로 피벗할 수 있다.

## 에이전트 활용법 (MCP)

- `ontology_query` — 하이브리드 검색. 설계 질문("N:M은 언제 정션 엔티티로 푸나?")에
  백본 개념 노드 + 코퍼스 근거 청크가 함께 반환된다.
- `query_bm25` — 패턴/개념 이름으로 결정적 조회 (`junction entity`, `god entity` 등).
- 그래프 탐색 — `pat-*`/`anti-*`/`con-*` 노드에서 `mentions`/`exemplifies` 역방향으로
  해당 패턴을 가르치는 트랙·아티클을 찾는다.

## 업데이트 / 재인제스트 루프

모든 쓰기가 안정 ID 기반 upsert라 스크립트는 몇 번을 돌려도 안전하다.

1. **업스트림 갱신**: Ontology-Playground를 다시 클론해 `content/learn/` →
   `seeds/ontology-playground/corpus/`로 복사 후 재실행:
   ```bash
   python scripts/seed_ontology_playground.py          # 전체 적용
   python scripts/seed_ontology_playground.py --dry-run  # 계획만 확인
   ```
2. **지식 추가**: 새 케이스스터디/문서는 `corpus/<track>/`에 md로 추가하거나,
   증류 지식이면 `distilled/knowledge.md`에 섹션으로 추가하고 재실행.
3. **백본 확장**: 새 패턴·개념은 `backbone.json`에 항목 추가(알리아스 포함) 후 재실행 —
   mentions 엣지는 알리아스 스캔으로 자동 갱신된다.

## AI 성장 루프 (지식체계 확장)

시드는 출발점이다. 이후 확장은 OpenCrab의 기존 파이프라인을 쓴다:

1. **추출**: 새 자료를 `ontology_ingest`로 넣고 `ontology_extract`(LLM)로 노드/엣지 후보 생성
2. **정합**: `canonicalize_find_and_propose` / `identity_*`로 중복·별칭 정리
3. **승격**: `promotion_register_candidate` → `promotion_validate_candidate` → `promotion_promote`로
   검증된 지식만 정식 그래프에 편입
4. **배포**: 검증된 그래프는 `opencrab export-neo4j-pack`으로 Pack v1 산출물로 내보내
   다른 인스턴스가 가져갈 수 있다 (`docs/opencrab-pack-v1.md`)

시드 코퍼스의 도메인 모델(엔티티 91종·관계 96개, `distilled/knowledge.md` 부록)은
아직 개념 노드로 승격하지 않았다 — 실제 프로젝트에서 해당 도메인을 다룰 때
extract→promotion 루프로 필요한 만큼만 키우는 것을 권장한다(과잉 모델링 방지).
