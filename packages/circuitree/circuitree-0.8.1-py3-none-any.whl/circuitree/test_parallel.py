from models import SimpleNetworkGrammar
from parallel import MultithreadedCircuiTree
from time import sleep


class TestTree(SimpleNetworkGrammar, MultithreadedCircuiTree):
    def get_reward(*a, **kw):
        print("sleeping")
        sleep(4)
        print("done sleeping")
        return 1.0


if __name__ == "__main__":
    mtree = TestTree(
        root="ABC::",
        components=["A", "B", "C"],
        interactions=["activates", "inhibits"],
        save_dir="/tmp/circuitree-tmp",
    )

    mtree.traverse(0)

    ...
