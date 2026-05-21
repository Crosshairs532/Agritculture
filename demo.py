from Agriculture.src.service.FarmService import AgricultureService
import os
from dotenv import load_dotenv
load_dotenv(override=True)
class demoPipeline:
    def __init__(self):
        pass
    def run(self):
        print("Running the demo pipeline...")
        agriculture_service = AgricultureService()
        agriculture_service.get_farm_summary()
if __name__ == "__main__":
    pipeline = demoPipeline()
    pipeline.run()