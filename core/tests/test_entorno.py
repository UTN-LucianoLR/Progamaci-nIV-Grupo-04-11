def test_fixtures_funcionan(ana, beto, proyecto, cliente):
    assert proyecto.memberships.count() == 2