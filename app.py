from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader
import pandas as pd
import joblib
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Load model
try:
    model = joblib.load("fake_instagram_account_model.pkl")
    app.logger.info(f"Model loaded. Expected features: {model.feature_names_in_}")
except Exception as e:
    app.logger.error(f"Failed to load model: {str(e)}")
    raise

def extract_features(username):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Calculate features to match training data
        username_length = len(username)
        num_nums_in_username = sum(c.isdigit() for c in username)
        fullname = profile.full_name or ""
        
        return {
            "profile pic": int(profile.profile_pic_url is not None),
            "nums/length username": num_nums_in_username/max(1, username_length),
            "fullname words": len(fullname.split()),
            "nums/length fullname": sum(c.isdigit() for c in fullname)/max(1, len(fullname)),
            "name==username": int(username.lower() == fullname.lower()),
            "description length": len(profile.biography or ""),
            "external URL": int(profile.external_url is not None),
            "private": int(profile.is_private),
            "#posts": profile.mediacount,
            "#followers": profile.followers,
            "#follows": profile.followees
        }
    except Exception as e:
        app.logger.error(f"Feature extraction failed: {str(e)}")
        return {"error": str(e)}

@app.route("/predict")
def predict():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    features = extract_features(username)
    if "error" in features:
        return jsonify({"error": features["error"]}), 500
    
    try:
        df = pd.DataFrame([features], columns=model.feature_names_in_)
        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0]
        confidence = round(max(proba) * 100, 2)
        
        return jsonify({
            "prediction": "FAKE" if pred == 1 else "REAL",
            "confidence": confidence
        })
    except Exception as e:
        app.logger.error(f"Prediction failed: {str(e)}")
        return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)