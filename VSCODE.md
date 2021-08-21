# VSCODE使用教學
下載網址 https://code.visualstudio.com/

---
VS Code編輯器上主要分成三個區塊，左邊是快速功能鈕，藍色框是快速功能鈕的顯示區，右邊綠色框是Python程式分頁的顯示區。

活動列 (Activity Bar)
預設會有 5 個 Activity 按鈕，
* 檔案總管 (Explorer)：可以在這裡管理所有的檔案及資料夾。
* 搜尋：針對全部的檔案的內容搜尋。
* 原始檔控制：使用 Git 做版本控制。
* 偵錯：編輯器少有的偵錯工具，必須安裝相對應的偵錯工具才能在該程式語言使用。
* 擴充工具：可以直接尋找想用的擴充工具，非常方便。
![VSCODE畫面](https://i2.wp.com/image.walker-a.com/2020/06/py01/py01-02.jpg?ssl=1)

點選紅色框鈕即可將快速功能顯示區隱藏起來，這樣可以讓程式分頁的區域變得更大。
![VSCODE畫面](https://i1.wp.com/image.walker-a.com/2020/06/py01/py01-04.jpg?ssl=1)

一般開發都是以資料夾視為一個專案的管理，所以先開啟檔案總管建立一個的資料夾，例如在C磁碟根目錄下建立python資料夾。
![VSCODE畫面](https://i2.wp.com/image.walker-a.com/2020/06/py01/py01-05.jpg?ssl=1)

直接按下【Ctrl+、】即可開啟終端機畫面(有用git要改開啟git bash畫面)
![VSCODE畫面](https://i1.wp.com/image.walker-a.com/2020/06/py01/py01-07-6.jpg?ssl=1)

如果Visual Studio Code在右下出現延伸模式安裝訊息，全部都案確定下載
```
套件下載(vscode內)
    1. Git Graph
    2. GitLens
    3. Material Icon Theme
```
![VSCODE畫面](https://i0.wp.com/image.walker-a.com/2020/06/python/py-37.jpg?ssl=1)

---
## 工作區 Workspace

如果說專案是檔案及子資料夾的集合體，那工作區就是專案 (主資料夾) 的集合體；一個工作區預設會有一個專案，這時可以將工作區視同為該專案，但是，你也可以在一個工作區中加入多個專案，這時 VS Code 的檔案總管的顯示方式會調整為顯示工作區的名稱及其下包含的專案名稱：
![VSCODE畫面](https://4.bp.blogspot.com/-2B79elXTFIY/W-GHD4Kr0wI/AAAAAAAAF-s/558Yzgdt7cUB_WFCSvvO2XrsOLaDh-0aQCLcBGAs/s1600/workspace-1.png)
圖 1 ：工作區中只有一個專案
![VSCODE畫面](https://1.bp.blogspot.com/-jvrd20lI0r0/W-GHEAk9M4I/AAAAAAAAF-w/ZWbtKLx9rFA5E8uBI_e23dMElmG0jAIEACLcBGAs/s1600/workspace-2.png)
圖 2 ：工作區中有兩個專案

當只有一個專案存在工作區中，該專案資料夾的名稱預設就是工作區的名稱；但是當一個工作區存在兩個以上的專案時，工作區名稱預設為「未命名」，你可以在選單中：檔案 > 另存工作區為... 來儲存該工作區。

建議的作法是只將有相關性的專案放在同一個工作區，否則最好保持一個工作區只有單個專案就好。因為一個專案就是一個主資料夾，如果日後想要移動專案到別的目錄下，只要將該主資料夾移動過去，然後用 VS Code 開啟該資料夾即可。

---
## 偵錯

要使用偵錯功能必須先安裝相關的擴充工具，然後建立組態檔，檔案會在 .vscode/launch.json，內容如下：
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/index.js"
        }
    ]
}
```
組態檔設定完成後，就可以在偵錯側選單內按下綠色執行鈕，結果會顯示在「偵錯主控台」面板。

---
ctrl+shift+p 快捷鍵大全