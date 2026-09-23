import runpy


def test_session_example_runs(capsys):
    runpy.run_module("src.memory.session", run_name="__main__")
    out = capsys.readouterr().out
    # Le modèle factice recopie les messages reçus : le 3e appel voit tout l'historique.
    assert "je m'appelle Alice." in out.splitlines()[-1]
    assert "J'étudie la médecine." in out.splitlines()[-1]


def test_chap4_threads_stay_separated(capsys):
    runpy.run_module("src.chap4_memory", run_name="__main__")
    lines = {line.split(" :", 1)[0]: line for line in capsys.readouterr().out.splitlines() if " :" in line}

    assert "Alice" in lines["Alice"] and "médecine" in lines["Alice"] and "Bob" not in lines["Alice"]
    assert "Bob" in lines["Bob"] and "cybersécurité" in lines["Bob"] and "Alice" not in lines["Bob"]
    assert "Charlie" in lines["Charlie"] and "Bob" not in lines["Charlie"]
