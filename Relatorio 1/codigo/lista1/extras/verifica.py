import numpy as np
A = np.array([[8,-4,-2],[-4,6,-2],[-2,-2,10]], float)
print([round(np.linalg.det(A[:k,:k]), 2) for k in (1, 2, 3)])
print(np.linalg.eigvalsh(A))