from src.core.runnable import run_invoke, run_batch, run_stream, run_with_retry

print("=== Invoke ===")
print(run_invoke("Donne-moi une définition simple de LangChain."))

print("\n=== Batch ===")
print(run_batch(["Donne-moi un synonyme de rapide", "Donne-moi un synonyme de heureux"]))

print("\n=== Stream ===")
run_stream("Écris un haïku sur l'intelligence artificielle")

print("\n=== With Retry ===")
print(run_with_retry("Dis bonjour après un retry"))