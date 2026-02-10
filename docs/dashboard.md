Dashboard Specification: HR Analytics

Index name: workers_matveeva
Dashboard name: dashboard_matveeva

Visualizations
--------------

1. salary_by_lastname_matveeva
   Type: Vertical Bar Chart
   Description: Average salary by top employee surnames
   X-axis: Surname (Фамилия.keyword)
   Y-axis: Average salary (Average of Зарплата)

2. employees_by_city_treemap_matveeva
   Type: Treemap
   Description: Employee distribution by city. Rectangle size proportional to employee count.
   Group by: City (Top values, Город)
   Metric: Count

3. avg_salary_matveeva
   Type: Metric
   Description: Overall average salary across all employees in dataset
   Metric: Average salary (Average of Зарплата)

4. height_distribution_by_value_bar_matveeva
   Type: Horizontal Bar Chart
   Description: Employee count per unique height value
   Y-axis: Height (Рост)
   X-axis: Count

Dataset statistics (workers_matveeva index)
--------------------------------------------
Total document count: 1 027
Salary range (after filtering): 50 000 – 200 000 RUB
Height range (after filtering): 161 – 190 cm
Average salary: 100 550 RUB
