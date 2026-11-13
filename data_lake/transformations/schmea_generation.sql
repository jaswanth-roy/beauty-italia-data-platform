
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FullName NVARCHAR(150),
    Email NVARCHAR(150),
    City NVARCHAR(100),
    CreatedAt DATETIME2 DEFAULT SYSDATETIME()
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(150),
    Category NVARCHAR(100),
    Brand NVARCHAR(100),
    UnitPrice DECIMAL(10,2)
);

CREATE TABLE Stores (
    StoreID INT PRIMARY KEY,
    StoreName NVARCHAR(150),
    City NVARCHAR(100)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    StoreID INT NULL,
    OrderSource NVARCHAR(30),
    OrderDate DATETIME2,
    OrderStatus NVARCHAR(30),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
);

CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    ProductID INT,
    StoreID INT,
    StockQuantity INT,
    LastUpdated DATETIME2 DEFAULT SYSDATETIME(),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
);

GO