from config.db import DBConnection
from src.logger import get_logger
from src.exception import CustomException
import pandas as pd
import sys

logger = get_logger("FarmService")
class FarmService:
    def __init__(self):
        self.db_connection = DBConnection()
    def _get_data(self, view_name):
        try:
            df = pd.read_sql(f'SELECT * FROM {view_name}', self.db_connection.engine)
            if df.empty:
                logger.warning("No data found in the database.")
            else:
                logger.info(f"Data retrieved successfully with {len(df)} records.")
            return df
            
        except Exception as e:
            logger.error(f"Error in _get_data: {e}")
            raise CustomException("Error in _get_data",e)
    def get_farm_summary(self, **filters):
        """
            region 
            farm_type
            year
            season
        """
        query_filters = {}

        try:
            df = self._get_data("vw_harvest_full")
            logger.info(f"Columns: {df.columns}")
            # filter
            for key ,val in filters.items():
                if val is not None and key in df.columns:
                    query_filters[key] = val
            
            logger.info(f" Query filters to apply: {query_filters}")

            if query_filters:
                logger.info(f"Applying filters: {query_filters}")
                for key, val in query_filters.items():
                    df = df[df[key] == val]
            # if filters.get("year"):
            #     query_filters["year"] = filters["year"]
            

            if df.empty:
                return {"total_farms": 0, "filters_applied": filters, "data": []}
            

            df['calculated_loss_pct'] = (df['quantity_lost_ton'] / df['quantity_harvested_ton']) * 100
            
            summary = df.groupby(['farm_name', 'region', 'farm_type']).agg({
            'revenue_bdt': 'sum',
            'input_cost_bdt': 'sum',  
            'net_profit_bdt': 'sum',
            'calculated_loss_pct': 'mean'
            }).reset_index()

            summary.columns = [
            'farm_name', 'region', 'farm_type', 
            'total_revenue_bdt', 'total_cost_bdt', 'net_profit_bdt', 'avg_loss_pct'
             ]
            return {
            "total_farms": int(summary['farm_name'].nunique()),
            "filters_applied": query_filters,
            "data": summary.round(2).to_dict(orient='records')
            }

        except Exception as e:
            logger.error(f"Error in get_farm_summary: {e}")
            raise CustomException("Error in get_farm_summary",e)