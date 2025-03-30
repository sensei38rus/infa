import sqlite3
connection = sqlite3.connect('bazo.db')
cursor = connection.cursor()

#создание таблиц
cursor.execute("""CREATE TABLE IF NOT EXISTS 'shops' (
               'shop_id' TEXT PRIMARY KEY,
               'district' TEXT NOT NULL
)""")



cursor.execute("""CREATE TABLE IF NOT EXISTS 'goods' (
               'articul' INTEGER PRIMARY KEY,
               'department' TEXT NOT NULL,
               'product_name' TEXT NOT NULL,
               'measure' TEXT NOT NULL,
               'volume' FLOAT NOT NULL,
               'supplier' TEXT NOT NULL
               ); """)



cursor.execute(""" CREATE TABLE IF NOT EXISTS 'trading' (
               'operation_id' INTEGER PRIMARY KEY ,
               'date' REAL NOT NULL,
               'shop_id' TEXT NOT NULL,
               'articul' INTEGER NOT NULL,
               'operation' TEXT NOT NULL,
               'amount' INTEGER NOT NULL,
               'price_per_each' INTEGER,
                FOREIGN KEY (shop_id) REFERENCES shops(shop_id),
                FOREIGN KEY (articul) REFERENCES goods(articul)
);""")


#заполнение
for s in open('shops.txt', 'r', encoding='utf-8'):
     data = s.strip().split('\t')
     cursor.execute('INSERT OR IGNORE INTO shops (shop_id, district) VALUES (?, ?)',
                          (data[0], data[1]))
connection.commit()



for s in open('goods.txt', 'r', encoding='utf-8'):
    data = s.strip().split('\t')
    cursor.execute('''
            INSERT OR IGNORE INTO goods (articul, department, product_name, measure, volume, supplier)
             VALUES (?, ?, ?, ?, ?, ?)
            ''', (int(data[0]), data[1], data[2], data[3], float(data[4]), data[5]))
    
connection.commit()



for s in open('trading.txt', 'r', encoding='utf-8'):
     data = s.strip().split('\t')
     operation_id = int(data[0])
     date = data[1]
     shop_id = data[2]
     articul = int(data[3])
     operation = data[4]
     amount = int(data[5])
     price = int(data[6])
     cursor.execute('''
           INSERT  OR IGNORE INTO trading (operation_id, date, shop_id, articul, operation, amount, price_per_each)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (operation_id, date, shop_id, articul, operation, amount, price))

connection.commit()



cursor.execute( """
SELECT 
    SUBSTR(t.date, 9, 2) AS day,
    SUM(t.amount * t.price_per_each) AS total_revenue
FROM 
    trading t
JOIN 
    goods g ON t.articul = g.articul
JOIN 
    shops s ON t.shop_id = s.shop_id
WHERE 
    g.department = 'Молоко'
    AND s.district = 'Заречный'
    AND t.operation = 'Продажа' 
GROUP BY 
    day
ORDER BY 
    total_revenue DESC
LIMIT 1
""")
result = cursor.fetchone()
print(f"День с максимальной выручкой: {result[0]}")





connection.close()

