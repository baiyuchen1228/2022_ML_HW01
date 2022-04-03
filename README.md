# ML_HW01
PLA with pocket_algorithm

### I.	Execution description
rand_samples用一條線上的x範圍1到30對照的y圍一個範圍，從這範圍裡隨機挑點，再依照點的位置給標籤。

sign計算兩個向量的內積，等於a * x1 + b * x2 + c * 1，判斷在線的哪一邊。

PLA對每個錯誤的點都做調整。

pocket_algorithm先把每個點隨機排序，遇到錯誤的點去做調整，挑整完之後看準確度有沒有提升，如果有就保留這個挑整，沒有就找下一個錯誤的點。

第四題的地方把正負的各後50個變成另一邊的錯誤標籤。

### II.	Experimental results

1.m = -1, b = 5

 ![image](https://user-images.githubusercontent.com/71372497/161429303-7946ab9e-239c-468d-beec-6cb2e1edbca3.png)
 
1.m = 1, b = 3

 ![image](https://user-images.githubusercontent.com/71372497/161429304-40114f5f-6dc6-4991-a5c7-7a2e4f830a8d.png)
 ![image](https://user-images.githubusercontent.com/71372497/161429311-ac30833f-b1c5-43ef-b221-025f7dcc24ca.png)
 ![image](https://user-images.githubusercontent.com/71372497/161429319-aac44b84-0406-40e4-9450-8c7d074531b2.png)
 ![image](https://user-images.githubusercontent.com/71372497/161429322-1544cccc-09cf-46ec-ae9b-99cf71ed7657.png)
 
2.w0=[0,0,0],平均迭代次數是35次。

3.多了挑選的步驟時間大概多了10~30倍。

4.迭代800多次之後大概可以分開來。

### III.	Conclusion
原本以為多那一個步驟只會多一點時間，但實做出來比想像的久。雖然比較久但比較實用，如果沒有用pocket algorithm對第四題的資料做的話會完全分不出來，實際那麼多筆資料一定會有一些是標記錯誤的，所以這個演算法是很重要的。
### IV.	Discussion
對Python不太熟悉所以寫的時候一直查資料，其中一個找最久的bug是array的等號比較像是指標指過去，所以在改動的時候會連上一個都改，要用copy()才能複製一份。
