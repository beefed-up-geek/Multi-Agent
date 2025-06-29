# filename: plot_titanic_age_pclass.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 데이터 다운로드 및 읽기
url = "https://github.com/mwaskom/seaborn-data/raw/master/titanic.csv"
data = pd.read_csv(url)

# 2. 데이터셋의 열 출력
print(data.columns)

# 3. 'age'와 'pclass' 간의 관계 차트 생성
plt.figure(figsize=(10, 6))
sns.boxplot(x='pclass', y='age', data=data)
plt.title('Age vs Pclass')
plt.xlabel('Passenger Class')
plt.ylabel('Age')

# 4. 차트를 파일로 저장
plt.savefig('age_vs_pclass.png')
plt.close()