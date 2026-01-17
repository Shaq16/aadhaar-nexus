"""
Chhattisgarh Aadhaar District Analysis
Replicates the UP analysis pipeline for Chhattisgarh state.
"""
from analysis_utils import run_state_analysis

# State configuration
STATE_NAME = "chhattisgarh"
STATE_VARIATIONS = [
    "Chhattisgarh", "CHHATTISGARH", "chhattisgarh", "Chattisgarh", "CHATTISGARH"
]
STANDARD_NAME = "Chhattisgarh"

if __name__ == "__main__":
    result = run_state_analysis(STATE_NAME, STATE_VARIATIONS, STANDARD_NAME)
    if result is not None:
        print(f"\n📊 Summary for {STANDARD_NAME}:")
        print(f"   Total districts: {len(result)}")
        print(f"   Average DEI score: {result['DEI'].mean():.4f}")
        print(f"   Average ASS score: {result['ASS'].mean():.4f}")
        print(f"   Average UBS score: {result['UBS'].mean():.4f}")
        print(f"   Average SRS score: {result['SRS'].mean():.4f}")
