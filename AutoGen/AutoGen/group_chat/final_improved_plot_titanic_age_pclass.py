# filename: final_improved_plot_titanic_age_pclass.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 데이터 다운로드 및 읽기
url = "https://github.com/mwaskom/seaborn-data/raw/master/titanic.csv"
data = pd.read_csv(url)

# 2. 'age' 변수의 결측값을 중앙값으로 대체
data['age'] = data['age'].fillna(data['age'].median())

# 3. 데이터셋의 열 출력 (확인용)
print(data.columns)

# 4. 'age'와 'pclass' 간의 관계 차트 생성
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")
sns.boxplot(x='pclass', y='age', data=data, hue='class', palette='pastel', dodge=True)
plt.title('Age vs Passenger Class', fontsize=16, fontweight='bold')
plt.xlabel('Passenger Class', fontsize=14, fontweight='bold')
plt.ylabel('Age', fontsize=14, fontweight='bold')

# 주석 추가
plt.text(0, 30, 'Class 1 Average', fontsize=12, color='black', ha='center')
plt.text(1, 28, 'Class 2 Average', fontsize=12, color='black', ha='center')
plt.text(2, 26, 'Class 3 Average', fontsize=12, color='black', ha='center')

# 5. 차트를 파일로 저장
plt.savefig('final_improved_age_vs_pclass.png')
plt.close()