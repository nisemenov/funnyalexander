from movies.models import Movie


def test_movie_create():
    movie = Movie.objects.create(
        title="test_title", 
        director="test_director",
        genre="test_genre",
        year=2025,
        review="test_review", 
        poster="test_poster"
    )
    assert movie
    assert Movie.objects.filter(title="test_title")
