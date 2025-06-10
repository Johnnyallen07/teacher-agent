def test_simple_math(client):
    res = client.query("2+2")
    assert "4" in next(res.results).text


def test_complex_math(client):
    res = client.query("Integrate sin x * cos x from 0 to 2*pi")
    # res.results is a generator of Pod objects whose id is "Result"
    for result in res.results:
        print(result.text)

    for pod in res.pods:
        print(f"=== {pod.title} ===")
        for sub in pod.subpods:
            print(sub.plaintext)
