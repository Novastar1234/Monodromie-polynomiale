from pathlib import Path
import subprocess

EXECUTABLE = (
    Path(__file__).resolve().parent
    / "Ocaml"
    / "schreier_sims_cli"
)


def est_generateur_from_str(permutations: list[str]) -> bool:
    if not EXECUTABLE.exists():
        raise FileNotFoundError(
            f"Executable not found: {EXECUTABLE}\n"
            "Compile it with:\n"
            "ocamlopt -o Ocaml/schreier_sims_cli "
            "Ocaml/schreier_sims.ml Ocaml/main.ml"
        )

    result = subprocess.run(
        [str(EXECUTABLE), *permutations],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or f"OCaml exited with code {result.returncode}"
        )

    output = result.stdout.strip().lower()

    if output == "true":
        return True
    if output == "false":
        return False

    raise ValueError(f"Unexpected OCaml output: {result.stdout!r}")

def perm_to_string(perm):
    ans=str(perm[0])
    for i in range(1,len(perm)):
        ans+= " " + str(perm[i])
    return ans
def est_generateur(perms):

    return est_generateur_from_str (list(map(perm_to_string, perms)))

#TEST
#def transpo(i,j,n):
#    ans = [i for i in range(n)]
#    ans[i],ans[j]=j,i
#    return ans
#assert( est_generateur([transpo(0, i, 100) for i in range(1, 100)]))
