import warnings

# Suppress only the specific FutureWarning related to clean_up_tokenization_spaces
def manage_warning():   
    warnings.filterwarnings(
        "ignore", 
        category=FutureWarning, 
        message=r"`clean_up_tokenization_spaces` was not set"
    )