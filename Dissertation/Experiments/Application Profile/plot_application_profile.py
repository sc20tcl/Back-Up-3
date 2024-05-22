import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

file_path = 'selected_replicas.csv'
data = pd.read_csv(file_path)


X = data['queries per second rate'].values.reshape(-1, 1)
y = data['replicas'].values

degree = 2
poly = PolynomialFeatures(degree)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)

y_poly_pred = model.predict(X_poly)

coefficients = model.coef_
intercept = model.intercept_

def optimum_pod_count(qps):
    return intercept + sum(c * (qps ** i) for i, c in enumerate(coefficients))

plt.figure(figsize=(10, 6))
plt.scatter(data['queries per second rate'], data['replicas'], color='blue', label='Observed data')
plt.plot(data['queries per second rate'], y_poly_pred, color='red', label='Fitted polynomial curve')
plt.xlabel('Queries per Second Rate')
plt.ylabel('Optimum Pod Count')
plt.title('Polynomial Relationship between Queries per Second Rate and Optimum Pod Count')
plt.legend()
plt.grid(True)


print("Polynomial formula:")
print(f"P = {intercept:.2f} ", end="")
for i, c in enumerate(coefficients[1:], 1):
    print(f"+ {c:.8f} * Q^{i} ", end="")
print()

plt.show()