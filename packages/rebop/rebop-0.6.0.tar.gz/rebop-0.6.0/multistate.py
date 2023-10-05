import rebop
import time

kon = 0.01
koff = 0.1
kAon = 0.01
kAoff = 0.1
kAp = 0.01
kAdp = 0.1

ms = rebop.Gillespie()

ms.add_reaction(kon, ["R", "L"], ["RL"], koff)
#ms.add_reaction(koff, ["RL"], ["R", "L"])
ms.add_reaction(kAon, ["R", "Au"], ["AuR"], kAoff)
#ms.add_reaction(kAoff, ["AuR"], ["R", "Au"])
ms.add_reaction(kon, ["L", "AuR"], ["AuRL"], koff)
#ms.add_reaction(koff, ["AuRL"], ["L", "AuR"])
ms.add_reaction(kAon, ["Au", "RL"], ["AuRL"], kAoff)
#ms.add_reaction(kAoff, ["AuRL"], ["Au", "RL"])
ms.add_reaction(kAp, ["AuRL"], ["ApRL"], kAdp)
#ms.add_reaction(kAdp, ["ApRL"], ["AuRL"])
ms.add_reaction(koff, ["ApRL"], ["L", "ApR"], kon)
#ms.add_reaction(kon, ["L", "ApR"], ["ApRL"])
ms.add_reaction(koff, ["ApRL"], ["RL", "Ap"], kon)
#ms.add_reaction(kon, ["RL", "Ap"], ["ApRL"])
ms.add_reaction(kAon, ["R", "Ap"], ["ApR"], kAoff)
#ms.add_reaction(kAoff, ["ApR"], ["R", "Ap"])
ms.add_reaction(kAdp, ["ApR"], ["AuR"])
ms.add_reaction(kAdp, ["Ap"], ["Au"])

print(ms)

tic = time.time()
for _ in range(10):
    df = ms.run({"R": 5360, "L": 1160, "Au": 5360}, tmax=10, nb_steps=1000)

print((time.time() - tic) / 10)
