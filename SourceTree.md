# SourceTree
SourceTree使用教學

下載網址 https://www.sourcetreeapp.com/

Sourcetree 的 GUI 管理界面，可以在 Sourcetree 內看完整的分支線圖，或在本地端修改的檔案 Commit 到分支上，也能完成在節點加上標籤。

---
 Git 的基本知識
![git圖片](https://static.coderbridge.com/img/techbridge/images/kdchang/cs101/git-workflow.png)
```
Git 可以分為 Local（本地）和 Remote（遠端）兩個環境，。在 Local 中我們又分為 working directory（工作資料夾）、staging area（暫存區）和 repositories（檔案庫）。
```
1. 安裝git https://git-scm.com/
2. 開啟github/gitlab複製clone，建立一個本機的 repository
3. 開啟cmd，cd到本地資料夾
        
        git init
4. 檢視狀態、新增、上傳或修改 commits
        
        git add . / git add main.py
        git commit -m "輸入內容"
        git push
        git status
---
`創git時要創建.gitignore檔`

---
Git 術語及中英文對照
https://www.itread01.com/content/1543581242.html

---
<font color=#A8DDCD> //比較現在檔案和上次 commit 之間的差異</font>


`git diff`

<font color=#A8DDCD>// 檔案尚未加入過追蹤時使用，即可恢復到檔案尚未加入暫存區</font>

`git rm --cached hello.py`

---
在 Github 或 Gitlab 中已經有專案，可直接從遠端 clone 到 Sourcetree 中。

如果要在本地端建立分支，只需要按下 [Branch] 鈕，並按下 [Create Branch]。

分支合併（Branch merge）
Git 的好處在於開發不同功能時，能夠使用不同的分支，當該功能開發完成而且要出版時，可以透過合併的方式，將完善的功能合併到主分支，甚至可以透過選擇分支的節點來合併，不一定要到最新的功能。
在 Sourcetree 中，只需要在想要合併的分支按下 [Merge] 便可以達成分支合併。

![git圖片](https://miro.medium.com/max/1050/1*49hwcb_VGayJa9rWHbr2PQ.png)
