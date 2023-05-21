# rankSimilarClothingItems

Api that scarps information from amazon and gives a list of most relevant similar item links in json format.

### Setup Intructions (For windows)
1. Installation
```
pip install -r requirement.py
```
2. Run server

```
python manage.py runserver
```
### Setup Instructions (For Ubuntu)
https://www.digitalocean.com/community/tutorials/how-to-install-django-and-set-up-a-development-environment-on-ubuntu-16-04

### Video Demonstration:
In thr folder **Working Video** (See Above)


### Phases In project
1. Phase 1: Api call and input data
2. Phase 2: Scrapping relevent information and store it
3. Phase 3: Calculating similarity between input text and  descriptions
4. Phase 4: Calculate ranks based on similarity and rating 
5. Phase 5: return a json response of relevent links

### Phase 1 : Api call and Input data

Api are written using Django framework.

Mehtods: GET and POST

GET: In get method the api return a json of the sucess code

POST: In post method the api returns a json with the revent and ranked list of links

```py
@api_view(['GET', 'POST'])
def get_ranked_list(request,*args, **kwargs):
    if request.method == 'POST':
        print('request:', request.data) 
        input_data = request.data['input_data'] #input data extraction 
        content = ranked_list_maker(input_data) #ranked list of list generation
        return Response(content) #json response
    content = {'success': 200}
    return Response(content) #json response
 ```
### Phase 2 : Scrapping relevent information and store it

Beautifulsoup4 is used for the scrapping. 

To scrap information related to the search input we used the amazon search query : 
```py
f"https://www.amazon.com/s?k={input_data}"
```
here input_data is the input description provided by the user

Once the entire information about the input information is scrapped. We sagregate information for price, rating, etc.

This segregation is done using different tags on the site:

For example:
```py
def get_price(soup):
        try:
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip() #retriving price by class attribute

        except:
            price = ""
    return price
  ```
  
 There majorly five active functions:
 ```
 get_title(soup)
 get_price(soup)
 get_rating(soup)
 get_review_count(soup)
 get_availiability(soup)
 ```
 as the name suggests each of these functions retrieves title, price, rating, review count and availiability of the products on a page respectively.
 
 Once the information is retrieved it is store in a python dictionary
 
 ```py
 d = {
 'title' : [title1, title2,....]
 'price' : [price1, price2,....]
 'rating': [rating1, rating2,...]
 'review': [review1,review2,....]
 'availiability': [availiability1,....]
 }
 ```
 
 ### Phase 3 : Calculating similarity between input text and  descriptions
 
 To calulate similarity between the input text and the product title(as amazon has generic title) BERT model and cosine similarity function is used.
 
 Using pre trained BERT model:
 ```py
 from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

# sentences = [
#     "blue shirt for men",
#     "blue demin shirt for women and men | medium | stylish",
# ]


model = SentenceTransformer('bert-base-nli-mean-tokens') #BERT model
```

Computing the similarity between the input and titles

```py
sentences = [input_data] + d['title']
    sentence_embeddings = model.encode(sentences) #encoding in BERT model
    
    #conine similarity 
    similarity_list = cosine_similarity(
    [sentence_embeddings[0]],
    sentence_embeddings[1:]
)
    similarity_list = list(similarity_list[0])

```

This main output of this phase is ```similarity_list```. It is list of the % of similary between input description and the title of each product.


### Phase 4 : Calculate ranks based on similarity and rating

In this phase we are equipped with two important factor of each product namely ```similarity_list``` and ```rating```.

We fit both these charactering into the  ranker formula( defined below)  and assigned to it's respective product.

Ranker Formula:
```
          C1G1 + C2G2 + ...
score = _____________________
          C1 + C2 + ....
          
  C1 = item credit
  G1 = item points
```

Here the item credit and item points for similarity:

```
"""
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
  ```
  
  Here is the item credit and item points for rating
  ```
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
    
  #   -------RATING CREDIT - 4 ------
  ```
  For each value of similarity and rating of a particular product is fed into the formula in the function ```ranker_function``` and final evaluation value is generated per product
  
Ranker function

```py

def ranker_function(n, similarity_list, rating_list):
 
  rank_list = [][:] #rank list
  
  for i in range(n):
    sim_val = similarity_list[i]
    rating_val = rating_list[i]
    
    # item point calculation of similarity
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
      
    # item point calculation of rating
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
      
    #apllying ranker formula
    rank = 5*sim_score + 4*rating_score
    rank/= (5 + 4)
    rank_list.append(rank)
    
    rank_list_index = sorted(range(len(rank_list)), key=lambda x: rank_list[x], reverse=True) # reverse sorted list of indexes
  # print(rank_list_index)
  return rank_list_index
  ```

Once the final evaluation score are calucated just sort the list in reverse order but the only catch instead of storing the evaluation values we make a **hash table** indexes of the sorted values and store them.
 
### Phase 5 : Return a json response of relevent links

In this final phase using the sorted hashes we created a ranked dictionary and convert it into json

Ranked dictionary:

```py
ranked_dict = { 1 : [title1,rating1, price1, review_count1, avaliability1] ,....}
```






  
