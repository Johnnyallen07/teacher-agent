def test_simple_math(client):
    res = client.query("2+2")
    assert "4" in next(res.results).text


