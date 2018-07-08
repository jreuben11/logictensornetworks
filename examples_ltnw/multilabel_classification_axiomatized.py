# -*- coding: utf-8 -*-
import logictensornetworks_wrapper as ltnw
import logging
logger = logging.getLogger()
logger.basicConfig = logging.basicConfig(level=logging.DEBUG)

import numpy as np
import matplotlib.pyplot as plt

nr_samples=1000
max_iterations=20000

data=np.random.uniform([0,0],[1.,1.],(nr_samples,2)).astype(np.float32)
data_A=data[np.where(np.sum(np.square(data-[.5,.5]),axis=1)<.09)]
data_B=data[np.where(np.sum(np.square(data-[.5,.5]),axis=1)>=.09)]
data_A,data_B=data_A[:min(len(data_A),len(data_B)),:],data_B[:min(len(data_A),len(data_B)),:]

print("# samples data_A: %s" % len(data_A))
print("# samples data_B: %s" % len(data_B))
print("# samples data: %s" % len(data))

ltnw.predicate("A",2)
ltnw.predicate("B",2)

ltnw.variable("?data_A",data_A)
ltnw.variable("?data_B",data_B)
ltnw.variable("?data",data)

ltnw.formula("forall ?data_A: A(?data_A)")
ltnw.formula("forall ?data_B: B(?data_B)")

ltnw.formula("forall ?data: A(?data) -> ~B(?data)")
ltnw.formula("forall ?data: ~B(?data) -> A(?data)")

ltnw.initialize_knowledgebase(initial_sat_level_threshold=.1)
sat_level=ltnw.train(max_iterations=max_iterations)

plt.figure(figsize=(10,8))
result=ltnw.ask("A(?data)")
plt.subplot(2,2,1)
plt.title("A(x) - training")
plt.scatter(data[:,0],data[:,1],c=result.squeeze())

result=ltnw.ask("B(?data)")
plt.subplot(2,2,2)
plt.title("B(x) - training")
plt.scatter(data[:,0],data[:,1],c=result.squeeze())

data_test=np.random.uniform([0,0],[1.,1.],(nr_samples,2)).astype(np.float32)
ltnw.variable("?data_test",data_test)
result=ltnw.ask("A(?data_test)")

plt.subplot(2,2,3)
plt.title("A(x) - test")
plt.scatter(data_test[:,0],data_test[:,1],c=result.squeeze())

result=ltnw.ask("B(?data_test)")
plt.subplot(2,2,4)
plt.scatter(data_test[:,0],data_test[:,1],c=result.squeeze())
plt.title("B(x) -test")
plt.show()

ltnw.constant("a",[0.5,.5])
ltnw.constant("b",[0.75,.75])
print("a is in A: %s" % ltnw.ask("A(a)"))
print("b is in A: %s" % ltnw.ask("A(b)"))
print("a is in B: %s" % ltnw.ask("B(a)"))
print("b is in B: %s" % ltnw.ask("B(b)"))
