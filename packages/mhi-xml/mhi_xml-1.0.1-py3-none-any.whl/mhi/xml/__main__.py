from mhi.xml import VERSION
from mhi.xml.buildtime import BUILD_TIME

def version():
    print(f"MHI Xml Library v{VERSION} ({BUILD_TIME})")
    print("(c) Manitoba Hydro International Ltd.")

def main():
    version()

if __name__ == '__main__':
    main()
