def decision_feedback_analysis(predictions, actuals):
    assert len(predictions) == len(actuals), "Prediction and actual length mismatch."
    
    feedback = []
    for pred, actual in zip(predictions, actuals):
        if pred == actual:
            feedback.append("✅ Correct")
        else:
            feedback.append("❌ Incorrect")
    
    return feedback


