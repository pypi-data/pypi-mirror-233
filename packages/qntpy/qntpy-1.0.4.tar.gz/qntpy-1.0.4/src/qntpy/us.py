from .quantity import *
# unit definition: us customary

# length
ft = Unit.derived(m, "ft", 0.3048)
inch = Unit.derived(ft, "in", 1/12)
thou = Unit.derived(inch, "thou", 1000)
mi = Unit.derived(ft, "mi", 5280)

# area
inch2 = Unit.derived(inch**2, "(in²)")
ft2 = Unit.derived(ft**2, "(ft²)")
mi2 = Unit.derived(mi**2, "(mi²)")
acre = Unit.derived(m**2, "acre", 4046.873)

# volume
ft3 = Unit.derived(m*m*m, "(ft³)", 0.02831685)
inch3 = Unit.derived(inch**3, "(in³)")
tsp = Unit.derived(mL, "tsp", 4.92892159375)
Tbsp = Unit.derived(tsp, "Tbsp", 3)
cup = Unit.derived(Tbsp, "cup", 16)
pint = Unit.derived(cup, "pint", 2)
quart = Unit.derived(pint, "quart", 2)
gal = Unit.derived(quart, "gal", 4)


# energy
Btu = Unit.derived(J, "Btu", 1055.056)

# power
hp = Unit.derived(W, "hp", 745.7)

# temperature
R = Unit.derived(K, "R", 0.5555556)
degF = Unit.derived(degC, "⁰F", 0.5555555555555556, -17.77777777777778)

# force
lbf = Unit.derived(N, "lbf", 4.448222)

# mass
lbm = Unit.derived(kg, "lbm", 0.4535924)
ton = Unit.derived(lbm, "ton", 2000)
slug = Unit.derived(lbf*s**2/ft, "slug")

# pressure
psi = Unit.derived(lbf/inch2, "psi")
ksi = kilo(psi)
Mpsi = mega(psi)
