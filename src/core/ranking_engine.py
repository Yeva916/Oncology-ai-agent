
import os

from dotenv import load_dotenv

from src.core.database import OncoDatabase
# from src.core.database import OncoDatabase
from src.core.rule_engine import rule_engine
from src.core.validator import InputData


class DecisionEngine:
    LINE_SCORE = {
        "first_line": 3,
        "second_line": 2,
        "alternative": 1
    }


    EVIDENCE_SCORE = {
        "High": 3,
        "Moderate": 2,
        "Low": 1
    }

    CONFIDENCE_MAP = {
        "High": 0.9,
        "Moderate": 0.7,
        "Low": 0.5
    }

    def rank_therapies(self,therapies):
        ranked = []

        for therapy in therapies:
            drug = therapy["drug"]
            line = therapy["line"]
            evidence = therapy.get("evidence_level", "Low")

            line_score = self.LINE_SCORE.get(line, 0)
            evidence_score = self.EVIDENCE_SCORE.get(evidence, 1)

            # weighted ranking formula
            score = (0.7 * line_score) + (0.3 * evidence_score)

            ranked.append({
                "drug": drug,
                "line": line,
                "evidence_level": evidence,
                "score": score
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return ranked
        
    def compute_confidence(self,evidence_level):
        return self.CONFIDENCE_MAP.get(evidence_level,0.5)

    def decide(self, therapies):
        ranked_therapies = self.rank_therapies(therapies)
        best_therapy = ranked_therapies[0]
        confidence = self.compute_confidence(best_therapy["evidence_level"])
        return {
            "recommended_therapy": best_therapy["drug"],
            "confidence_score": confidence,
            "ranked_therapies": ranked_therapies
        }

if __name__ == "__main__":
    load_dotenv()
    # print(os.getenv("DATA_DIR"))
    data = OncoDatabase.load_data(os.getenv("DATA_DIR"))
    print(data)
    # engine = DecisionEngine()
    input_data = {
        "mutation": "L858R",
        "cancer_type": "nsclc"
    }
    validated_data = InputData(**input_data)
    result = rule_engine(validated_data)
    print(result)
    # decision = engine.decide(result["therapy"])
    # print(decision)