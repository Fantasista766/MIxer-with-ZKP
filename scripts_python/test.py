import json

with open('proof.txt', 'r') as infile:
    proof_data = infile.read()
proof_data = json.loads(proof_data)
_pA, _pB, _pC, _pubSignals = proof_data

_pA = [int(i, 16) for i in _pA]
_pB = [[int(j, 16) for j in i] for i in _pB]
_pC = [int(i, 16) for i in _pC]
_pubSignals = [int(i, 16) for i in _pubSignals]

data = [_pA, _pB, _pC, _pubSignals]
for d in data:
    print(d)
