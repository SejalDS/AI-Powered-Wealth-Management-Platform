from Helper.VannaObject import MyVanna
from Helper.Credentials import Credentials

vn = MyVanna(config={'api_key': Credentials.open_ai_key, 'model': Credentials.model})

# Teach it about ClientPortfolioValue view queries
vn.train(question='Which clients have portfolio values above the average portfolio value?', sql='SELECT ClientID, ClientName, TotalPortfolioValue FROM ClientPortfolioValue WHERE TotalPortfolioValue > (SELECT AVG(TotalPortfolioValue) FROM ClientPortfolioValue) ORDER BY TotalPortfolioValue DESC')

vn.train(question='What is the average portfolio value across all clients?', sql='SELECT AVG(TotalPortfolioValue) AS AvgPortfolioValue FROM ClientPortfolioValue')

# Teach it about transaction queries
vn.train(question='Show total buy and sell amounts by month for year 2022', sql='SELECT MONTH(Date) AS TransactionMonth, Type, SUM(Amount) AS TotalAmount FROM Transactions WHERE YEAR(Date) = 2022 GROUP BY MONTH(Date), Type ORDER BY TransactionMonth')

vn.train(question='Show total transaction amounts by transaction type', sql='SELECT Type, COUNT(*) AS NumTransactions, SUM(Amount) AS TotalAmount, AVG(Amount) AS AvgAmount FROM Transactions GROUP BY Type')

# Teach it about asset queries
vn.train(question='For each asset type show the count minimum maximum and average value', sql='SELECT AssetType, COUNT(*) AS AssetCount, MIN(CurrentValue) AS MinValue, MAX(CurrentValue) AS MaxValue, AVG(CurrentValue) AS AvgValue FROM Assets GROUP BY AssetType')

vn.train(question='Show total wealth by asset type', sql='SELECT AssetType, COUNT(AssetID) AS NumberOfAssets, SUM(CurrentValue) AS TotalWealth FROM Assets GROUP BY AssetType ORDER BY TotalWealth DESC')

# Teach it about advisor queries  
vn.train(question='How many clients does each advisor manage', sql='SELECT a.Name AS AdvisorName, COUNT(c.ClientID) AS NumClients FROM Advisors a LEFT JOIN Clients c ON a.AdvisorID = c.AdvisorID GROUP BY a.AdvisorID, a.Name ORDER BY NumClients DESC')

# Teach it about portfolio risk queries
vn.train(question='Show average portfolio value by risk level', sql='SELECT p.RiskLevel, AVG(pa.Allocation * a.CurrentValue / 100.0) AS AvgPortfolioValue, COUNT(DISTINCT p.PortfolioID) AS NumPortfolios FROM Portfolios p JOIN PortfolioAssets pa ON p.PortfolioID = pa.PortfolioID JOIN Assets a ON pa.AssetID = a.AssetID GROUP BY p.RiskLevel')

# Teach it about complex joins
vn.train(question='Show clients with their advisor name and portfolio value above 3000', sql='SELECT c.Name AS ClientName, a.Name AS AdvisorName, cpv.TotalPortfolioValue FROM Clients c JOIN Advisors a ON c.AdvisorID = a.AdvisorID JOIN ClientPortfolioValue cpv ON c.ClientID = cpv.ClientID WHERE cpv.TotalPortfolioValue > 3000 ORDER BY cpv.TotalPortfolioValue DESC')

# Teach it about ranking
vn.train(question='Rank all clients by their total portfolio value', sql='SELECT ClientID, ClientName, TotalPortfolioValue, ROW_NUMBER() OVER (ORDER BY TotalPortfolioValue DESC) AS Rank FROM ClientPortfolioValue')

print('Training complete! 10 new question-SQL pairs added.')