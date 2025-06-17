import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sqlite3
from scipy.stats import ttest_ind
import scipy.stats as stats
warnings.filterwarnings("ignore")

# Creating the database connection
conn = sqlite3.connect('inventory.db')

#fethcing vendor summary data
df = pd.read_sql_query("SELECT * FROM final_summary_table", conn)
print(df.head())


"""
Exploratory Data Analysis

Earlier, we reviewed the database tables to pinpoint important variables, explore their relationships, and decide which ones to include in the final analysis.

In this stage of EDA, we will examine the resulting table to understand the distribution of each column. This will help us detect patterns, spot any anomalies, and ensure the data is accurate before moving on to deeper analysis.

"""

# Summary statistics of the data
summary_stats = df.describe().T
print("Summary Statistics:")
print(summary_stats)

# Distribution Plots for Numerical Columns
numerical_columns = df.select_dtypes(include=np.number).columns 

plt.figure(figsize=(15, 10))
for i , col in enumerate(numerical_columns):
    plt.subplot(4, 4, i + 1) # Grid of 4 rows and 4 columns
    sns.histplot(df[col], kde=True, bins=30)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


# Distribution Plots for Numerical Columns using boxplots


plt.figure(figsize=(15, 10))
for i , col in enumerate(numerical_columns):
    plt.subplot(4, 4, i + 1) # Grid of 4 rows and 4 columns
    sns.boxplot(df[col])
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


"""
Negative & Zero Values:

Gross Profit: The minimum value is -52,002.78, suggesting losses. This may happen when products are sold at a loss—either due to high costs or being sold at a discount below the purchase price.

Profit Margin: The margin goes as low as negative infinity, indicating scenarios where there’s no revenue or it's even less than the cost.

Total Sales Quantity & Sales Dollars: These metrics have a minimum of 0, showing some products were purchased but never sold—possibly due to being outdated or very slow-moving.

Outliers Detected via High Standard Deviations:

Purchase & Actual Prices: The maximum values (5,681.81 and 7,499.99) are much higher than the average values (24.39 and 35.64), suggesting the presence of premium or exceptionally high-priced products.

Freight Cost: With a wide range from 0.09 to 257,032.07, this could indicate inefficiencies in shipping or very large bulk orders.

Stock Turnover: Varies between 0 to 274.5. Low values suggest products stay in stock a long time, while high values mean rapid turnover. A turnover greater than 1 may indicate sales being met using previously stocked inventory rather than new purchases.

"""



# Filtering data by removing the inconsistent values
df = pd.read_sql_query("""
SELECT *
FROM final_summary_table 
WHERE GrossProfit > 0
AND ProfitMargin > 0
AND TotalSalesQuantity > 0 """, conn)

print("Filtered Data:")
print(df)


# Frequency plots for Categorical Columns
categorical_columns = ['VendorName', 'Description']

plt.figure(figsize=(12, 5))
for i, col in enumerate(categorical_columns):
    plt.subplot(1, 2, i + 1)
    sns.countplot(y=df[col], order=df[col].value_counts().index[:10]) # Top 10 categories
    plt.title(f'Frequency of {col}')
plt.tight_layout()
plt.show()


# Correlation Heatmap
plt.figure(figsize=(12, 8))
correlation_matrix = df[numerical_columns].corr()
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()



"""

Rephrased Correlation Insights:
Purchase Price shows a weak negative correlation with both Total Sales Dollars (-0.012) and Gross Profit (-0.016), suggesting that changes in purchase price have minimal influence on revenue or profitability.

There is a very strong positive correlation (0.999) between Total Purchase Quantity and Total Sales Quantity, indicating a highly efficient inventory turnover process.

A negative correlation (-0.179) between Profit Margin and Total Sales Price implies that as sales prices rise, profit margins may shrink—possibly due to competitive pricing or cost increases.

Stock Turnover is weakly negatively correlated with both Gross Profit (-0.038) and Profit Margin (-0.055), which suggests that a faster inventory turnover doesn't necessarily lead to greater profitability.

"""


"""Data Analysis and Hypothesis Testing
Identify Brands that needs promotional or Pricing adjustments which exhibit lower sales performance but higher profit margins."""

brand_performance = df.groupby('Description').agg({
    'TotalSalesDollars': 'sum',
    'ProfitMargin': 'mean',
}).reset_index()

brand_performance = brand_performance[brand_performance['TotalSalesDollars']<10000]  # better visualization of  sales brands

low_sales_threshold = brand_performance['TotalSalesDollars'].quantile(0.15)
high_margin_threshold = brand_performance['ProfitMargin'].quantile(0.85)

print("Brands with Low Sales and High Profit Margin:")
low_sales_high_margin_brands = brand_performance[
    (brand_performance['TotalSalesDollars'] <= low_sales_threshold) &
    (brand_performance['ProfitMargin'] >= high_margin_threshold)
]
print(low_sales_high_margin_brands)

# Scatter plot to show the visualization of low sales and high profit margin brands
plt.figure(figsize=(10, 6))
sns.scatterplot(data=brand_performance,x='TotalSalesDollars', y='ProfitMargin', color='Purple', label='All Brands', alpha=0.2)
sns.scatterplot(data=low_sales_high_margin_brands, x='TotalSalesDollars', y='ProfitMargin', color='Red', label='Target Brands')

plt.axhline(high_margin_threshold, color='green', linestyle='--', label='High Margin Threshold')
plt.axvline(low_sales_threshold, color='green', linestyle='--', label='Low Sales Threshold')

plt.title('Brands for Promotional or Pricing Adjustments')
plt.xlabel('Total Sales Dollars ($)')
plt.ylabel('Profit Margin (%)')
plt.legend()
plt.grid(True)
plt.show()


""" Which vendors and brands have the highest sales performance and profitability? """


def format_dollars(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.2f}K"
    else:
        return f"${value:.2f}"

top_vendors = df.groupby('VendorName')["TotalSalesDollars"].sum().nlargest(10)

top_brands = df.groupby('Description')["TotalSalesDollars"].sum().nlargest(10)

print("Top 10 Vendors by Total Sales Dollars:")
print(top_vendors.apply(lambda x: format_dollars(x)))
print("\nTop 10 Brands by Total Sales Dollars:")
print(top_brands.apply(lambda x: format_dollars(x)))


# Bar plot for top vendors
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
ax1 = sns.barplot(y=top_vendors.index, x=top_vendors.values, palette='viridis')
plt.title('Top 10 Vendors by Total Sales Dollars')

for bar in ax1.patches:
    ax1.text(bar.get_width() + (bar.get_width() * 0.02),
             bar.get_y() + bar.get_height() / 2,
              format_dollars(bar.get_width()),
              va='center', ha='left', fontsize=10, color='blue')
    
# Bar plot for top brands
plt.subplot(1, 2, 2)
ax2 = sns.barplot(y=top_brands.index.astype(str), x=top_brands.values, palette='plasma')
plt.title('Top 10 Brands by Total Sales Dollars')

for bar in ax2.patches:
    ax2.text(bar.get_width() + (bar.get_width() * 0.02),
             bar.get_y() + bar.get_height() / 2 ,
              format_dollars(bar.get_width()),
              va='center', ha='left', fontsize=10, color='blue')

plt.tight_layout()
plt.show()


# Which vendors contribute the most to total purchase dollars?
vendor_performance  = df.groupby('VendorName').agg({
    'TotalPurchaseDollars': 'sum',
    'GrossProfit': 'sum',
    'TotalSalesDollars': 'sum'
}).reset_index()


vendor_performance['PurchaseContribution'] = vendor_performance['TotalPurchaseDollars'] / vendor_performance['TotalPurchaseDollars'].sum() * 100

print("Top 10 Vendor's Performance:")
top_vendors = vendor_performance.sort_values(by='TotalPurchaseDollars', ascending=False).head(10)
print(top_vendors)

print(top_vendors['PurchaseContribution'].sum())

top_vendors['Cumulative_Contri'] = top_vendors['PurchaseContribution'].cumsum()
print("Cumulative Purchase Contribution of Top 10 Vendors:")
print(top_vendors)


# Pareto Chart for Vendor Purchase Contribution
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar plot for Purchase Contribution
sns.barplot(x=top_vendors['VendorName'], y=top_vendors['PurchaseContribution'], palette ='mako', ax=ax1)

for i, value in enumerate(top_vendors['PurchaseContribution']):
    ax1.text(i, value - 1, str(value)+'%', ha='center', fontsize=10, color='blue')

# Line plot for Cumulative Contribution
ax2 = ax1.twinx()
ax2.plot(top_vendors['VendorName'], top_vendors['Cumulative_Contri'], color='red', marker='o', label='Cumulative Contribution', linewidth=2 , linestyle='--')

ax1.set_xticklabels(top_vendors['VendorName'], rotation=45)
ax1.set_ylabel('Purchase Contribution (%)' , color = 'red')
ax2.set_ylabel('Cumulative Contribution (%)', color='blue')
ax1.set_xlabel('Vendor Name')
ax1.set_title('Pareto Chart :Vendor Purchase Contribution and Cumulative Contribution')

ax2.axhline(y=100, color='gray', linestyle='--', alpha=0.7)
ax2.legend(loc='upper right')

plt.show()



# How much  total procurement cost is dependent on the top vendors?

print("Total Procurement Cost by top 10 Vendors:")
top_vendors_proc = round(top_vendors['PurchaseContribution'].sum(), 2)
print(f"Total Procurement Cost by top 10 Vendors: {top_vendors_proc}%")

# Donut chart for Vendor Procurement Cost Contribution

vendors = list(top_vendors['VendorName'].values)
purchase_contributions = list(top_vendors['PurchaseContribution'].values)
total_contribution = sum(purchase_contributions)
remaining_contribution = 100 - total_contribution

#Appen "Other Vendors" to the list
vendors.append('Other Vendors')
purchase_contributions.append(remaining_contribution)

#Donut chart
fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(purchase_contributions, labels=vendors, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel", len(vendors)))
ax.set_title('Vendor Procurement Cost Contribution')

centre_circle = plt.Circle((0, 0), 0.70, color='white')
fig.gca().add_artist(centre_circle)

#Add total contribution annotation in the center
plt.text(0,0, f'Total Contribution: {total_contribution:.2f}%',  ha='center',va = 'center', fontsize=14, color='black', fontweight='bold')

plt.title(' Top 10 Vendor Procurement Cost Contribution')
plt.show()



#Does purchasing in bulk reduce the unit price and what is the optimal purchase volume for cost savings?

df['UnitPrice'] = df['TotalPurchaseDollars'] / df['TotalPurchaseQuantity']

df["OrderSize"]=pd.qcut(df['TotalPurchaseQuantity'],
                        q=3, 
                        labels=['Small', 'Medium', 'Large'])

print(df[['OrderSize', 'UnitPrice']])

df.groupby('OrderSize')['UnitPrice'].mean().plot(kind='bar', color='skyblue', figsize=(10, 6))



plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="OrderSize", y="UnitPrice", palette="Set2")
plt.title('Unit Price by Order Size')
plt.xlabel('Order Size')
plt.ylabel('Unit Price ($)')
plt.grid(True)
plt.show()



"""
Vendors who place large orders benefit from significantly lower unit prices (as low as $10.78), which can lead to higher profit margins when inventory is managed effectively.

There is a notable cost advantage — around 72% reduction in unit price — when shifting from small to large order sizes.

This indicates that bulk pricing effectively motivates vendors to buy in larger quantities, resulting in increased total sales even though the revenue earned per unit is lower.

"""


# Which vendors have low inventory turnover and high stock levels, indicating potential overstocking or slow-moving inventory?

turnover = df[df['StockTurnover'] < 1].groupby('VendorName')[['StockTurnover']].mean().sort_values(by='StockTurnover', ascending=True).head(10)

print("Vendors with Low Inventory Turnover:")
print(turnover)

# How much capital is locked in unsold invenotry per vendor and which vendors contribute the most to it ?

df["UnsoldInventoryValue"] = (df["TotalPurchaseQuantity"] - df["TotalSalesQuantity"]) * df["PurchasePrice"]

print("Total Unsold Inventory Value :" , format_dollars(df["UnsoldInventoryValue"].sum()))


inventory_value_per_vendor = df.groupby('VendorName')['UnsoldInventoryValue'].sum().reset_index()

# Sort Vendors with the highest unsold inventory value
inventory_value_per_vendor = inventory_value_per_vendor.sort_values(by='UnsoldInventoryValue', ascending=False)
inventory_value_per_vendor['UnsoldInventoryValue'] = inventory_value_per_vendor['UnsoldInventoryValue'].apply(lambda x: format_dollars(x))
print("Unsold Inventory Value per Vendor:")
print(inventory_value_per_vendor.head(10))



top_threshold = df["TotalSalesDollars"].quantile(0.75)
bottom_threshold = df["TotalSalesDollars"].quantile(0.25)

top_vendors = df[df["TotalSalesDollars"] >= top_threshold]["ProfitMargin"].dropna()
bottom_vendors = df[df["TotalSalesDollars"] <= bottom_threshold]["ProfitMargin"].dropna()

print("Top Vendors Profit Margin:")
print(top_vendors)

print("Bottom Vendors Profit Margin:")
print(bottom_vendors)


def confidence_interval(data , confidence = 0.95):
    mean_val = np.mean(data)
    std_err = np.std(data, ddof = 1)/ np.sqrt(len(data)) #Std error
    t_critical = stats.t.ppf((1 + confidence) / 2 , df =len(data)-1)
    margin_of_error = t_critical * std_err
    return mean_val , mean_val - margin_of_error , mean_val + margin_of_error



top_mean , top_lower , top_upper = confidence_interval(top_vendors)
low_mean , low_lower , low_upper = confidence_interval(bottom_vendors)

print(f"Top vendors 95 % CI : ({top_lower:.2f},{top_upper:.2f},{top_mean:.2f})")

print(f"Low vendors 95 % CI : ({low_lower:.2f},{low_upper:.2f},{low_mean:.2f})")


plt.figure(figsize=(12,6))

#Top Vendors Plot

sns.histplot(top_vendors , kde = True , color = 'blue', bins = 30 , alpha =0.5, label = "Top vendors")
plt.axvline(top_lower, color="blue", linestyle="--", label=f"Top Lower: {top_lower:.2f}")
plt.axvline(top_upper, color="blue", linestyle="--", label=f"Top Upper: {top_upper:.2f}")
plt.axvline(top_mean, color="blue", linestyle="-", label=f"Top Mean: {top_mean:.2f}")

# Low Vendors Plot
sns.histplot(bottom_vendors, kde=True, color="red", bins=30, alpha=0.5, label="Low Vendors")
plt.axvline(low_lower, color="red", linestyle="--", label=f"Low Lower: {low_lower:.2f}")
plt.axvline(low_upper, color="red", linestyle="--", label=f"Low Upper: {low_upper:.2f}")
plt.axvline(low_mean, color="red", linestyle="-", label=f"Low Mean: {low_mean:.2f}")

# Finalize Plot
plt.title("Confidence Interval Comparison: Top vs. Low Vendors (Profit Margin)")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.show()




"""
The confidence range for low-performing vendors (40.48% to 42.62%) is much higher than that for top-performing vendors (30.74% to 31.61%).

This means vendors with fewer sales often have better profit margins, possibly because of higher product pricing or lower operating costs.

For top vendors: To increase profits, they can consider adjusting prices, reducing costs, or offering product bundles.

For low vendors: Even though they earn more per sale, their low sales numbers suggest they may need better marketing, more competitive pricing, or improved distribution methods.

"""





"""
Is there a significant difference in profit margins between top-performing and low-performing vendors?

Hypothesis:

H₀ (Null Hypothesis): There is no significant difference in the mean profit margins of top-performing and low-performing vendors.

H₁ (Alternative Hypothesis): The mean profit margins of top-performing and low-performing vendors are significantly different.

"""

# Perform Two-Sample Test
t_stat , p_value = ttest_ind(top_vendors , bottom_vendors , equal_var=False)

# Results
print(f"T-stats: {t_stat: .4f}, P-Value : {p_value: .4f}")

if p_value < 0.05 :
    print("Reject Ho: There is a significant diff in profit margins between top and low -performing vendors. ")
else:
    print("Fail to Reject HoL No significant difference in profit margin .")



