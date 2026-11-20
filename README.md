# Blind Queen Mate

**Can you checkmate a lone king with king and queen while premoving everything, without ever seeing what Black plays?**

**[▶ Try the interactive board](https://anticommutator.github.io/blind-queen-mate/)**

## Rules of the puzzle

White commits to a fixed list of moves in advance. Every move in the list must be:
- **legal** whatever Black has played (the white king never steps next to a square the black king might be on, and the queen's path is never possibly blocked);
- **safe**: the queen never lands next to a square the black king might be on unless the white king protects her;
- **free of stalemate**: no square the black king might be on is ever left without a move while not in check.

The list wins if, after its last move, every square the black king could possibly be on is checkmated. Some lines mate before the list runs out.

## Results (exhaustive search)

The solver tracks the set of squares the black king could be on, and searches every reachable (white king, queen, set) state.

1. **Black king's square unknown:** impossible. For all 4032 placements of the white king and queen (White to move), no sequence exists.
2. **Black king's square known:** it depends on the position. In a sample of 600 random positions, about 60% have a premove mate (1 to 15 moves). For 17 of the others, none exists, proved by exhaustive search.
3. **One white setup works for every black king square.** Up to symmetry, exactly one placement has a premove mate for every legal black king start: **Kd4 Qf6** (equivalently Kd5 Qf3, Ke4 Qc6, Ke5 Qc3). The other 517 placements each have a black king square with no solution. The longest sequence the search needed was 10 moves.
4. **Sixteen sequences are needed.** From Kd4 Qf6, the 34 legal black king starts split into at least **16 regions**, each with one fixed sequence. Proof: only 82 of the 561 pairs of start squares can share a sequence. Every candidate group (all pairwise compatible) was then tested, and an exact set cover over the 31 largest winning groups gives 16. No group of 6 or more squares works.

| # | Black king starts on | Premove sequence |
|---|---|---|
| 1 | a1 b1 c1 d1 d2 | Qf2 Kc3 Qf1 Qd1 Qa1# |
| 2 | g1 g2 h1 h2 h3 | Qf4 Kd3 Ke2 Qg5 Kf1 Qg2 Qg6 Qg5 Qg2# |
| 3 | a2 a3 a4 b4 | Qb6 Kc3 Qa6 Qa4 Qa1# |
| 4 | a7 a8 b7 b8 c8 | Qd6 Kc4 Kb5 Qe7 Ka6 Qb7 Qf7 Qe7 Qb7# |
| 5 | e1 e2 | Ke4 Qb2 Kd3 Qd2 Qe2 Ke3 Kf3 Qg2# |
| 6 | a5 b5 | Kd5 Qb2 Kc4 Qb4 Qb5 Kc5 Kc6 Qb7# |
| 7 | g8 h7 | Kc5 Kd6 Ke7 Qg5 Kf6 Qg7# |
| 8 | b2 | Qc6 Qc4 Kd3 Kd2 Qb5 Kc1 Qb2 Qb6 Qb5 Qa4# |
| 9 | h5 | Qg7 Ke3 Kf3 Qg4 Qg2# |
| 10 | e8 | Qg7 Kc5 Kc6 Qd7 Qb7# |
| 11 | g3 | Qf5 Ke3 Qg5 Kf3 Qc1 Qh6 Qh4 Qf2# |
| 12 | c7 | Qe6 Kc5 Qe7 Kc6 Qa3 Qf8 Qd8 Qb6# |
| 13 | c2 | Kc4 Qf2 Kc3 Qf1 Qd1 Qa1# |
| 14 | b3 | Kd3 Qb6 Kc3 Qa6 Qa4 Qa1# |
| 15 | d7 | Kc5 Qg7 Qf7 Kc6 Qf8 Qd8 Qb6# |
| 16 | g4 | Ke3 Qg7 Qg6 Kf3 Qh6 Qh4 Qf2# |

The count of 16 is exact. The grouping is not unique, and the sequences are the ones the search found, not proven shortest.

## Reproducing

```sh
cd solver
cc -O2 -o kqk kqk.c
./kqk 27 45            # Kd4 Qf6: tests every black king square (squares numbered a1=0 … h8=63)
./kqk 4 3 60           # Ke1 Qd1 vs Ke8: prints -1 (no premove mate exists)
python3 cover.py       # pairs → candidate groups → minimum cover (needs pairs_results.txt from the pair run)
```

- `kqk.c`: fast exhaustive solver (best-first over belief states; prints the mate length, `-1` for none).
- `kqk.py`, `fast.py`: Python versions, which also print the move sequences.
- `scan2.py`: the unknown-king scan over all placements. `sample.py`: random known-king positions.
- `placements_results.txt`: result for each of the 518 placements distinct up to symmetry. `pairs_results.txt`: all 561 pairs. `maxwin.json`: the 31 largest winning groups.

## Related work

These study settings where White gets some information, unlike the fully blind version here:
- Kriegspiel (a referee reports illegal tries and checks): Ciancarini & Favini, *Solving Kriegspiel endings with brute force: the case of KR vs. K*; Favini's PhD thesis covers KQK.
- Fog of War / Dark chess: Gehnen & Stannat, *Fog of War Chess*, [arXiv:2601.18813](https://arxiv.org/abs/2601.18813).
