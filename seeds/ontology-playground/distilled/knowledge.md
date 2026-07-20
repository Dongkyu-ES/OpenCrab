# Ontology Playground — Learn 콘텐츠 지식 정리

> 출처: https://github.com/microsoft/Ontology-Playground (`content/learn/`, 13개 코스 / 60개 아티클, 2026-07-20 수집)
> 목적: Microsoft Fabric IQ 스타일 온톨로지 설계 지식을 구조화하고, OpenCrab 온톨로지 팩 후보 자료로 검토

## 0. 전체 트리

```
learn/
├── 📚 ontology-fundamentals (path, 6) ── 개념 백본
│   ├── 1. what-is-an-ontology
│   ├── 2. understanding-rdf-and-owl
│   ├── 3. fabric-iq-ontology-concepts
│   ├── 4. building-your-first-ontology
│   ├── 5. ontology-design-patterns
│   └── 6. contributing-to-the-catalogue
├── 입문 도메인 경로 (path, 각 4강: scenario → core → 확장 → complete)
│   ├── ☕ cosmic-coffee-path — Fourth Coffee (커피 체인 주문/매장/공급망)
│   ├── 🛒 ecommerce-path — E-Commerce Platform (마켓플레이스/장바구니)
│   ├── 🏦 finance-path — Banking & Finance (고객/계좌/거래)
│   ├── 🏥 healthcare-path — Healthcare System (진료/진단)
│   ├── 👥 hr-system-path — HR System (조직/배치)
│   ├── 🏭 manufacturing-path — Smart Manufacturing (공장/생산추적)
│   ├── 🎓 university-path — University System (학사/교수진)
│   └── 📦 supply-chain-disruption-path — 리스크 전파/완화 자동화
└── 심화 랩 (lab, 5~7강: 산업 표준·실전 규모)
    ├── 🏛️ fibo-loans-lab — FIBO 대출 온톨로지 (담보/상환/리스크)
    ├── 🛡️ fibo-risk-lab — FIBO 리스크 관리 (산업분류/지리/규제)
    ├── 🔬 iq-lab-retail-supply-chain — 리테일 공급망 (7강, 최대 규모)
    └── 🌾 zava-grove-to-shelf — 시맨틱 콜드체인 (농장→매대, 센서/품질)
```

## 1. 개념 백본 — Ontology Fundamentals

### 1.1 온톨로지 3요소 (What is an Ontology?)
- **Entity type**(사물의 범주) / **Property**(타입 있는 사실: string, integer, decimal, date, datetime, boolean) / **Relationship**(개체 간 방향성 연결)
- 온톨로지는 데이터가 아니라 **데이터의 형태(스키마)**. 시맨틱 쿼리(자연어→구조화 쿼리)의 기반
- 모든 엔티티는 인스턴스를 유일하게 구별하는 **identifier property** 최소 1개 필수

### 1.2 RDF/OWL 표현 (Understanding RDF and OWL)
- RDF = **subject → predicate → object 트리플** 그래프. W3C 표준
- OWL 매핑: `owl:Class` = 엔티티 타입, `owl:DatatypeProperty` = 원시값 속성, `owl:ObjectProperty` = 관계, `rdfs:domain`/`rdfs:range` = 속성 소속/타입
- 네임스페이스(xmlns)로 URI 전역 유일성 확보
- JSON(프로토타이핑/앱 설정) vs RDF/OWL(형식 모델/시스템 간 통합) 트레이드오프

### 1.3 Fabric IQ 개념 (Fabric IQ Ontology Concepts)
- IQ = 자연어 질문 → 온톨로지 참조 → SQL 생성. 4기둥: **엔티티 타입 / 속성 / 관계 / identifier**
- **카디널리티**(1:1, 1:N, N:1, N:M)가 GROUP BY·JOIN 생성의 정확성을 결정
- IQ 설계 지침: ① 비즈니스 용어로 명명(tbl_cust ✗) ② description으로 중의성 해소 ③ identifier 필수 ④ 카디널리티 명시 ⑤ 사용자가 질의할 개념만 모델링(내부 테이블 전부 ✗)

### 1.4 설계 워크플로우 (Building Your First Ontology)
- Designer에서 시각 설계 → Validate(identifier 존재, 참조 무결성, ID 중복) → RDF 미리보기 → 내보내기(RDF 다운로드 / 카탈로그 PR / JSON 복사)
- 예제: Library(Book–writtenBy(N:1)→Author, Book–borrowedBy(N:M)→Member)

### 1.5 설계 패턴 & 안티패턴 (Ontology Design Patterns) ★ 팩의 핵심 가치
**명명 규칙**: 엔티티=단수 명사, 속성=camelCase, 관계=동사구(placedBy, worksAt). 축약·내부 테이블명·범용명(Item/Record/Thing) 금지

**원칙**:
- One entity, one concept — 무관한 속성이 쌓이면 분리 (Person에 salary+patientId+courseGrade = god entity)
- Identifier는 유일·안정·비즈니스 키. 복합 키 회피
- FK가 아니라 **이름 있는 관계**로 모델링 (`fk_cust_id` → `placedBy`)
- 카디널리티 질문법: "A 하나에 B가 몇 개 붙을 수 있나?"

**안티패턴 표**: God entity(30+속성→분리) / identifier 누락 / 모호한 관계명(relatedTo→prescribes) / 순환 1:1(같은 엔티티→병합) / 과잉 모델링(모든 테이블→질의 대상만)

### 1.6 카탈로그 기여 (Contributing to the Catalogue)
- 기여 단위 = `ontology.rdf` + `metadata.json`(name/description/category/tags/icon/author)
- CI 검증: RDF 파싱, **round-trip fidelity**(parse(serialize(o)) 동등성), 메타데이터 스키마, 디렉터리 명명, 심링크 금지
- 권장 스코프: **엔티티 3~8개의 잘 집중된 온톨로지** > 30+개 스프롤

## 2. 도메인 트랙 총람 (12개, 상세는 부록 Digest A/B/C)

| 트랙 | 유형 | 엔티티 | 관계 | 시그니처 패턴 |
|---|---|---|---|---|
| Fourth Coffee ☕ | path | 6 | 7 | 허브 엔티티(Shipment), 크로스소스 통합(Lakehouse/Eventhouse/PBI) |
| E-Commerce 🛒 | path | 5 | 6 | 세션 엔티티(Cart), 1:1 관계, 피드백 루프(Review) |
| Banking & Finance 🏦 | path | 5 | 6 | 소유 체인, 다중 경로 관계(holds vs linked_to) |
| Healthcare 🏥 | path | 5 | 6 | 공유 엔티티(Appointment), 이중 저자, 케어 체인 |
| HR System 👥 | path | 5 | 4 | 정션 엔티티(Assignment), 역할 분리, 시간적 이력 |
| Smart Manufacturing 🏭 | path | 5 | 5 | IoT 소유 계층, 생산 체인, 품질 피드백 루프 |
| University 🎓 | path | 5 | 6 | 정션 엔티티(Enrollment), 전이적 질의, 허브(Department) |
| Supply Chain Disruption 📦 | path | 7 | 7 | 리스크 전파 캐스케이드, event→assessment→action→backup 라이프사이클 |
| FIBO Loans Lab 🏛️ | lab | 10 | 9 | FIBO IRI 적응(fibo-loan-ln-ln:*), classifier 엔티티, 집계 vs 원자 이벤트 |
| FIBO Risk Lab 🛡️ | lab | 11 | 9 | NAICS 분류 트리, 지리 계층, Basel III/OCC/FDIC 인코딩, 도메인 브리지 |
| IQ Retail Supply Chain 🔬 | lab | 15 | 18 | 링킹/인터섹션 엔티티, Eventhouse/Lakehouse 바인딩, GQL |
| Zava Grove-to-Shelf 🌾 | lab | 12 | 13 | 추적성 리니지, QC 이벤트, 콜드체인 시계열 센서, 숏컷 엣지(ofVariety) |
| **합계** | | **91** | **96** | |

## 3. 통합 패턴 카탈로그 (팩의 핵심 지식 자산)

**구조 패턴**
1. **정션(연관) 엔티티** — N:M을 속성 있는 중간 엔티티로 해소 (Assignment, Enrollment, OrderLine). 3개 도메인에서 반복 교육되며 일반화됨
2. **허브 엔티티** — 다수 관계가 모이는 중심 노드 (Shipment, Department, Store)
3. **분류 트리 / 지리 계층** — NAICS 산업분류, Region→Country→State
4. **Classifier 엔티티** — 분류 자체를 엔티티로 승격 (FIBO 대출/리스크 등급)
5. **숏컷 엣지** — 자주 쓰는 다단 경로를 의도적 지름길 관계로 비정규화 (Zava `ofVariety`)
6. **크로스소스 통합** — 서로 다른 저장소(Lakehouse/Eventhouse/시맨틱 모델)의 데이터를 하나의 온톨로지로 바인딩

**동적/시간 패턴**
7. **이벤트 모델링** — 집계(PaymentHistory) vs 원자 이벤트(Payment), QC 이벤트, 시계열 센서 판독
8. **리스크 전파 캐스케이드** — DisruptionEvent→RiskAssessment→MitigationAction→BackupSupplier 라이프사이클 + Activator 자동화
9. **피드백 루프** — 품질 검사→공정 조정, 리뷰→상품
10. **시간적 이력** — 기간 쌍(startDate/endDate)으로 배치·재직 이력

**표준 정합 패턴**
11. **표준 온톨로지 적응** — FIBO 클래스를 IQ 스타일로 단순화하되 원 IRI(`fibo-loan-ln-ln:*`, `fibo-fbc-dae-dbt:*`)와 owl:Restriction 출처를 보존, MIT 라이선스 어트리뷰션(EDM Council/OMG)
12. **규제 인코딩** — Basel III 위험가중치, OCC/FDIC 한도를 속성·플래그로

**안티패턴 (fundamentals 05)**
God entity(30+속성) / identifier 누락 / 모호한 관계명(relatedTo) / 순환 1:1 / 과잉 모델링(모든 내부 테이블 노출)

## 4. 수집 자료 검토 (인벤토리)

**모인 것**
- 개념 백본 6편: 온톨로지 정의 → RDF/OWL → Fabric IQ 4기둥 → 설계 워크플로우 → 패턴/안티패턴 → 카탈로그 기여 규칙
- 완결 도메인 온톨로지 12종: 엔티티 91종(속성·datatype·identifier 플래그 전수), 관계 96개(카디널리티 전수)
- 패턴 카탈로그 12종 + 안티패턴 5종 (여러 도메인에서 교차 검증된 형태)
- 퀴즈 약 50개(정답+해설 포함) — 그대로 평가/벤치마크 문항으로 쓸 수 있는 골드셋
- GQL(Cypher풍) 예시 질의, Fabric IQ 운영 개념(Data Agent, Eventhouse/Lakehouse 바인딩, Activator)

**품질 소견**
- 콘텐츠 자체 불일치 2건: FIBO 두 랩 모두 개요에서 관계 10개를 주장하나 본문에는 9개만 정의됨 (다이제스트에 플래그)
- path 트랙들은 RDF/OWL/IRI를 전혀 쓰지 않음(비즈니스 키 문자열 ID) — RDF 지식은 fundamentals와 FIBO 랩에만 존재
- 라이선스: MIT (Microsoft Corporation) + FIBO 부분은 EDM Council/OMG MIT 어트리뷰션 필요 → 팩 재배포에 법적 문제 없음, manifest에 어트리뷰션 명기 필요

## 5. OpenCrab 온톨로지 팩 설계안 (활용 방향 검토)

OpenCrab에는 "팩"이 두 층위로 존재하므로 이 자료는 두 방식 모두로 활용 가능:

### 방안 A — Pack v1 지식 팩: `ontology-playground-learn` (추천 1순위)
`docs/opencrab-pack-v1.md` 계약대로 evidence-backed 그래프 팩으로 빌드.
- **evidence**: 74개 md → 섹션 단위 청크 → `evidence/index.jsonl` (source.url = GitHub 원본, hash, section 위치)
- **concept 스페이스**: `Topic`(트랙 13) / `Concept`(패턴 12 + 안티패턴 5 + 핵심 개념: identifier, cardinality, junction entity…) / `Class`(도메인 엔티티 타입 91)
- **엣지**: `evidence —mentions/describes/exemplifies→ concept`, `Class —subclass_of/part_of/related_to→ Concept`, `Concept —related_to→ Concept` (모두 문법 매니페스트에 이미 존재하는 관계)
- **sample_queries.json**: 퀴즈 50문항 + "N:M은 언제 정션 엔티티로 풀어야 하나?" 류 패턴 질문 → relationship/multi-hop RAG 벤치마크 힌트(`retrieval_hints`)와 정확히 맞물림
- **활용**: 에이전트가 온톨로지 설계·리뷰할 때 패턴/안티패턴 레퍼런스로 RAG 검색. `canonicalize`·`promotion` 워크플로우의 설계 근거 인용에도 사용
- **빌드 경로**: md 청크 → `ontology_ingest` → `ontology_extract`/수동 노드·엣지 등록 → `promotion_validate_candidate` → Neo4j import/check → `opencrab export-neo4j-pack`

### 방안 B — 도메인 시드 스키마 팩 (선별 2~3종)
`opencrab/schemas/packs/*.yaml`에 파일만 추가하면 되는 구조. 91개 엔티티 전부가 아니라 실제 쓸 도메인만:
- 예: `retail-supply-chain.yaml` (Order, Product, Store, Shipment, Inventory, Supplier…), `fibo-lending.yaml` (Loan, Borrower, Collateral, PaymentSchedule, RiskClassifier…)
- **활용**: 새 프로젝트에서 `schema_pack_install`로 즉시 도메인 타입 체계 확보. 단, 현재 제너레이터는 최소 템플릿(required: [] / name·description·status)이라 속성 스키마를 살리려면 타입 YAML을 다이제스트 기반으로 수제 생성하는 편이 좋음

### 방안 C — 퀴즈 골드셋 벤치마크
퀴즈 50문항을 `sample_queries.json` + 평가셋으로 분리 포장. 팩 품질 게이트(`relationship_evidence_coverage`, `multihop_path_coverage`) 검증용 회귀 셋으로 사용.

### 권고
**A를 본체로, C를 A에 내장, B는 실수요 도메인 확정 후 선별** — A는 문법·검증 파이프라인이 이미 갖춰져 있어 즉시 빌드 가능하고, 마켓플레이스 메타데이터(README/sample_queries/community_reports)까지 자연스럽게 채워짐. B는 전체 12종을 다 팩으로 만들면 과잉 모델링 안티패턴을 스스로 범하는 셈이므로 선별 필수.

---
# 부록: 트랙별 상세 다이제스트

# Ontology-Playground Learn Content — Structured Digest (Digest A)

Source: `Ontology-Playground/content/learn/` — 4 tracks × 5 files each (`_meta.md` + 4 lessons). All lessons follow the same template: frontmatter (title, slug, description, order, `embed:` reference), entity tables (Property | Type | Identifier?), relationship bullets with cardinality, an `<ontology-embed>` component (with `diff` attribute from lesson 3 onward), a "What we learned" list, an embedded ```quiz``` block, and a closing GQL example in the final lesson.

---

## Track 1: Fourth Coffee (`cosmic-coffee-path`, icon ☕)

### 1. Scenario
A specialty coffee chain ("Fourth Coffee") operating stores across multiple cities, tracking customers, orders, products, suppliers, and shipments. Data is siloed across a lakehouse (customer profiles), a real-time Eventhouse (order transactions), and a Power BI semantic model (product analytics). The ontology unifies these so cross-system questions ("Which suppliers provide organic beans to our highest-capacity stores?") become single graph traversals instead of multi-system join archaeology.

### 2. Entity types (6)

**Customer**
- `customerId`: string (identifier)
- `name`: string
- `email`: string
- `loyaltyTier`: enum (Bronze, Silver, Gold, Platinum)
- `joinDate`: date
- `totalSpend`: decimal (USD)

**Order**
- `orderId`: string (identifier)
- `timestamp`: datetime
- `total`: decimal (USD)
- `status`: enum (Pending, Preparing, Ready, Completed, Cancelled)
- `paymentMethod`: enum (Card, Cash, Mobile, Gift Card)

**Product**
- `productId`: string (identifier)
- `name`: string
- `category`: enum (Espresso, Brewed, Cold Brew, Tea, Food, Merchandise)
- `price`: decimal (USD)
- `origin`: string
- `isOrganic`: boolean

**Store**
- `storeId`: string (identifier)
- `name`: string
- `city`: string
- `state`: string
- `openDate`: date
- `capacity`: integer (seating capacity)

**Supplier**
- `supplierId`: string (identifier)
- `name`: string
- `country`: string
- `certification`: enum (Fair Trade, Rainforest Alliance, Organic, Direct Trade, None)
- `rating`: decimal (1–5)

**Shipment** (hub entity)
- `shipmentId`: string (identifier)
- `dispatchDate`: date
- `arrivalDate`: date
- `status`: enum (In Transit, Delivered, Delayed)
- `weight`: decimal (kg)

### 3. Relationship types (7)
- `Customer —places→ Order` (one-to-many)
- `Order —contains→ Product` (many-to-many)
- `Order —processedAt→ Store` (many-to-one)
- `Product —sourcedFrom→ Supplier` (many-to-one)
- `Shipment —sentBy→ Supplier` (many-to-one)
- `Shipment —deliveredTo→ Store` (many-to-one)
- `Shipment —carries→ Product` (many-to-many)

### 4. Design patterns demonstrated
- **Hub entity**: Shipment connects three entities (Supplier via sentBy, Store via deliveredTo, Product via carries), bridging sourcing, logistics, and retail domains — explicitly named "Hub entity pattern" in a callout.
- **Identifier properties**: every entity has exactly one unique-key property.
- **Enum properties as model-level data quality**: loyaltyTier, status, category, certification constrain values to valid options.
- **Boolean flag filtering**: `isOrganic` for compliance/filter queries.
- **Cardinality vocabulary**: many-to-one framed as the canonical "belongs to / happens at" pattern (processedAt); many-to-many for bidirectional multiplicity (contains, carries).
- **Incremental growth / diff-driven evolution**: each embed uses `diff` against the previous step to visualize ontology deltas.

### 5. Progression logic
- **Lesson 1 (scenario-overview)**: domain framing, why-ontology motivation, key vocabulary (entity types, properties, identifier properties, relationships, hub entities). No model yet.
- **Lesson 2 (core-orders, step-1)**: Customer, Order, Product + places, contains → identifiers, enums, booleans, cardinality basics. 3 entities / 2 relationships.
- **Lesson 3 (adding-stores, step-2)**: + Store + processedAt → location modeling, many-to-one, integer properties, the diff view. 4 / 3.
- **Lesson 4 (complete-supply-chain, step-3)**: + Supplier, Shipment + 4 relationships → hub entities, supply chain closure, question→graph-path table, GQL. Final: 6 / 7.

### 6. Fabric IQ / RDF specifics
- Microsoft Fabric data-estate framing: **lakehouse**, **real-time Eventhouse**, **Power BI semantic model** as the source systems the ontology sits above.
- Output capabilities named: **graph queries, GQL, and natural-language Data Agent interactions**.
- **GQL** (ISO Graph Query Language, Cypher-style `MATCH (sup:Supplier)<-[:sentBy]-(s:Shipment)-[:deliveredTo]->(st:Store) …`) example; takeaway states GQL queries "map directly to ontology structure — no impedance mismatch."
- Embed/artifact ID convention: `official/cosmic-coffee-step-1` … `step-3`, rendered via `<ontology-embed id="…" diff="…">`; loadable from an in-app `#/catalogue`.
- No explicit RDF/OWL/IRI constructs mentioned.

---

## Track 2: E-Commerce Platform (`ecommerce-path`, icon 🛒)

### 1. Scenario
A general-purpose online marketplace handling buyers, products with inventory, shopping carts as pre-checkout sessions, completed orders, and product reviews. Data spans a transactional database (orders), a search engine (product discovery), and an analytics warehouse (buyer behavior). The ontology turns cross-system questions like "Which verified reviewers rated products they didn't purchase?" into graph pattern matching (existence of one path, absence of another).

### 2. Entity types (5)

**Buyer**
- `buyerId`: string (identifier)
- `email`: string
- `memberSince`: date
- `loyaltyTier`: string
- `totalSpent`: decimal (USD)

**Product**
- `sku`: string (identifier — Stock Keeping Unit, industry-standard e-commerce ID)
- `name`: string
- `category`: string
- `price`: decimal (USD)
- `stockQty`: integer

**Order**
- `orderId`: string (identifier)
- `orderDate`: datetime
- `status`: string
- `total`: decimal (USD)
- `shippingMethod`: string

**Shopping-Cart** (session entity)
- `cartId`: string (identifier)
- `createdAt`: datetime
- `itemCount`: integer (denormalized)
- `subtotal`: decimal (USD) (denormalized)

**Review**
- `reviewId`: string (identifier)
- `rating`: integer
- `title`: string
- `body`: string
- `verified`: boolean

### 3. Relationship types (6)
- `Buyer —places→ Order` (one-to-many)
- `Order —includes→ Product` (many-to-many)
- `Buyer —has_cart→ Shopping-Cart` (one-to-one)
- `Shopping-Cart —contains→ Product` (many-to-many)
- `Buyer —writes→ Review` (one-to-many)
- `Review —reviews→ Product` (many-to-one)

### 4. Design patterns demonstrated
- **Session entity**: Shopping-Cart models temporary, mutable, in-progress state (vs. accumulated Orders) — enables abandonment/conversion-funnel analysis.
- **One-to-one relationship**: `has_cart` as exclusive current-state pairing (one buyer ↔ one active cart), explicitly contrasted with one-to-many orders.
- **Denormalized summary properties**: `itemCount`/`subtotal` trade storage for query speed.
- **Feedback loop / dual-path cycle**: `Buyer → writes → Review → reviews → Product` creates a second path from Buyer to Product beside the purchase path — enabling comparative queries ("bought but didn't review" vs "reviewed but didn't buy").
- **Domain-standard identifiers**: `sku` instead of generic `productId`.
- **Boolean trust signal**: `verified` for trust-based filtering.

### 5. Progression logic
- **Lesson 1**: scenario, purchase-flow / one-to-one / feedback-loop / session-entity concepts.
- **Lesson 2 (core-marketplace, step-1)**: Buyer, Product, Order + places, includes → purchase-flow backbone, SKU. 3 / 2.
- **Lesson 3 (shopping-carts, step-2)**: + Shopping-Cart + has_cart, contains → session entities, one-to-one, denormalization. 4 / 4.
- **Lesson 4 (complete-platform, step-3)**: + Review + writes, reviews → feedback loop, funnel analysis, GQL. Final: 5 / 6.

### 6. Fabric IQ / RDF specifics
- GQL example joining cart to reviews: `MATCH (b:Buyer)-[:has_cart]->(c:Cart)-[:contains]->(p:Product)<-[:reviews]-(r:Review) WHERE r.verified = true …`.
- Embed IDs `official/ecommerce-step-1..3` with diff views; catalogue linking.
- Generic multi-system framing (transactional DB, search engine, analytics warehouse) rather than Fabric-item-specific naming. No RDF/OWL/IRI constructs.

---

## Track 3: Banking & Finance (`finance-path`, icon 🏦)

### 1. Scenario
A retail banking platform managing customers (with credit/risk profiles), accounts (checking/savings/brokerage), transactions, loans, and investment holdings. Data spans core banking systems, payment processors, credit bureaus, and brokerage platforms with mismatched schemas/identifiers. The ontology makes compliance-style traversals ("all transactions from accounts owned by high-risk customers with active loans > $100K") a single graph query.

### 2. Entity types (5)

**Customer**
- `customerId`: string (identifier)
- `name`: string
- `ssn`: string (metadata only — schema, not values)
- `creditScore`: integer (300–850)
- `riskProfile`: string

**Account**
- `accountNumber`: string (identifier)
- `type`: string (checking / savings / brokerage)
- `balance`: decimal (USD)
- `interestRate`: decimal (%)
- `openDate`: date

**Transaction**
- `transactionId`: string (identifier)
- `amount`: decimal (USD)
- `type`: string
- `timestamp`: datetime (time-of-day precision for fraud/audit)
- `merchant`: string

**Loan**
- `loanId`: string (identifier)
- `principal`: decimal (USD)
- `apr`: decimal (%)
- `term`: integer (months)
- `status`: string

**Investment**
- `holdingId`: string (identifier)
- `symbol`: string (e.g. MSFT, AAPL)
- `shares`: decimal
- `purchasePrice`: decimal (USD)
- `currentValue`: decimal (USD)

### 3. Relationship types (6)
- `Customer —owns→ Account` (one-to-many)
- `Account —has_transaction→ Transaction` (one-to-many)
- `Customer —has_loan→ Loan` (one-to-many)
- `Account —funds→ Loan` (one-to-many)
- `Customer —holds→ Investment` (one-to-many)
- `Account —linked_to→ Investment` (one-to-many)

### 4. Design patterns demonstrated
- **Ownership chain**: `Customer → Account → Transaction` as the drill-down backbone for compliance queries.
- **Multi-path relationships** (explicitly named pattern): Investment reachable from Customer both directly (`holds` = ownership) and via Account (`linked_to` = funding source); same for Loan (`has_loan` vs `funds`). Intentional redundancy modeling different semantics of the same connection.
- **Schema-not-data principle**: sensitive fields (`ssn`) are metadata describing what exists; the ontology is a schema, not a database — sensitive data stays in source systems.
- **Temporal precision modeling**: datetime (not date) for transactions, motivated by fraud detection/audit trails.
- **Typed numerics with units**: percentage units (interestRate, apr), duration-as-integer-with-unit (term in months), integer scores enabling range queries (creditScore > 700).
- **Merchant-as-property**: spending analysis via a string property without promoting Merchant to an entity — a deliberate modeling economy choice.

### 5. Progression logic
- **Lesson 1**: scenario, ownership chains, financial identifiers, risk/compliance, multi-path concept.
- **Lesson 2 (customer-accounts, step-1)**: Customer, Account + owns. Smallest starting step of any track: 2 / 1.
- **Lesson 3 (transactions, step-2)**: + Transaction + has_transaction → activity layer, datetime precision, chain extension. 3 / 2.
- **Lesson 4 (complete-banking, step-3)**: + Loan, Investment + 4 relationships → financial products, multi-path pattern, aggregation GQL. Final: 5 / 6.

### 6. Fabric IQ / RDF specifics
- Most advanced GQL example: aggregation with `WITH c, SUM(inv.currentValue) AS portfolio, SUM(loan.principal) AS debt WHERE portfolio > debt`.
- Embed IDs `official/finance-step-1..3` with diff views; catalogue linking.
- Source-system framing: core banking, payment processors, credit bureaus, brokerage platforms. No Fabric-item names, no RDF/OWL/IRI constructs.

---

## Track 4: Healthcare System (`healthcare-path`, icon 🏥)

### 1. Scenario
A hospital-network patient-care platform tracking patients (medical records, blood types, allergies), providers (licenses, departments), appointments, ICD-coded diagnoses, and prescriptions. Data is spread across EHR, scheduling, pharmacy, and billing systems. The ontology maps clinical cross-system questions ("severe diagnoses by cardiology providers with zero-refill prescriptions") onto graph traversals across the care chain.

### 2. Entity types (5)

**Patient**
- `patientId`: string (identifier)
- `mrn`: string (Medical Record Number — domain identifier mapping to the EHR)
- `dateOfBirth`: date
- `bloodType`: string
- `allergies`: string

**Provider**
- `providerId`: string (identifier)
- `name`: string
- `specialty`: string
- `licenseNumber`: string
- `department`: string

**Appointment** (shared entity)
- `appointmentId`: string (identifier)
- `scheduledTime`: datetime
- `duration`: integer (minutes)
- `type`: string
- `status`: string

**Diagnosis** (dual-connected entity)
- `diagnosisId`: string (identifier)
- `icdCode`: string (ICD standard code)
- `description`: string
- `severity`: string
- `diagnosedDate`: date

**Prescription**
- `rxNumber`: string (identifier — pharmacy-standard Rx number)
- `medication`: string
- `dosage`: string
- `frequency`: string
- `refillsRemaining`: integer

### 3. Relationship types (6)
- `Patient —has_appointment→ Appointment` (one-to-many)
- `Provider —sees→ Appointment` (one-to-many)
- `Patient —diagnosed_with→ Diagnosis` (one-to-many)
- `Provider —diagnoses→ Diagnosis` (one-to-many)
- `Diagnosis —treated_by→ Prescription` (one-to-many)
- `Provider —prescribes→ Prescription` (one-to-many)

### 4. Design patterns demonstrated
- **Shared entity / event-interaction pattern**: Appointment as the meeting point of two independent actors (Patient, Provider) — "common whenever two actors participate in the same event"; queryable from either perspective.
- **Dual authorship**: Diagnosis connected to both Patient (has the condition) and Provider (identified it) — patient-centric vs provider-centric views.
- **Care chain (process/workflow chain)**: `Patient → Diagnosis → Prescription`, with Provider attached at every stage — the most-connected entity mirroring real clinical workflow (role modeling by relationship fan-out rather than subclassing).
- **Standardized external codes for interoperability**: ICD codes, Rx numbers, MRN — the lesson explicitly distinguishes domain identifiers (mrn) coexisting with ontology identifiers (patientId).
- **Duration/count integers with units**: duration (minutes), refillsRemaining.
- **Negative-path queries**: "severe diagnoses with no → Prescription" (absence-of-edge pattern).

### 5. Progression logic
- **Lesson 1**: scenario, clinical workflows, shared relationships, care chains, standardized identifiers.
- **Lesson 2 (care-delivery, step-1)**: Patient, Provider, Appointment + has_appointment, sees → the scheduling triangle. 3 / 2.
- **Lesson 3 (diagnoses, step-2)**: + Diagnosis + diagnosed_with, diagnoses → ICD interoperability, dual connection, severity stratification. 4 / 4.
- **Lesson 4 (complete-care, step-3)**: + Prescription + treated_by, prescribes → treatment chain closure, refill/adherence queries, GQL. Final: 5 / 6.

### 6. Fabric IQ / RDF specifics
- GQL example: `MATCH (p:Patient)-[:diagnosed_with]->(d:Diagnosis)-[:treated_by]->(rx:Prescription) WHERE d.severity = 'severe' AND rx.refillsRemaining <= 1 …`.
- Embed IDs `official/healthcare-step-1..3` with diff views; catalogue linking.
- Source-system framing: EHR, scheduling systems, pharmacy databases, billing platforms. External vocabularies referenced (ICD) but not as RDF imports. No RDF/OWL/IRI constructs.

---

## Cross-track observations

- **Totals**: 21 entity types, 25 relationships across 4 tracks (6/7 coffee, 5/6 each for the other three).
- **Uniform pedagogy template**: scenario overview (why-ontology motivating query) → 3 incremental build steps → final lesson with question→graph-path table, GQL query, cumulative build table, key takeaways, and a quiz per build lesson.
- **Shared conventions**: single string identifier per entity; typed properties with units in parentheses (USD, %, kg, months, minutes); enum types only in the coffee track (other tracks use plain strings for the same role, e.g. status/loyaltyTier); relationship names are lowerCamelCase in coffee (`processedAt`, `sourcedFrom`) but snake_case elsewhere (`has_cart`, `diagnosed_with`).
- **Pattern coverage by track**: coffee = hub entity + enums; ecommerce = session entity + one-to-one + feedback loop + denormalization; finance = ownership chains + multi-path + schema-vs-data; healthcare = shared entity + dual authorship + process chain + standard codes.
- **Fabric IQ surface**: only the coffee track names Fabric items (lakehouse, Eventhouse, Power BI semantic model) and "Data Agent" natural-language interaction; all tracks converge on GQL as the query language and `official/<track>-step-N` embed artifacts with diff visualization. Nowhere in the four tracks are RDF, OWL, IRIs, or export formats (e.g., Turtle/JSON-LD) mentioned — the material is Fabric-ontology-native, not RDF-framed.
# Digest B — Ontology-Playground Learn Tracks (HR, Manufacturing, University, Supply Chain Disruption)

Source: `Ontology-Playground/content/learn/{hr-system-path, manufacturing-path, university-path, supply-chain-disruption-path}` — all `.md` files including `_meta.md` (21 files total across the 4 tracks; each track = `_meta.md` + 4 numbered lessons).

---

## Track 1: HR System (`hr-system-path`, icon 👥)

**Meta:** "Model an HR platform with employees, departments, positions, assignments, and performance reviews." Type: path.

### 1. Scenario
A growing organization needs a shared human-resources ontology because data is scattered across payroll tools, HRIS, spreadsheets, and manager notes. The motivating cross-functional question: "Which departments have the highest number of senior employees rated outstanding in the last review cycle?" — which spans employee records, org structure, role definitions, and review outcomes. The ontology turns manual joins across disconnected systems into a connected graph query.

### 2. Entity types (5)

| Entity | Properties (name: type; ✓ = identifier) |
|---|---|
| **Employee** | employeeId: string ✓; name: string; hireDate: date; employmentStatus: enum; jobLevel: enum |
| **Department** | departmentId: string ✓; name: string; budget: decimal; status: enum |
| **Position** | positionId: string ✓; title: string; level: enum; salaryBand: string |
| **Assignment** (junction) | assignmentId: string ✓; startDate: date; endDate: date; isPrimary: boolean |
| **PerformanceReview** | reviewId: string ✓; reviewPeriod: string; rating: enum; reviewDate: date |

Design note: `employeeId` is a stable business identifier — mutable attributes like email must not be primary keys. Position separates role definition (title, level, salaryBand) from the person filling it.

### 3. Relationship types (4)

| Relationship | Cardinality |
|---|---|
| Employee —(has)→ Assignment | one-to-many |
| Assignment —(to)→ Department | many-to-one |
| Assignment —(to)→ Position | many-to-one |
| Employee —(has)→ PerformanceReview | one-to-many |

(Relationships are stated structurally, e.g. "`Employee` -> `Assignment` (one-to-many)"; no verb-style relation names are given in this track.)

### 4. Design patterns demonstrated
- **Junction/association entity**: Assignment resolves the Employee↔Department↔Position many-to-many staffing problem and carries relationship-owned attributes (startDate, endDate, isPrimary). Explicitly generalized: Student–Course via Enrollment, Customer–Product via Order line items. Rule taught: "Use junction entities when relationships need their own attributes."
- **Separation of concerns / role modeling**: person (Employee), org unit (Department), and role definition (Position) as distinct entities — collapsing into one "EmployeeProfile" would lose historical staffing changes, role transitions, and open positions existing before a hire.
- **Temporal modeling**: startDate/endDate on Assignment, reviewDate/reviewPeriod on PerformanceReview enable time-aware queries ("Who was in Finance during Q2?", "Which employees changed departments this year?", inactive assignments via endDate set or isPrimary=false).
- **Stable identifiers** for every entity; **controlled vocabularies** via enum properties (employmentStatus, jobLevel, rating, status, level).
- **Outcome attachment**: PerformanceReview attaches measurable outcomes to workforce entities for people analytics.

### 5. Progression logic
1. **01 Scenario overview** — domain, motivating question, 4-step plan, key concepts (stable identifiers, junction entities, temporal properties, enums).
2. **02 Organization core** — Employee + Department + Position (organizational backbone, identifiers, why separation matters). Quiz on Position-as-entity.
3. **03 Assignments** — adds Assignment junction entity for time-aware staffing history. Quiz on why Assignment is its own entity.
4. **04 Complete model** — adds PerformanceReview; full 5-entity graph; example-question-to-graph-path table; key takeaways; quiz on which entity enables historical analysis. Links to catalogue/designer.

### 6. Fabric IQ / RDF specifics
- No Fabric IQ, RDF/OWL, IRI, or export-format mentions in this track.
- Playground-specific mechanics: frontmatter `embed: community/ravi-chandu/hr-system` and `<ontology-embed id="community/ravi-chandu/hr-system" height="460px">` component; hash-route links `#/catalogue/community/ravi-chandu/hr-system` and `#/designer/community/ravi-chandu/hr-system`; ` ```quiz ` fenced blocks with `[correct]` markers and `>` explanations.

---

## Track 2: Smart Manufacturing (`manufacturing-path`, icon 🏭)

**Meta:** "Model an IoT-enabled factory — machines, sensors, work orders, parts, and quality checks." Type: path.

### 1. Scenario
A smart manufacturing facility with data flowing from IoT sensors, MES (Manufacturing Execution Systems), ERP platforms, and quality management databases. Motivating question: "Which machines with abnormal sensor readings produced parts that failed quality checks last week?" — spanning IoT telemetry, production schedules, part tracking, and inspection records. The ontology maps this to `Machine → Sensor (reading > threshold)` plus `Machine → Work-Order → Part → Quality-Check (passed=false)`.

### 2. Entity types (5)

| Entity | Properties (name: type; ✓ = identifier) |
|---|---|
| **Machine** | machineId: string ✓; name: string; type: string; status: string (running/idle/maintenance/offline); installDate: date |
| **Sensor** | sensorId: string ✓; type: string; unit: string; lastReading: float; threshold: float |
| **Work-Order** | workOrderId: string ✓; priority: string; status: string; startDate: date; dueDate: date |
| **Part** | partId: string ✓; name: string; material: string; weight: float; tolerance: float |
| **Quality-Check** | checkId: string ✓; inspector: string; checkDate: date; passed: boolean; defectCode: string |

Property semantics taught: `threshold` = alert boundary (alarm when lastReading > threshold, predictive maintenance); `tolerance` = acceptable manufacturing deviation (tighter tolerance → higher-precision machine required); `passed` boolean = ship-vs-rework decision point; `defectCode` = failure categorization for root cause analysis; dual dates (startDate/dueDate) = schedule adherence.

### 3. Relationship types (5, all named)

| Relationship | Cardinality |
|---|---|
| Sensor —monitors→ Machine | many-to-one |
| Work-Order —assigned_to→ Machine | many-to-one |
| Work-Order —produces→ Part | one-to-many |
| Machine —has_part→ Part | one-to-many |
| Quality-Check —inspects→ Part | many-to-one (a part may undergo multiple inspections: initial + re-check after rework) |

### 4. Design patterns demonstrated
- **IoT ownership hierarchy**: sensors belong to machines; direction matters (Sensor→Machine, parent-child), which is "how IoT platforms organize telemetry data".
- **Threshold-based alerting / predictive maintenance**: lastReading vs. threshold comparison.
- **Production chain via scheduling/event entity**: `Machine ← Work-Order → Part` — the middle entity represents the event, explicitly compared to Appointment connecting Patient and Provider in healthcare.
- **Quality feedback loop**: failed check reverses the chain `Quality-Check (passed=false) → Part → Work-Order → Machine` to identify problematic machines — root cause analysis / continuous improvement.
- **Status/state modeling** for real-time operational tracking; **boolean decision points** (passed).
- **Dual-perspective edges**: both Work-Order→Part (produces) and Machine→Part (has_part) model output from scheduling and equipment perspectives.

### 5. Progression logic
1. **01 Scenario overview** — domain, question, 3-step build plan (final: 5 entities, 5 relationships), key concepts (IoT hierarchies, production chains, quality loops, operational status).
2. **02 Factory floor** — Machine + Sensor + `monitors` (embed `official/manufacturing-step-1`). Quiz on lastReading/threshold.
3. **03 Production tracking** — adds Work-Order + Part + `assigned_to`/`produces`/`has_part` (embed step-2 with `diff` against step-1). Quiz on tolerance.
4. **04 Complete factory** — adds Quality-Check + `inspects`; question→path table; GQL query; cumulative build table; takeaways; quiz on the feedback loop. Embed step-3 diffed against step-2.

### 6. Fabric IQ / RDF specifics
- No Fabric IQ / RDF / OWL / IRI mentions.
- **GQL query example** (property-graph, Cypher-style syntax labeled ` ```gql `): `MATCH (s:Sensor)-[:monitors]->(m:Machine)-[:has_part]->(p:Part)<-[:inspects]-(qc:QualityCheck) WHERE s.lastReading > s.threshold AND qc.passed = false RETURN ...` — note label `QualityCheck` (no hyphen) vs. entity name `Quality-Check`.
- Playground mechanics: staged official embeds `official/manufacturing-step-1..3` with `diff="<previous-step>"` attribute to highlight additions; catalogue links.

---

## Track 3: University System (`university-path`, icon 🎓)

**Meta:** "Model an academic institution — students, courses, enrollments, professors, and departments." Type: path.

### 1. Scenario
A university management system whose data lives across SIS, LMS, HR, and academic planning databases. Motivating question: "Which departments have professors teaching courses where over 50% of enrolled students scored below a C?" — mapped to `Department → Professor → Course → Enrollment (grade < C) ← Student`. Final model: 5 entities, 6 relationships covering complete academic administration.

### 2. Entity types (5)

| Entity | Properties (name: type; ✓ = identifier) |
|---|---|
| **Student** | studentId: string ✓; name: string; gpa: float (0.0–4.0); enrollmentYear: integer; major: string |
| **Course** | courseId: string ✓; title: string; credits: integer; level: string (100/200/300/400); maxEnrollment: integer |
| **Enrollment** (junction) | enrollmentId: string ✓; semester: string; grade: string; enrollDate: date; status: string |
| **Professor** | professorId: string ✓; name: string; rank: string (Assistant/Associate/Full); tenured: boolean; officeHours: string |
| **Department** | departmentId: string ✓; name: string; building: string; budget: float; headOfDept: string |

Note: `headOfDept` references a professor who leads the department — called out as "a self-referential pattern common in organizational hierarchies" (modeled as a string property, not an edge).

### 3. Relationship types (6, all named)

| Relationship | Cardinality |
|---|---|
| Student —enrolls_in→ Enrollment | one-to-many |
| Enrollment —for_course→ Course | many-to-one |
| Professor —teaches→ Course | one-to-many |
| Professor —advises→ Student | one-to-many |
| Professor —belongs_to→ Department | many-to-one |
| Department —offers→ Course | one-to-many |

### 4. Design patterns demonstrated
- **Junction entity pattern** (flagship lesson): Enrollment resolves Student↔Course many-to-many while carrying grade, semester, status — "one of the most common patterns in ontology design"; attributes belong to the connection, not the endpoints.
- **Transitive / multi-hop queries**: Professor → Course → Enrollment → Student connects entities with no direct relationship ("Which students are taking courses from tenured professors?") — presented as a core strength of graph ontologies.
- **Organizational hierarchy + hub entity**: Department sits atop the ontology, connecting to both Professor (belongs_to) and Course (offers); the hub position enables department-level aggregate queries.
- **Property-type pedagogy**: float (gpa — aggregates/thresholds), integer (credits, maxEnrollment — capacity/workload planning), boolean (tenured — categorical filtering), defined-hierarchy strings (rank).
- **Temporal data**: semesters, enrollDate, academic years.
- **Self-reference hint**: headOfDept.

### 5. Progression logic
1. **01 Scenario overview** — domain, question, 3-step build plan, key concepts (junction entities, academic hierarchies, grade tracking, temporal data).
2. **02 Academic core** — Student + Course + Enrollment with `enrolls_in`/`for_course` (embed `official/university-step-1`). Quiz on why Enrollment is a separate entity.
3. **03 Faculty** — adds Professor with `teaches`/`advises`; transitive queries (embed step-2, diff step-1). Quiz on transitive queries.
4. **04 Complete university** — adds Department with `belongs_to`/`offers`; question→path table; GQL query; cumulative build table; takeaways; quiz on hub entities (embed step-3, diff step-2).

### 6. Fabric IQ / RDF specifics
- No Fabric IQ / RDF / OWL / IRI mentions.
- **GQL query example**: `MATCH (d:Department)-[:offers]->(c:Course)<-[:for_course]-(e:Enrollment)<-[:enrolls_in]-(s:Student) WHERE e.grade IN ['C','D','F'] RETURN d.name, c.title, COUNT(e) AS struggling_count ORDER BY struggling_count DESC`.
- Playground mechanics: `official/university-step-1..3` embeds with diff attribute; quiz blocks; catalogue links.

---

## Track 4: Supply Chain Disruption & Risk Propagation (`supply-chain-disruption-path`, icon 📦)

**Meta:** "Master proactive risk management — model how supplier disruptions cascade through components and product lines, and automate mitigation decisions with ontology-driven data agents." Type: path.

### 1. Scenario
A manufacturing operation dependent on a complex supplier web, where a single disruption (natural disaster, geopolitical event, quality issue, cyber attack) cascades through components → product lines → revenue → production timelines. Worked example: a 48-hour Taiwan semiconductor supplier power outage → ChipX component → 3 product lines → production halt in 2 weeks → $12M revenue at risk. The ontology lets an AI agent detect, trace, quantify, recommend, and act in minutes instead of days of manual spreadsheet analysis. Advertised outcome: a 7-entity, ~40-property, 7-relationship, "Fabric IQ compatible" ontology.

### 2. Entity types (7), organized in 4 tiers

**Tier 1 — The network**

| Entity | Properties |
|---|---|
| **Supplier** | supplierId: string ✓ (e.g. "SUPP-00456"); name: string; country: string; tier: enum (Tier 1/2/3); reliabilityScore: decimal (0–100); singleSourced: boolean |
| **Component** | componentId: string ✓ ("COMP-SEM-0821"); name: string; category: enum (Electronic/Mechanical/Chemical/Packaging/Raw Material); daysOfSupplyOnHand: integer; criticalityLevel: enum (Critical/High/Medium/Low) |
| **ProductLine** | productLineId: string ✓ ("PL-LAP-2024"); name: string; annualRevenue: decimal; marketSegment: string; productionStatus: enum (Active/At Risk/Halted/Discontinued) |

**Tier 2 — The disruption**

| Entity | Properties |
|---|---|
| **DisruptionEvent** | eventId: string ✓ ("DISR-202405-TAIWAN-001"); type: enum (Natural Disaster/Geopolitical/Financial/Logistics/Quality Recall/Pandemic/Cyber Attack); severity: enum (Critical/High/Medium/Low); startDate: date; estimatedDurationDays: integer; region: string |

**Tier 3 — The analysis**

| Entity | Properties |
|---|---|
| **RiskAssessment** | assessmentId: string ✓ ("RA-20240501-SEM-001"); assessedDate: datetime; revenueAtRisk: decimal (USD); timeToImpactDays: integer; confidenceLevel: enum (High/Medium/Low); recommendedAction: string |
| **MitigationAction** | actionId: string ✓ ("MA-20240501-ALT-SUPP"); type: enum (Activate Alternative Supplier/Increase Safety Stock/Redesign Component/Reduce Production/Expedite Shipment/Customer Communication); status: enum (Proposed/Approved/In Progress/Completed/Cancelled); estimatedCost: decimal (USD); leadTimeSavedDays: integer |

**Tier 4 — The backup**

| Entity | Properties |
|---|---|
| **AlternativeSupplier** | altSupplierId: string ✓ ("ALTSUPP-00789"); name: string; country: string; qualificationStatus: enum (Pre-qualified/Approved/Pending Audit/Not Qualified); capacityAvailable: integer (units/month); pricePremiumPercent: decimal (%) |

Property-type table taught (string/integer/decimal/date/datetime/enum/boolean) with agent-facing uses: search & filtering, threshold alerts, cost-benefit calc, timeline comparisons, audit trails/trending, classification/decision trees, risk flagging. Track claims "40 properties" total (properties listed per entity are "key properties").

### 3. Relationship types (7, the cascade)

| # | Relationship | Cardinality | Why |
|---|---|---|---|
| 1 | Supplier —supplies→ Component | 1:N | Disrupting one supplier affects all dependent components |
| 2 | Component —usedIn→ ProductLine | M:N | Components reused; products share components |
| 3 | DisruptionEvent —affects→ Supplier | M:N | One disaster hits multiple suppliers; a supplier faces multiple threats |
| 4 | DisruptionEvent —triggers→ RiskAssessment | 1:N | Each disruption spawns assessments per affected product line |
| 5 | RiskAssessment —recommends→ MitigationAction | 1:N | Each assessment yields a prioritized action list |
| 6 | MitigationAction —activates→ AlternativeSupplier | M:N | One action can bring multiple backups online |
| 7 | AlternativeSupplier —canReplace→ Supplier | M:1 | Multiple pre-qualified backups per critical primary supplier |

### 4. Design patterns demonstrated
- **Risk/impact propagation (cascade) modeling**: the 7 relationships encode how impact flows Disruption → Supplier → Component → ProductLine, then into the analysis/response chain (→ RiskAssessment → MitigationAction → AlternativeSupplier → back to Supplier). A full worked cascade tree (Taiwan outage → $80M at risk → activate ChipX Europe) is given.
- **Event–analysis–action lifecycle**: separate entities for the trigger (DisruptionEvent), quantified analysis (RiskAssessment), and response (MitigationAction) — an event-sourcing-like decomposition supporting audit and learning (estimated vs. actual cost/effectiveness).
- **Backup/substitution modeling**: AlternativeSupplier with qualificationStatus, capacity, and price premium; `canReplace` closes the loop to the primary supplier.
- **Risk-amplifier flags**: singleSourced boolean, criticalityLevel, daysOfSupplyOnHand for threshold-driven urgency (formulas given: `revenue_at_risk = annualRevenue/365 * daysOfSupplyOnHand`; `urgency = 100 - daysOfSupplyOnHand*10`).
- **Tiered entity architecture**: Tier 1 network / Tier 2 disruption / Tier 3 analysis / Tier 4 backup.
- **Enum-heavy controlled vocabularies + human-readable structured ID conventions** (prefix + date + region/domain codes, e.g. "DISR-202405-TAIWAN-001") for agent-referenceable instances.
- **Rule-based automation over the graph**: IF/THEN policy (revenueAtRisk > $50M AND timeToImpactDays < 5 → create PO, update schedule, notify, trigger Activator alerts, monitor status).
- **Continuous-improvement metrics**: detection speed < 1h, trace accuracy > 95%, impact estimate ±10%, time-to-mitigation < 2h, cost efficiency ±5%, revenue protection > 80%.

### 5. Progression logic
1. **01 Scenario overview** — challenge, real-world example, agent value proposition, 4-step plan, key concepts (disruption events, impact propagation, risk assessment, mitigation actions, alternative suppliers).
2. **02 Core entities & properties** — all 7 entities with key properties across 4 tiers; property-type/validation table; identifier conventions; cardinality preview (1:N, M:N, M:1).
3. **03 Risk propagation model** — the 7 relationships one by one with mini instance diagrams, query examples per relationship, full cascade trace, the 6-step agent loop (Detect/Trace/Quantify/Recommend/Act/Learn), cardinality rules table.
4. **04 Mitigation execution & automation** — 5-phase operational timeline (Detection min 0 → Trace min 5 → Quantify min 15 → Recommend min 20 → Execute min 25), end-to-end day-by-day workflow narrative, Fabric IQ data-agent grounding dialogues, automation rules, continuous-improvement metric table, production-readiness summary.

Unlike the other three tracks, this one has **no embeds, no quizzes, and no GQL blocks** — it teaches through instance-level ASCII cascade diagrams, pseudo-query walk-throughs, and agent conversation transcripts.

### 6. Fabric IQ / RDF specifics
- **Fabric IQ is explicit and central** (unique among the 4 tracks): "Fabric IQ compatibility for data agent grounding and real-time alerting" (lesson 01); lesson 04 has a "Connecting to Fabric IQ" section showing a natural-language user query grounded by a data agent against the ontology (multi-hop traversal + filter pseudo-query `AlternativeSupplier WHERE canReplace.Supplier.name = "ChipX Corp" AND qualificationStatus = "Approved"`), and the summary claims "Fabric IQ compatible for natural-language agents" and "Automation-ready with enum classifications and timestamps".
- **Activator** (Fabric Real-Time Intelligence alerting) is referenced twice: "Create Activator alerts with escalation policy" and "Activator triggered … escalation policy notifies leadership".
- Other Fabric-adjacent vocabulary: "data agent", "grounding", real-time dashboards, escalation policies, automated procurement workflows.
- No RDF/OWL constructs, no IRI conventions (identifiers are business-key strings like "SUPP-00456"), no export formats mentioned.

---

## Cross-track synthesis

| Track | Entities | Relationships | Signature pattern | Query formalism | Embeds |
|---|---|---|---|---|---|
| HR System | 5 | 4 | Junction entity (Assignment) + role separation + temporal staffing history | none (path tables only) | community/ravi-chandu/hr-system |
| Smart Manufacturing | 5 | 5 | IoT hierarchy + production chain + quality feedback loop | GQL (Cypher-style) | official/manufacturing-step-1..3 (with diff) |
| University | 5 | 6 | Junction entity (Enrollment) + transitive queries + hub entity (Department) | GQL (Cypher-style) | official/university-step-1..3 (with diff) |
| Supply Chain Disruption | 7 | 7 | Risk propagation cascade + event/analysis/action lifecycle + backup substitution | pseudo-queries + Fabric IQ agent transcripts | none |

- **Totals: 22 entity types, 22 relationship types** across the 4 tracks.
- Shared pedagogy: every track opens with a cross-system business question that becomes a graph path; entities carry a string identifier property marked ✓; property datatypes are used didactically (enum = controlled status, boolean = decision point, float/decimal = thresholds & aggregates, date pairs = temporal analysis).
- Recurring content mechanics: YAML frontmatter (title/slug/description/order, `embed`), `<ontology-embed>` with optional `diff` attribute for staged builds, ` ```quiz ` blocks with `[correct]` markers, `#/catalogue` and `#/designer` hash-route links.
- The junction-entity pattern is taught in three domains (Assignment, Enrollment, and Work-Order-as-event) and explicitly generalized; the supply-chain track is the only one addressing Fabric IQ, agents, Activator, and operational automation. No track uses RDF/OWL/IRI terminology.
# Digest C — Ontology-Playground Advanced Lab Tracks

Structured extraction of the 4 advanced "lab" tracks from Microsoft Ontology-Playground learn content.
Source root: `Ontology-Playground/content/learn/`

Labs covered:

1. **FIBO Loans Lab** (`fibo-loans-lab/`, 🏛️) — 10 entities, 10 relationships claimed (9 named in lessons)
2. **FIBO Risk Management Lab** (`fibo-risk-lab/`, 🛡️) — 11 entities, 10 relationships claimed (9 named in lessons)
3. **IQ Lab: Retail Supply Chain** (`iq-lab-retail-supply-chain/`, 🔬) — 15 entities, 18 relationships
4. **Zava Grove-to-Shelf: Semantic Cold Chain** (`zava-grove-to-shelf/`, 🌾) — 12 entities, 13 relationships

All labs share a common lesson format: `_meta.md` frontmatter (title, slug, description, type: lab, icon), per-lesson frontmatter (`order`, `embed: official/<slug>-step-N`, some with `reviewStatus: under-human-review` on FIBO labs), `<ontology-embed>` tags with `diff="previous-step"` for incremental graph rendering, and a ```quiz``` block per lesson (multiple choice with `[correct]` marker and `>` explanation).

---

## Lab 1: FIBO Loans Lab

### 1. Scenario

A loans/lending ontology adapted from the EDM Council + OMG **Financial Industry Business Ontology (FIBO)** (MIT License, github.com/edmcouncil/fibo, spec.edmcouncil.org/fibo). The lab extracts a teachable subset of the huge FIBO module family — primarily `LOAN/LoansGeneral/Loans` plus `FBC/DebtAndEquities/Debt`, `FBC/ProductsAndServices/ClientsAndAccounts`, `FND/OwnershipAndControl/Ownership` — so learners can model loan contracts, collateral, servicing/payment audit trails, and risk classifiers. Target questions: collateralized loans with subordinate liens, interest-only loans above a principal threshold, payment patterns by servicer, ownership structures correlated with repayment issues.

### 2. Entity types (10)

| Entity | Properties (name: datatype) | FIBO source |
|---|---|---|
| **Loan** | loanId: string (id); principalAmount: decimal (USD); isInterestOnly: boolean | `fibo-loan-ln-ln:Loan` (LOAN/LoansGeneral/Loans) |
| **Borrower** | borrowerId: string (id); name: string; creditScore: integer (e.g. FICO) | `fibo-fbc-dae-dbt:Borrower` (FBC/DebtAndEquities/Debt) |
| **Lender** | lenderId: string (id); name: string; lenderType: string ("bank", "credit union", "mortgage company") | `fibo-fbc-dae-dbt:Lender` (FBC/DebtAndEquities/Debt) |
| **Collateral** | assetType: string (id; "real property", "vehicle", "securities"); appraisedValue: decimal (USD) | `fibo-fbc-dae-dbt:Collateral` |
| **LoanPaymentSchedule** | scheduleId: string (id); expectedPayments: integer | `fibo-loan-ln-ln:LoanPaymentSchedule` |
| **Servicer** | servicerId: string (id); organizationName: string | `fibo-loan-ln-ln:Servicer` |
| **PaymentHistory** | paymentHistoryId: string (id) | `fibo-loan-ln-ln:PaymentHistory` (extends FBC transaction-record patterns) |
| **PaymentTransaction** | paymentTransactionId: string (id); amount: decimal (USD); postedAt: datetime | `fibo-loan-ln-ln:IndividualPaymentTransaction`, based on `fibo-fbc-pas-caa:IndividualTransaction` |
| **OwnershipInterest** | (classifier entity — no property table given) | `fibo-loan-ln-ln:OwnershipInterest`, grounded in `fibo-fnd-oac-own:Ownership` |
| **LenderLienPosition** | (classifier entity — no property table given) | `fibo-loan-ln-ln:LenderLienPosition` |

### 3. Relationship types (9 named; overview claims 10)

| Relationship | Cardinality | Semantics |
|---|---|---|
| `Loan —owedBy→ Borrower` | many-to-one | loan owed by exactly one borrower; borrower may hold many loans |
| `Loan —originatedBy→ Lender` | many-to-one | one lender originates many loans |
| `Loan —securedBy→ Collateral` | one-to-many | a loan can be secured by multiple assets |
| `Loan —repaidBySchedule→ LoanPaymentSchedule` | one-to-one | one primary repayment schedule per loan |
| `Loan —servicedBy→ Servicer` | many-to-one | many loans serviced by one org |
| `LoanPaymentSchedule —hasPaymentHistory→ PaymentHistory` | one-to-one | links scheduled expectations to actual records |
| `PaymentHistory —hasIndividualPayment→ PaymentTransaction` | one-to-many | history contains many atomic events |
| `OwnershipInterest —classifiesCollateralOwnership→ Collateral` | one-to-many | classifier of collateral ownership type |
| `Collateral —hasLienPosition→ LenderLienPosition` | many-to-one | lender claim seniority |

### 4. Design patterns demonstrated

- **Adaptation of an industry-standard ontology (FIBO)**: simplifying deep OWL class hierarchies into a direct-entity model while preserving semantics and citing source module IRIs; explicit MIT-license attribution practice.
- **Directional obligation modeling**: relationships point from the contract instrument (Loan) to party roles (`owedBy`, `originatedBy`) — FIBO's pattern of modeling obligations from the instrument.
- **Party-role simplification**: FIBO's contract-party role concepts (Borrower/Lender as roles grounded in FND Parties) flattened to direct entities for clarity.
- **Aggregate vs. atomic event separation**: PaymentHistory (aggregate record) vs. PaymentTransaction (atomic event) — FIBO's transaction-record pattern; supports reconciliation and audit.
- **Audit-trail path modeling**: `Loan → LoanPaymentSchedule → PaymentHistory → PaymentTransaction` traversal for delinquency analysis and servicing quality metrics.
- **Explicit classifier entities**: OwnershipInterest and LenderLienPosition are entities whose only role is to categorize others — used for credit risk, loss-given-default, portfolio risk aggregation, and regulatory capital.
- **Security-agreement/collateral modeling**: collateral as pledged asset; noted that FIBO Mortgages constrains collateral to `fibo-fnd-plc-rp:RealProperty` via `owl:Restriction` blocks.

### 5. Progression logic (5 lessons, 4 build steps)

1. **01 Scenario Overview** — what FIBO is, module map, licensing; no entities.
2. **02 Core Loan Triad** (step-1 embed) — Loan, Borrower, Lender + owedBy, originatedBy. Foundation triangle.
3. **03 Collateral and Schedules** (step-2, diff step-1) — +Collateral, LoanPaymentSchedule + securedBy, repaidBySchedule. Adds security agreements and temporal obligations.
4. **04 Servicing and Payment History** (step-3, diff step-2) — +Servicer, PaymentHistory, PaymentTransaction + servicedBy, hasPaymentHistory, hasIndividualPayment. Adds operational lifecycle / audit trail.
5. **05 Risk and Classifiers** (step-4, diff step-3) — +OwnershipInterest, LenderLienPosition + classifiesCollateralOwnership, hasLienPosition. Adds risk/underwriting classification layer; shows complete external subset `external/fibo/loans-general`.

Each step's lesson embeds the incremental graph via `<ontology-embed id="official/fibo-loans-step-N" diff="official/fibo-loans-step-(N-1)">`.

### 6. Standards & Fabric IQ specifics

- **FIBO prefixed IRIs referenced**: `fibo-loan-ln-ln:Loan`, `:LoanPaymentSchedule`, `:Servicer`, `:PaymentHistory`, `:IndividualPaymentTransaction`, `:OwnershipInterest`, `:LenderLienPosition`; `fibo-fbc-dae-dbt:Borrower`, `:Lender`, `:Collateral`; `fibo-fbc-pas-caa:IndividualTransaction`; `fibo-fnd-oac-own:Ownership`; `fibo-fnd-plc-rp:RealProperty`.
- **FIBO modules**: LOAN/LoansGeneral/Loans, LOAN/RealEstateLoans/Mortgages (incl. `LoanSecuredByRealEstate`, `SecurityAgreement`), FBC/DebtAndEquities/Debt, FBC/ProductsAndServices/ClientsAndAccounts, FND/OwnershipAndControl/Ownership, FND/Parties.
- **OWL constructs**: FIBO published as OWL ontologies; `owl:Restriction` blocks used in Mortgages to constrain collateral/contract semantics; RDF source files cited (`Mortgages.rdf`, `Loans.rdf`).
- **Playground constructs**: `official/fibo-loans-step-1..4` embeds with diff rendering; `external/fibo/loans-general` catalogue ontology.
- **Licensing**: MIT License, copyright EDM Council Inc. & OMG Inc.

---

## Lab 2: FIBO Risk Management Lab

### 1. Scenario

A banking **concentration-risk** ontology: regulators (OCC, FDIC, Basel Committee) require banks to monitor and limit portfolio exposure concentrated in a single industry, geography, or product type. The ontology encodes explicit semantics (e.g. "residential mortgage has a 35% Basel risk weight"), enables cross-domain graph queries (jurisdiction disaster flags → loans → concentration categories), and provides regulatory traceability (every limit links to its mandating regulation). Adapted from FIBO's classification, geographic, debt/equity, and regulatory framework modules (MIT License).

### 2. Entity types (11)

**Industry domain**

| Entity | Properties |
|---|---|
| **Sector** | sectorCode: string (id, e.g. "31-33"); sectorName: string; description: string |
| **Subsector** | subsectorCode: string (id, e.g. "311"); subsectorName: string |
| **IndustryGroup** | naicsCode: string (id, official NAICS code); name: string; cyclicality: string ("high"/"low"/"counter-cyclical"); climateSensitivity: string ("high"/"moderate"/"low"); essentialServices: boolean; description: string |

**Geography domain**

| Entity | Properties |
|---|---|
| **Region** | regionCode: string (id); regionName: string; description: string; disasterProfile: string |
| **Country** | countryCode: string (id, ISO code); countryName: string; economicZone: string ("developed"/"emerging"); currency: string; regulatoryFramework: string |
| **Jurisdiction** | code: string (id, e.g. "FL", "CA"); name: string; hurricaneZone: boolean; floodZone: boolean; earthquakeZone: boolean; wildfireZone: boolean; coastal: boolean; latitude: decimal; longitude: decimal |

**Loan classification domain**

| Entity | Properties |
|---|---|
| **ConcentrationCategory** | categoryId: string (id, e.g. "CRE", "C&I", "CONSUMER"); name: string; description: string; occGuidance: string. Examples: CRE, C&I, Consumer, Agriculture |
| **LoanType** | loanTypeCode: string (id, e.g. "residential_mortgage"); name: string; baselRiskWeight: decimal (%); regulatoryTreatment: string; capitalTier: string; description: string. Example weights: residential mortgage 35%, auto 75%, SBA 0% (gov-guaranteed), construction 150%, CRE mortgage 100% |
| **CollateralType** | collateralTypeCode: string (id); name: string; recoveryExpectation: string ("high"/"moderate"/"low"); description: string |

**Regulation domain**

| Entity | Properties |
|---|---|
| **Regulation** | regulationCode: string (id, e.g. "OCC_CRE_2006"); name: string; issuingAuthority: string (OCC, FDIC, Basel Committee); effectiveDate: date; scope: string; description: string |
| **RegulatoryLimit** | limitId: string (id); limitName: string; category: string; thresholdPct: decimal (%); severity: string ("warning"/"action required"/"supervisory intervention"); description: string. Example limits: CRE concentration 300% of capital (OCC 2006-46); climate+hurricane 15% of portfolio (internal policy); geographic concentration 20% (OCC Bulletin 2011-12); industry concentration 25% (FDIC Risk Management) |

### 3. Relationship types (9 named; overview claims 10)

| Relationship | Cardinality |
|---|---|
| `Subsector —partOfSector→ Sector` | many-to-one |
| `IndustryGroup —belongsToSubsector→ Subsector` | many-to-one |
| `Jurisdiction —inCountry→ Country` | many-to-one |
| `Jurisdiction —inRegion→ Region` | many-to-one |
| `LoanType —loanClassifiedAs→ ConcentrationCategory` | many-to-one |
| `CollateralType —collateralClassifiedAs→ ConcentrationCategory` | many-to-one |
| `CollateralType —typicallySecuredBy→ LoanType` | many-to-many |
| `RegulatoryLimit —mandatedBy→ Regulation` | many-to-one |
| `RegulatoryLimit —limitAppliesToCategory→ ConcentrationCategory` | many-to-one |

### 4. Design patterns demonstrated

- **Classification hierarchy (strict tree)**: Sector ← Subsector ← IndustryGroup, each child exactly one parent; enables roll-up aggregation, drill-down analysis, risk attribute inheritance. Built on the **NAICS** taxonomy.
- **Geographic hierarchy**: Region / Country / Jurisdiction, with Jurisdiction attaching to both Country and Region.
- **Boolean risk-flag pattern**: Jurisdiction uses independent booleans (hurricaneZone, floodZone, earthquakeZone, wildfireZone, coastal) instead of a single riskType enum, because a jurisdiction can be in multiple disaster zones simultaneously (FL: hurricane+flood; CA: earthquake+wildfire) — enables compound multi-dimension filtering.
- **Independent subgraphs joined later**: after step 2 the industry and geography hierarchies are deliberately disconnected; the lab shows them connecting via loan/regulatory layers.
- **Hub entity**: ConcentrationCategory — LoanType, CollateralType, and RegulatoryLimit all point at it; central node for compliance queries.
- **Cross-domain bridge**: `limitAppliesToCategory` completes a traversal path Jurisdiction(hurricaneZone) → ConcentrationCategory → RegulatoryLimit → Regulation; graph traversals replace multi-table warehouse JOINs.
- **Regulatory-traceability encoding**: quantitative thresholds (Basel III risk weights, OCC/FDIC concentration limits) as first-class data properties on entities, with limits linked to the mandating regulation.

### 5. Progression logic (5 lessons, 4 build steps)

1. **01 Scenario Overview** — concentration risk concept, four-domain plan.
2. **02 Step 1: Industry Classification** (step-1) — Sector, Subsector, IndustryGroup + partOfSector, belongsToSubsector.
3. **03 Step 2: Geographic Hierarchy** (step-2, diff step-1) — Region, Country, Jurisdiction + inCountry, inRegion; two independent subgraphs.
4. **04 Step 3: Loan Classification** (step-3, diff step-2) — ConcentrationCategory, LoanType, CollateralType + loanClassifiedAs, collateralClassifiedAs, typicallySecuredBy; hub pattern; Basel III risk weights.
5. **05 Step 4: Regulatory Context** (step-4, diff step-3) — Regulation, RegulatoryLimit + mandatedBy, limitAppliesToCategory; closes the cross-domain loop.

### 6. Standards & Fabric IQ specifics

- **Standards**: FIBO (EDM Council, MIT License, copyright (c) 2016-2025 EDM Council/OMG); NAICS industry codes; ISO country codes; Basel III standardized risk weights; OCC guidance (2006-46, Bulletin 2011-12) and FDIC risk management guidance.
- **No explicit FIBO IRIs** are cited in this lab (unlike the loans lab) — modules referenced generically as "classification, geographic, debt/equity, and regulatory frameworks from the FIBO family".
- **Playground constructs**: `official/fibo-risk-step-1..4` embeds with diffs; external catalogue ontologies `external/fibo/industry-classification`, `external/fibo/geographic-hierarchy`, `external/fibo/loan-classification`, `external/fibo/regulatory-context`.
- Positioning: graph traversals vs. "complex multi-table JOINs in a traditional data warehouse".

---

## Lab 3: IQ Lab: Retail Supply Chain

### 1. Scenario

A fictional retail company manages orders, products, customers, warehouses and shipments across regions, with data split between a Microsoft Fabric **Eventhouse** (real-time: orders, shipments, demand signals) and a **Lakehouse** (dimensional: catalogs, customer profiles, forecasts). The ontology is a semantic layer that maps business concepts to sources so cross-system questions ("Which promotions drove returns in the southwest region?") become graph traversals and natural-language Data Agent questions, instead of manual multi-system joins.

### 2. Entity types (15)

| Entity | Properties (✓ = identifier) |
|---|---|
| **Customer** | customerId: string ✓; name: string; email: string; loyaltyTier: string; lifetimeValue: decimal (USD) |
| **Order** | orderId: string ✓; orderDate: datetime; status: string; totalAmount: decimal (USD) |
| **Product** | productId: string ✓; name: string; unitCost: decimal (USD); discountPercent: decimal (%) |
| **OrderLine** | orderLineId: string ✓; quantity: integer; lineTotal: decimal (USD) |
| **ProductCategory** | categoryId: string ✓; categoryName: string |
| **Region** | regionId: string ✓; regionName: string; timezone: string; coldChainRequired: boolean |
| **Store** | storeId: string ✓; storeName: string; address: string |
| **Shipment** | shipmentId: string ✓; shipDate: date; deliveryDate: date; status: string |
| **Carrier** | carrierId: string ✓; carrierName: string; serviceType: string |
| **Warehouse** | warehouseId: string ✓; warehouseName: string; capacity: integer |
| **Inventory** | inventoryId: string ✓; stockLevel: integer; reorderPoint: integer |
| **Forecast** | forecastId: string ✓; forecastDate: date; predictedDemand: integer |
| **DemandSignal** | signalId: string ✓; signalDate: datetime; signalStrength: decimal |
| **Promotion** | promotionId: string ✓; promotionName: string; isActivePromotion: boolean |
| **Return** | returnId: string ✓; returnDate: date; reason: string |

### 3. Relationship types (18)

| Relationship | Cardinality |
|---|---|
| `Order —OrderPlacedByCustomer→ Customer` | many-to-one |
| `Order —OrderContainsProduct→ Product` | many-to-many (superseded conceptually by OrderLine in step 2) |
| `Order —OrderHasLineItem→ OrderLine` | one-to-many |
| `OrderLine —OrderLineReferencesProduct→ Product` | many-to-one |
| `Product —ProductInCategory→ ProductCategory` | many-to-one |
| `Order —OrderFulfilledToRegion→ Region` | many-to-one |
| `Store —StoreInRegion→ Region` | many-to-one |
| `Shipment —ShipmentFulfillsOrder→ Order` | many-to-one (split shipments allowed) |
| `Shipment —ShipmentByCarrier→ Carrier` | many-to-one |
| `Shipment —ShipmentDepartedFromWarehouse→ Warehouse` | many-to-one |
| `Inventory —InventoryForProduct→ Product` | many-to-one |
| `Inventory —InventoryAtWarehouse→ Warehouse` | many-to-one |
| `Forecast —ForecastForProduct→ Product` | many-to-one |
| `DemandSignal —DemandSignalForProduct→ Product` | many-to-one |
| `DemandSignal —DemandSignalInRegion→ Region` | many-to-one |
| `Promotion —PromotionForProduct→ Product` | many-to-one |
| `Return —ReturnForOrder→ Order` | many-to-one |
| `Return —ReturnOfProduct→ Product` | many-to-one |

### 4. Design patterns demonstrated

- **Entity-type fundamentals**: singular business-meaningful names (Customer, not `tbl_cust`), mandatory identifier property, business-friendly property names mapped from cryptic source columns (`cust_lt_val` → lifetime value).
- **Cardinality semantics**: one-to-one / one-to-many / many-to-one / many-to-many taught explicitly with counting/aggregation implications.
- **Linking (junction/association) entity**: OrderLine bridges the Order↔Product many-to-many to carry per-association attributes (quantity, lineTotal) — "the ontology equivalent of an association table".
- **Category hierarchy / roll-up**: Product → ProductCategory.
- **Geographic hierarchy**: Store → Region via many-to-one; roll-up from granular to aggregate; extendable to City/State/Country.
- **Boolean business-rule property**: Region.coldChainRequired captures a yes/no rule as a queryable attribute.
- **Hub entity**: Shipment connects Order, Carrier, Warehouse simultaneously (transaction/event entity bridging domains).
- **Intersection entity**: Inventory sits between Product and Warehouse ("how much of Product X at Warehouse Y?").
- **Cross-source unification**: one entity graph over multiple Fabric engines — Inventory/DemandSignal from Eventhouse, Forecast from Lakehouse, Product from both.
- **Historical + real-time + predictive unification**: orders (happened), inventory/demand signals (happening), forecasts (will happen) under one model.
- **Graph traversal replaces SQL joins**; "the ontology is the API" — GQL and Data Agent both follow the model structure.

### 5. Progression logic (7 lessons, 6 build steps)

| Step | Lesson | Entities added (cumulative) | Key concept |
|---|---|---|---|
| — | 01 Scenario Overview | — | Eventhouse/Lakehouse problem, semantic layer |
| 1 | 02 Core Commerce | Customer, Order, Product (3) | entity types, identifiers, cardinality |
| 2 | 03 Order Details & Categories | OrderLine, ProductCategory (5) | linking entities, hierarchies |
| 3 | 04 Geography | Region, Store (7) | geographic structure, boolean properties |
| 4 | 05 Fulfillment & Logistics | Shipment, Carrier, Warehouse (10) | hub entities, cross-domain connections |
| 5 | 06 Inventory & Demand | Inventory, Forecast, DemandSignal (13) | cross-source unification, planning data |
| 6 | 07 Complete Model | Promotion, Return (15) | closing the loop, GQL querying |

Each lesson embeds `official/iq-lab-retail-step-N` with `diff` against step N-1.

### 6. Standards & Fabric IQ specifics

- **Microsoft Fabric IQ concepts**: Eventhouse (real-time/streaming) vs. Lakehouse (dimensional/batch ML) source binding; data bindings map concepts to sources ("adding a new binding extends the model without breaking queries"); natural-language **Data Agent** answering from ontology structure; a per-entity source-binding table (Inventory→Eventhouse, Forecast→Lakehouse, DemandSignal→Eventhouse, Product→both).
- **GQL** (Graph Query Language) example given:
  ```gql
  MATCH (r:Return)-[:ReturnOfProduct]->(p:Product)<-[:PromotionForProduct]-(promo:Promotion)
  WHERE promo.isActivePromotion = true
  RETURN promo.promotionName, p.name, r.reason
  ```
- Example question→graph-path table (Promotion → Product ← Return; Return → Product ← Inventory → Warehouse; Customer ← Order → OrderLine → Product ← Promotion; Inventory → Product ← Forecast; etc.).
- No FIBO/RDF/OWL references — this lab is pure Fabric IQ modeling vocabulary. Step ontologies loadable from the playground catalogue.

---

## Lab 4: Zava Grove-to-Shelf: Semantic Cold Chain

### 1. Scenario

**Zava** is a fictional global premium fresh fruit & vegetable producer/distributor: multi-origin sourcing (partner farms in Spain, Ecuador, South Africa, Tunisia, Germany…), a four-stage quality-control regime (field, packhouse, destination DC, store), reefer-container cold-chain logistics with continuous temperature sensors, retail partners (DCs/stores placing orders by variety), and a grower sustainability program ("Zava Dreams"). Data is fragmented across agronomy ERPs, packhouse QC apps, IoT eventhouses, retail EDI feeds and CSR spreadsheets; the ontology's flagship use case is the cold-chain breach question — "a reefer with 18t of Nadorcott mandarins crossed 9°C in transit: which retailer orders are at risk and what's the revenue exposure?"

### 2. Entity types (12)

| Entity | Properties (✓ = identifier) |
|---|---|
| **Grower** | growerId: string ✓; name: string; country: string; partnerSince: date; isMasterGrower: boolean (strategic long-term partner flag) |
| **Farm** | farmId: string ✓; name: string; country: string; region: string; hectares: decimal (ha) |
| **Plot** | plotId: string ✓; hectares: decimal (ha); plantingYear: integer |
| **FruitVariety** | varietyId: string ✓; commercialName: string; category: string; shelfLifeDays: integer (days). (Breach query also references a `maxStorageTempC` threshold per variety.) |
| **HarvestLot** | lotId: string ✓; harvestDate: date; kilograms: decimal (kg); qcGrade: string |
| **QualityCheck** | checkId: string ✓; stage: integer (1–4); passed: boolean; defectRate: decimal (%); checkedAt: datetime |
| **Shipment** | shipmentId: string ✓; departureDate: datetime; etaDate: datetime; modality: string; containerId: string |
| **ColdChainSensor** | sensorId: string ✓; sensorModel: string; temperatureC: decimal (°C); humidityPct: decimal (%) |
| **RetailDC** | dcId: string ✓; name: string; country: string; city: string; retailerCode: string |
| **Store** | storeId: string ✓; name: string; retailerName: string; country: string; city: string |
| **Order** | orderId: string ✓; kilograms: decimal (kg); orderDate: date; deliveryDate: date; status: string; unitPriceEur: decimal (EUR) |
| **SustainabilityProgram** | programId: string ✓; name: string; focusArea: string; startYear: integer |

### 3. Relationship types (13)

| Relationship | Cardinality |
|---|---|
| `Grower —owns→ Farm` | one-to-many |
| `Farm —contains→ Plot` | one-to-many |
| `Plot —grows→ FruitVariety` | many-to-one |
| `HarvestLot —fromPlot→ Plot` | many-to-one |
| `HarvestLot —ofVariety→ FruitVariety` | many-to-one (deliberate shortcut; captures *as-harvested* variety which can differ from plot's nominal variety after replanting) |
| `QualityCheck —checks→ HarvestLot` | many-to-one |
| `Shipment —carries→ HarvestLot` | one-to-many |
| `Shipment —monitoredBy→ ColdChainSensor` | one-to-many |
| `Shipment —deliveredTo→ RetailDC` | many-to-one |
| `RetailDC —supplies→ Store` | one-to-many |
| `Store —places→ Order` | one-to-many |
| `Order —forVariety→ FruitVariety` | many-to-one (orders placed against varieties, not lots — key to matching breached lots to exposed open orders) |
| `Farm —participatesIn→ SustainabilityProgram` | many-to-many (a farm may join multiple programs; a program enrolls many farms) |

### 4. Design patterns demonstrated

- **End-to-end traceability chain**: `Grower → Farm → Plot → FruitVariety` gives plot-level identity (Plot is a first-class entity, not a Farm property, because a farm hosts multiple plots with different varieties).
- **Lineage anchor / traceability unit**: HarvestLot is the unit every downstream event (breach, return, claim) points back to.
- **Event modeling over boolean flattening**: QualityCheck as a first-class event entity with `stage: 1–4` rather than four boolean columns on HarvestLot — preserves defectRate/checkedAt per inspection and enables aggregation/filtering by stage ("which growers fail stage 3 most often?").
- **Cold-chain sensor / time-series entity modeling**: ColdChainSensor is the canonical Fabric IQ **time-series entity**, bound to an Eventhouse rather than a Lakehouse table; the ontology hides the storage split.
- **Hub entities (three named)**: HarvestLot = lineage hub; Shipment = lakehouse↔eventhouse hub (bridges static lineage and streaming telemetry); FruitVariety = supply↔demand hub.
- **Deliberate redundant edge (shortcut relation)**: `ofVariety` alongside `fromPlot→grows` — skips a hop and preserves as-harvested semantics.
- **Variety-level (not lot-level) demand matching**: `Order forVariety FruitVariety` cross-references at-risk lots with open orders for the same variety.
- **Many-to-many CSR overlay**: SustainabilityProgram attached via one many-to-many edge so CSR questions "ride the same graph as revenue questions".
- **Ontology as contract**: GQL queries, Fabric Data Agent prompts, and Activator rules all reference the same entity/relationship names.

### 5. Progression logic (6 lessons, 5 build steps)

| Step | Lesson | Entities added (cumulative) | Key concept |
|---|---|---|---|
| — | 01 Scenario Overview | — | five-system data problem, breach question |
| 1 | 02 Orchard Foundation | Grower, Farm, Plot, FruitVariety (4) | multi-origin sourcing, traceability anchor |
| 2 | 03 Harvest & Quality | HarvestLot, QualityCheck (6) | lineage events, four-stage QC regime |
| 3 | 04 Cold-Chain Logistics | Shipment, ColdChainSensor (8) | hub entities, time-series binding |
| 4 | 05 Retail Fulfillment | RetailDC, Store, Order (11) | closing the loop to revenue |
| 5 | 06 Complete Model | SustainabilityProgram (12) | many-to-many CSR overlay |

The breach query is introduced in step 3 as a partial traversal and deliberately "closed" in step 4 once retail entities exist:
`ColdChainSensor[breach] → Shipment → HarvestLot —ofVariety→ FruitVariety; Shipment → RetailDC → Store → Order[forVariety = breached variety, status=open]`, revenue exposure = Σ(kilograms × unitPriceEur). Each lesson embeds `official/zava-grove-to-shelf-step-N` with diff.

### 6. Standards & Fabric IQ specifics

- **Fabric IQ concepts**: Eventhouse vs. Lakehouse binding split hidden by the ontology; ColdChainSensor as the canonical time-series entity; tables/event streams **bound** to concepts ("New retailer? Add bindings, model stays the same"); Fabric IQ **Data Agent** answering business-English questions; **Activator** rules referencing ontology names; GQL mentioned as consumer of the model.
- **No FIBO/RDF/OWL references** — quiz distractors explicitly debunk "required by RDF" claims. Fictional-brand scenario (Zava, "Dreams" program).
- Final lesson invites opening `official/zava-grove-to-shelf-step-5` in the playground "to query, extend, or export it".

---

## Cross-lab summary

| Lab | Steps | Entities | Relationships (as enumerated in lessons) | Signature patterns |
|---|---|---|---|---|
| FIBO Loans | 4 | 10 | 9 (claims 10) | FIBO adaptation, classifier entities, aggregate-vs-atomic payment events, audit-trail path |
| FIBO Risk | 4 | 11 | 9 (claims 10) | classification tree (NAICS), geographic hierarchy, boolean risk flags, hub entity, cross-domain bridge, Basel III/OCC/FDIC encoding |
| IQ Retail Supply Chain | 6 | 15 | 18 | linking/junction entity, hub entity, intersection entity, cross-source (Eventhouse/Lakehouse) unification, GQL |
| Zava Grove-to-Shelf | 5 | 12 | 13 | traceability lineage, QC event modeling, cold-chain time-series sensor entity, triple hubs, shortcut edge, many-to-many CSR overlay |
| **Total** | 19 | **48** | **49 enumerated (51 claimed)** | |

Shared authoring conventions: progressive step ontologies (`official/<lab>-step-N`) with visual diffs against the previous step, one quiz per lesson, "real questions this model supports" framing, graph-traversal-vs-SQL-JOIN value proposition, and (FIBO labs only) explicit MIT-license attribution to EDM Council/OMG with source-module citations. The two FIBO labs teach standards alignment; the two IQ labs (retail, Zava) teach Fabric IQ operational concepts (bindings, Eventhouse/Lakehouse, Data Agent, GQL, Activator).

Note on discrepancies: both FIBO labs advertise 10 relationships in their overview lessons but only 9 named relationships appear across their lesson bodies and summary tables; the enumerated counts above reflect what the content actually defines.
