# GitHub Copilot HCDカスタマイズテンプレート

GitHub Copilotを、簡易的なデータ可視化からHCD（人間中心設計）に基づく調査・設計・実装・評価まで一貫して活用するためのリポジトリテンプレートです。

## できること

- Streamlitによるデータ分析・可視化アプリの素早い試作
- 課題・対象ユーザー・利用状況を踏まえた可視化設計
- 調査計画、アンケート、ペルソナ、JTBD、要求定義
- Python、Streamlit、React、TypeScriptの実装とテスト
- ユーザビリティ、アクセシビリティ、コード品質のレビュー

## 構成

```text
.
├── .github/
│   ├── copilot-instructions.md      # リポジトリ全体の常時ルール
│   ├── agents/                      # 7種類の専門エージェント
│   ├── instructions/                # ファイル種別ごとの常時ルール
│   ├── prompts/                     # 25種類の明示実行プロンプト
│   └── skills/                      # 3種類の再利用可能な専門スキル
├── .vscode/
│   └── settings.json                # プロンプトと指示ファイルを有効化
├── docs/
│   ├── how-to/                      # 導入・ユースケース・HCD手順
│   ├── reference/                   # 全カスタマイズの仕様
│   └── templates/                   # 調査・設計成果物の雛形
├── scripts/
│   └── validate_copilot_customizations.py
└── README.md
```

## 導入

1. このZIPを展開します。
2. 中身を対象リポジトリのルートへコピーします。
3. `docs/templates/project-context.md`を記入します。
4. 設定を検証します。

```bash
python scripts/validate_copilot_customizations.py --strict
```

5. VS Codeで対象リポジトリを開き、Copilot Chatで`/setup-copilot-context`を実行します。

既存プロジェクトへ導入する場合、`.vscode/settings.json`は上書きせず、必要な設定だけを既存ファイルへ統合してください。

## 目的別の開始方法

| 目的 | 最初に使うプロンプト | 主な流れ |
| --- | --- | --- |
| Streamlitで素早く試作 | `/analyze-data` | analyze-data → prototype-streamlit → write-tests |
| HCDに基づき可視化を設計 | `/hcd-discovery` | hcd-discovery → design-visualization → prototype-ui → usability-review |
| 調査・ペルソナから開始 | `/research-plan` | research-plan → design-survey → analyze-survey → create-persona → define-requirements |
| 既存機能を実装・変更 | `/implement-change` | implement-change → write-tests → review-code |
| 品質を評価 | `/usability-review` | usability-review → accessibility-review → release-readiness |

詳しい選び方は[ユースケースガイド](docs/how-to/use-cases.md)を参照してください。

## ドキュメント

- [クイックスタート](docs/how-to/quickstart.md)
- [3つのユースケース](docs/how-to/use-cases.md)
- [HCD・UI/UXワークフロー](docs/how-to/hcd-uiux-workflow.md)
- [エージェント・スキル・プロンプトのカスタマイズガイド](docs/reference/customizations.md)
- [成果物テンプレート一覧](docs/templates/README.md)

## 収録内容

- エージェント: 7種類
- スキル: 3種類
- プロンプト: 25種類
- パス別指示ファイル: 4種類
- HCD・UX成果物テンプレート: 8種類
- 依存パッケージ不要の検証スクリプト

## カスタマイズ時の原則

- プロジェクト固有の常時ルールは`.github/copilot-instructions.md`へ記載します。
- 特定ファイルだけに適用するルールは`.github/instructions/`へ追加します。
- 繰り返し呼び出す作業は`.github/prompts/`へ追加します。
- 専門的な役割や権限を分離するときは`.github/agents/`へ追加します。
- 複数のエージェント・プロンプトで再利用する手順は`.github/skills/`へ追加します。
- 同じルールを複数箇所へ重複させず、参照先を一つに保ちます。

## 注意

- プロンプトファイルは主に対応IDEから明示実行する機能です。
- エージェントやスキルの利用可否は、Copilotプラン、組織ポリシー、IDEのバージョンにより異なります。
- エージェントの`tools`は最小権限を基本とし、レビュー担当には編集権限を与えていません。
- テンプレート内の`[要確認]`は導入先の情報に置き換えてください。

## 日本語表記の方針

人が読む説明、見出し、入力例、テンプレート、検証メッセージは日本語で統一しています。一方、GitHub CopilotやVS Codeが識別するファイル名、YAMLキー、`tools`の値、スラッシュコマンド名、プログラムの識別子は、互換性と保守性を維持するため仕様どおりの英語表記を使用します。
