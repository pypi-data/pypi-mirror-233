from models import CircuiTree
from models import SimpleNetworkGrammar
from parallel import MultithreadedCircuiTree
from time import sleep


# class TestTree(SimpleNetworkGrammar, MultithreadedCircuiTree):
class TestTree(SimpleNetworkGrammar, CircuiTree):
    def get_reward(self, state, *args, **kwargs):
        if self.has_motif(state, "AAa_ABa_BAi"):
            return 1.0
        else:
            return 0.0


if __name__ == "__main__":
    mtree = TestTree(
        root="ABC::",
        components=["A", "B", "C"],
        interactions=["activates", "inhibits"],
        # save_dir="/tmp/circuitree-tmp",
    )

    n_steps = 1_000
    for step in range(n_steps):
        print(f"step {step}")
        sel_path, reward, sim_node = mtree.traverse()
        print(f"\tsel_path: {sel_path}")
        print(f"\tsim_node: {sim_node}")
        print(f"\treward: {reward}")
        
        ...
    
    ...