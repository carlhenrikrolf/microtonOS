# Chords

> [!warning]
> These are like my opinions, man. Not some kind of universal theory of human aesthetical preferences in harmony.

Most music of the world let several notes sound simultaneously.
Singing in octaves is common.
So is using a drone—a constant note played simultaneously as the melody.
When I say *chord*, I mean something more complicated.
Typically at least three notes playing simultaneously and several notes changing at the same time.
There is plenty of theoretical tools for analysing chord progressions.
However, they generalise poorly across different cultures and tunings.
Therefore, I only analyse chord progression in terms of unstable and stable chords, or tension and release if you will.

## Equal

There are two ways of thinking of equal distances in pitch: in Hertz (Hz) and in cents (¢).
The relationship between them is
$$z\ \mathrm{cents} = 1200\log_2\left(\frac{x\ \mathrm{Hz}}{y\ \mathrm{Hz}}\right)$$
so if a distance in cents is constant, then it is not in Hz and vice versa.
The concept of ombak from Balinese music (in European organ music this corresponds to voix céleste and in accordion music to tremolo) illustrates the relationship.
In *ombak* each note is doubled at slightly different frequences.
The difference is constant in Hz causing beating.
However, the musical scales are constant in terms of cents.

<img src="../resources/beating.png" width="60%" />

Above, two oscillscopes have been superimposed.
Each oscilloscope shows the waveform of a constant Hz pair.
The difference between them is that the distance between average frequency of the two oscilloscopes is one octave.
As an octave is a doubling of frequencies it is only constant in terms of cents.
Apart from ombak, constant differences in Hz are uncommon although they could play a role in ancient Andean music and Australian aboriginal music.

Equal distances in terms of cents is much more common and is used in chords in European, American, Melanesian, Georgian, and Bantu musics.
One useful technique when notes are at an equal distance is *planing*.
In planing, the distances between the notes in the chords is constant.
However, the chord as a whole moves up and down.
Another useful technique is *line clichés*.
In a line cliché, one set of notes is constant (similar to a drone) whereas another set of notes move in equal steps up or down.

## Harmonic

![oscilloscopes](../resources/oscilloscopes.png)

## Pythagorean

**12edo.**

![circle of fifths in 12edo](../resources/twelve5ths.svg)

|style     |voices (in 12edo)|fifths (number of)|
|----------|-----------------|------------------|
|rock, metal, many traditional musics|7|0|
|pop, hip hop, European classical music, and many more|3,4,5|1 to 2|
|jazz, RnB|2,3,4,5|2 to 5|
|flamenco|2,3,4,5|1 to 6|
|salsa, tango|8,9|2 to 3|
|12-tone music|any|unlimited|

**Other edos.**

![circle of fifths in 19edo](../resources/nineteen5ths.svg)

![circles of fifths in 15edo](../resources/fifteen5ths.svg)


## Repetition legitimises

Below, degree is the number of steps in an equal division. It does not matter precisely, but each degree is around 350¢/2=175¢. In other words, it's a kind of average between one and two semitones.

| Degree | Pyth- | agorean                            | harm- | onic   |
| ------ | ----- | ---------------------------------- | ----- | ------ |
| 1      | ±0    |                                    | 4     |        |
| 2      | +2    | 2                                  |       |        |
| 3      | +4    |                                    | 5     | ±\*,aug\*\*    |
| 4      | -1    | 4,11                               |       |        |
| 5      | +1    |                                    | 6     |        |
| 6      | -4    | &flat;6,&flat;13                   |       |        |
| 7      | -2    | 7                                  | 7     | harm7  |
| 8      | ±0    |                                    | 8     |        |
| 9      | +2    | 2,9                                | 9     | 9      |
| 10     | +4    |                                    | 2x5   | ±\*    |
| 11     | +6    | &sharp;4,&sharp;11                 | 11    | harm11 |
| 12     | +1    |                                    | 2x6   |        |
| 13     | +3    | 6,13                               | 13    | harm13 |
| 14     | +5    | maj7                               | 15    | neu7   |
| 15     | +7    | &flat;2,&flat;9,&sharp;8,&sharp;15 | 17    | harm15 |
| 16     | -3    | m\*,min\*                          | 19    | -\*,dim\*\*    |

Note that susX replaces the major third with X, and symbols marked with \* also replace the major third. If a Pythagorean symbol is empty, it means that it's inherent.
The symbols marked by \*\* iteratively stack major thirds and minor thirds respectively.
In 12edo, 3-note and 4-note chords respectively are the only options but other tuning systems can use more notes.
If a harmonic symbol is empty, it means that its not defined.

As an example, consider the [demo song in 9ed3/2](https://github.com/user-attachments/assets/df7541df-ebf6-41b0-8a2d-45e2938c4093).


<table>
<tr><td>Adim<sup>9</sup></td><td>D-<sup>7</sup></td><td>G±neu<sup>7</sup>harm<sup>11</sup></td><td>A±harm<sup>7</sup></td></tr>
<tr><td>A&#x1D1EA;-<sup>7</sup></td><td>G&flat;±neu<sup>7</sup></td><td>F&#x1D1EA;±neu<sup>7</sup></td><td></td>
<tr><td>Adim<sup>9</sup></td><td>D-<sup>7</sup></td><td>G±neu<sup>11</sup></td><td>B&#x1D1E9;±E&#x1D1E9;±</td></tr>
<tr><td>Adim<sup>9</sup></td><td>D-<sup>7</sup></td><td>G±neu<sup>7</sup>harm<sup>11</sup></td><td></td></tr>
</table>

If half-sharp &#x1D1E9; (sori) and half-flat &#x1D1EA; (koron) are not rendered to symbols similar to > and p respectively, then the affected chords should be read as Ap±harm<sup>7</sup>, Fp±neu<sup>7</sup>, B>±, and E>±.
([Downloading GNU Unifont](https://www.unifoundry.com/pub/unifont/unifont-16.0.02/font-builds/unifont_upper-16.0.02.otf) provides rendering support.)
I have used different symbols for F&#x1D1EA;  and E&#x1D1E9; to emphasise that F&#x1D1EA;  is only 1170¢ below E&#x1D1E9;. Note that the Pythagorean major one step larger than the harmonic and the Pythagorean minor is one step smaller than the harmonic.




