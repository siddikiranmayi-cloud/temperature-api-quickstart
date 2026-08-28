from pathlib import Path
from dotenv import load_dotenv

from fortyguard import FortyGuardClient
from fortyguard.samples import MANHATTAN_POLYGON

# Path to .env file relative to this file's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_client():
    return FortyGuardClient()


def run_exceedance_analysis():
    client = get_client()

    response = client.create_heatmap(
        polygon_aoi=MANHATTAN_POLYGON,
        start_date="2024-07-15",
        end_date="2024-07-21",
        filter_type=4,
        analytic_type="exceedance",
        threshold=35.0,
        direction="above",
        granularity=100,
    )

    return response


def run_temperature_analysis():
    client = get_client()

    response = client.create_heatmap(
        polygon_aoi=MANHATTAN_POLYGON,
        start_date="2024-07-15",
        start_time="14:00",
        filter_type=1,
        granularity=100,
                                                
                        
                        
    )

    return response
def run_heatmap_analysis():
    client = get_client()

    response = client.create_heatmap(
polygon_aoi=MANHATTAN_POLYGON,
        start_date="2024-07-15",
        start_time="14:00",
        filter_type=1,
        granularity=100,
    )

    return response

        