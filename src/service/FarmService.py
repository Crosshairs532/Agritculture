from warnings import filters

from fastapi import HTTPException

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
        
    def get_Single_Farm_Performance(self, farm_id: str, **filters):
        
        logger.info(f"Fetching performance for farm_id: {farm_id}")

        query_filters = {}
        try:
            single_farm_query = f"SELECT * from dim_farm WHERE farm_id = '{farm_id}'"
            single_farm_df = pd.read_sql(single_farm_query, self.db_connection.engine)


            if single_farm_df.empty:
                raise CustomException(f"Farm ID {farm_id} not found", 404)
            farm_name = single_farm_df["farm_name"].values[0]   
            for key ,val in filters.items():
                if val is not None:
                    query_filters[key] = val
            
            vw_harvest_full_farm = pd.read_sql(f"SELECT * from vw_harvest_full WHERE farm_name = '{farm_name}'", self.db_connection.engine)

            owner_name = vw_harvest_full_farm["owner_name"].values[0]
            region = vw_harvest_full_farm["region"].values[0]

            for key, val in query_filters.items():
                if val is not None and key in vw_harvest_full_farm.columns:
                    vw_harvest_full_farm = vw_harvest_full_farm[vw_harvest_full_farm[key] == val]

            performance_list = vw_harvest_full_farm[[
                'crop_name', 'year', 'market_type', 
                'quantity_sold_ton', 'revenue_bdt', 'net_profit_bdt', 'quality_grade'
            ]].to_dict(orient='records')

            response = {
                'farm_id': farm_id,
                'farm_name': farm_name,
                'owner_name': owner_name,
                'region': region,
                "filters_applied:": query_filters,
                'performance_data': performance_list
            }

            return response
        
        except Exception as e:
            logger.error(f"Error in get_Single_Farm_Performance: {e}")
            raise CustomException("Error in get_Single_Farm_Performance",e)

    def get_top_farms(self, **filters):
        """
            metric 
            limit 
            --------
            region
            farm_type
            year
        """
        query_filters = {}
        metric_map = {
            "profit": "net_profit_bdt",
            "revenue": "revenue_bdt",
            "yield": "actual_yield_ton_per_ha"
        }
        metric = filters.pop("metric", "profit") 
        if metric is None: 
            metric = "profit"

        logger.info(f"Fetching top farms based on metric: {metric}")
        limit = filters.pop("limit", 10)
        # get query metric  or default profit
        metric_column = metric_map.get(metric, "net_profit_bdt") 
        try: 
            df = self._get_data("vw_harvest_full")

            # filtered by year, region, farm_type
            for key, val in filters.items():
                if val is not None and key in df.columns:
                    query_filters[key] = val
                    df = df[df[key] == val]

            if df.empty:
                return {"metric": metric, "filters_applied": query_filters, "rankings": []}

            agg_type = 'mean' if metric == 'yield' else 'sum'
            ranking_df = df.groupby(['farm_name', 'region', 'farm_type']).agg({
                metric_column: agg_type,
                'revenue_bdt': 'sum',    
                'net_profit_bdt': 'sum'  
            }).reset_index()
            ranking_df = ranking_df.sort_values(by=metric_column, ascending=False).head(limit)
            ranking_df['rank'] = range(1, len(ranking_df) + 1)
            ranking_df = ranking_df.rename(columns={
                'revenue_bdt': 'total_revenue_bdt'
            })

            query_filters["limit"] = limit
            result = {
                "metric":metric, 
                "filters_applied": query_filters,
                "rankings":ranking_df.round(2).to_dict(orient='records')
            }

            return result

        except Exception as e:
            logger.error(f"Error in get_top_farms: {e}")
            raise CustomException("Error in get_top_farms",e)