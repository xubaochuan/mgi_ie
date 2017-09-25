#coding=utf-8
import open_ie_api as openie

def main():
    s = "Born in Honolulu, Hawaii, Obama is a US Citizen"
    results = openie.call_api_single(s)
    print results

if __name__=='__main__':
    main()
