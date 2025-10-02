# Experimental Music

> [!warning]
> I guess any person's knowledge of experimental musics will always be limited ...

**12 tones.**
Numerous more or less experimental scales have been proposed for 12edo.
One feature of 12edo is that 12 is divisible by 2, 3, 4, and 6—many more options than other numbers of a similar size.
This provides numerous symmetries that have been exploited in the scales below.

|                       | 12edo                            |
| --------------------- | -------------------------------- |
| diminished<br />scale | 2,3,5,6,<br />8,9,11,12          |
| augmented<br />scale  | 1,4,5,<br />8,9,12               |
| whole-tone<br />scale | 2,4,6,<br />8,10,12              |
| 12-tone<br />scale    | 1,2,3,4,5,6,<br />7,8,9,10,11,12 |

Equal distance scales are not uncommon in traditional musics, byt numbers 12 and 6 are rare for an equal division, whereas 7 and 5 are much more common.

**No octaves.**
The Bohlen-Pierce tuning is a 7-limit tuning but without the octave.
It is well approximated by splitting the third harmonic into 13 equal steps.
Below is the lambda scale.

| ratio | factorisation                   | 13ed3 |
| ----- | ------------------------------- | ----- |
| 1     | $1$                             | 0     |
| 25/21 | $3^{-1}\times5^{2}\times7^{-1}$ | 2     |
| 9/7   | $3^{2}\times7^{-1}$             | 3     |
| 7/5   | $5^{-1}\times7$                 | 4     |
| 5/3   | $3^{-1}\times5$                 | 6     |
| 9/5   | $3^{2}\times5^{-1}$             | 7     |
| 15/7  | $3\times5\times7^{-1}$          | 9     |
| 7/3   | $3^{-1}\times7$                 | 10    |
| 25/9  | $3^{-2}\times5^{2}$             | 12    |
| 3     | $3$                             | 13    |

The lambda scale works well with timbres that are rich in odd harmonics but low on even harmonics (i.e. the octaves), e.g. the clarinet or square waves in synthesisers.
The \{0,6,10\} chord in 13ed3 (3:5:7 in just intonation) can be seen as corresponding to the major chord \{0,4,7\} (4:5:6) in 12edo.

**Utonality.**
Utonality is a kind of opposite to otonality.
Otonality, in turn, is just another name for the harmonic series.
Utonality can be obtained from otonality by switching the direction of all the intervals,
i.e. an interval that was ascending is now descending.
Assuming that octaves are equivalent and moving all intervals into the same octave, we get the scale below.

| ratio | cents |
| ----- | ----- |
| 1     | 0     |
| 16/15 | 112   |
| 8/7   | 231   |
| 16/13 | 359   |
| 4/3   | 498   |
| 16/11 | 649   |
| 32/21 | 729   |
| 8/5   | 813   |
| 32/19 | 902   |
| 16/9  | 996   |
| 32/17 | 1095  |

Unlike the harmonic series, utonality does not occur naturally.

**Combination product sets.**
Given a set of intervals (e.g. harmonics 1,3,5,7), a combination product set is built through the following algorithm.

0. Create a set $S$ of by multiplying each pair, triplet, etc. of intervals (e.g. $S\coloneqq\{1\times3,1\times5,1\times7,3\times5,3\times7,5\times7\}$ $= \{3,5,7,15,21,35\}$).
1. For $x$ in $S$, $x\coloneqq\frac{x}{\min S}$ (e.g. $S\coloneqq \{3/3,5/3,7/3,15/3,21/3,35/3\}$ $=\{1,5/3,7/3,5,7,35/3\}$)
2. For $x$ in $S$, divide $x$ (repeatedly) by 2 until it is less than an octave (e.g. $S\coloneqq\{1,5/3,7/6,5/4,7/4,35/24\}$)
3. Sort $S$ in the order of acending intervals (e.g. $S\coloneqq\{1,7/6,5/4,35/7,5/3,7/4\}$)

Starting from a four intervals set yields a 6-tone scale called a *hexany*.
A five intervals set yields a 10-tone scale called a *dekany*.
A six intervals set yields a 10-tone scale called an *eikosany*.

|          | cents                                                                                   |
| -------- | --------------------------------------------------------------------------------------- |
| hexany   | 272,386,655<br />888,969,1200                                                           |
| dekany   | 84,204,267,471,583,<br />702,286,969,1018,1200                                          |
| eikosany | 53,84,165,204,267,369,432,471,551,583,<br />636,702,786,818,867,969,1018,1049,1133,1200 |

## References

<details><summary>Wikipedia </summary>

- *[Octatonic scale](https://en.wikipedia.org/w/index.php?title=Octatonic_scale&oldid=1235540752)*
- *[Hexatonic scale](https://en.wikipedia.org/w/index.php?title=Hexatonic_scale&oldid=1272973815)*
- *[Twelve-tone technique](https://en.wikipedia.org/w/index.php?title=Twelve-tone_technique&oldid=1270565378)*
- *[Bohlen-Pierce scale](https://en.wikipedia.org/w/index.php?title=Bohlen%E2%80%93Pierce_scale&oldid=1268289453)*
- *[Otonality and utonality](https://en.wikipedia.org/w/index.php?title=Otonality_and_utonality&oldid=1244997284)*
- *[Hexany](https://en.wikipedia.org/w/index.php?title=Hexany&oldid=1208478592)*

</details>

<details><summary>Xenharmonic Wiki</summary>

- *[Otonality and utonality](https://en.xen.wiki/index.php?title=Otonality_and_utonality&oldid=156337)*
- *[Combination product set](https://en.xen.wiki/index.php?title=Combination_product_set&oldid=169344)*
- *[Hexany](https://en.xen.wiki/index.php?title=Hexany&oldid=172064)*
- *[Dekany](https://en.xen.wiki/index.php?title=Dekany&oldid=172054)*

</details>

12tone. *[The Tonality Cube](https://www.youtube.com/watch?v=-GeR8XbFxvI)*. YouTube.

Kraig Grady. [The hexany, the eikosany, and the other combination product sets](https://web.archive.org/web/2/https://anaphoria.com/wilsoncps.html)* The Wilson Archives (anaphoria.com).