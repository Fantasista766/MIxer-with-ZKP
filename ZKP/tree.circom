pragma circom 2.1.6;

include "/home/dima/circomlib/circuits/mimcsponge.circom";

template CalculateRoot(K) {
    // k - глубина дерева
    signal input leafHash;
    signal input proofHashes[K];
    signal output root; // Use the root signal

    signal tmpRoots[K + 1];

    tmpRoots[0] <== leafHash;

    component mimcSponges[K];

    for (var i = 0; i < K; i++) {
        mimcSponges[i] = MiMCSponge(2, 2, 1);  
        mimcSponges[i].ins <== [tmpRoots[i], proofHashes[i]];
        mimcSponges[i].k <== 2;
        tmpRoots[i + 1] <== mimcSponges[i].outs[0];
    }

    root <== tmpRoots[K];
}

template MerkleProof(K) {
    signal input leafHash;
    signal input proofHashes[K];
    signal output merkleRoot;

    component calculateRoot = CalculateRoot(K);
    calculateRoot.leafHash <== leafHash;
    calculateRoot.proofHashes <== proofHashes;
    calculateRoot.root ==> merkleRoot;
}

component main = MerkleProof(2);
