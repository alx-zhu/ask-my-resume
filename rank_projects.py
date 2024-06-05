import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Tuple

nltk.download("stopwords")
nltk.download("wordnet")


# Preprocess text for usage in NLP
def preprocess_text(text: str):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    words = [word for word in text.split(" ") if word not in stopwords.words("english")]
    lemmatized = [WordNetLemmatizer().lemmatize(word) for word in words]
    return " ".join(lemmatized)


# Rank projects against a single keyphrase
def rank_texts_by_single_keyphrase(texts, keyphrase: str):
    processed_texts = [preprocess_text(text) for text in texts]
    processed_keyphrase = preprocess_text(keyphrase)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_texts + [processed_keyphrase])

    project_vectors = tfidf_matrix[:-1]
    keyphrase_vector = tfidf_matrix[-1]

    similarity_scores = cosine_similarity(project_vectors, keyphrase_vector).flatten()
    print(similarity_scores)

    sorted_indices = np.argsort(similarity_scores)[::-1]
    ranked_texts = [texts[i] for i in sorted_indices]
    ranked_scores = [similarity_scores[i] for i in sorted_indices]

    for rank, (text, score) in enumerate(zip(ranked_texts, ranked_scores), start=1):
        print(f"Rank {rank}: {text} (Score: {score:.4f})")


# Generic function to rank texts by a list of keyphrases
def rank_texts_by_keyphrases(texts, keyphrase_score_pairs: List[Tuple[str, float]]):
    processed_texts = [preprocess_text(text) for text in texts]
    processed_keyphrases = [
        preprocess_text(keyphrase) for (keyphrase, _) in keyphrase_score_pairs
    ]
    keyword_scores = [score for (_, score) in keyphrase_score_pairs]
    print(processed_keyphrases, keyword_scores)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_texts + processed_keyphrases)

    project_vectors = tfidf_matrix[: len(processed_texts)]
    keyphrase_vectors = tfidf_matrix[len(processed_texts) :]

    # Cosine similarity between all projects and all keyphrases
    similarity_scores = cosine_similarity(project_vectors, keyphrase_vectors)
    print(similarity_scores)

    # Multiple cosine similarity by the keyword's weight (from KeyBERT similarity)
    weighted_scores_matrix = similarity_scores * keyword_scores
    print(weighted_scores_matrix)

    # Sum to get total weighted similarity
    weighted_scores = np.sum(weighted_scores_matrix, axis=1)
    print(weighted_scores)

    # Rank based on weighted similarity
    sorted_indices = np.argsort(weighted_scores)[::-1]
    ranked_scores = [weighted_scores[i] for i in sorted_indices]
    ranked_texts = [texts[i] for i in sorted_indices]

    # Print and return the ranking by index, and ranked pairs of (project, similarity score)
    text_score_pairs = zip(ranked_texts, ranked_scores)
    for rank, (text, score) in enumerate(text_score_pairs, start=1):
        print(f"Rank {rank}: {text} (Score: {score:.4f})")

    # return sorted_indices, text_score_pairs
    return sorted_indices, ranked_scores, ranked_texts


# Rank projects by keyphrases
def rank_projects_by_keyphrases(
    projects, keyphrase_score_pairs: List[Tuple[str, float]], threshold=0.01
):
    project_texts = [
        f"{project['title']} {project['description']}" for project in projects
    ]

    # Get rankings for the projects
    ranks, ranked_scores, _ = rank_texts_by_keyphrases(
        project_texts, keyphrase_score_pairs
    )

    # Remove any projects with less correlation than the threshold
    res = []
    for i in range(len(ranks)):
        if ranked_scores[i] > threshold:
            res.append(projects[ranks[i]])
        else:
            break
    return res

    # Return projects in rank order
    # return [projects[i] for i in ranks]


# Rank experiences by keyphrases
def rank_experiences_by_keyphrases(
    experiences, keyphrase_score_pairs: List[Tuple[str, float]], threshold=0
):
    experience_texts = [
        f"{experience['title']} at {experience['company']} {experience['description']}"
        for experience in experiences
    ]

    ranks, ranked_scores, _ = rank_texts_by_keyphrases(
        experience_texts, keyphrase_score_pairs
    )

    # Remove any experiences with less correlation than the threshold
    res = []
    for i in range(len(ranks)):
        if ranked_scores[i] > threshold:
            res.append(experiences[ranks[i]])
        else:
            break

    return res

    # return [experiences[i] for i in ranks]


# **** EXAMPLE USAGE ****
#
# from constants import SAMPLE_RESUME
#
# rank_projects_by_single_keyphrase(SAMPLE_RESUME["projects"], "distributed systems")
#
# rank_projects_by_keyphrases(
#     SAMPLE_RESUME["projects"],
#     [
#         ("distributed systems", 200),
#         ("concurrency", 1),
#         ("consensus", 1000),
#         ("parallel", 0),
#     ],
# )
