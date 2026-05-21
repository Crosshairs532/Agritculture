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
            df = self._get_data("vw_farm_profitability")
            logger.info(f"Columns: {df.columns}")
            # filter
            for key ,val in filters.items():
                if val is not None and key in df.columns:
                    query_filters[key] = val

            if query_filters:
                logger.info(f"Applying filters: {query_filters}")
                for key, val in query_filters.items():
                    df = df[df[key] == val]
            if filters.get("year"):
                query_filters["year"] = filters["year"]
            summary = df.groupby(['farm_name', 'region', 'farm_type']).agg({
            'total_revenue_bdt': 'sum',
            'total_cost_bdt': 'sum',
            'total_profit_bdt': 'sum',
            'loss_pct': 'mean'
                    }).reset_index()
            summary.rename(columns={
                "total_profit_bdt": "net_profit_bdt",
                "loss_pct": "avg_loss_pct",
            }, inplace=True)

            return {
                "total_farms": int(summary['farm_name'].nunique()),
                "filters_applied": query_filters,
                "data": summary.to_dict(orient='records')
                }

        except Exception as e:
            logger.error(f"Error in get_farm_summary: {e}")
            raise CustomException("Error in get_farm_summary",e)