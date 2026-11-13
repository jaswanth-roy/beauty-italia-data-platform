
-- 1. CUSTOMERS
INSERT INTO dbo.Customers
(CustomerID, FullName, Email, City)
VALUES
(1, 'Marco Rossi', 'marco@example.com', 'Milano'),
(2, 'Giulia Bianchi', 'giulia@example.com', 'Piacenza'),
(3, 'Sara Verdi', 'sara@example.com', 'Roma'),
(4, 'Luca Ferrari', 'luca@example.com', 'Parma'),
(5, 'Anna Romano', 'anna@example.com', 'Torino');

-- 2. PRODUCTS
INSERT INTO dbo.Products
(ProductID, ProductName, Category, Brand, UnitPrice)
VALUES
(101, 'Hydrating Face Cream', 'Skincare', 'BellaSkin', 29.99),
(102, 'Vitamin C Serum', 'Skincare', 'BellaSkin', 39.99),
(103, 'Matte Lipstick', 'Makeup', 'ColorBeauty', 19.99),
(104, 'Luxury Perfume', 'Fragrance', 'Essenza', 79.99),
(105, 'Shampoo Repair', 'Haircare', 'HairPro', 14.99),
(106, 'Night Face Mask', 'Skincare', 'BellaSkin', 24.99),
(107, 'Mascara Volume', 'Makeup', 'ColorBeauty', 16.99),
(108, 'Body Lotion', 'Bodycare', 'Essenza', 12.99);

-- 3. STORES
INSERT INTO dbo.Stores
(StoreID, StoreName, City)
VALUES
(1, 'Milano Central', 'Milano'),
(2, 'Piacenza Beauty Store', 'Piacenza'),
(3, 'Roma Shopping Center', 'Roma');

-- 4. ORDERS
INSERT INTO dbo.Orders
(OrderID, CustomerID, StoreID, OrderSource, OrderDate, OrderStatus)
VALUES
(1001, 1, NULL, 'Ecommerce', '2026-11-10 10:30:00', 'Completed'),
(1002, 2, 2, 'Retail', '2026-11-10 11:00:00', 'Completed'),
(1003, 3, NULL, 'Ecommerce', '2026-11-10 12:15:00', 'Processing'),
(1004, 4, 1, 'Retail', '2026-11-11 09:30:00', 'Completed'),
(1005, 5, NULL, 'Ecommerce', '2026-11-11 14:20:00', 'Shipped'),
(1006, 1, 1, 'Retail', '2026-11-12 10:00:00', 'Completed'),
(1007, 2, NULL, 'Ecommerce', '2026-11-12 11:45:00', 'Processing'),
(1008, 3, 3, 'Retail', '2026-11-12 13:00:00', 'Completed');

-- 5. ORDER ITEMS
INSERT INTO dbo.OrderItems
(OrderItemID, OrderID, ProductID, Quantity, UnitPrice)
VALUES
(1, 1001, 101, 2, 29.99),
(2, 1001, 103, 1, 19.99),
(3, 1002, 104, 1, 79.99),
(4, 1002, 108, 2, 12.99),
(5, 1003, 102, 1, 39.99),
(6, 1003, 106, 2, 24.99),
(7, 1004, 105, 3, 14.99),
(8, 1005, 107, 2, 16.99),
(9, 1005, 103, 1, 19.99),
(10, 1006, 101, 1, 29.99),
(11, 1007, 104, 1, 79.99),
(12, 1008, 108, 3, 12.99);

-- 6. INVENTORY
INSERT INTO dbo.Inventory
(InventoryID, ProductID, StoreID, StockQuantity)
VALUES
(1, 101, 1, 120),
(2, 102, 1, 80),
(3, 103, 1, 150),
(4, 104, 2, 45),
(5, 105, 2, 90),
(6, 106, 3, 60),
(7, 107, 3, 110),
(8, 108, 2, 200);

GO




SELECT
    o.OrderID,
    c.FullName,
    o.OrderSource,
    o.OrderStatus,
    SUM(oi.Quantity * oi.UnitPrice) AS OrderTotal
FROM dbo.Orders o
JOIN dbo.Customers c
    ON o.CustomerID = c.CustomerID
JOIN dbo.OrderItems oi
    ON o.OrderID = oi.OrderID
GROUP BY
    o.OrderID,
    c.FullName,
    o.OrderSource,
    o.OrderStatus
ORDER BY o.OrderID;
GO
