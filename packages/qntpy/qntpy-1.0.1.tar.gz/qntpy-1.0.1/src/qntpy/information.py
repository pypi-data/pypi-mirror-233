from .quantity import *

bit = Unit({"b": 1}, "b")
nybble = Unit.derived(bit, "nybble", 4)
byte = Unit.derived(bit, "B", 8)

addBaseUnit(bit)

kB = kilo(byte)
MB = mega(byte)
GB = giga(byte)
TB = tera(byte)
PB = Unit.derived(TB, "PB", 1000)
EB = Unit.derived(TB, "EB", 1000)

KiB = Unit.derived(byte,"KiB", 1024)
MiB = Unit.derived(KiB, "KiB", 1024)
GiB = Unit.derived(MiB, "GiB", 1024)
TiB = Unit.derived(GiB, "TiB", 1024)
PiB = Unit.derived(TiB, "PiB", 1024)
EiB = Unit.derived(PiB, "EiB", 1024)

def help():
    print("data units; base unit = bit (b)")
    print("--------------------------------")
    print("included units:")
    print("byte, kB, MB, GB, TB, PB, EB")
    print("KiB, MiB, GiB, TiB, PiB, EiB")
    print("note: kilobyte et al. scale by 1000, kibibyte et al. scale by 1024")
    print("---------------------------------")
    print("example:")
    print()
    print(">>> from qpy.quantity import *")
    print(">>> from qpy.information import *")
    print(">>> storageDensity = 12*MB/kg")
    print(">>> print(storageDensity*150*g).termsOf(KiB)")
    print("1757.8125 KiB")

if __name__ == "__main__":
    help()

