from typing import List


def is_valid_split(split: dict) -> bool:
    """
        The expected dictionary should be as follows, first indexing by set 
        and then by genre, to obtain a list of indices representing the songs 
        in the dataset that belong to a specific set and genre.
        
        `For example`:
        
        ```
        split = {
            'train': {
                'blues': [11, 1, 4, 5],
                'classical': [43, 23, 32, 4],
                ...
            }
            'val': {
                ...   
            }
            'test' : {
                ...
            }
        }
        ```
    """
    
    GENRES = {'blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock'}
    
    if set(split.keys()) != {'test', 'train', 'val'}:
        # missing sets in the split
        return False

    for _, genres in split.items():
        if isinstance(genres, dict):
            if set(genres.keys()) != GENRES:
                # missing genres in the split
                return False
            
            amount = -1
            for _, indexs in genres.items():
                if isinstance(indexs, List):

                    if amount == -1:
                        amount = len(indexs)
                
                    if amount != len(indexs):
                        return False

                else:
                    # sintax error
                    return False
        else:
            # sintax error
            return False

    return True
