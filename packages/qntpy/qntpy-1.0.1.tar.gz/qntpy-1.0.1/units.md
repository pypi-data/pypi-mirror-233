this list contains almost every currently usable unit and constant in the package. 

looking for a unit that isn't here? remember, you can [define your own](./README.md#defining-custom-units)!

Variable Name | Commensurability | Description
--- | --- | ---
---|**SI Base Units**|---
`m` | length | the SI unit meter
`s` | time | the SI unit second
`kg`|mass|the SI unit kilogram
`cd`|luminous intensity|the SI unit candela
`K`|temperature|the SI unit kelvin
`A`|electric current|the SI unit ampere
`mol`|unitless|$6.02214076\times10^{23}{}$
---|**SI Derived Units**|---
`Hz`|regular frequency|the SI unit hertz
`N`|force|the SI unit newton
`Pa`|pressure|the SI unit pascal
`J`|energy|the SI unit joule
`W`|power|the SI unit watt
`C`|electric charge|the SI unit coulomb
`V`|electric potential|the SI unit volt
`F`|capacitance|the SI unit farad
`ohm`|resistance|the SI unit ohm
`S`|conductance|the SI unit siemens
`Wb`|magnetic flux|the SI unit weber
`T`|magnetic flux density|the SI unit tesla
`H`|inductance|the SI unit henry
`Sv`|radiation dosage (J/kg)|the SI unit sievert
---|**Misc. Derived Units**|---
`nm,um,mm,cm,km,Gm,Mm`|length|nano,micro,milli,centi,kilo,giga,megameter
`au`|length|astronomical unit
`pc`|length|parsec
`ly`|length|lightyear
`ft`|length|foot, $.3048\space m$
`inch`|length|inch, $\frac{1}{12}\space ft$
`thou`|length|$\frac1{1000}\space inch$
`mi`|length|$5280\space ft$
`m2`|area|meters squared
`inch2`|area|$inch^2$
`ft2`|area|$ft^2$
`mi2`|area|$mi^2$
`acre`|area|acre, $4046.873\space m^2$
`ha`|area|hectare
`m3`|volume|meters cubed
`ft3`|volume|$ft^3$
`in3`|volume|$inch^3$
`L`|volume|liter, $.001\space m^3$
`mL`|volume|milliliter, $.001\space L$
`tsp`|volume|teaspooon, $4.92892159375\space mL$
`Tbsp`|volume|tablespoon, $3\space tsp$
`cup`|volume|$16\space Tbsp$
`pint`|volume|$2\space cup$
`quart`|volume|$2\space pint$
`gal`|volume|$4\space quart$
`ms, us, ns, ps`|time|milli, micro, nano,picosecond
`minute`|time|$60\space s$
`hr`|time|$60\space minute$
`day`|time|$24\space hr$
`wk`|time|$7\space day$
`yr`|time|$365.25\space day$
`My`|time|$10^6\space yr$
`aeon`|time|$10^9\space yr$
`kJ,MJ,GJ`|energy|kilo,mega,gigajoule
`Wh`|energy|watt*hr
`kWh,MWh,GWh,TWh`|energy|kilo,mega,giga.terawatthour
`cal`|energy|the small calorie, $4.184 J$
`kcal`|energy|the large Calorie, $4184 J$
`Btu`|energy|British thermal unit, $1055.056\space J$
`eV`|energy|the electron-volt, $1.602176634\times10^{-19}\space J$
`keV,MeV,GeV,TeV`|energy|kilo,mega,giga,teraelectronvolt
`mW,kW,MW,GW,TW`|power|milli,kilo,mega,giga,terawatt
`hp`|energy|horsepower, $745.7\space W$
`kN,MN,GN`|force|kilo,mega,giganewton
`lbf`|force|poundforce, $4.448222\space N$
`lbm`|mass|poundmass, $0.4535924\space kg$
`ton`|mass|ton, $2000\space lbm$
`slug`|mass|slug, $1\frac{lbf\space s^2}{ft}{}$
`ng,ug,mg,g`|mass|nano,micro,milli,gram
`eVc2`|mass|electron-volt divided by the speed of light squared, $1.78266192\times10^{-36}\space kg$
`keVc2,MeVc2,GeVc2,TeVc2`|mass|kilo,mega,giga,teraelectronvolt/c2
`mA,kA`|electric current|milli,kiloamp
`mV,kV`|electric potential|milli,kilovolt
`pF,nF,uF,mF`|capacitance|pico,nano,micro,millifarad
`nH,uH,mH`|inductance|nano,micro,millihenry
`kohm,Mohm,Gohm`|resistance|kilo,mega,gigaohm
`kHz,MHz,GHz,THz`|regular frequency|kilo,mega,giga,terahertz
`kPa,MPa,GPa`|pressure|kilo,mega,gigapascal
`psi`|pressure|$1\frac{lbf}{inch^2}{}$
`ksi, Mpsi`|pressure|kilo,megapsi
`deg`|unitless|one angular degree
`R`|temperature|the Rankine scale
`degC`|temperature|degrees Celsius ([non-absolute unit](./README.md#non-absolute-units))
`degF`|temperature|degrees Fahrenheit ([non-absolute unit](./README.md#non-absolute-units))
---|**Other Units**|---
`bit`|information|information equal to one boolean value
`nybble`|information|$4 \space b$
`byte`|information|$8\space b$
`kB,MB,GB,TB,PB,EB`|information|kilo,mega,giga,tera,peta,exabyte (scaling by $1000$)
`kiB,MiB,GiB,TiB,PiB,EiB`|information|kibi,mebi,gibi,tebi,pebi,exibyte (scaling by $1024$)

by importing `qntpy.constants`, you can also access several physics and engineering constants:

Variable Name|Description|Significant Figures
---|---|---
`G`|gravitational constant|6
`c`|speed of light|exact
`h`|Planck constant|exact
`k`|Boltzmann constant|exact
`R_ideal`|ideal gas constant|exact
`e`|elementary charge|exact
`sigma_sb`|Stefan-Boltzmann constant|exact, with error $5\epsilon(math.pi)$ (implementation-dependent)
`g_earth`|standard gravity|exact
`mu_0`|vacuum permeability|12
`e_0`|vacuum permittivity|12
`k_e`|Coulomb constant|11
`m_e`|electron mass|11
`m_p`|proton mass|12
`m_n`|neutron mass|12
`l_planck`|Planck distance|7
`m_planck`|Planck mass|7
`t_planck`|Planck time|7
`T_planck`|Planck temperature|7
`E_planck`|Planck energy|7
