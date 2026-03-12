
class DecisionEngine:
    PRIORITY_SCORES ={
        "first_line": 3,
        "second_line": 2,
        "alternative": 1
    }

    EVIDENCE_CONFIDENCE ={
        "High":0.9,
        "Moderate":0.7,
        "Low":0.5
    }

    def rank_therapy(self,therapy_candidates):
        ranked = []
        for therapy in therapy_candidates:
            drug = therapy["drug"]
            thrapy_type = therapy["type"]
            priority = self.PRIORITY_SCORES.get(thrapy_type,0)

            score = 0.7 *priority + 0.3 *1

            ranked.append({
                "drug": drug,
                "type": thrapy_type,
                "score": score
            })

        ranked.sort(key=lambda x:x["score"],reverse=True)
        return ranked
        
    def compute_confidence(self,evidence_level):
        return self.EVIDENCE_CONFIDENCE.get(evidence_level,0.5)

    def decide(self,therapy_candidate,evidence_level):
        ranked = self.rank_therapy(therapy_candidate)
        best = ranked[0]["drug"]
        confidence = self.compute_confidence(evidence_level)
        return {
            "recommended_therapy":best,
            "confidence_score": confidence,
            "ranked_therapies": ranked
        }

if __name__ == "__main__":
    engine = DecisionEngine()
    therapy_candidates = [
        {"drug": "Osimertinib", "type": "first_line"},
        {"drug": "Erlotinib", "type": "second_line"},
        {"drug": "Gefitinib", "type": "alternative"}
    ]
    evidence_level = "High"
    decision = engine.decide(therapy_candidates,evidence_level)
    print(decision)