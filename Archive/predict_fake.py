import instaloader
import pandas as pd
import joblib
import re

# Load the saved model
model = joblib.load("fake_instagram_account_model.pkl")

# Fetch profile info using Instaloader
def get_profile_data(username):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        
        return {
            "num_followers": profile.followers,
            "num_following": profile.followees,
            "num_posts": profile.mediacount,
            "has_profile_picture": int(profile.profile_pic_url is not None),
            "bio_length": len(profile.biography or ""),
            "is_verified": int(profile.is_verified)
        }
    except Exception as e:
        print("❌ Error:", e)
        return None

# Predict function
def predict(username):
    data = get_profile_data(username)
    if not data:
        return

    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    
    print(f"\n🔎 Account: @{username}")
    print("🟠 Prediction:", "FAKE ❌" if prediction == 1 else "REAL ✅")

# === Main Program ===
if __name__ == "__main__":
    user_input = input("Enter an Instagram username: ")
    predict(user_input)
