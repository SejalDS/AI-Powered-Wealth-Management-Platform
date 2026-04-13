CREATE TABLE Advisors (
    AdvisorID INT PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    ContactInfo NVARCHAR(100)
);

CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    ContactInfo NVARCHAR(100),
    AdvisorID INT,
    RiskProfile NVARCHAR(50),
    FOREIGN KEY (AdvisorID) REFERENCES Advisors(AdvisorID)
);

CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    AccountType NVARCHAR(50) NOT NULL,
    ClientID INT,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

CREATE TABLE Assets (
    AssetID INT PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    AssetType NVARCHAR(50),
    CurrentValue DECIMAL(18, 2)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    AssetID INT,
    Date DATETIME,
    Type NVARCHAR(50),
    Amount DECIMAL(18, 2),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID),
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID)
);

CREATE TABLE Portfolios (
    PortfolioID INT PRIMARY KEY,
    ClientID INT,
    Name NVARCHAR(100),
    RiskLevel NVARCHAR(50),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

CREATE TABLE PortfolioAssets (
    PortfolioAssetID INT PRIMARY KEY,
    PortfolioID INT,
    AssetID INT,
    Allocation DECIMAL(18, 2),
    FOREIGN KEY (PortfolioID) REFERENCES Portfolios(PortfolioID),
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID)
);

CREATE TABLE Projections (
    ProjectionID INT PRIMARY KEY,
    PortfolioID INT,
    FutureValue DECIMAL(18, 2),
    ProjectionDate DATETIME,
    FOREIGN KEY (PortfolioID) REFERENCES Portfolios(PortfolioID)
);