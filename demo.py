from src.service.FarmService import FarmService
import os
from dotenv import load_dotenv
load_dotenv(override=True)
class demoPipeline:
    def __init__(self):
        pass
    def run(self):
        print("Running the demo pipeline...")
        farm_service = FarmService()
        farm_service.get_farm_summary()
if __name__ == "__main__":
    pipeline = demoPipeline()
    pipeline.run()