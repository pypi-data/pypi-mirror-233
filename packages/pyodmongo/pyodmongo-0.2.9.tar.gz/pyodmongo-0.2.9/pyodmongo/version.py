import platform
import sys
import pymongo
import motor


VERSION = "0.2.9"

info = {
    "PyODMongo version": VERSION,
    "Pymongo version": pymongo.__version__,
    "Motor version": motor._version.version,
    "Python version": sys.version,
    "Platform": platform.platform(),
}

print("\n".join([f"{key}: {value}" for key, value in info.items()]))
