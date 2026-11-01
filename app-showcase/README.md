# Daisaku Seto - iOS Apps Showcase 📱✨

iOSデベロッパー **Daisaku Seto** のApp Store公開作品を美しく並べるモダンポートフォリオサイトです。

## 特徴
- 🎨 **Apple & Vercel風の洗練されたダークグラスモーフィズムデザイン**
- ⚡️ **GitHub Pages 完全対応**（単一の静的ファイルで依存関係なし、完全無料で全世界公開）
- 🔍 **リアルタイム検索 & カテゴリフィルター**（音楽、ツール、ゲーム、ライフスタイル）
- 📸 **スクリーンショットプレビューモーダル**（各アプリのスクショ・説明文・App Storeリンクをリッチ表示）
- 🤖 **自動更新スクリプト付き**（新しいアプリをリリースした時も、コマンド1つで即座に同期）

---

## 使い方・ローカルで確認する

今すぐMacのブラウザで開いて確認できます：

```bash
open index.html
```

---

## GitHub Pages で全世界に無料公開する手順（3分で完了！）

1. **GitHubで新しいリポジトリを作成**  
   - リポジトリ名例: `app-showcase` または `portfolio`  
   - （もし `ユーザー名.github.io` というリポジトリ名にすると、`https://ユーザー名.github.io` という最短URLになります）

2. **このフォルダをGitリポジトリにしてPushする**
   ```bash
   cd /Users/setodaisaku/Developer/app-showcase
   git init
   git add .
   git commit -m "Initial commit: iOS apps showcase"
   git branch -M main
   git remote add origin https://github.com/<あなたのユーザー名>/<リポジトリ名>.git
   git push -u origin main
   ```

3. **GitHub Pages を有効化**
   - GitHubのリポジトリページへ行き、**Settings** → **Pages** を開く
   - **Branch** を `main`、フォルダを `/ (root)` に設定して「Save」をクリック
   - 1〜2分待つと、全世界に公開されたURLが発行されます！🎉

---

## 新しいアプリをリリースしたときの更新方法

```bash
python3 generate.py
git commit -am "Update app showcase"
git push
```
これだけで最新のApp Store情報が自動反映されます。
