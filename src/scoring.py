def score_game(review_count, discount_percent):
    """
    Weighted scoring: reviews 70%, discount 30%.
    Larger titles are prioritized, while significant discounts still
    contribute without dominating the ranking.
    """
    score = (review_count / 1000) * 0.7 + (discount_percent * 0.3)
    return score