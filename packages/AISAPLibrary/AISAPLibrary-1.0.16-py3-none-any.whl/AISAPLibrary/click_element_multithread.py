from AISAPLibrary import AISAPLibrary
import sys

if __name__ == '__main__':
    try :
        sap = AISAPLibrary()
        sap.connect_to_session()
        sap.connect_to_existing_connection(sys.argv[1])
        sap.click_element_other_session(str(sys.argv[2]), str(sys.argv[3]))
    except :
        print(sys.argv[1])
        print(sys.argv[2])
        print(sys.argv[3])
        print('Error in calling function please follow this order')