from spicelib.log.ltsteps import LTSpiceLogReader


log = LTSpiceLogReader("4_NJF_Bias.log")

print(log.stepset)
print(log.dataset)
print(log.step_count)
