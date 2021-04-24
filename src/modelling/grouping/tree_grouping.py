import numpy as np
import edlib


def group_news(df, tree, embs, debug=False, r_min=0.01, r_max=4.0, r_start=0.25, r_step=0.1, vc_min=0.01, vc_max=0.04, delta_max=0.01):

    '''
    NEWS GROUPING LOGIC
    :param df: dataframe with news
    :param tree: KDtree built on embs for the data in df
    :param embs: embeddings for each text created with the NN used for multiclass classification
    :return:
    '''
    
    total = len(df)
    grouped_ind = []  # creating a list to store papers already used in other groups
    news_groups = []  # groups of news
    ungrouped_list = []  # herea will be papers ungrouped due to the strict logic

    for index, rows in df.iterrows():

        if index in grouped_ind:
            pass

        else:
            if debug:
                print(index, '/', total)

            r_curr = r_start
            variative_criterium_norm = vc_min + 0.0000001
            flag_single = 0
            delta = 0

            # defining the search radius individually for each news group
            while vc_max > variative_criterium_norm > vc_min and r_max > r_curr > r_min and delta < delta_max:
                #print(embs[index])
                ind = tree.query_radius(np.array([embs[index]]), r=r_curr)

                # checking that we have more than 0 results for the current query
                if len(ind[0]) > 1.0:

                    # this guarantees that we shall not go to the second curcle of radius increase
                    if flag_single > 0.1:
                        flag_single = 10

                    variative_criterium = 0.

                    # clac variative criterium
                    for j in range(len(ind[0])):
                        if debug:
                            print(df.title[ind[0][j]])

                        if len(ind[0]) > j+1:
                            a = df.title[ind[0][j]]
                            b = df.title[ind[0][j + 1]]
                            delta = edlib.align(a, b)['editDistance'] / np.average([len(a), len(b)])
                            variative_criterium += delta

                    variative_criterium_norm = variative_criterium / len(ind[0])
                    r_curr -= r_step
                    if debug:
                        print('VC:', variative_criterium_norm, '\n', 'r:', r_curr, '\n' * 2)

                else:
                    #print(df.title[ind[0][0]])
                    if flag_single < 5:
                        flag_single +=1
                        variative_criterium = vc_min + 0.1
                        r_curr += 5*r_step
                        if debug:
                            print('VC:', variative_criterium_norm, '\n', 'r:', r_curr, '\n' * 2)
                    else:
                        break     
                        

            # SIMPLISTIC groups grouping logic - ver 3.0
            if len(ind[0]) > 0.1:
                news_groups.append(list(ind[0]))
                grouped_ind.extend(list(ind[0]))
        
    # Preparing output    
    groups_out = []
    groups_titles = []
    
    for group in news_groups:
        
        groups_out.append({'title': df['title'][group[0]], 'articles': [df['id'][paper] for paper in group]})
        titles = [df.title[paper] for paper in group] 
        groups_titles.append(titles)   
      
    return news_groups #, groups_out, groups_titles