import numpy as np
from collections import Counter

class BTLModel:
    def __init__(self, num_items):
        self.num_items = num_items
        self.estimates = np.ones(num_items, dtype=np.float64) / num_items  # 初始化每個項目的勝率估計值

    def maximize_log_likelihood(self, mat, max_iters=20, err_tol=1e-3):
        num_games = Counter() # 計算每個項目之間的比賽次數
        for i in range(self.num_items):
            for j in range(i + 1, self.num_items):
                total = mat[i][j] + mat[j][i]
                if total > 0:
                    num_games[(i, j)] = total 
                    
        
        for _ in range(max_iters): # 迭代更新勝率估計值
            old_estimates = self.estimates.copy() # 複製舊的勝率估計值
            for i in range(self.num_items):
                denom = sum(num_games[tuple(sorted([i, j]))] / (self.estimates[i] + self.estimates[j]) for j in range(self.num_items) if i != j)
                self.estimates[i] = 1.0 * sum(mat[i][j] for j in range(self.num_items) if i != j) / denom if denom > 0 else 0
                
            norm = np.linalg.norm(self.estimates)
            self.estimates /= norm

            if np.sum(np.abs(self.estimates - old_estimates)) < err_tol:
                print('Converged after', _ + 1, 'iterations')
                break
        # print('Final estimates:', (self.estimates * 100).round(2))

    def get_estimates(self):
        self.estimates *= 100
        return self.estimates