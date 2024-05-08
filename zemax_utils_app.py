try:
    from TaskBuilder import *
    from UI import UIMainWindow
except ImportError as ex:
    print(f"ZemaxUtilsImportException {ex}")
    a = input("Enter any key...")
    exit(-1)

if __name__ == "__main__":
    try:
        UIMainWindow.run()
    except Exception as ex:
        print(f"ZemaxUtilsException {ex}")
    a = input("Enter any key...")
