import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib import ticker as mtick

st.set_page_config(page_title='APP', layout='wide')

plt.style.use('seaborn')
df = pd.read_csv('superstore.csv')
df["Sales"] = df["Sales"].apply(pd.to_numeric, errors='coerce').fillna(0.0)
df['Order Date'] = pd.to_datetime(df['Order Date'])
# df.iloc[df['Order Date'].sort_values().index,:]

for i in range(len(df)):
    df['Order Date'][i] = str(df['Order Date'][i].year) + '-' + str(df['Order Date'][i].month)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df = df.drop(columns=['Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Row ID'])
df = df.drop_duplicates()
df['Year'] = df['Order Date'].apply(lambda x: str(x)[0:4])

# df['Margin'] = df['Profit']/df['Sales']

def get_fig(*key):
    # categ = df.groupby(['Order Date', 'Ship Mode'])['Profit'].sum()
    if obj == 'Margin':
        categ = df.groupby(['Order Date', 'Ship Mode'])[['Profit', 'Sales']].sum()
        categ['Margin'] = categ['Profit'] / categ['Sales']
        categ = categ['Margin']
    else:
        categ = df.groupby(['Order Date', 'Ship Mode'])[obj].sum()
    year_month = []
    for i in range(len(categ)):
        if categ.index[i][0] in year_month:
            year_month.remove(categ.index[i][0])
        year_month.append(categ.index[i][0])
    yearmonth = []
    for i in range(len(year_month)):
        yearmonth.append(str(year_month[i].year) + '-' + str(year_month[i].month))
    year_month = yearmonth

    a = FirstClass = []
    b = SecondClass = []
    c = SameDay = []
    SameDay.append(0)
    SameDay.append(0)
    SameDay.append(0)
    SameDay.append(0)
    d = StandardClass = []
    for i in range(len(categ)):
        if categ.index[i][1] == 'First Class':
            FirstClass.append(categ[i])
        if categ.index[i][1] == 'Second Class':
            SecondClass.append(categ[i])
        if categ.index[i][1] == 'Same Day':
            SameDay.append(categ[i])
        if categ.index[i][1] == 'Standard Class':
            StandardClass.append(categ[i])

    fig_ship_mode_analysis = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.plot(year_month, a, marker='*', label='First Class')
    plt.plot(year_month, b, marker='^', label='Second Class')
    plt.plot(year_month, c, marker='s', label='Same Day')
    plt.plot(year_month, d, marker='*', label='Standard Class')
    plt.xlabel('Time', fontsize=0.05)
    plt.legend()
    # 主流还是standard class，technology 的销售情况和firstclass有关系，

    fig_ship_mode_count = plt.figure(figsize=(7, 6))
    plt.xticks(rotation=45)
    sns.countplot(x=df['Ship Mode'], palette='rocket')
    plt.title("Ship Mode count")

    # categ = df.groupby(['Order Date', 'Category'])['Sales'].sum()
    if obj == 'Margin':
        categ = df.groupby(['Order Date', 'Category'])[['Profit', 'Sales']].sum()
        categ['Margin'] = categ['Profit'] / categ['Sales']
        categ = categ['Margin']
    else:
        categ = df.groupby(['Order Date', 'Category'])[obj].sum()

    a = Furniture = []
    b = OfficeSupplies = []
    c = Technology = []
    for i in range(len(categ)):
        if categ.index[i][1] == 'Furniture':
            Furniture.append(float(categ[i]))
        if categ.index[i][1] == 'Office Supplies':
            OfficeSupplies.append(categ[i])
        if categ.index[i][1] == 'Technology':
            Technology.append(categ[i])
    fig_fur_off_tec = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.plot(year_month, a, marker='*', label='Furniture')
    plt.plot(year_month, b, marker='^', label='Office Supplies')
    plt.plot(year_month, c, marker='s', label='Technology')
    plt.xlabel('Time', fontsize=0.01)
    plt.legend()
    # 三条曲线相似，说明利润与三种类型的商品本身的区别关系不大，而在于外部市场环境，或企业内部统一的流程或程序

    if len(y)>0:
        fig_cat_pro = plt.figure(figsize=(5, 4))
        df[df['Year'].isin(y)].groupby('Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=15)
        fig_subcat_pro = plt.figure(figsize=(5, 4))
        df[df['Year'].isin(y)].groupby('Sub-Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=70)
        fig_subcat_count = plt.figure(figsize=(7, 6))
        plt.xticks(rotation=45)
        sns.countplot(x=df[df['Year'].isin(y)]['Sub-Category'], palette='rocket')
        plt.title("Sub-Category count")
    else:
        fig_cat_pro = plt.figure(figsize=(5, 4))
        df.groupby('Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=15)
        fig_subcat_pro = plt.figure(figsize=(5, 4))
        df.groupby('Sub-Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=70)
        fig_subcat_count = plt.figure(figsize=(7, 6))
        plt.xticks(rotation=45)
        sns.countplot(x=df['Sub-Category'], palette='rocket')
        plt.title("Sub-Category count")

    fig_fot, ax = plt.subplots(figsize=(5,5))
    sales_per_subcategory = df.groupby(["Category", "Sub-Category"], as_index=False)[["Sales", "Profit"]].sum()
    sales_per_subcategory["profit_margin"] = sales_per_subcategory["Profit"] / sales_per_subcategory["Sales"]
    #Sorting the dataframe based on profit margin
    sales_per_subcategory.sort_values(by="profit_margin", inplace=True, ascending=False)
    mean_profit = df['Profit'].sum()/df['Sales'].sum()

    #Plotting the profit margin per sub-category.
    sns.barplot(y=sales_per_subcategory["Sub-Category"], x=sales_per_subcategory["profit_margin"], hue=sales_per_subcategory["Category"], 
            hue_order=["Furniture", "Office Supplies", "Technology"], alpha=0.55, dodge=False,
           ax=ax)
    
    #Cleaning out bar junk
    ax.spines["left"].set_position("zero")
    ax.spines[["right","top"]].set_visible(False)
    ax.set(ylabel=None, xlabel="Profit Margin (%)")
    def move_ylabel_tick(index: list):
        """
        Moving the provided ylabel ticks
        """
        for tick in index:
            ax.get_yticklabels()[tick].set_x(0.02)
            ax.get_yticklabels()[tick].set_horizontalalignment("left")
    #Moving the y-labels on sub-categories that are making a loss in order to prevent collision of the bar and the text.
    move_ylabel_tick([-1, -2, -3])
    #Plotting a vertical line and annotating the Superstore's aggregate profit margin.
    ax.axvline(mean_profit, color="red", label="Mean Profit(All Types)", alpha=0.67, ls="--")
    ax.text(x=mean_profit+0.01, y=len(sales_per_subcategory)-0.7, s=f"{mean_profit*100 :.1f}%", color="red")

    #Setting the title and legend.
    ax.set_title("Profit Margin by Sub-category", fontdict={"fontsize":14})
    ax.legend(loc=(1, 0.9))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # categ = df.groupby(['Order Date', 'Segment'])['Profit'].sum()

    if obj == 'Margin':
        categ = df.groupby(['Order Date', 'Segment'])[['Profit', 'Sales']].sum()
        categ['Margin'] = categ['Profit'] / categ['Sales']
        categ = categ['Margin']
    else:
        categ = df.groupby(['Order Date', 'Segment'])[obj].sum()

    a = Consumer = []
    b = Corporate = []
    c = HomeOffice = []
    for i in range(len(categ)):
        if categ.index[i][1] == 'Consumer':
            a.append(float(categ[i]))
        if categ.index[i][1] == 'Corporate':
            b.append(categ[i])
        if categ.index[i][1] == 'Home Office':
            c.append(categ[i])
    fig_seg_line = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.plot(year_month, a, label='Consumer')
    plt.plot(year_month, b, label='Corporate')
    plt.plot(year_month, c, label='Home Office')
    plt.xlabel('Time', fontsize=0.01)
    plt.legend()

    fig_seg_bar = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.bar(year_month, a, label='Consumer')
    plt.bar(year_month, b, label='Corporate')
    plt.bar(year_month, c, label='Home Office')
    plt.xlabel('Time', fontsize=0.01)
    plt.legend()

    # ten_ = df.groupby('City')['Profit'].sum().sort_values().tail(10)

    if obj == 'Margin':
        ten_ = df.groupby('City')[['Profit', 'Sales']].sum()
        ten_['Margin'] = ten_['Profit'] / ten_['Sales']
        ten_ = ten_['Margin'].sort_values().tail(10)
    else:
        ten_ = df.groupby('City')[obj].sum().sort_values().tail(10)

    value = ten_.values.tolist()
    ten = ten_.index.tolist()

    fig_city_pro = plt.figure(figsize=(15, 8))
    # 绘制条形图
    plt.barh(range(len(value)), value, height=0.5, color='orange')  # 区别于竖的条形图 不能使用width
    # 设置字符串到X轴
    plt.yticks(range(len(value)), ten)
    # for a, b in enumerate(value):
    #     plt.text(a+0.1, b+1,a,ha='left',va='bottom')
    plt.grid(alpha=0.3)

    def city_profit(category):
        fig_city = plt.figure(figsize=(5, 4))
        category_1 = df[df['Category'] == category]
        # category_1.groupby('City')['Profit'].sum().sort_values(ascending=False)[:5].plot(kind='bar',
        #                                                                                  title="Top 5 Cities that made the most profit in {}".format(
        #                                                                                      category), rot=15)

        if obj == 'Margin':
            category_1 = category_1.groupby('City')[['Profit', 'Sales']].sum()
            category_1['Margin'] = category_1['Profit'] / category_1['Sales']
            category_1 = category_1['Margin']
            category_1.sort_values(ascending=False)[:5].plot(kind='bar',
                                                             title="Top 5 Cities that made the most {} in {}".format(
                                                                 obj,
                                                                 category), rot=15)
        else:
            category_1.groupby('City')[obj].sum().sort_values(ascending=False)[:5].plot(kind='bar',
                                                                                        title="Top 5 Cities that made the most {} in {}".format(
                                                                                            obj,
                                                                                            category), rot=15)
        return fig_city

    fig_city_pro_tec = city_profit('Technology')
    fig_city_pro_fur = city_profit('Furniture')
    fig_city_pro_sup = city_profit('Office Supplies')

    return fig_ship_mode_analysis, fig_ship_mode_count, fig_fur_off_tec, fig_cat_pro, fig_subcat_pro, fig_subcat_count, fig_fot, fig_seg_line, fig_seg_bar, fig_city_pro, fig_city_pro_tec, fig_city_pro_fur, fig_city_pro_sup

#st.pyplot(get_fig(df, obj)[6])

fig_shipmodepie = plt.figure(figsize=(5,4))
table1 = df.groupby('Ship Mode')['Profit'].sum()
x = []
y = []
i = 0
k = 0
while i <= 3:
    x.append(table1[i])
    i += 1
while k <= 3:
    y.append(table1.index[k])
    k +=1
plt.pie(x, labels = y, autopct='%1.1f%%', counterclock=False, startangle=90)
plt.title('Profit Ratio')
plt.tight_layout()
plt.show()

fig_catepie = plt.figure(figsize=(5,4))
table2 = df.groupby('Category')['Profit'].sum()
x = []
y = []
i = 0
k = 0
while i <= 2:
    x.append(table2[i])
    i += 1
while k <= 2:
    y.append(table2.index[k])
    k +=1
plt.pie(x, labels = y, autopct='%1.1f%%', counterclock=False, startangle=90)
plt.title('Profit Ratio')
plt.tight_layout()
plt.show()

fig_cus_order = plt.figure(figsize=(5, 4))
df['Customer ID'].value_counts().sort_values().tail(15).plot(kind='barh', ylabel = 'Customer ID', title='Top 15')
fig_cus_profit = plt.figure(figsize=(5, 4))
df.groupby('Customer ID')['Profit'].sum().sort_values().tail(15).plot(kind='barh', title='Top 15', color='red')

cids = set(df['Customer ID'])
years = list(df['Order Date'])
years = set([str(y)[0:4] for y in years])
y = []

# 前端
st.title('Business Analysis of Retail and Shipping')
st.subheader('by Yimin Zhou & Xinyue Cao')
st.image('WechatIMG66.jpeg')

tab = st.sidebar.radio('Choose Analyze Types:',
                       ["Ship Mode Analysis", "Product Analysis", "Segment Analysis", "Region Analysis"])
if tab == 'Ship Mode Analysis':
    st.subheader('Ship Mode Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[0])
    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(get_fig(df, obj)[1])
    with c2:
        st.pyplot(fig_shipmodepie)
    expander = st.expander('Profit Analysis')
    expander.write('The similarity of the three curves indicates that profit has little to do with the difference between the three types of goods themselves, but rather with the external market environment, or the uniform processes or procedures within the company.')
    expander.write('Even the standard class segment, which is the main source of profit, can have negative profit at some times, and the stability of the company in transporting goods still needs to be improved.')
    expander.write('According to Margin Analysis, the margins of all transportation services are positive and relatively stable, except for the unstable profit structure of Same Day service. Considering the number of orders and the low profit of Same Day service, the company should reduce or optimize the business in this area.')
    expander.write()
    expander.write()
    left_column, right_column = st.columns(2)
    pressed = left_column.button('Potential proportion')
    if pressed:
        right_column.write('The profit curve of technology products is similar to the profit curve of First Class, and as the potential and profits of technology products increase, the First Class segment should be given more attention by the company.')

elif tab == 'Product Analysis':
    st.subheader('Product Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[2])
    y = st.multiselect('Please Choose Year', years)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.pyplot(get_fig(df, obj, y)[3])
    with c2:
        st.pyplot(get_fig(df, obj, y)[4])
    with c3:
        st.pyplot(get_fig(df, obj, y)[5])
    
    st.subheader('On Whole Scale:')
    plt.style.use('fivethirtyeight')
    st.pyplot(get_fig(df, obj)[6])
    c4, c5 = st.columns([5, 5])
    with c4:
        
        st.pyplot(fig_catepie)
    with c5:
        expander = st.expander('Profit Analysis')
        expander.write('The company has a very high margin (more than double the company’s total margin) on a few of the sub-categories. Mainly within Office Supplies. Half of Technology’s subcategories also have a high margin. The chart also confirms that the profit margin on the sub-categories within Furniture are low. Two of the sub-categories from Furniture are even being sold at a loss. But technology is contributing most to the profit because of the outstanding performance in sales.')
    left_column, right_column = st.columns(2)
    pressed = left_column.button('Potential proportion')
    if pressed:
        right_column.write('Even though for Furniture the overall sales are increasing month by month, nearly half of the months have a negative margin and the profit is fluctuating around 0 for a long time, the company should reduce the furniture business or carry out related cost control.')

elif tab == 'Segment Analysis':
    st.subheader('Segment Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[7])
        st.write(obj)
        st.pyplot(get_fig(df, obj)[8])
    c3, c4 = st.columns([5, 5])
    with c3:
        st.subheader('Customer ID & Product Ordered')
        st.pyplot(fig_cus_order)
        #fig_cus_order = plt.figure(figsize=(5, 4))
        #df['Customer ID'].value_counts()[:15].plot(kind='barh', title='Customer ID & Product Ordered')
    with c4:
        st.subheader('Customer ID & Most Profit')
        st.pyplot(fig_cus_profit)
    profitslide = st.slider('Select the profit range($):', 0.0, 8400.0, 3000.0)
    df1 = df[df.Profit >= profitslide]
    st.dataframe(df1)
    cid = st.text_input('Please Input a Customer ID:')
    query = st.button('Query')
    if query:
        dfc = df[df['Customer ID'] == cid]
        if len(dfc) == 0:
            st.warning('The Customer ID You Input Does Not Exist')
        else:
            st.dataframe(df[df['Customer ID'] == cid])
            total_profit = df[df['Customer ID'] == cid]['Profit'].sum()
            st.metric('Total Profit Gained', total_profit, '$')
    left_column, right_column = st.columns(2)
    pressed = left_column.button('Profit Analysis')
    if pressed:
        right_column.write('The consumer segment has a bit lower profit margin comparing with Corporate and Home Office. This is most likely explained by the high volume of sales it was doing in Furniture, which we saw before has the lowest profit margin out of all the categories of products.')
    expander = st.expander('Potential proportion')
    expander.write('High profits and the volume of orders placed are not directly related to the two top15 list of IDs do not overlap, which is the same trend as technology products, because the number of technology products but the price is high. Therefore the buyer of technology is the most important ones.')

elif tab == 'Region Analysis':
    st.subheader('Region Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[9])
    c1, c2, c3 = st.columns(3)
    with c1:
        st.pyplot(get_fig(df, obj)[10])
    with c2:
        st.pyplot(get_fig(df, obj)[11])
    with c3:
        st.pyplot(get_fig(df, obj)[12])
    left_column, right_column = st.columns(2)
    pressed = left_column.button('Profit Analysis')
    if pressed:
        right_column.write('New York City contributed the highest profit. Although margin is not in the top15 but with sales and in the technology products to the company brought the highest profit. The margin of large cities is not high, and margin is inversely proportional, small cities are the opposite but large cities have high sales, resulting in higher profit.')
    expander = st.expander('Potential proportion')
    expander.write('The company should focus its attention on these big cities. And optimize the cost structure and increase the margin in the big cities to further increase the profit.')
    

    