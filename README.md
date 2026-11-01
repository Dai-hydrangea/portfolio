# つくったもの棚 — D.Seto works

瀬戸大作（D.Seto）が公開している App Store アプリを、ジャンルごとの「池」に
浮かべて眺めるポートフォリオ。アイコンをタップすると詳細がせり上がります。

- Live: https://dai-hydrangea.github.io/portfolio/
- App Store: https://apps.apple.com/jp/developer/daisaku-seto/id1889853807
- note: https://note.com/daisaku_seto

## 構成
- `index.html` — 本体（単一HTML、依存なし）
- `data.js` — アプリ一覧（アイコン/スクショ/物語）。Apple lookup API から生成
- `raw.json` — 生成元の生データ（開発者ID 1889853807）

## データ更新
App Store を更新したら `raw.json` を取り直し、`data.js` を作り直す（Python スクリプトで生成）。
