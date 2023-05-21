
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

# sentences = [
#     "blue shirt for men",
#     "blue demin shirt for women and men couple shirt",
# ]


model = SentenceTransformer('bert-base-nli-mean-tokens')
# sentence_embeddings = model.encode(sentences)

# print(cosine_similarity(
#     [sentence_embeddings[0]],
#     sentence_embeddings[1:]
# ))


def ranker_function(n, similarity_list, rating_list):
  #  """
  #   ------SIMILARITY SCROCES-----
    
  #   10 :  > 0.90
  #   9: >0.8 and  <0.90
  #   8: >0.7 and <0.8
  #   7: > 0.6 and < 0.7
  #   6: > 0.5 and <0.6
  #   5: >0.4 and <0.5
  #   4: >0.3 and <0.4
  #   3: >0.2 and<0.3
  #   2: <0.2
    
  #   -------SIMILARITY CREDIT - 5 -------
    
  #   ------RATING SCROCES-----
    
  #   10 :  > 4.8
  #   9: >4.5 and  <4.8
  #   8: >4.0 and <4.5
  #   7: > 3.5 and < 4.0
  #   6: > 3.0 and <3.5
  #   5: >2.5 and <3.0
  #   4: >2.0 and <2.5
  #   3: >1.5 and<2
  #   2: <1.5
    
  #   -------RATING CREDIT - 4 -------
  # """
  rank_list = [][:]
  for i in range(n):
    sim_val = similarity_list[i]
    rating_val = rating_list[i]
    
    if sim_val > 0.9:
      sim_score = 10
    elif sim_val > 0.8:
      sim_score = 9
    elif sim_val > 0.7:
      sim_score = 8
    elif sim_val > 0.6:
      sim_score = 7
    elif sim_val > 0.5:
      sim_score = 6
    elif sim_val > 0.4:
      sim_score = 5
    elif sim_val > 0.3:
      sim_score = 4
    elif sim_val > 0.2:
      sim_score = 3
    else:
      sim_score = 2
  
    if rating_val > 4.8:
      rating_score = 10
    elif rating_val > 4.5:
      rating_score = 9
    elif rating_val > 4.0:
      rating_score = 8
    elif rating_val > 3.5:
      rating_score = 7
    elif rating_val > 3.0:
      rating_score = 6
    elif rating_val > 2.5:
      rating_score = 5
    elif rating_val > 2.0:
      rating_score = 4
    elif rating_val > 1.5:
      rating_score = 3
    else:
      rating_score = 2
    
    rank = 5*sim_score + 4*rating_score
    rank/= (5 + 4)
    rank_list.append(rank)
  
  
  rank_list_index = sorted(range(len(rank_list)), key=lambda x: rank_list[x], reverse=True)
  # print(rank_list_index)
  return rank_list_index
