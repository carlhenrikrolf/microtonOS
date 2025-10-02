## Isomorphic Layouts
I suggest to think of musically useful isomorphic layouts as belonging to one of four categories.
Each category depends on three parameters:
whether the layout is mirrored (flipped) in the left–right direction,
whether it is flipped in the up–down position,
and the value of the "dilation".
The dilation is notated $d$ and defined separately for each category below.
A suitable value is the size of the minor or neutral third.
For a more jazzy sound (or the Studio Ghibli sound), try the major third or perfect fourth.
Below, the layouts are named according to $d=3$.

DEFAULT ⚫⚫ **Exquis.**
$d=3$ is the Exquis default layout.
How the number of steps depend on d is shown by arrows.
Number of steps for $d=3$ is also given as an example in the centres of the hexagons.
$d=3$ plus left--right flip is the Gerhard layout used in Shiverware's Musix Pro.

![Exquis](resources/hexagonal_vs_rectangular.svg)

To the right, you can see a suggestion on how to map the hexagonal layout to a rectangular layout.
$d=5$.
This is the layout used on a bass guitar in standard tuning. 

⚫🔴 **Harmonic table.**
$d=3$ is the harmonic table.
The harmonic table has been used in C-thru's AXiS controllers as well as in the Lumatone controller.
$d=2$ is the Park layout used in Shiverware's Musix Pro.

![Harmonic table](resources/harmonic_table.svg)

⚫🟠 **Wicki–Hayden.**
$d=3$ is the Wicki--Hayden layout. For calculations, see below. The Wicki–Hayden layout is used in concertinas although it was originally designed for the bandoneón (popular in Argentine tango).
The bandoneón typically uses a non-isomorphic layout that is different between the left and right hands as well as whether the instrument is squeezed or dragged. Life is short so we will ignore such complex layouts.

![Wicki--Hayden](resources/wicki-hayden_tilted.svg)

<details>
<summary>
Calculations with <i>f</i><sub>3</sub>.
</summary>

$f_3$ is defined by $f_3(d)=\mathrm{round}\frac{d}{3}$ if $d\mod 3 > 0$
else $f_3(d)= \max(i)$ such that $i\in\mathbf{N}$, $i\mod 2 > 0$, and $1 \leq i < \frac{d}{3})$.
$\mathrm{round}(x)$ rounds $x$ to the nearest integer and $x \mod y > 0$ if and only if $x$ is not divisible by $y$.
It is easiest to break this down into two cases.
If $d$ is not divisible by $3$, $f_3(d)$ is the integer nearest the fraction $d/3$.
Otherwise, it is the largest odd integer less than $d/3$.
For example, if you want to use $d=6$ for 24edo and you use $\mathrm{round}(d/3)$ instead (as in the first case), the layout will only use half of the tones and be equivalent to 12edo.

</details>


⚫🟡 **Jankó.**
Bosanquet–Wilson layouts.
$d=3$ is the Jankó layout.
$d=4$ is the type C accordion layout.
Both $d=3$ and $d=4$ are given as examples below.
$d=4$ plus left–right flip corresponds to both the type B accordion layout and the dugmetara layout (popular in the Balkans).
$d=5, 6, 8,$ and $13$
correspond to the Lumatone presets for 19edo, both 22edo and 24edo, 31edo, and 53edo respectively. 

![Jankó](resources/janko_tilted.svg)

For large $d$, the 1D tuning invariant layouts, i.e., Exquis and the harmonic table,
benefit from a split keyboard as shown below (in respective order).
The filled hexagons represent a muted splitting line.
$+,0,-$ represent three consecutive steps
(note that $+,0,-$ does not indicate whether pitch is rising or falling).

![Splits](resources/splits.svg)

For the 2D tuning invariant layouts, i.e., Wicki–Hayden and Jankó,
even modest values for $d$ benefit from a split.
As these layouts are "tilted" to fit the Exquis better,
so are their splitting lines.

![Slashes](resources/slashes.svg)
