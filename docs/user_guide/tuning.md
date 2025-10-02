## Tunings

I have tried to cover tunings from all parts of the world, but you should certainly not take this as a complete collection.[^world]

<table><tr><td>equal divisions of the octave (edos)<br />
🟥🟧🟥🟧🟥🟥🟧🟥🟧🟥🟧🟥<br />
other equal divisions<br />
🟥🟪🟥🟪🟥🟥🟪🟥🟪🟥🟪🟥<br />
equal Hz steps<br />
🟦🟪🟦🟪🟦🟦🟪🟦🟪🟦🟪🟦<br />
ombak<br />
🟦🟩🟦🟩🟦🟦🟩🟦🟩🟦🟩🟦<br />
unequal (e.g. just intonation, subsets)<br />
🟨🟩🟨🟩🟨🟨🟩🟨🟩🟨🟩🟨
</td></tr></table>

Above, there are five different classes of tunings.
On the exquis, pads are assigned different colors depending on their corresponding keys on the keyboard.
Some pads are not lit:

- Standard (12 tones per octave).
Pads corresponding to white keys are lit.
Pads corresponding to black keys are dark.
Only used for the default 12edo tuning.
- Macrotonal (≤12 tones per octave).
Pads corresponding to every other octave on the keyboard are lit.
The other octaves are dark.
Muted keys lack corresponding pads.
- Microtonal (≥12 tones per octave).
Pads corresponding to both white and black keys are lit.
Pads corresponding to notes in between the keys are dark.

The Halberstadt mapping is outlines below.
Two manuals are illustrated.
Depending on how sharp the sharps and double-sharps (# and x) are, the lower manual may be the same as the upper or one step lower.

$$\begin{matrix} \ & \ & \mathrm{d\flat} & \mathrm{e\flat} & \ & \mathrm{g\flat} & \mathrm{a\flat} & \mathrm{B\flat} & \
\cr \ &\mathrm{c} & \mathrm{d} & \mathrm{e} & \mathrm{f} & \mathrm{g} & \mathrm{A} & \mathrm{B} & \mathrm{C}
\cr \ & \ & \ & \ & \ & \ & \ & \ & \
\cr \ & \mathrm{c\sharp} & \mathrm{d\sharp} & \ & \mathrm{f\sharp} & \mathrm{g\sharp} & \mathrm{A\sharp} & \ & \ 
\cr \mathrm{b\sharp} & \mathrm{c\times} & \mathrm{d\times} & \mathrm{e\sharp} & \mathrm{f\times} & \mathrm{g\times} & \mathrm{A\times} & \mathrm{B\sharp} & \ \end{matrix}$$

The keynames are replaced with various numbers in the tunings below.
The numbers represent steps, ratios, or frequencies.
The following symbols are also used.

<table>
<tr><td>subscript</td><td>notes switchable through key or pedal presses</td></tr>
<tr><td> □ </td><td>not mapped to any note</td></tr>
<tr><td>+,-</td><td>if after a number, pengumbang or pengisep respectively, else as usual
<tr><td>/,[]</td><td>ditto/repeat marks (in ratios, / functions as usual)</td></tr>
</table>

Full details of the tunings can be found and edited in [src/mtsesp_master/presets/tunings.py](src/mtsesp_master/presets/tunings.py).

[^world]: There are multiple cultures I have failed to acquire enough information about. Pre-colonial American cultures are particularly absent. It feels like it should be possible to find scales on flutes from archaelogical excavations—especially from the Maya, Aztec, and Anazasi cultures. Furthermore, there ought to be knowledge about scales in Inuit throat singing. In Africa, southern parts might hold a distinct musical culture from the interactions between the Khoisan and Bantu peoples in e.g. the Xhosa Kingdom. Furthermore, I have found very little information about tuning the tube zither from Madagascar apart from that it is roughly diatonic. Finally, Polynesian music is supposedly distinct from other Austronesian music traditions.

⚫⚫
**5edo -10Hz (ombak).**
Roughly 240¢ steps.
Approximates the sléndro scale in [Indonesian classical music](learn/indonesian.md).
Alternating pengumbang ang pengisep notes, with pengisep in 5edo and pengumbang 10Hz lower.
Mapped to black keys.
See also *15edo*.

$$\begin{matrix} & & 0 & 1 & & 2 & 3 & 4 &
\cr & \Box & \Box & \Box & \Box & \Box & \Box & \Box & \Box
\cr & \ & \ & \ & \ & \ & \ & \ & \
\cr & {0-} & {1-} & & {2-} & {3-} & {4-} & &
\cr \Box & \Box & \Box & \Box & \Box & \Box & \Box & \Box & \end{matrix}$$

⚫🔴
**Hexany (uneven).**
A 6-tone scale in just intonation.
A combination product set used in [experimental musics](learn/experimental.md).

$$\begin{matrix} & \Box & \Box & & 35/7 & 5/3 & 7/4 & \cr 1 & 7/6 & 5/4 & \Box & \Box & \Box & \Box & 2\end{matrix}$$

⚫🟠
**43Hz B&flat;=413Hz.**
Uneven in terms of cents but even in terms of Hz.
Possibly used in [Ancient Andean music](learn/andean.md).
Mapped to black keys plus the D-key.

$$\begin{matrix} & -215\mathrm{Hz} & -129\mathrm{Hz} & & -86\mathrm{Hz} & -43\mathrm{Hz} & \mathrm{B\flat} & 
\cr \Box & -172\mathrm{Hz} & \Box & \Box & \Box & \Box & \Box & \Box\end{matrix}$$

⚫🟡
**Narrow 13ed3.**
146¢ steps.
Also known as the equally tempered Bohlen–Pierce scale.
Used in [experimental music](learn/experimental.md).
Mapped to white keys.

$$\begin{matrix} & \Box & \Box & & \Box & \Box & \Box &
\cr 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7\end{matrix}$$


⚫🟢
**20Hz A=440Hz.**
The [harmonic series](learn/harmonic.md).
An important concept in many musics.
Used more literally in [Mongolian throat singing](learn/mongolian.md) and [Chinese guqin music](learn/chinese.md).
Mapped to the white keys.

$$\begin{matrix} & \Box & \Box & & \Box & \Box & \Box &
\cr -100\mathrm{Hz} & -80\mathrm{Hz} & -60\mathrm{Hz} & -40\mathrm{Hz} & -20\mathrm{Hz} & \mathrm{A} & +20\mathrm{Hz} & +40\mathrm{Hz}\end{matrix}$$

⚫🔵
**9edo +8Hz (ombak).**
Roughly 133¢ steps.
Approximates the pélog scales in [Indonesian classical music](learn/indonesian.md).
Alternating pengumbang ang pengisep notes, with pengumbang in 9edo and pengisep 8Hz higher.
Common pélog scales are mapped to the black keys.
The B, C, E, and F-keys can be used as accidentals.

$$\begin{matrix} & & 1+ & 2+ & & 5+ & 6+ & 7+ & &
\cr & 0+ & \Box & 3+ & 4+ & \Box & \Box & 8+ & 9+
\cr & \ & \ & \ & \ & \ & \ & \ & \
\cr & 1 & 2 & & 5 & 6 & 7 &
\cr 0 & \Box & 3 & 4 & \Box & \Box & 8 & 9 & \end{matrix}$$

⚫🟣
**Dekany (uneven).**
A 10-tone scale in just intonation.
A combination product set used in [experimental music](learn/experimental.md).



⚫⚪
**11 huis (uneven).**
Series of notes $1\leq p/q\leq2$ for $p,q\in\mathbb{N}$.
Coincides with the notes produced by pinching technique (an yin) on hui 7 and above in [Chinese guqin music](learn/chinese.md).
In addition, it includes the unmarked 7/6, 7/5, and 7/4.
The G#/Ab key is muted and A is the root.

$$\begin{bmatrix} & 5/8 & 7/10 & & 5/6 & \Box & 8/7& \cr 3/5 & 2/3 & 3/4 & 4/5 & 7/8 & 1 & 7/6 & 6/5\end{bmatrix}$$

🔴⚫
**11 harmonics (uneven).**
Series of notes $1\leq p/2^{n} \leq2$ for $p,n\in\mathbb{N}$.
The [harmonic (otonal) series](learn/harmonic.md) reduced into an octave.
Coincides with the notes produced by guqin flageolet technique, 泛音 (fan yin), or any flageolet techniques on any other instruments, e.g. guitar, for that matter.
The D key is muted and F is the root.

$$\begin{bmatrix} & 13/16 & 7/8 & & 17/16 & 19/16 & 21/16 &
\cr 3/8 & \Box & 15/16 & 1 & 9/8 & 5/4 & 11/8 & 3/2 \end{bmatrix}$$


🔴🔴
**11 subharmonics (uneven).**
Series of notes $1\leq2^{n}/q \leq2$ for $q,n\in\mathbb{N}$.
The [subharmonic (utonal) series](learn/experimental.md) reduced into an octave.
Used in experimental music.
The G#/Ab key is muted and F is the root.

$$\begin{bmatrix} & 4/5 & 8/9 & & 16/15 & \Box & 4/3 &
\cr 16/21 & 16/19 & 16/17 & 1 & 8/7 & 16/13 & 16/11 & 32/21 \end{bmatrix}$$

��🟠
**12edo ±3Hz ombak.**
Approximates the pélog scales in [Balinese classical music](learn/indonesian.md).
Alternating pengumbang ang pengisep notes, with pengumbang 3Hz lower than 12edo and pengisep 3Hz higher.
Without ombak, it can also simulate an untuned piano.

$$\begin{matrix} & & 1+ & 3+ & & 6+ & 8+ & 10+ &
\cr & 0+ & 2+ & 4+ & 5+ & 7+ & 9+ & 11+ & 12+
\cr & \ & \ & \ & \ & \ & \ & \ & \
\cr & 1- & 3- & & 6- & 8- & 10- & &
\cr 0- & 2- & 4- & 5- & 7- & 9- & 11- & 12- &
\end{matrix}$$

DEFAULT
🔴🟡
**12edo.**
100¢ steps.
"Normal" tuning.
Approximates the perfect fifth well.
Was independently discovered in [China](learn/east_asian.md) and [Europe](learn/european.md).
From China, it influencedd [Japanese music](learn/japanese.md).
From Europe, it influenced [Romani music](learn/romani.md) and [American music](learn/american.md).
It is good for approximating [Ethiopian secular music](learn/ethiopian.md), and is used to approximate most of the rest of the world's music despite not being optimal.
Indeed, most contemporary music is in 12edo.

$$\begin{matrix} & 1 & 3 & & 6 & 8 & 10 &
\cr 0 & 2 & 4 & 5 & 7 & 9 & 11 & 12 \end{matrix}$$

**Wide 8edPhi.**
The Sevish golden ratio scale.

$$\begin{matrix} & 1 & 3 & & 6 & 8 & 10 &
\cr 0 & 2 & 4 & 5 & 7 & 9 & 11 & 12 \end{matrix}$$

🔴🟢
**10Hz A=441Hz.**
Approximates [Australian aboriginal music](learn/australian.md).

$$\begin{matrix} & -80\mathrm{Hz} & -60\mathrm{Hz} & & -30\mathrm{Hz} & -10\mathrm{Hz} & +10\mathrm{Hz} &
\cr -90\mathrm{Hz} & -70\mathrm{Hz} & -50\mathrm{Hz} & -40\mathrm{Hz} & -20\mathrm{Hz} & \mathrm{A} & +20\mathrm{Hz} & +30\mathrm{Hz} \end{matrix}$$

🔴🔵
**Wide 8ed3/2.**
88¢ steps.
The 4ed3/2 subset is used in [Georgian traditional music](learn/georgian.md).
This subset is mapped to white keys.

$$\begin{matrix} \ & 1 & 3 & \ & 7 & 9 & 11 & \
\cr 0 & 2 & 4_5 & 6 & 8 & 10 & 12_{13} & 14 \end{matrix}$$

🔴🟣 
**14edo.**
86¢ steps.
The 7-note subset approximates scales used by many cultures around the world such as in [Thai classical music](learn/thai.md), [Bantu traditional music](learn/bantu.md), [Melanesian traditional music](learn/melanesian.md) and, for bala, in [Malian classical music](learn/malian.md).
It was possibly used in [ancient Andean music](learn/andean.md).

$$\begin{matrix} \ & 1 & 3 & \ & 7 & 9 & 11 & \
\cr 0 & 2 & 4_5 & 6 & 8 & 10 & 12_{13} & 14 \end{matrix}$$

🔴⚪ 
**15edo.**
80¢ steps.
The 5-note subset approximates scales used in [Bantu traditional music](learn/bantu.md) as well ezil scale in [Ethiopian Christian music](learn/ethiopian.md).
All the 15 notes are useful for salendro scales [Sundanese classical music](learn/indonesian.md).
See also *5edo (ombak)*.

$$\begin{matrix} \ & 0 & 3 & \ & 6 & 9 & 12 & \
\cr -1 & 2_1 & 4 & 5 & 8_7 & 11_{10} & 13 & 14 \end{matrix}$$

🟠⚫ 
**Narrow 9ed3/2.**
78¢ steps.
Approximates the Carlos alpha scale, which is [rich in harmonics](learn/harmonic.md).
It completely misses the octave, but (or because of this) approximates maqam saba from [Arabic classical music](learn/arabic.md) very well.
The notes are mapped such that maqam saba can be played from D above middle C the same way as maqam saba would be played in other tunings.

$$\begin{matrix} \ &-2_{-1} & 1 & \ & 5 & 7_8 & 10 & \
\cr -3 & 0 & 2_3 & 4 & 6 & 9 & 11_{12} & 13 \end{matrix}$$

🟠🔴 
**16edo.**
75¢ steps.
Used to approximate pélog scales in [Sundanese classical music](learn/indonesian.md).

$$\begin{matrix} \ & 2 & 4 & \ & 9 & 11 & 13 & \
\cr 0_1 & 3 & 5_6 & 8_7 & 10 & 12 & 15_{14} & 16 \end{matrix}$$

��🟠 
**17edo.**
71¢ steps.
Approximates [Burmese classical music](learn/burmese.md) and the salendro bedantara scale of [Sundanese classical music](learn/indonesian.md).
I approximate [Iranian classical music](learn/iranian.md) with 17edo.

$$\begin{matrix} & 1_2 & 4 & & 8_9 & 11_{12} & 14 &
\cr 0 & 3 & 5_6 & 7 & 10 & 13 & 15_{16} & 17 \end{matrix}$$

🟠🟡 
**17 Pythagoreans (uneven).**
[Pythagorean tuning](learn/pythagorean.md) seems to have been developed independently in East Asia and the Middle East.
The 17 notes have historically been a foundation for [Iranian](learn/iranian.md), [Arabic](learn/arabic.md), and [Turkish](learn/turkish.md) music.
[Ancient greek music](learn/greek.md) used a 12-note subset, and so have [Chinese](learn/chinese.md) and [Japanese](learn/japanese.md) classical musics.

$$\begin{matrix} & & 2^8 3^{-5} _{2^{16} 3^{-10}} & 2^5 3^{-3} & \ & 2^{-10} 3^{-6} _{2^{18} 3^{-11}} & 2^{7} 3^{-4} _{2^{15} 3^{-9}} & 2^{4} 3^{-2} & \
\cr & 1 & 2^{-3} 3^2 & 2^{13} 3^{-8} _{2^{-6} 3^4} & 2^2 3^{-1} & 2^{-1} 3 & 2^{-4}3^{3} & 2^{12} 3^{-7} _{2^{20} 3^{-12}} & 2
\cr \ & \ & \ & \ & \ & \ & \ & \ & \
\cr & 2^{16} 3^{-10} _{2^8 3^{-5}} & / & \ & 2^{18} 3^{-11} _{2^{-10} 3^{-6}} & 2^{15} 3^{-9} _{2^{7} 3^{-4}} & / & \ & \
\cr / & / & / & 2^{-6} 3^4 _{2^{13} 3^{-8}} & / & / & 2^{20} 3^{-12} _{2^{12} 3^{-7}} & / & \ \end{matrix}$$

🟠🟢 
**19 from 41edo (uneven).**
Multiples of 29¢ steps.
Approximates the perfect fifth *very* well.
Approximates [Malian classical music](learn/malian.md).
The black keys plus C and F (i.e. like a Db major scale) approximates 7edo used to play the bala.
The remaining keys can be used for various kora tunings.

$$\begin{matrix} & & & -12 & -6 & & 6 & 12 & 17 &
\cr & & -17 & -10_{-9_{-11}} & -4_{-3} & 0 & 7_8 & 13_{14_{11}} & 21 & 24
\cr & \ & \ & \ & \ & \ & \ & \ & \
\cr & & / & / & & / & / & / & &
\cr & / & -9_{-11_{-10}} & -3_{-4} & / & 8_7 & 14_{11_{13}} & / & / & \end{matrix}$$

🟠🔵
**19edo.**
63¢ steps.
Approximates 1/3 meantone tuning used in [European classical music](learn/european.md) from the 1600s.
In particular, it approximates the European major and, especially, minor thirds well.

$$\begin{matrix} & 2_1 & 5_4 & & 10_9 & 13_{12} & 16_{15} &
\cr 0 & 3 & 6_7 & 8 & 11 & 14 & 17_{18} & 19 \end{matrix}$$

🟠🟣 
**19 from 48edo (uneven).**
Multiples of 25¢ steps.
Used in contemporary [Turkish music](learn/turkish.md).

$$\begin{matrix} \ & \ & 4_3 & 12_{13} & \ & 24_{23} & 32_{31} & 40_{41} & \
\cr \ & 0 & 8 & 15_{16} & 20 & 28 & 36 & 43_{44} & 48
\cr \ & \ & \ & \ & \ & \ & \ & \ & \
\cr  \ & 3_4 & 13_{12} & \ & 23_{24} & 31_{32} & 41_{40} & \ & \
\cr / & / & 16_{15} & / & / & / & 44_{43} & / & \
\end{matrix}$$

🟠⚪ 
**8ed4/3.**
62¢ steps.
Approximates the Carlos beta scale, which is [rich in harmonics](learn/harmonic.md).
Used in [Georgian traditional music](learn/georgian.md).
Can be useful for approximating jins hijaz in [Arabic](learn/arabic.md) and [Iranian classical music](learn/iranian.md).

$$\begin{matrix} \ & 2_1 & 5_4 & \ & 10_9 & 13_{12} & 16_{15} & \
\cr 0 & 3 & 6_7 & 8 & 11 & 14 & 17_{18} & 19 \end{matrix}$$

🟡⚫ 
~~**Eikosany (uneven).**
A 20-note scale in just intonation.
A combination product set used in [experimental music](learn/experimental.md).~~

🟡🔴
**22edo.**
55¢ steps.
Is [rich in harmonics](learn/harmonic.md).
Is a decent approximation of an ['Are'are tuning](learn/melanesian.md).
I approximate the ararai scale of [Ethiopian Christian music](learn/ethiopian.md).
The ararai scale is mapped to the black keys.

$$\begin{matrix} \ & 2_1 & 4_5 & \ & 10_{11} & 14_{15} & 18_{19} & \
\cr 0 & 3 & 7_6 & 9_8 & 13_{12} & 16_{17} & 20_{21} & 22 \end{matrix}$$

🟡🟠
**22 from 53edo (uneven).**
Multiples of 23¢ steps.
Approximates the perfect fifth *very* well.
A 22-note subset of 53edo.
Approximates [Indian classical music](learn/indian.md) well—in particular, its [22 shrutis](learn/shruti.md).
Used in [Turkish classical music](learn/turkish.md).

$$\begin{matrix} & & -18_{-17} & -9_{-8} & & 4_5 & 13_{14} & 22_{23} & &
\cr & -22 & -14_{-13} & -5_{-4} & 0 & 9_8 & 18_{17} & 26_{27} & 31
\cr & \ & \ & \ & \ & \ & \ & \ & \
\cr & -17_{-18} & -8_{-9} & & 5_4 & 14_{13} & 23_{22} &
\cr / & -13_{-14} & -4_{-5} & / & 8_9 & 17_{18} & 27_{26} & / & \end{matrix}$$

🟡🟡
**24edo.**
50¢ steps.
Approximates the perfect fifth well.
Used in contemporary [Arabic](learn/arabic.md) and [Iranian](learn/iranian.md) music.
Approximates [Burmese classical music](learn/burmese.md).
Can be used for niche cases in [Greek](learn/greek.md), [Japanese](learn/east_asian.md) and [American](learn/american.md) music.

$$\begin{matrix} \ & 2_1 & 6_5 & \ & 12_{11} & 16_{15} & 20_{19} & \
\cr 0_{-1} & 4_{3} & 7_{8} & 10_9 & 14_{13} & 18_{17} & 21_{22} & 24_{23} \end{matrix}$$

🟡🟢
**29edo.**
41¢ steps.
Approximates the perfect fifth well.
Approximates [Arabic classical music](learn/arabic.md).
I have approximated [Iranian classical music](learn/iranian.md) with 17edo, but 29edo would also have been a good choice.

$$\begin{matrix} \ & 2_3 & 7_8 & \ & 14_{15} & 19_{20} & 24_{25} & \
\cr 0 & 5 & 9_{10} & 12 & 17 & 22 & 26_{27} & 29 \end{matrix}$$

🟡🔵
**31edo.**
39¢ steps.
Approximates 1/4 meantone tuning used in [European classical music](learn/european.md) from the 1600s.
Closely approximates the [harmonic seventh](learn/harmonic.md) (the seventh harmonic) used in some European music but completely lacking from 12edo.

$$\begin{matrix} \ & 3_2 & 8_7 & \ & 16_{15} & 21_{20} & 26_{25} & \
\cr 0 & 5_6 & 10_9 & 13 & 18_{19} & 23_{24} & 28_{27} & 31 \end{matrix}$$

🟡🟣 
**Narrow 20ed3/2.**
35¢ steps.
34 steps in a compressed octave
Approximates the Carlos gamma scale, which is [rich in harmonics](learn/harmonic.md).

$$\begin{matrix} \ & 3_2 & 9_8 & \ & 17_{16} & 23_{22} & 28_{27} & \
\cr 0_{-1} & 6_5 & 11_{10} & 14_{13} & 20_{19} & 25_{24} & 31_{30} & 34_{33} \end{matrix}$$

🟡⚪ 
**Wide 20ed3/2.**
Same as before but mapped to 35 steps in a streched octave.
It can approximate both the "minor" and the "major" scales in [Georgian traditional music](learn/georgian.md).

$$\begin{matrix} \ & -9 & -5 & \ & 6 & 10 & 19 & \
\cr -10_{-11} & -7 & 0 & 5_4 & 9 & 15_{14} & 20 & 25_{24} \end{matrix}$$

[Chords](learn/chords.md) have traditionally only been important only in a few of the cultures mentioned above.

