# Pythagorean Tuning

Pythagorean tuning is a kind of just tuning (i.e., based on rational numbers).
Although, it is named after Pythagoras of triangle-fame and his followers, pythagorean tuning precedes them.
It seems to have been independently developed in the Middle East and China.
It is based on multiplying and dividing the frequencies by 2 and 3 (the second and third harmonics).
For this reason, it is also called a 3-limit tuning.
The octave is 2, the perfect fifth 3/2, and the perfect fouth 4/3.
The tuning is calculated in algorithmic steps:

0. Start at an arbitrary initial frequency.
1. Multiply last frequency with 3/2
2. Divide last frequency with 4/3

Continue by repeating steps 1. and 2.

- If you go up to step 5., you get a major pentatonic scale.
- If you go up to step 7., you get a lydian scale (a mode of the major scale).
- if you go up to step 12., you get a chromatic scale.

An issue is that step 13. is nearly but not quite an octave.
The resulting unevenness is often considered unpleasant.
A solution is to equally split the octave in 12 steps (12edo).
This results in equal temperament, i.e. all intervals apart from the octave are slightly off.
If you continue until step 53., you end up closer to the octave,
and, therefore, 53edo has a very small error.

The table below shows a 17-tone Pythagorean scale proposed by Medieval Iranian music theorist صفی الدین اورموی (Safi al-Din al-Urmawi al-Baghdadi).
Furthermore, you can see comparisons to different temperaments.


| ratio          | factorisation         | 17edo | error <br /> (cents) | 24edo | error <br /> (cents) | 29edo | error <br /> (cents) | 53edo | error <br /> (cents) |
| -------------- | --------------------- | ----- | -------------------- | ----- | -------------------- | ----- | -------------------- | ----- | -------------------- |
| 1              | $1$                   | 0     | 0.00                 | 0     | 0.00                 | 0     | 0.00                 | 0     | 0.00                 |
| 256/243        | $2^{8}\times3^{-5}$   | 1     | -19.64               | 2     | 9.78                 | 2     | -7.47                | 4     | 0.34                 |
| 65536/59049    | $2^{16}\times3^{-10}$ | 2     | -39.27               | 3     | -30.45               | 4     | -14.93               | 8     | 0.68                 |
| 9/8            | $2^{-3}\times3^{2}$   | 3     | 7.85                 | 4     | -3.91                | 5     | 2.99                 | 9     | -0.14                |
| 32/27          | $2^{5}\times3^{-3}$   | 4     | -11.78               | 6     | 5.87                 | 7     | -4.48                | 13    | 0.20                 |
| 8192/6561      | $2^{13}\times3^{-8}$  | 5     | -31.42               | 7     | -34.36               | 9     | -11.95               | 17    | 0.55                 |
| 81/64          | $2^{-6}\times3^{4}$   | 6     | 15.71                | 8     | -7.82                | 10    | 5.97                 | 18    | -0.27                |
| 4/3            | $2^{2}\times3^{-1}$   | 7     | -3.93                | 10    | 1.96                 | 12    | -1.49                | 22    | 0.07                 |
| 1024/729       | $2^{10}\times3^{-6}$  | 8     | -23.56               | 12    | 11.73                | 14    | -8.96                | 26    | 0.41                 |
| 262144/177147  | $2^{18}\times3^{-11}$ | 9     | -43.20               | 13    | -28.49               | 16    | -16.43               | 30    | 0.75                 |
| 3/2            | $2^{-1}\times3^{1}$   | 10    | 3.93                 | 14    | -1.96                | 17    | 1.49                 | 31    | -0.07                |
| 128/81         | $2^{7}\times3^{-4}$   | 11    | -15.71               | 16    | 7.82                 | 19    | -5.97                | 35    | 0.27                 |
| 32768/19683    | $2^{15}\times3^{-9}$  | 12    | -35.35               | 17    | -32.40               | 21    | -13.44               | 39    | 0.61                 |
| 27/16          | $2^{-4}\times3^{3}$   | 13    | 11.78                | 18    | -5.87                | 22    | 4.48                 | 40    | -0.20                |
| 16/9           | $2^{4}\times3^{-2}$   | 14    | -7.85                | 20    | 3.91                 | 24    | -2.99                | 44    | 0.14                 |
| 4096/2187      | $2^{12}\times3^{-7}$  | 15    | -27.49               | 22    | 13.69                | 26    | -10.45               | 48    | 0.48                 |
| 1048576/531441 | $2^{20}\times3^{-12}$ | 16    | -47.13               | 23    | -26.54               | 28    | -17.92               | 52    | 0.82                 |
| 2              | $2$                   | 17    | 0.00                 | 24    | 0.00                 | 29    | 0.00                 | 53    | 0.00                 |

## References

Ozan Yarman. 2007. *[A Comparative Evaluation of Pitch Notations in Turkish Makam Music: Abjad Scale & 24-Tone Pythagorean Tuning – 53 Equal Division of the Octave as a Common Grid](https://web.archive.org/web/20241227163624/https://musicstudies.org/wp-content/uploads/2017/01/Abjad_JIMS_071203.pdf)*. Journal of interdisciplinary music studies.

Wikipedia. *12 Equal Temperament*. Section *[History](https://en.wikipedia.org/w/index.php?title=12_equal_temperament&oldid=1227218014#History)*.