import pandas as pd
from .Helper.FabricsConnection import get_connection
from .Helper.VannaObject import MyVanna
from .Helper.Credentials import Credentials
import os
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize Vanna model
vn = MyVanna(config={'api_key': Credentials.open_ai_key, 'model': Credentials.model})

# Connect to Fabric
conn = get_connection()

def run_sql(sql: str):
    df = pd.read_sql_query(sql, conn)
    return df

vn.run_sql = run_sql
vn.run_sql_is_set = True


def ask_fabric(question: str) -> str:
    try:
        client_match = re.search(r'client\s*(?:id\s*)?(\d+)', question, re.IGNORECASE)

        if client_match:
            client_id = client_match.group(1)
            sql = f"""
            SELECT c.ClientID, c.Name AS ClientName, c.RiskProfile,
                   p.PortfolioID, p.Name AS PortfolioName, p.RiskLevel,
                   a.Name AS AssetName, a.AssetType, a.CurrentValue,
                   pa.Allocation
            FROM Clients c
            LEFT JOIN Portfolios p ON c.ClientID = p.ClientID
            LEFT JOIN PortfolioAssets pa ON p.PortfolioID = pa.PortfolioID
            LEFT JOIN Assets a ON pa.AssetID = a.AssetID
            WHERE c.ClientID = {client_id}
            """
            try:
                df = run_sql(sql)
                if df.empty:
                    return f"No data found for client {client_id}."
                return df.to_string()
            except Exception as e:
                return f"Error running client query: {str(e)}"

        # Check for asset type questions
        asset_keywords = ['asset type', 'wealth summary', 'total wealth', 'asset distribution']
        if any(kw in question.lower() for kw in asset_keywords):
            try:
                df = run_sql("SELECT AssetType, NumberOfAssets, TotalWealth FROM OverallWealthSummary ORDER BY TotalWealth DESC")
                return f"Results:\n{df.to_string()}"
            except:
                pass

        # Check for advisor questions
        if 'advisor' in question.lower():
            try:
                df = run_sql("SELECT a.AdvisorID, a.Name AS AdvisorName, COUNT(c.ClientID) AS NumClients FROM Advisors a LEFT JOIN Clients c ON a.AdvisorID = c.AdvisorID GROUP BY a.AdvisorID, a.Name ORDER BY NumClients DESC")
                return f"Results:\n{df.to_string()}"
            except:
                pass

        # For everything else, use Vanna
        sql = vn.generate_sql(question)
        if sql:
            try:
                df = run_sql(sql)
                if df.empty:
                    return "Query executed successfully but returned no results."
                return f"SQL: {sql}\n\nResults:\n{df.to_string()}"
            except Exception as exec_err:
                return f"Generated SQL failed: {str(exec_err)}. SQL was: {sql}"
        else:
            return "Could not generate a SQL query for this question."
    except Exception as e:
        return f"Error querying database: {str(e)}"