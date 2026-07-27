# クイックスタート

## 1. コピー

ZIPを展開し、内容を対象リポジトリのルートへコピーします。既存の`.github`や`.vscode/settings.json`がある場合は、ファイル単位で統合してください。

## 2. 検証

```bash
python scripts/validate_copilot_customizations.py --strict
```

`エラー: 0件、警告: 0件`になれば、テンプレート自体の構造は正常です。

## 3. プロジェクト情報の登録

Copilot Chatで次を実行します。

```text
/setup-copilot-context
```

結果として`docs/templates/project-context.md`が更新されます。自動で確認できなかった`[要確認]`は、プロジェクト担当者が記入してください。

## 4. 最初のタスク

実装から始める場合:

```text
/implement-change ユーザーが達成したいこと、対象範囲、制約、受け入れ条件
```

Streamlit試作から始める場合:

```text
/analyze-data data/sample.csvを使い、月ごとの変化と異常値を確認したい
```

HCDから始める場合:

```text
/hcd-discovery 対象ユーザー、解決したい問題、既知の情報、事業上の制約
```

## 5. 結果の確認

Copilotの出力では、最低限次を確認します。

- 事実と仮定が分離されている
- 変更対象が依頼範囲に収まっている
- テストや検証の結果が記載されている
- 未確認事項や残存リスクが明示されている
- 調査結果、ユーザー発言、数値が創作されていない

## トラブルシューティング

### プロンプトが表示されない

- ファイルが`.github/prompts/*.prompt.md`にあるか確認します。
- VS CodeとGitHub Copilot拡張を更新します。
- `chat.promptFiles`が有効か確認します。
- VS Codeのコマンドパレットから`Chat: Open Customizations`を実行し、認識状態を確認します。

### エージェントが表示されない

- ファイルが`.github/agents/*.agent.md`にあるか確認します。
- YAMLフロントマターに`description`があるか確認します。
- 組織のCopilotポリシーでエージェントの利用が許可されているか確認します。

### スキルが自動で使われない

スキルは説明文とタスクの一致に基づいて選択されます。明示する場合は、プロンプト本文や依頼文でスキル名を指定してください。
