import streamlit as st
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load pickled files
with open('model/coursera_df.pkl', 'rb') as f:
    coursera_df = pickle.load(f)

with open('model/tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('model/tfidf_matrix.pkl', 'rb') as f:
    tfidf_matrix = pickle.load(f)

with open('model/pop_score.pkl', 'rb') as f:
    pop_score = pickle.load(f)



# Recommendation functions
def content_based_recommendations(user_input, tfidf=tfidf, tfidf_matrix=tfidf_matrix, df=coursera_df, top_n=10):
    user_tfidf = tfidf.transform([user_input])
    cosine_sim = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    top_indices = cosine_sim.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][['course_title', 'subject', 'level', 'content_duration', 'num_subscribers', 'num_reviews', 'profit']]

def popularity_based_recommendations(top_n=10):
    df = coursera_df.copy()
    df['popularity_score'] = pop_score
    df_sorted = df.sort_values(by='popularity_score', ascending=False)
    return df_sorted[['course_title', 'subject', 'level', 'content_duration', 'num_subscribers', 'num_reviews', 'profit']].head(top_n)


    matches = coursera_df[coursera_df['course_title'].str.contains(course_title, case=False, na=False)]
    if matches.empty:
        return None
    idx = matches.index[0]
    sim_scores = list(enumerate(hybrid_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [x for x in sim_scores if x[0] != idx]
    top_indices = [i for i, score in sim_scores[:top_n]]
    return coursera_df.iloc[top_indices][['course_title', 'subject', 'level', 'content_duration', 'num_subscribers', 'num_reviews', 'profit']]

# Display function for professional output
import pandas as pd
# import streamlit as st

def display_courses(courses):
    for idx, row in courses.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            # Course title with book emoji
            st.markdown(f"### 📘 {row['course_title']}")
            
            # Colored badges for subject and level
            subject_html = f"<span style='background-color: #5bc0de; color: white; padding: 5px 10px; border-radius: 5px;'>{row['subject']}</span>"
            level_html = f"<span style='background-color: #f0ad4e; color: white; padding: 5px 10px; border-radius: 5px; margin-left: 10px;'>{row['level']}</span>"
            st.markdown(subject_html + level_html, unsafe_allow_html=True)
            
            # Duration
            st.markdown(f"**Duration:** {row['content_duration']}")
            
            # Clickable course URL if available
            if 'url' in row and pd.notna(row['url']):
                st.markdown(f"[🔗 Go to Course]({row['url']})")
        
        with col2:
            # Display subscribers, reviews, and profit with commas and defaults
            subscribers = f"{row.get('num_subscribers', 0):,}" if pd.notna(row.get('num_subscribers')) else "N/A"
            reviews = f"{row.get('num_reviews', 0):,}" if pd.notna(row.get('num_reviews')) else "N/A"
            profit = f"${row.get('profit', 0):,}" if pd.notna(row.get('profit')) else "N/A"
            
            st.markdown(f"**Subscribers:** {subscribers}  \n"
                        f"**Reviews:** {reviews}  \n"
                        f"**Profit:** {profit}")
        
        st.markdown("---")  # Divider between courses



# Streamlit UI
st.title("Course Recommendation System")

rec_type = st.radio("Choose Recommendation Type:",
                    ("Content-Based", "Popularity-Based"))

if rec_type == "Content-Based":
    course_input = st.selectbox("Select or enter course title:", coursera_df['course_title'].tolist())
    if st.button("Recommend"):
        results = content_based_recommendations(course_input)
        if results is not None and not results.empty:
            display_courses(results)
        else:
            st.write("No matching courses found.")

elif rec_type == "Popularity-Based":
    st.write("Top 10 Popular Courses:")
    results = popularity_based_recommendations()
    display_courses(results)


