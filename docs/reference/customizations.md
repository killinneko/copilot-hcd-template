# GitHub Copilotカスタマイズガイド

この文書は、収録するエージェント、スキル、プロンプトの選び方と個別仕様をまとめたリファレンスです。

## 1. 仕組みの違い

| 種別 | 役割 | 適用方法 | 保存場所 |
| --- | --- | --- | --- |
| リポジトリ共通指示 | リポジトリ全体の常時ルール | 自動 | `.github/copilot-instructions.md` |
| パス別指示 | 特定ファイルの常時ルール | `applyTo`に一致すると自動 | `.github/instructions/` |
| エージェント | 誰が、どの権限で担当するか | 選択またはプロンプトから指定 | `.github/agents/` |
| プロンプト | 何の作業をどう実行するか | `/プロンプト名`で明示実行 | `.github/prompts/` |
| スキル | 複数作業で再利用する専門手順 | タスクに応じて自動または明示 | `.github/skills/` |
| `AGENTS.md` | 複数のAIエージェントで共有する作業規範 | 対応エージェントが自動参照 | `AGENTS.md` |

基本的には、常時守る内容を指示ファイルへ、担当者と権限をエージェントへ、反復する依頼をプロンプトへ、複数の担当や依頼で共有する専門手順をスキルへ置きます。

## 2. エージェント一覧

| エージェント | 主な用途 | 編集 | コマンド |
| --- | --- | --- | --- |
| 実装 | 機能実装、修正、リファクタリング | 可 | 可 |
| コードレビュー | コードレビュー | 不可 | 不可 |
| HCDリサーチ | 調査計画、アンケート、ペルソナ | 可 | 不可 |
| UX設計 | 要求、情報設計、UI、ユーザビリティ | 可 | 不可 |
| データ可視化 | 分析、可視化、Streamlit | 可 | 可 |
| アクセシビリティ | WCAG観点のレビュー | 不可 | 不可 |
| テスト品質 | テスト設計・実装、リリース判定 | 可 | 可 |

## 3. エージェント詳細

### 3.1 実装

定義: [implementation.agent.md](../../.github/agents/implementation.agent.md)

- 使用時期: 仕様と受け入れ条件が決まり、コードを変更するとき
- 必要な入力: 期待する結果、対象範囲、制約、受け入れ条件
- 実行内容: 関連コードの調査、最小変更、テスト、文書更新、検証
- 成果物: 実装コード、テスト、更新文書、検証結果
- 注意点: 大規模整理は自動的に行わず、依頼達成に必要な範囲へ限定する
- 主なプロンプト: `/implement-change`、`/debug-issue`、`/refactor-code`

### 3.2 コードレビュー

定義: [code-review.agent.md](../../.github/agents/code-review.agent.md)

- 使用時期: 実装後またはPR前に欠陥と回帰リスクを確認するとき
- 必要な入力: 差分、対象ファイル、要件、期待動作
- 実行内容: 正確性、セキュリティ、保守性、テスト、文書の読み取りレビュー
- 成果物: 重要度、証拠、影響、修正案を含む指摘
- 注意点: 読み取り専用。レビュー中にファイルを変更しない
- 主なプロンプト: `/review-code`

### 3.3 HCDリサーチ

定義: [hcd-research.agent.md](../../.github/agents/hcd-research.agent.md)

- 使用時期: ユーザーや課題の理解、調査、ペルソナ、JTBDを扱うとき
- 必要な入力: 調査判断、対象者、既知の証拠、制約
- 実行内容: 調査設計、倫理・個人情報確認、証拠の統合、要求への接続
- 成果物: 調査計画、アンケート、ペルソナ、JTBD
- 注意点: 回答、引用、参加者、結果を創作しない。仮説は明示する
- 主なプロンプト: `/research-plan`、`/design-survey`、`/create-persona`

### 3.4 UX設計

定義: [ux-design.agent.md](../../.github/agents/ux-design.agent.md)

- 使用時期: ユーザー要求を構造、フロー、画面、状態へ変換するとき
- 必要な入力: 対象ユーザー、タスク、要求、制約、証拠
- 実行内容: ジャーニー、要求、情報設計、プロトタイプ、専門家レビュー
- 成果物: フロー、サイトマップ、画面仕様、評価指摘
- 注意点: 見た目よりもタスク達成と状態設計を優先する
- 主なプロンプト: `/define-requirements`、`/prototype-ui`、`/usability-review`

### 3.5 データ可視化

定義: [data-visualization.agent.md](../../.github/agents/data-visualization.agent.md)

- 使用時期: データ調査、グラフ選定、ダッシュボード、Streamlit試作
- 必要な入力: データ、ユーザーの問い、意思決定、利用状況
- 実行内容: 品質確認、集計定義、可視化比較、実装、値の検証
- 成果物: 分析計画、可視化仕様、Streamlitアプリ
- 注意点: 見栄えからグラフを選ばず、欠損・集計・不確実性を明記する
- 主なプロンプト: `/analyze-data`、`/design-visualization`、`/prototype-streamlit`

### 3.6 アクセシビリティ

定義: [accessibility.agent.md](../../.github/agents/accessibility.agent.md)

- 使用時期: UIのアクセシビリティ障壁を確認するとき
- 必要な入力: 対象ページ、コンポーネント、主要タスク、利用技術
- 実行内容: セマンティクス、キーボード、フォーカス、名前、エラー、視認性のレビュー
- 成果物: 重要度、影響、WCAG基準、修正案、確認方法を含む指摘
- 注意点: 読み取り専用。自動検査やコード確認だけで準拠を断定しない
- 主なプロンプト: `/accessibility-review`

### 3.7 テスト品質

定義: [test-quality.agent.md](../../.github/agents/test-quality.agent.md)

- 使用時期: テスト追加、品質リスク整理、リリース判定
- 必要な入力: 変更動作、受け入れ条件、対象環境、リスク
- 実行内容: リスクベースのテスト設計、実装、実行、未検証範囲の整理
- 成果物: テストコード、テストマトリクス、リリース判定
- 注意点: 実装詳細ではなく外部から観察できる動作を優先する
- 主なプロンプト: `/write-tests`、`/release-readiness`

## 4. スキル一覧

| スキル | 専門領域 | 主な利用場面 |
| --- | --- | --- |
| hcd-workflow | HCDの計画から評価まで | 調査、要求、設計、評価 |
| data-visualization | データ品質と可視化選定 | 分析、ダッシュボード、Streamlit |
| accessible-ui | アクセシブルなUI | 設計、実装、レビュー |

## 5. スキル詳細

### 5.1 hcd-workflow

定義: [hcd-workflow/SKILL.md](../../.github/skills/hcd-workflow/SKILL.md)

調査の目的と意思決定を定義し、利用状況の把握、証拠の統合、要求定義、設計、評価までを一つの循環として扱います。特に、観察事実・解釈・仮定・決定を分離し、ペルソナや要求を証拠へ追跡できるようにします。

利用例:

```text
/hcd-workflowスキルを使用して、このダッシュボードの調査を計画してください。
```

### 5.2 data-visualization

定義: [data-visualization/SKILL.md](../../.github/skills/data-visualization/SKILL.md)

ユーザーの問いと意思決定から出発し、データ品質、粒度、指標、次元、欠損、不確実性を確認したうえで視覚表現を選びます。チャートの見栄えではなく、分析目的、誤読防止、アクセシビリティ、値の検証を重視します。

### 5.3 accessible-ui

定義: [accessible-ui/SKILL.md](../../.github/skills/accessible-ui/SKILL.md)

セマンティックHTML、キーボード操作、フォーカス、ラベル、状態通知、エラー、リフロー、コントラスト、動き、ターゲットサイズを一連の手順で確認します。自動テストだけに依存せず、手動確認項目を残します。

## 6. プロンプト一覧

| 工程 | プロンプト | 担当エージェント | 主な成果物 |
| --- | --- | --- | --- |
| 導入 | `/setup-copilot-context` | 実装 | プロジェクト情報 |
| 実装 | `/implement-change` | 実装 | コード、テスト、文書 |
| 品質 | `/write-tests` | テスト品質 | テスト |
| 品質 | `/review-code` | コードレビュー | レビュー指摘 |
| 分析 | `/analyze-data` | データ可視化 | 分析計画・品質報告 |
| 試作 | `/prototype-streamlit` | データ可視化 | Streamlitアプリ |
| 可視化 | `/design-visualization` | データ可視化 | 可視化仕様 |
| 発見 | `/hcd-discovery` | HCDリサーチ | 発見事項の概要 |
| 調査 | `/research-plan` | HCDリサーチ | 調査計画 |
| 調査 | `/design-survey` | HCDリサーチ | 調査票 |
| 調査 | `/analyze-survey` | データ可視化 | 分析結果 |
| 統合 | `/create-persona` | HCDリサーチ | ペルソナ |
| 統合 | `/define-jtbd` | HCDリサーチ | JTBD |
| 統合 | `/map-user-journey` | UX設計 | ジャーニー |
| 要求 | `/define-requirements` | UX設計 | 要求一覧 |
| 設計 | `/design-information-architecture` | UX設計 | 情報構造・サイトマップ |
| 設計 | `/prototype-ui` | UX設計 | UIプロトタイプ |
| 評価 | `/usability-test-plan` | HCDリサーチ | テスト計画 |
| 評価 | `/usability-review` | UX設計 | UX指摘 |
| 評価 | `/accessibility-review` | アクセシビリティ | アクセシビリティ指摘 |
| 改善 | `/implement-accessibility-fixes` | 実装 | 修正・テスト |
| 保守 | `/refactor-code` | 実装 | リファクタリング |
| 障害 | `/debug-issue` | 実装 | 原因・修正・回帰テスト |
| 文書 | `/document-feature` | 実装 | 利用文書 |
| リリース | `/release-readiness` | テスト品質 | リリース判定 |

## 7. プロンプト詳細

### 導入・実装・品質

#### `/setup-copilot-context`

- 使用時期: 導入直後、またはプロジェクト構成が大きく変わったとき
- 入力: 目的、既知の制約、分かっているコマンド
- 処理: リポジトリを調べ、確認できる事実だけをプロジェクト文脈へ記録
- 成果物: `docs/templates/project-context.md`
- 次: 目的に応じた各プロンプト

#### `/implement-change`

- 使用時期: 受け入れ条件がある機能追加・変更
- 入力: 結果、範囲、制約、受け入れ条件
- 処理: 調査、最小実装、テスト、文書、検証
- 成果物: 実装一式と検証報告
- 次: `/review-code`または`/release-readiness`

#### `/write-tests`

- 使用時期: 変更部分のテスト不足を補うとき
- 入力: 対象動作、バグ、要件
- 処理: リスク整理、正常・境界・異常・復旧のテスト
- 成果物: テストコードと未検証範囲
- 次: `/review-code`

#### `/review-code`

- 使用時期: 実装後、PR前
- 入力: 差分、ファイル、要件
- 処理: 読み取り専用レビュー
- 成果物: 重要度付き指摘
- 次: 指摘を`/implement-change`へ渡す

### データ分析・可視化

#### `/analyze-data`

- 使用時期: データを初めて扱うとき
- 入力: データパス、問い、意思決定
- 処理: スキーマ、粒度、欠損、重複、範囲、品質、分析案
- 成果物: 再現可能な分析計画
- 次: `/design-visualization`または`/prototype-streamlit`

#### `/prototype-streamlit`

- 使用時期: 短期間で動く可視化を作るとき
- 入力: データ、問い、操作、制約
- 処理: 読込・変換・表示を分離してアプリ化
- 成果物: Streamlitアプリ、テスト、起動方法
- 次: `/write-tests`、必要ならHCD工程

#### `/design-visualization`

- 使用時期: 表現方法を比較して決めるとき
- 入力: ユーザー、問い、データ、利用状況
- 処理: グラフ候補比較、エンコーディング、操作、誤読、A11y
- 成果物: `visualization-spec.md`
- 次: `/prototype-ui`または`/prototype-streamlit`

### HCD・リサーチ

#### `/hcd-discovery`

- 使用時期: 設計前に問題空間を整理するとき
- 入力: アイデア、対象者、既知の証拠、制約
- 処理: ユーザー、目標、状況、仮定、リスク、未知事項の整理
- 成果物: 発見事項の概要と次の調査提案
- 次: `/research-plan`または`/define-requirements`

#### `/research-plan`

- 使用時期: インタビュー、観察、アンケートなどを計画するとき
- 入力: 支援する意思決定、対象者、期間、制約
- 処理: 問い、方法、参加者、手順、倫理、分析、判断基準
- 成果物: `research-plan.md`
- 次: `/design-survey`または実査

#### `/design-survey`

- 使用時期: アンケートを作成・改善するとき
- 入力: 調査目的、回答者、判断、制約
- 処理: 目的と質問・尺度・分析の対応付け、バイアス確認
- 成果物: `survey.md`
- 次: パイロット、実査、`/analyze-survey`

#### `/analyze-survey`

- 使用時期: 回答データを受領したとき
- 入力: 回答、調査票、問い、セグメント
- 処理: 除外、欠損、再符号化、分母、記述分析、限界
- 成果物: 根拠付き結果
- 次: `/create-persona`または`/define-requirements`

#### `/create-persona`

- 使用時期: 行動差を設計判断に利用するとき
- 入力: 調査結果、セグメント、行動、目標
- 処理: 根拠追跡、ニーズ、障壁、状況、設計示唆
- 成果物: `persona.md`
- 次: `/define-jtbd`、`/map-user-journey`

#### `/define-jtbd`

- 使用時期: ユーザーが求める進歩を解決策から切り離して表現するとき
- 入力: 証拠、きっかけ、現在行動、望む結果
- 処理: 機能的・感情的・社会的なジョブの整理
- 成果物: 優先度と根拠付きJTBD
- 次: `/define-requirements`

#### `/map-user-journey`

- 使用時期: 複数段階・接点にまたがる体験を整理するとき
- 入力: ユーザー、シナリオ、開始・終了、証拠
- 処理: 目標、行動、接点、感情、課題、機会の整理
- 成果物: `user-journey.md`
- 次: `/define-requirements`

### 要求・設計・評価

#### `/define-requirements`

- 使用時期: 調査結果を実装可能な条件へ変換するとき
- 入力: 証拠、事業目標、制約、リリース
- 処理: ID、根拠、優先度、受け入れ条件の付与
- 成果物: `requirements.md`
- 次: 各設計プロンプト

#### `/design-information-architecture`

- 使用時期: 内容、機能、ナビゲーションを整理するとき
- 入力: コンテンツ、主要タスク、ユーザー、制約
- 処理: 階層、ラベル、ナビゲーション、検索・絞り込み
- 成果物: IAと検証計画
- 次: `/prototype-ui`

#### `/prototype-ui`

- 使用時期: 評価可能な画面・操作を作るとき
- 入力: 主要タスク、要求、忠実度、技術
- 処理: フロー、通常・例外状態、アクセシブルな構造
- 成果物: プロトタイプ
- 次: `/usability-test-plan`

#### `/usability-test-plan`

- 使用時期: 代表ユーザーによる評価を準備するとき
- 入力: プロトタイプ、対象者、問い、制約
- 処理: 中立的タスク、測定、進行、同意、分析
- 成果物: `usability-test-plan.md`
- 次: 実査、改善

#### `/usability-review`

- 使用時期: ユーザーテスト前後の専門家評価
- 入力: 画面・フロー、対象者、主要タスク
- 処理: 状態可視性、言葉、制御、整合性、エラー、認知負荷
- 成果物: 重要度付きUX指摘
- 注意点: ユーザー調査の代替ではない

#### `/accessibility-review`

- 使用時期: UI実装またはプロトタイプの障壁確認
- 入力: ページ、フロー、コンポーネント
- 処理: WCAG 2.2 AAを中心とした読み取りレビュー
- 成果物: A11y指摘と手動確認項目
- 次: `/implement-accessibility-fixes`

#### `/implement-accessibility-fixes`

- 使用時期: 確認済みA11y指摘を修正するとき
- 入力: 指摘、対象、優先度
- 処理: セマンティクス中心の修正と回帰テスト
- 成果物: 修正コード、テスト、未確認項目
- 次: 再レビューと手動確認

### 保守・リリース

#### `/refactor-code`

- 使用時期: 外部動作を変えず構造を改善するとき
- 入力: 対象、問題、維持する動作
- 処理: 不変条件の定義、保護テスト、限定的な整理
- 成果物: リファクタリングと同等性の証拠

#### `/debug-issue`

- 使用時期: 再現可能またはログのある障害
- 入力: 症状、期待、再現、ログ、環境
- 処理: 事実と仮説の分離、根本原因、回帰テスト、最小修正
- 成果物: 原因、修正、検証結果

#### `/document-feature`

- 使用時期: 機能や手順を利用者向けに文書化するとき
- 入力: 機能、読者、前提、保存場所
- 処理: 実装確認、目的志向の説明、例、制約、トラブル対応
- 成果物: READMEまたは`docs/how-to/`の文書

#### `/release-readiness`

- 使用時期: リリース前の最終判断
- 入力: 範囲、要求、環境、期限
- 処理: テスト、ビルド、設定、移行、監視、ロールバック、UX、A11y、文書
- 成果物: 準備完了 / 条件付きで準備完了 / 準備未完了の判定

## 8. 代表的な組み合わせ

### 実装修正

```text
/implement-change → /write-tests → /review-code → /release-readiness
```

### Streamlit簡易試作

```text
/analyze-data → /prototype-streamlit → /write-tests
```

### HCD可視化

```text
/hcd-discovery → /define-requirements → /design-visualization
→ /prototype-ui → /usability-review → /accessibility-review
```

### 調査から開始

```text
/research-plan → /design-survey → 実査 → /analyze-survey
→ /create-persona → /define-jtbd → /define-requirements
```

## 9. 保守ルール

- 同じ指示をエージェント、プロンプト、スキルへ重複して書かない
- エージェントの権限は必要最小限にする
- プロンプトは一つの明確な成果物を中心にする
- スキルの`description`には、何ができるかだけでなく、いつ使うかを書く
- ファイル名を変更したら、文書・プロンプト・検証スクリプトの参照も更新する
- 追加・変更後は検証スクリプトを実行する
