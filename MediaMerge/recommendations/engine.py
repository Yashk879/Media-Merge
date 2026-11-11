from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from media_assets.models import MediaAsset

def recommend_for_user(user, limit=10):
    assets = list(MediaAsset.objects.filter(status="ready").prefetch_related("categories"))
    if not assets:
        return []

    watched = set(user.watch_history.values_list("asset_id", flat=True))
    watched_assets = [a for a in assets if a.id in watched]

    def text(asset):
        cats = " ".join(c.name for c in asset.categories.all())
        tags = " ".join(asset.tags or [])
        return f"{asset.title} {asset.description} {cats} {tags}"

    corpus = [text(a) for a in assets]
    matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus)

    if not watched_assets:
        return sorted(assets, key=lambda x: x.view_count, reverse=True)[:limit]

    watched_indices = [assets.index(a) for a in watched_assets]
    profile = matrix[watched_indices].mean(axis=0)
    scores = cosine_similarity(profile, matrix).flatten()

    ranked = sorted(
        [(score, asset) for score, asset in zip(scores, assets) if asset.id not in watched],
        key=lambda x: x[0],
        reverse=True,
    )
    return [asset for _, asset in ranked[:limit]]
